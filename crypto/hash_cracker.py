"""
Hash Cracker para el Desencriptador Supremo
Soporte para múltiples tipos de hash y métodos de cracking
"""

import hashlib
import bcrypt
import hmac
import binascii
import re
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
import time
import logging

class HashCracker:
    """Crackeador de hashes principal"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_hashes = {
            'md5': self._crack_md5,
            'sha1': self._crack_sha1,
            'sha256': self._crack_sha256,
            'sha512': self._crack_sha512,
            'ntlm': self._crack_ntlm,
            'bcrypt': self._crack_bcrypt,
            'lm': self._crack_lm
        }
        
        # Patrones para auto-detección
        self.hash_patterns = {
            'md5': re.compile(r'^[a-fA-F0-9]{32}$'),
            'sha1': re.compile(r'^[a-fA-F0-9]{40}$'),
            'sha256': re.compile(r'^[a-fA-F0-9]{64}$'),
            'sha512': re.compile(r'^[a-fA-F0-9]{128}$'),
            'ntlm': re.compile(r'^[a-fA-F0-9]{32}$'),
            'bcrypt': re.compile(r'^\$2[aby]?\$[0-9]{2}\$[./A-Za-z0-9]{53}$'),
            'lm': re.compile(r'^[a-fA-F0-9]{32}$')
        }
        
        self.is_running = False
        self.stop_event = threading.Event()
        
    def detect_hash_type(self, hash_string):
        """Auto-detecta el tipo de hash"""
        hash_string = hash_string.strip()
        
        detected_types = []
        
        for hash_type, pattern in self.hash_patterns.items():
            if pattern.match(hash_string):
                # Dar prioridades específicas
                if hash_type == 'bcrypt' and hash_string.startswith('$2'):
                    detected_types.append((hash_type, 0.95))
                elif hash_type == 'sha256' and len(hash_string) == 64:
                    detected_types.append((hash_type, 0.8))
                elif hash_type == 'sha1' and len(hash_string) == 40:
                    detected_types.append((hash_type, 0.7))
                elif hash_type == 'md5' and len(hash_string) == 32:
                    detected_types.append((hash_type, 0.6))
                elif hash_type == 'sha512' and len(hash_string) == 128:
                    detected_types.append((hash_type, 0.9))
                else:
                    detected_types.append((hash_type, 0.5))
        
        # Ordenar por confianza
        detected_types.sort(key=lambda x: x[1], reverse=True)
        
        return detected_types if detected_types else [('unknown', 0.0)]
    
    def crack_hash(self, hash_string, hash_type=None, wordlists=None, max_threads=8, callback=None):
        """Intenta crackear un hash"""
        try:
            hash_string = hash_string.strip().lower()
            
            # Auto-detectar tipo si no se especifica
            if hash_type is None:
                detected = self.detect_hash_type(hash_string)
                if detected and detected[0][1] > 0.5:
                    hash_type = detected[0][0]
                else:
                    return {'success': False, 'error': 'Tipo de hash no detectado'}
            
            hash_type = hash_type.lower()
            
            if hash_type not in self.supported_hashes:
                return {'success': False, 'error': f'Tipo de hash no soportado: {hash_type}'}
            
            self.is_running = True
            self.stop_event.clear()
            
            # Preparar wordlists
            if not wordlists:
                wordlists = self._get_default_wordlists()
            
            # Crear cola de contraseñas
            password_queue = queue.Queue()
            result_queue = queue.Queue()
            
            # Cargar contraseñas en la cola
            total_passwords = self._load_wordlists(wordlists, password_queue)
            
            if total_passwords == 0:
                return {'success': False, 'error': 'No se encontraron contraseñas en los diccionarios'}
            
            # Iniciar workers
            crack_function = self.supported_hashes[hash_type]
            
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                # Enviar trabajos
                futures = []
                for i in range(max_threads):
                    future = executor.submit(
                        self._hash_worker,
                        crack_function,
                        hash_string,
                        password_queue,
                        result_queue,
                        callback
                    )
                    futures.append(future)
                
                # Esperar resultado
                start_time = time.time()
                while self.is_running and not self.stop_event.is_set():
                    try:
                        result = result_queue.get(timeout=1)
                        if result:
                            self.stop()
                            elapsed_time = time.time() - start_time
                            return {
                                'success': True,
                                'password': result,
                                'hash_type': hash_type,
                                'time_elapsed': elapsed_time,
                                'attempts': total_passwords - password_queue.qsize()
                            }
                    except queue.Empty:
                        if password_queue.empty():
                            break
                        continue
            
            self.is_running = False
            elapsed_time = time.time() - start_time
            return {
                'success': False,
                'error': 'Hash no crackeado',
                'hash_type': hash_type,
                'time_elapsed': elapsed_time,
                'attempts': total_passwords
            }
            
        except Exception as e:
            self.logger.error(f"Error crackeando hash: {e}")
            return {'success': False, 'error': str(e)}
    
    def _hash_worker(self, crack_function, target_hash, password_queue, result_queue, callback):
        """Worker para cracking de hashes"""
        attempts = 0
        
        while not self.stop_event.is_set():
            try:
                password = password_queue.get(timeout=1)
                
                # Probar contraseña
                if crack_function(target_hash, password):
                    result_queue.put(password)
                    return
                
                attempts += 1
                
                # Callback para estadísticas
                if callback and attempts % 1000 == 0:
                    callback({
                        'attempts': attempts,
                        'current_password': password,
                        'queue_size': password_queue.qsize()
                    })
                
                password_queue.task_done()
                
            except queue.Empty:
                break
            except Exception as e:
                self.logger.error(f"Error en worker de hash: {e}")
                break
        
        result_queue.put(None)
    
    def _crack_md5(self, target_hash, password):
        """Crackea hash MD5"""
        try:
            test_hash = hashlib.md5(password.encode()).hexdigest().lower()
            return test_hash == target_hash.lower()
        except:
            return False
    
    def _crack_sha1(self, target_hash, password):
        """Crackea hash SHA1"""
        try:
            test_hash = hashlib.sha1(password.encode()).hexdigest().lower()
            return test_hash == target_hash.lower()
        except:
            return False
    
    def _crack_sha256(self, target_hash, password):
        """Crackea hash SHA256"""
        try:
            test_hash = hashlib.sha256(password.encode()).hexdigest().lower()
            return test_hash == target_hash.lower()
        except:
            return False
    
    def _crack_sha512(self, target_hash, password):
        """Crackea hash SHA512"""
        try:
            test_hash = hashlib.sha512(password.encode()).hexdigest().lower()
            return test_hash == target_hash.lower()
        except:
            return False
    
    def _crack_ntlm(self, target_hash, password):
        """Crackea hash NTLM"""
        try:
            # NTLM = MD4(UTF-16LE(password))
            password_utf16 = password.encode('utf-16le')
            test_hash = hashlib.new('md4', password_utf16).hexdigest().lower()
            return test_hash == target_hash.lower()
        except:
            return False
    
    def _crack_bcrypt(self, target_hash, password):
        """Crackea hash bcrypt"""
        try:
            return bcrypt.checkpw(password.encode(), target_hash.encode())
        except:
            return False
    
    def _crack_lm(self, target_hash, password):
        """Crackea hash LM (simplificado)"""
        try:
            # LM hash es más complejo, implementación básica
            # Convertir a mayúsculas y truncar a 14 caracteres
            password = password.upper()[:14]
            
            # Rellenar con nulos si es necesario
            password = password.ljust(14, '\x00')
            
            # Dividir en dos partes de 7 caracteres
            left = password[:7]
            right = password[7:]
            
            # Simular el hash LM (implementación simplificada)
            # En una implementación real, usarías DES con claves específicas
            test_hash = hashlib.md5((left + right).encode()).hexdigest().lower()
            return test_hash == target_hash.lower()
        except:
            return False
    
    def _load_wordlists(self, wordlists, password_queue):
        """Carga wordlists en la cola"""
        total_passwords = 0
        
        for wordlist_path in wordlists:
            try:
                with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        password = line.strip()
                        if password:
                            password_queue.put(password)
                            total_passwords += 1
                            
                            # También probar variaciones comunes
                            variations = self._generate_variations(password)
                            for variation in variations:
                                password_queue.put(variation)
                                total_passwords += 1
                                
            except FileNotFoundError:
                self.logger.warning(f"Wordlist no encontrada: {wordlist_path}")
            except Exception as e:
                self.logger.error(f"Error cargando wordlist {wordlist_path}: {e}")
        
        return total_passwords
    
    def _generate_variations(self, password):
        """Genera variaciones comunes de una contraseña"""
        variations = []
        
        # Variaciones básicas
        variations.append(password.capitalize())
        variations.append(password.upper())
        variations.append(password.lower())
        
        # Variaciones con números
        for i in range(10):
            variations.append(password + str(i))
            variations.append(str(i) + password)
        
        # Variaciones comunes
        variations.extend([
            password + "!",
            password + "123",
            password + "1",
            "123" + password,
            password + "2024",
            password + "2025"
        ])
        
        return list(set(variations))  # Eliminar duplicados
    
    def _get_default_wordlists(self):
        """Obtiene wordlists por defecto"""
        default_lists = [
            "./data/common-passwords.txt",
            "./data/spanish.txt"
        ]
        
        # Verificar que existan
        existing_lists = []
        for wordlist in default_lists:
            if os.path.exists(wordlist):
                existing_lists.append(wordlist)
        
        return existing_lists
    
    def calculate_hash(self, text, hash_type):
        """Calcula hash de un texto"""
        try:
            hash_type = hash_type.lower()
            
            if hash_type == 'md5':
                return hashlib.md5(text.encode()).hexdigest()
            elif hash_type == 'sha1':
                return hashlib.sha1(text.encode()).hexdigest()
            elif hash_type == 'sha256':
                return hashlib.sha256(text.encode()).hexdigest()
            elif hash_type == 'sha512':
                return hashlib.sha512(text.encode()).hexdigest()
            elif hash_type == 'ntlm':
                return hashlib.new('md4', text.encode('utf-16le')).hexdigest()
            elif hash_type == 'bcrypt':
                salt = bcrypt.gensalt()
                return bcrypt.hashpw(text.encode(), salt).decode()
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Error calculando hash: {e}")
            return None
    
    def stop(self):
        """Detiene el cracking"""
        self.is_running = False
        self.stop_event.set()
    
    def get_hash_info(self, hash_string):
        """Obtiene información detallada sobre un hash"""
        detected_types = self.detect_hash_type(hash_string)
        
        info = {
            'hash': hash_string,
            'length': len(hash_string),
            'detected_types': detected_types,
            'is_hex': all(c in '0123456789abcdefABCDEF' for c in hash_string),
            'possible_algorithms': []
        }
        
        # Información específica por longitud
        length = len(hash_string)
        if length == 32:
            info['possible_algorithms'].extend(['MD5', 'NTLM', 'LM'])
        elif length == 40:
            info['possible_algorithms'].append('SHA1')
        elif length == 64:
            info['possible_algorithms'].append('SHA256')
        elif length == 128:
            info['possible_algorithms'].append('SHA512')
        
        return info
