"""
Sistema de Logging para el Desencriptador Supremo
"""

import logging
import os
from datetime import datetime
import sys

class Logger:
    """Manejador de logs de la aplicación"""
    
    def __init__(self, log_level=logging.INFO):
        self.log_level = log_level
        self.setup_logging()
        
    def setup_logging(self):
        """Configura el sistema de logging"""
        # Crear directorio de logs si no existe
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Nombre del archivo de log con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"desencriptador_{timestamp}.log")
        
        # Configurar formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Configurar logger principal
        self.logger = logging.getLogger('DesencriptadorSupremo')
        self.logger.setLevel(self.log_level)
        
        # Handler para archivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Log inicial
        self.logger.info("Sistema de logging inicializado")
        self.logger.info(f"Archivo de log: {log_file}")
    
    def debug(self, message):
        """Log nivel DEBUG"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log nivel INFO"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log nivel WARNING"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log nivel ERROR"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log nivel CRITICAL"""
        self.logger.critical(message)
    
    def log_attack_start(self, attack_type, parameters):
        """Log específico para inicio de ataque"""
        self.info(f"ATAQUE INICIADO - Tipo: {attack_type}, Parámetros: {parameters}")
    
    def log_attack_result(self, attack_type, success, result=None, duration=None):
        """Log específico para resultado de ataque"""
        if success:
            self.info(f"ATAQUE EXITOSO - Tipo: {attack_type}, Resultado: {result}, Duración: {duration}")
        else:
            self.info(f"ATAQUE FALLIDO - Tipo: {attack_type}, Duración: {duration}")
    
    def log_performance(self, operation, duration, details=None):
        """Log específico para métricas de rendimiento"""
        message = f"PERFORMANCE - {operation}: {duration:.2f}s"
        if details:
            message += f" - {details}"
        self.info(message)
    
    def log_security_event(self, event_type, details):
        """Log específico para eventos de seguridad"""
        self.warning(f"SEGURIDAD - {event_type}: {details}")


class PerformanceLogger:
    """Logger especializado en métricas de rendimiento"""
    
    def __init__(self, main_logger):
        self.main_logger = main_logger
        self.metrics = {}
    
    def start_operation(self, operation_name):
        """Inicia el seguimiento de una operación"""
        self.metrics[operation_name] = {
            'start_time': datetime.now(),
            'end_time': None,
            'duration': None
        }
    
    def end_operation(self, operation_name, details=None):
        """Termina el seguimiento de una operación"""
        if operation_name in self.metrics:
            self.metrics[operation_name]['end_time'] = datetime.now()
            duration = (self.metrics[operation_name]['end_time'] - 
                       self.metrics[operation_name]['start_time']).total_seconds()
            self.metrics[operation_name]['duration'] = duration
            
            self.main_logger.log_performance(operation_name, duration, details)
            return duration
        return None
    
    def get_metrics(self):
        """Obtiene todas las métricas registradas"""
        return self.metrics.copy()
