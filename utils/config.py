"""
Sistema de Configuración para el Desencriptador Supremo
"""

import json
import os
from pathlib import Path
import logging

class Config:
    """Manejador de configuración de la aplicación"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        
        # Configuración por defecto
        self.default_config = {
            "general": {
                "theme": "dark",
                "language": "es",
                "auto_save": True,
                "backup_enabled": True
            },
            "performance": {
                "use_gpu": True,
                "use_multithread": True,
                "max_threads": 16,
                "memory_optimization": False,
                "cache_enabled": True,
                "cache_size_mb": 512
            },
            "attacks": {
                "default_charset": "abcdefghijklmnopqrstuvwxyz0123456789",
                "max_password_length": 12,
                "timeout_minutes": 60,
                "save_progress": True,
                "auto_resume": True
            },
            "paths": {
                "dictionaries": "./data/dictionaries/",
                "wordlists": "./data/wordlists/",
                "certificates": "./data/certificates/",
                "output": "./output/",
                "temp": "./temp/",
                "logs": "./logs/"
            },
            "security": {
                "log_passwords": False,
                "secure_delete": True,
                "encrypt_temp_files": True,
                "audit_trail": True
            },
            "advanced": {
                "debug_mode": False,
                "verbose_logging": False,
                "experimental_features": False,
                "cuda_device_id": 0,
                "opencl_platform": 0
            }
        }
        
        self.config = self.default_config.copy()
        
    def load_config(self):
        """Carga la configuración desde archivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    
                # Merge con configuración por defecto
                self._merge_config(self.config, loaded_config)
                self.logger.info("Configuración cargada exitosamente")
            else:
                self.logger.info("Archivo de configuración no encontrado, usando configuración por defecto")
                self.save_config()
                
        except Exception as e:
            self.logger.error(f"Error cargando configuración: {e}")
            self.logger.info("Usando configuración por defecto")
    
    def save_config(self):
        """Guarda la configuración actual al archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            self.logger.info("Configuración guardada exitosamente")
            return True
        except Exception as e:
            self.logger.error(f"Error guardando configuración: {e}")
            return False
    
    def _merge_config(self, default, loaded):
        """Merge recursivo de configuraciones"""
        for key, value in loaded.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
            else:
                default[key] = value
    
    def get(self, section, key=None, default=None):
        """Obtiene un valor de configuración"""
        try:
            if key is None:
                return self.config.get(section, default)
            else:
                return self.config.get(section, {}).get(key, default)
        except:
            return default
    
    def set(self, section, key, value):
        """Establece un valor de configuración"""
        try:
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = value
            return True
        except Exception as e:
            self.logger.error(f"Error estableciendo configuración: {e}")
            return False
    
    def reset_to_defaults(self):
        """Resetea la configuración a valores por defecto"""
        self.config = self.default_config.copy()
        self.save_config()
        self.logger.info("Configuración reseteada a valores por defecto")
    
    def create_directories(self):
        """Crea los directorios necesarios según la configuración"""
        paths = self.get("paths", default={})
        
        for path_name, path_value in paths.items():
            try:
                Path(path_value).mkdir(parents=True, exist_ok=True)
                self.logger.debug(f"Directorio creado/verificado: {path_value}")
            except Exception as e:
                self.logger.error(f"Error creando directorio {path_value}: {e}")
    
    def validate_config(self):
        """Valida la configuración actual"""
        errors = []
        
        # Validar paths
        paths = self.get("paths", default={})
        for path_name, path_value in paths.items():
            if not isinstance(path_value, str):
                errors.append(f"Path {path_name} debe ser una cadena")
        
        # Validar performance
        performance = self.get("performance", default={})
        max_threads = performance.get("max_threads", 1)
        if not isinstance(max_threads, int) or max_threads < 1 or max_threads > 64:
            errors.append("max_threads debe ser un entero entre 1 y 64")
        
        cache_size = performance.get("cache_size_mb", 512)
        if not isinstance(cache_size, int) or cache_size < 64 or cache_size > 8192:
            errors.append("cache_size_mb debe ser un entero entre 64 y 8192")
        
        # Validar attacks
        attacks = self.get("attacks", default={})
        max_length = attacks.get("max_password_length", 12)
        if not isinstance(max_length, int) or max_length < 1 or max_length > 32:
            errors.append("max_password_length debe ser un entero entre 1 y 32")
        
        timeout = attacks.get("timeout_minutes", 60)
        if not isinstance(timeout, int) or timeout < 1:
            errors.append("timeout_minutes debe ser un entero positivo")
        
        if errors:
            self.logger.warning(f"Errores de validación en configuración: {errors}")
            return False, errors
        
        self.logger.info("Configuración validada exitosamente")
        return True, []
    
    def export_config(self, file_path):
        """Exporta la configuración a un archivo específico"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            self.logger.info(f"Configuración exportada a: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error exportando configuración: {e}")
            return False
    
    def import_config(self, file_path):
        """Importa configuración desde un archivo específico"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Validar configuración importada
            temp_config = self.config.copy()
            self._merge_config(temp_config, imported_config)
            
            # Si la validación pasa, aplicar la configuración
            self.config = temp_config
            self.save_config()
            
            self.logger.info(f"Configuración importada desde: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error importando configuración: {e}")
            return False
    
    def get_performance_config(self):
        """Obtiene configuración optimizada de rendimiento"""
        return {
            'use_gpu': self.get("performance", "use_gpu", True),
            'use_multithread': self.get("performance", "use_multithread", True),
            'max_threads': min(self.get("performance", "max_threads", 16), 32),
            'memory_optimization': self.get("performance", "memory_optimization", False),
            'cache_enabled': self.get("performance", "cache_enabled", True),
            'cache_size_mb': self.get("performance", "cache_size_mb", 512)
        }
    
    def get_attack_config(self):
        """Obtiene configuración para ataques"""
        return {
            'default_charset': self.get("attacks", "default_charset", "abcdefghijklmnopqrstuvwxyz0123456789"),
            'max_password_length': self.get("attacks", "max_password_length", 12),
            'timeout_minutes': self.get("attacks", "timeout_minutes", 60),
            'save_progress': self.get("attacks", "save_progress", True),
            'auto_resume': self.get("attacks", "auto_resume", True)
        }
    
    def get_paths_config(self):
        """Obtiene configuración de rutas"""
        return self.get("paths", default={})
    
    def get_security_config(self):
        """Obtiene configuración de seguridad"""
        return {
            'log_passwords': self.get("security", "log_passwords", False),
            'secure_delete': self.get("security", "secure_delete", True),
            'encrypt_temp_files': self.get("security", "encrypt_temp_files", True),
            'audit_trail': self.get("security", "audit_trail", True)
        }
