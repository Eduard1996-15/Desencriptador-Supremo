"""
Motor de Ataques del Desencriptador Supremo
Implementa múltiples tipos de ataques: fuerza bruta, diccionario, híbridos, etc.
"""

import threading
import time
import itertools
import string
import hashlib
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
import psutil
import logging

class AttackEngine:
    """Motor principal de ataques"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.stats = {
            'passwords_tried': 0,
            'start_time': 0,
            'speed': 0,
            'current_password': '',
            'estimated_time': 0
        }
        self.stop_event = threading.Event()
        self.workers = []
        
    def brute_force_attack(self, target_function, charset=None, min_length=1, max_length=8, 
                          num_threads=None, callback=None):
        """
        Ataque de fuerza bruta
        """
        if charset is None:
            charset = string.ascii_lowercase + string.digits
            
        if num_threads is None:
            num_threads = min(multiprocessing.cpu_count(), 16)
            
        self.is_running = True
        self.stop_event.clear()
        self.stats['start_time'] = time.time()
        self.stats['passwords_tried'] = 0
        
        try:
            # Usar ThreadPoolExecutor para mejor gestión de hilos
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                # Generar trabajos para cada longitud
                for length in range(min_length, max_length + 1):
                    if self.stop_event.is_set():
                        break
                        
                    # Dividir el espacio de búsqueda entre hilos
                    chunk_size = len(charset) ** length // num_threads
                    if chunk_size < 1:
                        chunk_size = 1
                    
                    futures = []
                    
                    # Crear trabajos
                    for i in range(0, len(charset) ** length, chunk_size):
                        if self.stop_event.is_set():
                            break
                            
                        future = executor.submit(
                            self._brute_force_worker,
                            target_function,
                            charset,
                            length,
                            i,
                            min(i + chunk_size, len(charset) ** length),
                            callback
                        )
                        futures.append(future)
                    
                    # Procesar resultados
                    for future in as_completed(futures):
                        if self.stop_event.is_set():
                            break
                            
                        result = future.result()
                        if result:
                            self.is_running = False
                            return result
            
            self.is_running = False
            return None
            
        except Exception as e:
            self.logger.error(f"Error en ataque de fuerza bruta: {e}")
            self.is_running = False
            return None
    
    def _brute_force_worker(self, target_function, charset, length, start_idx, end_idx, callback):
        """Worker para ataque de fuerza bruta"""
        try:
            count = 0
            for i in range(start_idx, end_idx):
                if self.stop_event.is_set():
                    return None
                
                # Generar contraseña desde índice
                password = self._index_to_password(i, charset, length)
                
                # Probar contraseña
                if target_function(password):
                    self.logger.info(f"¡Contraseña encontrada: {password}")
                    return password
                
                # Actualizar estadísticas
                count += 1
                self.stats['passwords_tried'] += 1
                self.stats['current_password'] = password
                
                # Callback para actualizar UI
                if callback and count % 100 == 0:
                    self._update_stats()
                    callback(self.stats)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error en worker de fuerza bruta: {e}")
            return None
    
    def _index_to_password(self, index, charset, length):
        """Convierte un índice a contraseña"""
        password = ""
        base = len(charset)
        
        for _ in range(length):
            password = charset[index % base] + password
            index //= base
            
        return password
    
    def dictionary_attack(self, target_function, dictionaries, num_threads=None, callback=None):
        """
        Ataque de diccionario
        """
        if num_threads is None:
            num_threads = min(multiprocessing.cpu_count(), 8)
        
        self.is_running = True
        self.stop_event.clear()
        self.stats['start_time'] = time.time()
        self.stats['passwords_tried'] = 0
        
        try:
            # Crear cola de contraseñas
            password_queue = queue.Queue()
            
            # Cargar diccionarios en la cola
            total_passwords = self._load_dictionaries(dictionaries, password_queue)
            
            if total_passwords == 0:
                self.logger.warning("No se encontraron contraseñas en los diccionarios")
                return None
            
            # Crear y ejecutar workers
            result_queue = queue.Queue()
            
            for i in range(num_threads):
                worker = threading.Thread(
                    target=self._dictionary_worker,
                    args=(target_function, password_queue, result_queue, callback)
                )
                worker.daemon = True
                worker.start()
                self.workers.append(worker)
            
            # Esperar resultado o finalización
            while self.is_running and not self.stop_event.is_set():
                try:
                    result = result_queue.get(timeout=1)
                    if result:
                        self.stop()
                        return result
                except queue.Empty:
                    # Verificar si todos los workers terminaron
                    if password_queue.empty() and all(not w.is_alive() for w in self.workers):
                        break
                    continue
            
            self.is_running = False
            return None
            
        except Exception as e:
            self.logger.error(f"Error en ataque de diccionario: {e}")
            self.is_running = False
            return None
    
    def _load_dictionaries(self, dictionaries, password_queue):
        """Carga diccionarios en la cola"""
        total_passwords = 0
        
        for dict_path in dictionaries:
            try:
                with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        password = line.strip()
                        if password:
                            password_queue.put(password)
                            total_passwords += 1
                            
            except FileNotFoundError:
                self.logger.warning(f"Diccionario no encontrado: {dict_path}")
            except Exception as e:
                self.logger.error(f"Error cargando diccionario {dict_path}: {e}")
        
        return total_passwords
    
    def _dictionary_worker(self, target_function, password_queue, result_queue, callback):
        """Worker para ataque de diccionario"""
        count = 0
        
        while not self.stop_event.is_set():
            try:
                password = password_queue.get(timeout=1)
                
                # Probar contraseña
                if target_function(password):
                    self.logger.info(f"¡Contraseña encontrada: {password}")
                    result_queue.put(password)
                    return
                
                # Actualizar estadísticas
                count += 1
                self.stats['passwords_tried'] += 1
                self.stats['current_password'] = password
                
                # Callback para actualizar UI
                if callback and count % 50 == 0:
                    self._update_stats()
                    callback(self.stats)
                
                password_queue.task_done()
                
            except queue.Empty:
                break
            except Exception as e:
                self.logger.error(f"Error en worker de diccionario: {e}")
                break
        
        result_queue.put(None)
    
    def hybrid_attack(self, target_function, base_passwords, transformations, 
                     num_threads=None, callback=None):
        """
        Ataque híbrido: aplica transformaciones a contraseñas base
        """
        if num_threads is None:
            num_threads = min(multiprocessing.cpu_count(), 8)
        
        self.is_running = True
        self.stop_event.clear()
        self.stats['start_time'] = time.time()
        self.stats['passwords_tried'] = 0
        
        try:
            # Generar todas las combinaciones
            password_queue = queue.Queue()
            
            for base_password in base_passwords:
                # Aplicar transformaciones
                variants = self._apply_transformations(base_password, transformations)
                for variant in variants:
                    password_queue.put(variant)
            
            # Ejecutar workers
            result_queue = queue.Queue()
            
            for i in range(num_threads):
                worker = threading.Thread(
                    target=self._dictionary_worker,  # Reutilizar worker de diccionario
                    args=(target_function, password_queue, result_queue, callback)
                )
                worker.daemon = True
                worker.start()
                self.workers.append(worker)
            
            # Esperar resultado
            while self.is_running and not self.stop_event.is_set():
                try:
                    result = result_queue.get(timeout=1)
                    if result:
                        self.stop()
                        return result
                except queue.Empty:
                    if password_queue.empty() and all(not w.is_alive() for w in self.workers):
                        break
                    continue
            
            self.is_running = False
            return None
            
        except Exception as e:
            self.logger.error(f"Error en ataque híbrido: {e}")
            self.is_running = False
            return None
    
    def _apply_transformations(self, base_password, transformations):
        """Aplica transformaciones a una contraseña base"""
        variants = [base_password]  # Incluir original
        
        for transform in transformations:
            new_variants = []
            
            for variant in variants:
                if transform == 'capitalize':
                    new_variants.append(variant.capitalize())
                elif transform == 'upper':
                    new_variants.append(variant.upper())
                elif transform == 'lower':
                    new_variants.append(variant.lower())
                elif transform == 'reverse':
                    new_variants.append(variant[::-1])
                elif transform == 'l33t':
                    new_variants.append(self._apply_l33t(variant))
                elif transform.startswith('append_'):
                    suffix = transform[7:]  # Remove 'append_'
                    new_variants.append(variant + suffix)
                elif transform.startswith('prepend_'):
                    prefix = transform[8:]  # Remove 'prepend_'
                    new_variants.append(prefix + variant)
                elif transform.startswith('year_'):
                    year = transform[5:]
                    new_variants.extend([variant + year, year + variant])
                    
            variants.extend(new_variants)
        
        return list(set(variants))  # Eliminar duplicados
    
    def _apply_l33t(self, password):
        """Aplica transformaciones l33t speak"""
        l33t_map = {
            'a': '4', 'A': '4',
            'e': '3', 'E': '3',
            'i': '1', 'I': '1',
            'o': '0', 'O': '0',
            's': '5', 'S': '5',
            't': '7', 'T': '7',
            'l': '1', 'L': '1'
        }
        
        result = ""
        for char in password:
            result += l33t_map.get(char, char)
        
        return result
    
    def mask_attack(self, target_function, mask, num_threads=None, callback=None):
        """
        Ataque con máscara (ej: ?l?l?l?d?d?d para 3 letras + 3 dígitos)
        """
        charset_map = {
            '?l': string.ascii_lowercase,
            '?u': string.ascii_uppercase,
            '?d': string.digits,
            '?s': string.punctuation,
            '?a': string.ascii_letters + string.digits + string.punctuation
        }
        
        # Parsear máscara
        positions = []
        i = 0
        while i < len(mask):
            if i < len(mask) - 1 and mask[i:i+2] in charset_map:
                positions.append(charset_map[mask[i:i+2]])
                i += 2
            else:
                positions.append([mask[i]])  # Carácter literal
                i += 1
        
        if not positions:
            return None
        
        self.is_running = True
        self.stop_event.clear()
        self.stats['start_time'] = time.time()
        self.stats['passwords_tried'] = 0
        
        try:
            if num_threads is None:
                num_threads = min(multiprocessing.cpu_count(), 16)
            
            # Calcular total de combinaciones
            total_combinations = 1
            for pos in positions:
                total_combinations *= len(pos)
            
            # Dividir trabajo entre hilos
            chunk_size = max(1, total_combinations // num_threads)
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                
                for i in range(0, total_combinations, chunk_size):
                    future = executor.submit(
                        self._mask_worker,
                        target_function,
                        positions,
                        i,
                        min(i + chunk_size, total_combinations),
                        callback
                    )
                    futures.append(future)
                
                # Procesar resultados
                for future in as_completed(futures):
                    if self.stop_event.is_set():
                        break
                    
                    result = future.result()
                    if result:
                        self.is_running = False
                        return result
            
            self.is_running = False
            return None
            
        except Exception as e:
            self.logger.error(f"Error en ataque con máscara: {e}")
            self.is_running = False
            return None
    
    def _mask_worker(self, target_function, positions, start_idx, end_idx, callback):
        """Worker para ataque con máscara"""
        try:
            count = 0
            for i in range(start_idx, end_idx):
                if self.stop_event.is_set():
                    return None
                
                # Generar contraseña desde índice
                password = self._index_to_mask_password(i, positions)
                
                # Probar contraseña
                if target_function(password):
                    self.logger.info(f"¡Contraseña encontrada: {password}")
                    return password
                
                # Actualizar estadísticas
                count += 1
                self.stats['passwords_tried'] += 1
                self.stats['current_password'] = password
                
                # Callback para actualizar UI
                if callback and count % 100 == 0:
                    self._update_stats()
                    callback(callback)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error en worker de máscara: {e}")
            return None
    
    def _index_to_mask_password(self, index, positions):
        """Convierte índice a contraseña según máscara"""
        password = ""
        
        for position in reversed(positions):
            password = position[index % len(position)] + password
            index //= len(position)
        
        return password
    
    def rainbow_table_attack(self, target_hash, table_path):
        """
        Ataque con tablas arcoíris (implementación básica)
        """
        try:
            self.logger.info(f"Buscando hash {target_hash} en tabla arcoíris...")
            
            with open(table_path, 'r') as f:
                for line in f:
                    parts = line.strip().split(':')
                    if len(parts) == 2:
                        stored_hash, password = parts
                        if stored_hash.lower() == target_hash.lower():
                            self.logger.info(f"¡Hash encontrado en tabla arcoíris: {password}")
                            return password
            
            return None
            
        except FileNotFoundError:
            self.logger.error(f"Tabla arcoíris no encontrada: {table_path}")
            return None
        except Exception as e:
            self.logger.error(f"Error en ataque con tabla arcoíris: {e}")
            return None
    
    def _update_stats(self):
        """Actualiza estadísticas del ataque"""
        current_time = time.time()
        elapsed_time = current_time - self.stats['start_time']
        
        if elapsed_time > 0:
            self.stats['speed'] = self.stats['passwords_tried'] / elapsed_time
            
            # Estimar tiempo restante (muy aproximado)
            if self.stats['speed'] > 0:
                # Esto es muy simplificado, en realidad depende del espacio de búsqueda
                self.stats['estimated_time'] = "Calculando..."
            else:
                self.stats['estimated_time'] = "∞"
    
    def stop(self):
        """Detiene todos los ataques en curso"""
        self.logger.info("Deteniendo ataques...")
        self.stop_event.set()
        self.is_running = False
        
        # Esperar a que terminen los workers
        for worker in self.workers:
            if worker.is_alive():
                worker.join(timeout=5)
        
        self.workers.clear()
    
    def get_stats(self):
        """Obtiene estadísticas actuales"""
        self._update_stats()
        return self.stats.copy()
    
    def estimate_time(self, charset_size, password_length, passwords_per_second):
        """Estima tiempo para ataque de fuerza bruta"""
        total_combinations = charset_size ** password_length
        if passwords_per_second > 0:
            seconds = total_combinations / passwords_per_second
            return self._format_time(seconds)
        return "∞"
    
    def _format_time(self, seconds):
        """Formatea tiempo en formato legible"""
        if seconds < 60:
            return f"{seconds:.1f} segundos"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minutos"
        elif seconds < 86400:
            return f"{seconds/3600:.1f} horas"
        elif seconds < 31536000:
            return f"{seconds/86400:.1f} días"
        else:
            return f"{seconds/31536000:.1f} años"
