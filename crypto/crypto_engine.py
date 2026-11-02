"""
Motor Criptográfico del Desencriptador Supremo
Maneja múltiples algoritmos de encriptación y desencriptación
"""

import os
import hashlib
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization, padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES, DES, DES3, Blowfish, ChaCha20
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import logging

class CryptoEngine:
    """Motor principal de criptografía"""
    
    def __init__(self):
        self.backend = default_backend()
        self.logger = logging.getLogger(__name__)
        self.supported_algorithms = {
            'AES-256-CBC': self._aes_decrypt,
            'AES-256-GCM': self._aes_gcm_decrypt,
            'AES-128-CBC': self._aes_decrypt,
            'RSA': self._rsa_decrypt,
            'DES': self._des_decrypt,
            '3DES': self._3des_decrypt,
            'Blowfish': self._blowfish_decrypt,
            'ChaCha20': self._chacha20_decrypt,
            'RC4': self._rc4_decrypt
        }
        
    def detect_encryption_type(self, data):
        """
        Detecta automáticamente el tipo de encriptación
        """
        try:
            # Análisis de entropía
            entropy = self._calculate_entropy(data)
            
            # Análisis de patrones
            patterns = self._analyze_patterns(data)
            
            # Análisis de headers
            headers = self._analyze_headers(data)
            
            # Determinar tipo más probable
            candidates = []
            
            if entropy > 7.5:  # Alta entropía = probablemente encriptado
                if len(data) % 16 == 0:
                    candidates.append(('AES', 0.8))
                if len(data) % 8 == 0:
                    candidates.extend([('DES', 0.6), ('3DES', 0.7), ('Blowfish', 0.6)])
                if patterns.get('base64_like', False):
                    candidates.append(('Base64+Crypto', 0.7))
                    
            # Verificar headers específicos
            if headers:
                for header_type, confidence in headers:
                    candidates.append((header_type, confidence))
                    
            # Ordenar por confianza
            candidates.sort(key=lambda x: x[1], reverse=True)
            
            return candidates if candidates else [('Unknown', 0.0)]
            
        except Exception as e:
            self.logger.error(f"Error detectando tipo de encriptación: {e}")
            return [('Unknown', 0.0)]
    
    def _calculate_entropy(self, data):
        """Calcula la entropía de Shannon"""
        if not data:
            return 0
            
        # Contar frecuencias
        freq = {}
        for byte in data:
            freq[byte] = freq.get(byte, 0) + 1
            
        # Calcular entropía
        entropy = 0
        length = len(data)
        for count in freq.values():
            p = count / length
            if p > 0:
                entropy -= p * (p.bit_length() - 1)
                
        return entropy
    
    def _analyze_patterns(self, data):
        """Analiza patrones en los datos"""
        patterns = {}
        
        # Verificar si parece Base64
        try:
            base64.b64decode(data)
            patterns['base64_like'] = True
        except:
            patterns['base64_like'] = False
            
        # Verificar repeticiones
        patterns['repetitions'] = len(data) - len(set(data))
        
        # Verificar secuencias
        sequences = 0
        for i in range(len(data) - 1):
            if isinstance(data[i], int) and isinstance(data[i+1], int):
                if abs(data[i] - data[i+1]) == 1:
                    sequences += 1
        patterns['sequences'] = sequences
        
        return patterns
    
    def _analyze_headers(self, data):
        """Analiza headers para identificar formato"""
        headers = []
        
        if not data:
            return headers
            
        # Headers comunes
        header_signatures = {
            b'-----BEGIN CERTIFICATE-----': ('X509_PEM', 0.9),
            b'-----BEGIN PRIVATE KEY-----': ('RSA_PEM', 0.9),
            b'-----BEGIN RSA PRIVATE KEY-----': ('RSA_PEM', 0.95),
            b'-----BEGIN ENCRYPTED PRIVATE KEY-----': ('Encrypted_PEM', 0.95),
            b'\x30\x82': ('DER_Certificate', 0.8),
            b'PK\x03\x04': ('ZIP_Archive', 0.9),
            b'\x89PNG': ('PNG_Image', 0.95),
            b'\xff\xd8\xff': ('JPEG_Image', 0.95)
        }
        
        for signature, (type_name, confidence) in header_signatures.items():
            if data.startswith(signature):
                headers.append((type_name, confidence))
                
        return headers
    
    def decrypt_with_password(self, encrypted_data, password, algorithm=None):
        """
        Intenta desencriptar datos con una contraseña
        """
        try:
            if algorithm is None:
                # Auto-detectar algoritmo
                detected = self.detect_encryption_type(encrypted_data)
                if detected and detected[0][1] > 0.5:
                    algorithm = detected[0][0]
                else:
                    # Probar algoritmos comunes
                    algorithms_to_try = ['AES-256-CBC', 'AES-128-CBC', 'DES', '3DES']
                    for algo in algorithms_to_try:
                        try:
                            result = self._try_decrypt(encrypted_data, password, algo)
                            if result:
                                return result, algo
                        except:
                            continue
                    return None, None
            
            # Intentar desencriptar con algoritmo específico
            if algorithm in self.supported_algorithms:
                result = self.supported_algorithms[algorithm](encrypted_data, password)
                return result, algorithm
            else:
                raise ValueError(f"Algoritmo no soportado: {algorithm}")
                
        except Exception as e:
            self.logger.error(f"Error desencriptando: {e}")
            return None, None
    
    def _try_decrypt(self, data, password, algorithm):
        """Intenta desencriptar con un algoritmo específico"""
        try:
            return self.supported_algorithms[algorithm](data, password)
        except:
            return None
    
    def _aes_decrypt(self, encrypted_data, password, key_size=256):
        """Desencripta usando AES"""
        try:
            # Asumir que los primeros 16 bytes son el IV
            if len(encrypted_data) < 32:
                return None
                
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]
            
            # Derivar clave de la contraseña
            salt = iv  # Usar IV como salt por simplicidad
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=key_size // 8,
                salt=salt,
                iterations=100000,
                backend=self.backend
            )
            key = kdf.derive(password.encode())
            
            # Desencriptar
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            decrypted = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Remover padding
            unpadder = padding.PKCS7(128).unpadder()
            unpadded = unpadder.update(decrypted) + unpadder.finalize()
            
            return unpadded
            
        except Exception as e:
            self.logger.debug(f"AES decrypt failed: {e}")
            return None
    
    def _aes_gcm_decrypt(self, encrypted_data, password):
        """Desencripta usando AES-GCM"""
        try:
            if len(encrypted_data) < 28:  # IV(12) + Tag(16)
                return None
                
            iv = encrypted_data[:12]
            tag = encrypted_data[-16:]
            ciphertext = encrypted_data[12:-16]
            
            # Derivar clave
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=iv,
                iterations=100000,
                backend=self.backend
            )
            key = kdf.derive(password.encode())
            
            # Desencriptar
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(iv, tag),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            decrypted = decryptor.update(ciphertext) + decryptor.finalize()
            
            return decrypted
            
        except Exception as e:
            self.logger.debug(f"AES-GCM decrypt failed: {e}")
            return None
    
    def _rsa_decrypt(self, encrypted_data, private_key_data):
        """Desencripta usando RSA"""
        try:
            # Cargar clave privada
            try:
                private_key = serialization.load_pem_private_key(
                    private_key_data.encode() if isinstance(private_key_data, str) else private_key_data,
                    password=None,
                    backend=self.backend
                )
            except:
                # Intentar con contraseña
                private_key = serialization.load_pem_private_key(
                    private_key_data.encode() if isinstance(private_key_data, str) else private_key_data,
                    password=b"",  # Contraseña vacía
                    backend=self.backend
                )
            
            # Desencriptar
            decrypted = private_key.decrypt(
                encrypted_data,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            return decrypted
            
        except Exception as e:
            self.logger.debug(f"RSA decrypt failed: {e}")
            return None
    
    def _des_decrypt(self, encrypted_data, password):
        """Desencripta usando DES"""
        try:
            from Crypto.Cipher import DES
            
            if len(encrypted_data) < 16:
                return None
                
            iv = encrypted_data[:8]
            ciphertext = encrypted_data[8:]
            
            # Preparar clave (DES usa 8 bytes)
            key = hashlib.md5(password.encode()).digest()[:8]
            
            cipher = DES.new(key, DES.MODE_CBC, iv)
            decrypted = cipher.decrypt(ciphertext)
            
            # Remover padding
            pad_len = decrypted[-1] if isinstance(decrypted[-1], int) else ord(decrypted[-1])
            if pad_len <= 8:
                decrypted = decrypted[:-pad_len]
            
            return decrypted
            
        except Exception as e:
            self.logger.debug(f"DES decrypt failed: {e}")
            return None
    
    def _3des_decrypt(self, encrypted_data, password):
        """Desencripta usando 3DES"""
        try:
            from Crypto.Cipher import DES3
            
            if len(encrypted_data) < 16:
                return None
                
            iv = encrypted_data[:8]
            ciphertext = encrypted_data[8:]
            
            # Preparar clave (3DES usa 24 bytes)
            key_material = hashlib.sha256(password.encode()).digest()
            key = key_material[:24]
            
            cipher = DES3.new(key, DES3.MODE_CBC, iv)
            decrypted = cipher.decrypt(ciphertext)
            
            # Remover padding
            pad_len = decrypted[-1] if isinstance(decrypted[-1], int) else ord(decrypted[-1])
            if pad_len <= 8:
                decrypted = decrypted[:-pad_len]
            
            return decrypted
            
        except Exception as e:
            self.logger.debug(f"3DES decrypt failed: {e}")
            return None
    
    def _blowfish_decrypt(self, encrypted_data, password):
        """Desencripta usando Blowfish"""
        try:
            from Crypto.Cipher import Blowfish
            
            if len(encrypted_data) < 16:
                return None
                
            iv = encrypted_data[:8]
            ciphertext = encrypted_data[8:]
            
            # Preparar clave
            key = hashlib.sha256(password.encode()).digest()[:56]  # Máximo 56 bytes
            
            cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
            decrypted = cipher.decrypt(ciphertext)
            
            # Remover padding
            pad_len = decrypted[-1] if isinstance(decrypted[-1], int) else ord(decrypted[-1])
            if pad_len <= 8:
                decrypted = decrypted[:-pad_len]
            
            return decrypted
            
        except Exception as e:
            self.logger.debug(f"Blowfish decrypt failed: {e}")
            return None
    
    def _chacha20_decrypt(self, encrypted_data, password):
        """Desencripta usando ChaCha20"""
        try:
            if len(encrypted_data) < 12:
                return None
                
            nonce = encrypted_data[:12]
            ciphertext = encrypted_data[12:]
            
            # Derivar clave
            key = hashlib.sha256(password.encode()).digest()
            
            cipher = ChaCha20.new(key=key, nonce=nonce)
            decrypted = cipher.decrypt(ciphertext)
            
            return decrypted
            
        except Exception as e:
            self.logger.debug(f"ChaCha20 decrypt failed: {e}")
            return None
    
    def _rc4_decrypt(self, encrypted_data, password):
        """Desencripta usando RC4"""
        try:
            from Crypto.Cipher import ARC4
            
            # Preparar clave
            key = hashlib.sha256(password.encode()).digest()
            
            cipher = ARC4.new(key)
            decrypted = cipher.decrypt(encrypted_data)
            
            return decrypted
            
        except Exception as e:
            self.logger.debug(f"RC4 decrypt failed: {e}")
            return None
    
    def verify_decryption(self, decrypted_data):
        """
        Verifica si los datos desencriptados son válidos
        """
        if not decrypted_data:
            return False, "Datos vacíos"
        
        # Verificaciones básicas
        checks = []
        
        # 1. Verificar si contiene texto legible
        try:
            text = decrypted_data.decode('utf-8')
            printable_ratio = sum(1 for c in text if c.isprintable()) / len(text)
            if printable_ratio > 0.8:
                checks.append(("Texto UTF-8 válido", 0.9))
        except:
            pass
        
        # 2. Verificar entropía (debe ser menor que datos encriptados)
        entropy = self._calculate_entropy(decrypted_data)
        if entropy < 6.0:  # Entropía baja indica éxito probable
            checks.append(("Entropía baja", 0.7))
        
        # 3. Verificar patrones conocidos
        if b'<?xml' in decrypted_data[:100]:
            checks.append(("XML detectado", 0.95))
        elif b'{\n' in decrypted_data[:50] or b'{\r\n' in decrypted_data[:50]:
            checks.append(("JSON/Config detectado", 0.8))
        elif decrypted_data.startswith(b'-----BEGIN'):
            checks.append(("Formato PEM detectado", 0.95))
        
        # Calcular confianza total
        if checks:
            confidence = max(check[1] for check in checks)
            reasons = [check[0] for check in checks]
            return True, f"Confianza: {confidence:.2f} - {', '.join(reasons)}"
        else:
            return False, "No se detectaron patrones válidos"
    
    def get_encryption_info(self, data):
        """Obtiene información detallada sobre la encriptación"""
        info = {
            'size': len(data),
            'entropy': self._calculate_entropy(data),
            'detected_types': self.detect_encryption_type(data),
            'patterns': self._analyze_patterns(data),
            'headers': self._analyze_headers(data)
        }
        
        return info
