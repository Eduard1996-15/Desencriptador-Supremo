"""
Sistema Avanzado de Extracción de Claves Privadas
Implementa múltiples métodos de ataque para certificados protegidos
"""

import os
import sys
import threading
import hashlib
import itertools
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography import x509
import logging
import time

class AdvancedPrivateKeyExtractor:
    """Extractor avanzado de claves privadas con múltiples métodos de ataque"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stop_flag = False
        
    def extract_private_key(self, cert_path, method="auto", **kwargs):
        """
        Extrae clave privada usando diferentes métodos
        
        Args:
            cert_path: Ruta al certificado
            method: Método de extracción ('password', 'bruteforce', 'dictionary', 'hybrid', 'auto')
            **kwargs: Parámetros adicionales según el método
        """
        
        if method == "auto":
            return self._auto_extract(cert_path, **kwargs)
        elif method == "password":
            return self._extract_with_password(cert_path, kwargs.get('password'))
        elif method == "bruteforce":
            return self._bruteforce_extract(cert_path, **kwargs)
        elif method == "dictionary":
            return self._dictionary_extract(cert_path, **kwargs)
        elif method == "hybrid":
            return self._hybrid_extract(cert_path, **kwargs)
        else:
            return {'success': False, 'error': f'Método no reconocido: {method}'}
    
    def _auto_extract(self, cert_path, password_hint=None, **kwargs):
        """Extracción automática con múltiples estrategias optimizada para RSA antiguos"""
        results = {'attempts': [], 'total_time': 0}
        start_time = time.time()
        
        self.logger.info(f"🚀 Iniciando extracción automática para: {cert_path}")
        
        # Analizar el archivo primero
        file_info = self._analyze_certificate_file(cert_path)
        
        # Estrategias específicas para RSA 4096 + SHA256 (antiguos y vulnerables)
        if file_info.get('rsa_size') == 4096 and 'sha256' in file_info.get('signature_algorithm', '').lower():
            self.logger.info("🎯 RSA 4096 + SHA256 detectado - Aplicando estrategias específicas")
            
            # 1. Contraseñas por defecto para CAs antiguas
            default_passwords = [
                '',  # Sin contraseña
                'changeit', 'password', 'admin', 'test', 'ca', 'root', 'private',
                'certificate', 'key', 'ssl', 'rsa', 'ca-key', 'private-key',
                '123456', 'password123', 'admin123', 'test123', 'changeme',
                '12345678', 'qwerty', 'abc123', 'default', 'secret',
                # Patrones específicos para CAs
                'ca-password', 'rootca', 'intermediate', 'signing-key',
                'ca123', 'root123', 'ca-test', 'demo-ca', 'dev-ca',
                # Fechas comunes en CAs de prueba
                '2020', '2021', '2022', '2023', '2024', '2025',
                # Nombres comunes de organizaciones
                'company', 'corporation', 'organization', 'test-org'
            ]
            
            for password in default_passwords:
                if self.stop_flag:
                    break
                    
                result = self._extract_with_password(cert_path, password)
                results['attempts'].append({
                    'method': 'default_passwords',
                    'password': password if password else '<empty>',
                    'success': result['success']
                })
                
                if result['success']:
                    results['success'] = True
                    results['password'] = password
                    results['method'] = 'default_passwords'
                    results['private_key'] = result['private_key']
                    results['total_time'] = time.time() - start_time
                    self.logger.info(f"✅ Contraseña encontrada: {password if password else '<vacía>'}")
                    return results
            
            # 2. Generación de contraseñas basada en información del certificado
            cert_passwords = self._generate_certificate_based_passwords(file_info)
            
            for password in cert_passwords[:50]:  # Limitamos a 50 para no sobrecargar
                if self.stop_flag:
                    break
                    
                result = self._extract_with_password(cert_path, password)
                results['attempts'].append({
                    'method': 'certificate_based',
                    'password': password,
                    'success': result['success']
                })
                
                if result['success']:
                    results['success'] = True
                    results['password'] = password
                    results['method'] = 'certificate_based'
                    results['private_key'] = result['private_key']
                    results['total_time'] = time.time() - start_time
                    self.logger.info(f"✅ Contraseña basada en certificado encontrada: {password}")
                    return results
        
        # 3. Estrategia de fuerza bruta optimizada para RSA antiguos
        if file_info.get('likely_weak', False):
            self.logger.info("🔓 Aplicando fuerza bruta optimizada para certificados débiles")
            
            # Patrones comunes en certificados de prueba/desarrollo
            patterns = [
                # Números simples
                *[str(i) for i in range(10000)],
                # Patrones alfabéticos
                *[chr(i) * j for i in range(ord('a'), ord('z')+1) for j in range(1, 6)],
                # Combinaciones simples
                *[''.join(p) for p in itertools.product('abc123', repeat=3)],
                # Patrones de teclado
                'qwerty', 'asdf', 'zxcv', '1234', '123456', '12345678',
                # Palabras relacionadas con CA
                'ca', 'cert', 'key', 'ssl', 'tls', 'pki', 'x509'
            ]
            
            for password in patterns[:1000]:  # Limitamos para evitar sobrecargar
                if self.stop_flag:
                    break
                    
                result = self._extract_with_password(cert_path, password)
                results['attempts'].append({
                    'method': 'pattern_bruteforce',
                    'password': password,
                    'success': result['success']
                })
                
                if result['success']:
                    results['success'] = True
                    results['password'] = password
                    results['method'] = 'pattern_bruteforce'
                    results['private_key'] = result['private_key']
                    results['total_time'] = time.time() - start_time
                    self.logger.info(f"✅ Contraseña de patrón encontrada: {password}")
                    return results
        start_time = time.time()
        
        # 1. Intentar sin contraseña
        self.logger.info("🔓 Intentando extracción sin contraseña...")
        result = self._extract_with_password(cert_path, None)
        results['attempts'].append({'method': 'no_password', 'result': result})
        
        if result['success']:
            results['total_time'] = time.time() - start_time
            return result
        
        # 2. Contraseñas comunes basadas en el archivo
        self.logger.info("🎯 Probando contraseñas basadas en el archivo...")
        file_based_passwords = self._generate_file_based_passwords(cert_path)
        
        for password in file_based_passwords:
            if self.stop_flag:
                break
            
            result = self._extract_with_password(cert_path, password)
            results['attempts'].append({'method': 'file_based', 'password': password, 'result': result})
            
            if result['success']:
                result['method_used'] = 'file_based_password'
                result['password_found'] = password
                results['total_time'] = time.time() - start_time
                return result
        
        # 3. Diccionario rápido
        self.logger.info("📚 Probando diccionario común...")
        dict_result = self._dictionary_extract(cert_path, 
                                               wordlist_path=kwargs.get('wordlist_path'),
                                               max_attempts=1000)
        results['attempts'].append({'method': 'dictionary', 'result': dict_result})
        
        if dict_result['success']:
            dict_result['method_used'] = 'dictionary'
            results['total_time'] = time.time() - start_time
            return dict_result
        
        # 4. Fuerza bruta limitada
        if kwargs.get('allow_bruteforce', False):
            self.logger.info("⚡ Iniciando fuerza bruta limitada...")
            bf_result = self._bruteforce_extract(cert_path, 
                                                 max_length=kwargs.get('max_length', 6),
                                                 charset=kwargs.get('charset', 'abcdefghijklmnopqrstuvwxyz0123456789'))
            results['attempts'].append({'method': 'bruteforce', 'result': bf_result})
            
            if bf_result['success']:
                bf_result['method_used'] = 'bruteforce'
                results['total_time'] = time.time() - start_time
                return bf_result
        
        # No se encontró la contraseña
        results['total_time'] = time.time() - start_time
        return {
            'success': False, 
            'error': 'No se pudo extraer la clave privada con ningún método',
            'detailed_results': results
        }
    
    def _extract_with_password(self, cert_path, password):
        """Extrae clave privada con contraseña específica"""
        try:
            with open(cert_path, 'rb') as f:
                data = f.read()
            
            # Determinar formato del archivo
            if cert_path.lower().endswith(('.p12', '.pfx')):
                return self._extract_from_pkcs12(data, password)
            elif b'-----BEGIN' in data:
                return self._extract_from_pem(data, password)
            else:
                return self._extract_from_der(data, password)
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _extract_from_pkcs12(self, data, password):
        """Extrae de formato PKCS#12"""
        try:
            password_bytes = password.encode() if password else None
            
            private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                data, password_bytes
            )
            
            if private_key:
                # Serializar clave privada sin protección
                pem_key = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                
                return {
                    'success': True,
                    'private_key_pem': pem_key.decode(),
                    'key_type': private_key.__class__.__name__,
                    'key_size': getattr(private_key, 'key_size', 'Unknown'),
                    'format': 'PKCS#12',
                    'has_certificate': certificate is not None,
                    'additional_certs': len(additional_certificates) if additional_certificates else 0
                }
            else:
                return {'success': False, 'error': 'No se encontró clave privada en el archivo PKCS#12'}
                
        except Exception as e:
            return {'success': False, 'error': f'Error PKCS#12: {str(e)}'}
    
    def _extract_from_pem(self, data, password):
        """Extrae de formato PEM"""
        try:
            password_bytes = password.encode() if password else None
            
            # Intentar como clave privada directa
            try:
                private_key = serialization.load_pem_private_key(data, password=password_bytes)
                
                # Serializar sin protección
                pem_key = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                
                return {
                    'success': True,
                    'private_key_pem': pem_key.decode(),
                    'key_type': private_key.__class__.__name__,
                    'key_size': getattr(private_key, 'key_size', 'Unknown'),
                    'format': 'PEM'
                }
                
            except ValueError:
                # Si falla, intentar como certificado con clave incluida
                return {'success': False, 'error': 'Archivo PEM no contiene clave privada o contraseña incorrecta'}
                
        except Exception as e:
            return {'success': False, 'error': f'Error PEM: {str(e)}'}
    
    def _extract_from_der(self, data, password):
        """Extrae de formato DER"""
        try:
            password_bytes = password.encode() if password else None
            
            private_key = serialization.load_der_private_key(data, password=password_bytes)
            
            # Serializar sin protección
            pem_key = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            return {
                'success': True,
                'private_key_pem': pem_key.decode(),
                'key_type': private_key.__class__.__name__,
                'key_size': getattr(private_key, 'key_size', 'Unknown'),
                'format': 'DER'
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Error DER: {str(e)}'}
    
    def _generate_file_based_passwords(self, cert_path):
        """Genera contraseñas basadas en el nombre y ubicación del archivo"""
        passwords = []
        
        file_path = Path(cert_path)
        filename = file_path.stem
        
        # Basado en nombre del archivo
        passwords.extend([
            filename,
            filename.lower(),
            filename.upper(),
            f"{filename}123",
            f"{filename}2023",
            f"{filename}2024",
            f"{filename}2025",
        ])
        
        # Palabras comunes de certificados
        cert_words = ['certificate', 'cert', 'key', 'private', 'ssl', 'tls']
        passwords.extend(cert_words)
        
        # Combinaciones
        for word in cert_words:
            passwords.extend([
                f"{filename}{word}",
                f"{word}{filename}",
                f"{filename}_{word}",
                f"{word}_{filename}"
            ])
        
        # Contraseñas muy comunes
        common = [
            'password', 'admin', 'root', 'test', 'demo', 'temp',
            '123456', 'password123', 'admin123', 'test123',
            'changeme', 'default', 'secret', 'secure'
        ]
        passwords.extend(common)
        
        return list(set(passwords))  # Eliminar duplicados
    
    def _dictionary_extract(self, cert_path, wordlist_path=None, max_attempts=None, progress_callback=None):
        """Extracción usando diccionario"""
        try:
            # Cargar diccionario
            if not wordlist_path:
                # Usar diccionario por defecto
                wordlist_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'common-passwords.txt')
            
            if not os.path.exists(wordlist_path):
                return {'success': False, 'error': f'Diccionario no encontrado: {wordlist_path}'}
            
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            
            if max_attempts:
                passwords = passwords[:max_attempts]
            
            self.logger.info(f"📚 Probando {len(passwords)} contraseñas del diccionario...")
            
            # Probar cada contraseña
            for i, password in enumerate(passwords):
                if self.stop_flag:
                    break
                
                if progress_callback:
                    progress_callback(i + 1, len(passwords))
                
                result = self._extract_with_password(cert_path, password)
                
                if result['success']:
                    result['password_found'] = password
                    result['attempts_made'] = i + 1
                    result['total_passwords'] = len(passwords)
                    return result
            
            return {
                'success': False, 
                'error': f'Contraseña no encontrada en {len(passwords)} intentos',
                'attempts_made': len(passwords)
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Error en ataque de diccionario: {str(e)}'}
    
    def _bruteforce_extract(self, cert_path, charset='abcdefghijklmnopqrstuvwxyz0123456789', 
                           min_length=1, max_length=6, max_threads=4, progress_callback=None):
        """Extracción por fuerza bruta"""
        try:
            self.logger.info(f"⚡ Iniciando fuerza bruta: {min_length}-{max_length} chars, charset: {charset[:10]}...")
            
            total_combinations = sum(len(charset) ** length for length in range(min_length, max_length + 1))
            
            if total_combinations > 100000000:  # 100M
                return {'success': False, 'error': f'Demasiadas combinaciones: {total_combinations:,}'}
            
            attempts = 0
            found_password = None
            
            # Generar y probar contraseñas
            for length in range(min_length, max_length + 1):
                if self.stop_flag or found_password:
                    break
                
                self.logger.info(f"🔍 Probando longitud {length}...")
                
                # Usar ThreadPoolExecutor para paralelización
                with ThreadPoolExecutor(max_workers=max_threads) as executor:
                    # Generar lotes de contraseñas
                    batch_size = 1000
                    batch = []
                    
                    for password_tuple in itertools.product(charset, repeat=length):
                        if self.stop_flag:
                            break
                        
                        password = ''.join(password_tuple)
                        batch.append(password)
                        
                        if len(batch) >= batch_size:
                            # Enviar lote a los workers
                            future = executor.submit(self._test_password_batch, cert_path, batch)
                            result = future.result()
                            
                            attempts += len(batch)
                            
                            if progress_callback:
                                progress_callback(attempts, total_combinations)
                            
                            if result['success']:
                                found_password = result['password']
                                break
                            
                            batch = []
                    
                    # Probar último lote
                    if batch and not found_password:
                        future = executor.submit(self._test_password_batch, cert_path, batch)
                        result = future.result()
                        
                        attempts += len(batch)
                        
                        if result['success']:
                            found_password = result['password']
            
            if found_password:
                final_result = self._extract_with_password(cert_path, found_password)
                final_result['password_found'] = found_password
                final_result['attempts_made'] = attempts
                final_result['total_combinations'] = total_combinations
                return final_result
            else:
                return {
                    'success': False, 
                    'error': f'Contraseña no encontrada en {attempts:,} intentos',
                    'attempts_made': attempts,
                    'total_combinations': total_combinations
                }
                
        except Exception as e:
            return {'success': False, 'error': f'Error en fuerza bruta: {str(e)}'}
    
    def _test_password_batch(self, cert_path, passwords):
        """Prueba un lote de contraseñas"""
        for password in passwords:
            if self.stop_flag:
                break
            
            result = self._extract_with_password(cert_path, password)
            if result['success']:
                return {'success': True, 'password': password}
        
        return {'success': False}
    
    def _hybrid_extract(self, cert_path, base_wordlist=None, variations=True, progress_callback=None):
        """Extracción híbrida: diccionario + variaciones"""
        try:
            # Cargar diccionario base
            if not base_wordlist:
                base_wordlist = os.path.join(os.path.dirname(__file__), '..', 'data', 'common-passwords.txt')
            
            if not os.path.exists(base_wordlist):
                return {'success': False, 'error': 'Diccionario base no encontrado'}
            
            with open(base_wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                base_passwords = [line.strip() for line in f if line.strip()]
            
            # Generar variaciones
            all_passwords = set(base_passwords)
            
            if variations:
                self.logger.info("🔄 Generando variaciones de contraseñas...")
                
                for base_pwd in base_passwords[:500]:  # Limitar para evitar explosión
                    if self.stop_flag:
                        break
                    
                    # Variaciones comunes
                    variations_list = [
                        base_pwd.upper(),
                        base_pwd.lower(),
                        base_pwd.capitalize(),
                        f"{base_pwd}123",
                        f"{base_pwd}1",
                        f"{base_pwd}01",
                        f"123{base_pwd}",
                        f"1{base_pwd}",
                        f"{base_pwd}!",
                        f"{base_pwd}@",
                        f"!{base_pwd}",
                        f"{base_pwd}2023",
                        f"{base_pwd}2024",
                        f"{base_pwd}2025",
                    ]
                    
                    all_passwords.update(variations_list)
            
            passwords_list = list(all_passwords)
            self.logger.info(f"🎯 Probando {len(passwords_list)} contraseñas híbridas...")
            
            # Probar todas las contraseñas
            for i, password in enumerate(passwords_list):
                if self.stop_flag:
                    break
                
                if progress_callback:
                    progress_callback(i + 1, len(passwords_list))
                
                result = self._extract_with_password(cert_path, password)
                
                if result['success']:
                    result['password_found'] = password
                    result['attempts_made'] = i + 1
                    result['total_passwords'] = len(passwords_list)
                    result['method_used'] = 'hybrid'
                    return result
            
            return {
                'success': False,
                'error': f'Contraseña no encontrada en {len(passwords_list)} intentos híbridos',
                'attempts_made': len(passwords_list)
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Error en ataque híbrido: {str(e)}'}
    def _analyze_certificate_file(self, cert_path):
        """Analiza el archivo de certificado para obtener información útil"""
        info = {
            'file_size': 0,
            'format': 'unknown',
            'rsa_size': None,
            'signature_algorithm': None,
            'subject_info': {},
            'likely_weak': False
        }
        
        try:
            # Información básica del archivo
            info['file_size'] = os.path.getsize(cert_path)
            
            # Leer contenido
            with open(cert_path, 'rb') as f:
                content = f.read()
            
            # Detectar formato
            if content.startswith(b'-----BEGIN'):
                info['format'] = 'PEM'
            elif content.startswith(b'\x30\x82'):
                info['format'] = 'DER'
            else:
                info['format'] = 'unknown'
            
            # Intentar parsear como certificado X.509
            try:
                if info['format'] == 'PEM':
                    if b'-----BEGIN CERTIFICATE-----' in content:
                        cert = x509.load_pem_x509_certificate(content)
                    elif b'-----BEGIN PRIVATE KEY-----' in content:
                        # Es una clave privada, intentar extraer información
                        try:
                            private_key = serialization.load_pem_private_key(content, password=None)
                            if hasattr(private_key, 'key_size'):
                                info['rsa_size'] = private_key.key_size
                        except:
                            pass
                        return info
                    else:
                        return info
                else:
                    cert = x509.load_der_x509_certificate(content)
                
                # Extraer información del certificado
                public_key = cert.public_key()
                if hasattr(public_key, 'key_size'):
                    info['rsa_size'] = public_key.key_size
                
                # Algoritmo de firma
                info['signature_algorithm'] = cert.signature_algorithm_oid._name
                
                # Información del sujeto
                subject = cert.subject
                for attribute in subject:
                    info['subject_info'][attribute.oid._name] = attribute.value
                
                # Determinar si es probablemente débil
                info['likely_weak'] = self._is_likely_weak_certificate(cert, info)
                
            except Exception as e:
                self.logger.debug(f"No se pudo parsear como certificado X.509: {e}")
            
            # Intentar como PKCS#12
            try:
                with open(cert_path, 'rb') as f:
                    p12_content = f.read()
                
                # Intentar con contraseña vacía primero
                try:
                    private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(p12_content, None)
                    if certificate:
                        public_key = certificate.public_key()
                        if hasattr(public_key, 'key_size'):
                            info['rsa_size'] = public_key.key_size
                        info['format'] = 'PKCS12'
                        info['signature_algorithm'] = certificate.signature_algorithm_oid._name
                except:
                    pass
                    
            except Exception as e:
                self.logger.debug(f"No se pudo parsear como PKCS#12: {e}")
            
        except Exception as e:
            self.logger.error(f"Error analizando archivo: {e}")
        
        return info
    
    def _is_likely_weak_certificate(self, cert, info):
        """Determina si un certificado es probablemente débil/de prueba"""
        weak_indicators = 0
        
        # RSA 4096 con SHA256 es considerado débil en contextos modernos
        if info.get('rsa_size') == 4096 and 'sha256' in info.get('signature_algorithm', '').lower():
            weak_indicators += 2
        
        # Certificados autofirmados son más probables de tener contraseñas débiles
        if cert.issuer == cert.subject:
            weak_indicators += 1
        
        # Nombres comunes que sugieren certificados de prueba
        subject_info = info.get('subject_info', {})
        test_patterns = ['test', 'demo', 'example', 'localhost', 'development', 'dev', 'staging']
        
        for field_value in subject_info.values():
            if isinstance(field_value, str):
                for pattern in test_patterns:
                    if pattern.lower() in field_value.lower():
                        weak_indicators += 1
                        break
        
        # Validez muy larga (más de 10 años) sugiere certificado de prueba
        try:
            validity_period = cert.not_valid_after - cert.not_valid_before
            if validity_period.days > 3650:  # 10 años
                weak_indicators += 1
        except:
            pass
        
        return weak_indicators >= 2
    
    def _generate_certificate_based_passwords(self, file_info):
        """Genera contraseñas basadas en información del certificado"""
        passwords = []
        subject_info = file_info.get('subject_info', {})
        
        # Extraer palabras de la información del sujeto
        words = []
        for value in subject_info.values():
            if isinstance(value, str):
                # Dividir por espacios, puntos, guiones, etc.
                import re
                extracted_words = re.findall(r'\w+', value.lower())
                words.extend(extracted_words)
        
        # Generar combinaciones
        for word in words:
            if len(word) >= 3:  # Solo palabras de 3+ caracteres
                passwords.extend([
                    word,
                    word.capitalize(),
                    word.upper(),
                    f"{word}123",
                    f"{word}2024",
                    f"{word}2023",
                    f"123{word}",
                    f"{word}!",
                    f"{word}_key",
                    f"{word}_password",
                    f"{word}_ca",
                    f"ca_{word}",
                    f"{word}_cert"
                ])
        
        # Añadir combinaciones con el tamaño de RSA
        if file_info.get('rsa_size'):
            rsa_size = str(file_info['rsa_size'])
            passwords.extend([
                f"rsa{rsa_size}",
                f"key{rsa_size}",
                f"cert{rsa_size}",
                rsa_size
            ])
        
        # Eliminar duplicados y devolver
        return list(set(passwords))
    
    def stop_extraction(self):
        """Detiene la extracción en curso"""
        self.stop_flag = True
        self.logger.info("🛑 Deteniendo extracción...")
    
    def reset_stop_flag(self):
        """Reinicia la bandera de parada"""
        self.stop_flag = False
