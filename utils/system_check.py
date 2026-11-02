"""
Verificador de Sistema para el Desencriptador Supremo
Verifica requisitos y capacidades del sistema
"""

import sys
import platform
import psutil
import subprocess
import os
import logging
from pathlib import Path

class SystemChecker:
    """Verificador de requisitos del sistema"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def check_python_version(self):
        """Verifica la versión de Python"""
        try:
            version = sys.version_info
            if version.major >= 3 and version.minor >= 8:
                self.logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
                return True
            else:
                self.logger.warning(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.8+")
                return False
        except Exception as e:
            self.logger.error(f"Error verificando versión de Python: {e}")
            return False
    
    def check_memory(self):
        """Verifica la memoria RAM disponible"""
        try:
            memory = psutil.virtual_memory()
            total_gb = memory.total / (1024**3)
            available_gb = memory.available / (1024**3)
            
            self.logger.info(f"💾 RAM Total: {total_gb:.1f}GB, Disponible: {available_gb:.1f}GB")
            
            if total_gb >= 8:
                self.logger.info("✅ Memoria suficiente para operaciones intensivas")
                return True
            elif total_gb >= 4:
                self.logger.warning("⚠️ Memoria limitada - Rendimiento puede verse afectado")
                return True
            else:
                self.logger.warning("❌ Memoria insuficiente - Se recomienda 8GB+")
                return False
                
        except Exception as e:
            self.logger.error(f"Error verificando memoria: {e}")
            return False
    
    def check_cpu(self):
        """Verifica información de CPU"""
        try:
            cpu_count = psutil.cpu_count()
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()
            
            self.logger.info(f"🔄 CPU: {cpu_count} núcleos físicos, {cpu_count_logical} lógicos")
            
            if cpu_freq:
                self.logger.info(f"🔄 Frecuencia: {cpu_freq.current:.0f}MHz")
            
            # Verificar carga actual
            cpu_percent = psutil.cpu_percent(interval=1)
            self.logger.info(f"🔄 Uso actual: {cpu_percent}%")
            
            return {
                'physical_cores': cpu_count,
                'logical_cores': cpu_count_logical,
                'frequency': cpu_freq.current if cpu_freq else 0,
                'usage': cpu_percent
            }
            
        except Exception as e:
            self.logger.error(f"Error verificando CPU: {e}")
            return None
    
    def check_cuda(self):
        """Verifica disponibilidad de CUDA"""
        try:
            # Intentar importar pycuda
            try:
                import pycuda.driver as cuda
                import pycuda.autoinit
                
                # Obtener información de dispositivos CUDA
                cuda.init()
                device_count = cuda.Device.count()
                
                if device_count > 0:
                    for i in range(device_count):
                        device = cuda.Device(i)
                        name = device.name()
                        memory = device.total_memory() // (1024**2)  # MB
                        
                        self.logger.info(f"🎮 GPU CUDA {i}: {name} ({memory}MB)")
                    
                    return True
                else:
                    self.logger.info("ℹ️ No se encontraron dispositivos CUDA")
                    return False
                    
            except ImportError:
                self.logger.info("ℹ️ PyCUDA no disponible")
                return False
                
        except Exception as e:
            self.logger.debug(f"Error verificando CUDA: {e}")
            return False
    
    def check_opencl(self):
        """Verifica disponibilidad de OpenCL"""
        try:
            import pyopencl as cl
            
            platforms = cl.get_platforms()
            if platforms:
                for platform in platforms:
                    devices = platform.get_devices()
                    for device in devices:
                        name = device.name.strip()
                        device_type = cl.device_type.to_string(device.type)
                        memory = device.global_mem_size // (1024**2)  # MB
                        
                        self.logger.info(f"🔧 OpenCL {device_type}: {name} ({memory}MB)")
                
                return True
            else:
                self.logger.info("ℹ️ No se encontraron dispositivos OpenCL")
                return False
                
        except ImportError:
            self.logger.info("ℹ️ PyOpenCL no disponible")
            return False
        except Exception as e:
            self.logger.debug(f"Error verificando OpenCL: {e}")
            return False
    
    def check_permissions(self):
        """Verifica permisos del sistema"""
        try:
            # Verificar permisos de escritura en directorio actual
            current_dir = Path.cwd()
            test_file = current_dir / "test_write_permission.tmp"
            
            try:
                test_file.write_text("test")
                test_file.unlink()
                write_permission = True
            except:
                write_permission = False
            
            # Verificar si se ejecuta como administrador (Windows)
            is_admin = False
            if platform.system() == "Windows":
                try:
                    import ctypes
                    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                except:
                    is_admin = False
            else:
                is_admin = os.geteuid() == 0
            
            self.logger.info(f"🔐 Permisos de escritura: {'✅' if write_permission else '❌'}")
            self.logger.info(f"🔐 Ejecutando como admin: {'✅' if is_admin else '❌'}")
            
            return {
                'write_permission': write_permission,
                'is_admin': is_admin
            }
            
        except Exception as e:
            self.logger.error(f"Error verificando permisos: {e}")
            return {'write_permission': False, 'is_admin': False}
    
    def check_dependencies(self):
        """Verifica dependencias principales"""
        dependencies = {
            'cryptography': 'Criptografía principal',
            'customtkinter': 'Interfaz gráfica moderna',
            'pycryptodome': 'Algoritmos adicionales',
            'psutil': 'Información del sistema',
            'numpy': 'Cálculos matemáticos',
            'pillow': 'Procesamiento de imágenes'
        }
        
        results = {}
        
        for dep, description in dependencies.items():
            try:
                __import__(dep)
                self.logger.info(f"✅ {dep} - {description}")
                results[dep] = True
            except ImportError:
                self.logger.warning(f"❌ {dep} - {description} - NO INSTALADO")
                results[dep] = False
        
        return results
    
    def check_network(self):
        """Verifica conectividad de red (para actualizaciones)"""
        try:
            import socket
            
            # Intentar conectar a un servidor DNS público
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            self.logger.info("🌐 Conectividad de red: ✅")
            return True
        except:
            self.logger.warning("🌐 Conectividad de red: ❌")
            return False
    
    def get_system_info(self):
        """Obtiene información completa del sistema"""
        info = {
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': sys.version,
            'architecture': platform.architecture()[0]
        }
        
        # Información de memoria
        memory = psutil.virtual_memory()
        info['memory_total'] = memory.total
        info['memory_available'] = memory.available
        
        # Información de CPU
        info['cpu_count'] = psutil.cpu_count()
        info['cpu_count_logical'] = psutil.cpu_count(logical=True)
        
        # Información de disco
        disk = psutil.disk_usage('.')
        info['disk_total'] = disk.total
        info['disk_free'] = disk.free
        
        return info
    
    def run_full_check(self):
        """Ejecuta verificación completa del sistema"""
        self.logger.info("🔍 Iniciando verificación completa del sistema...")
        
        results = {
            'python_version': self.check_python_version(),
            'memory': self.check_memory(),
            'cpu_info': self.check_cpu(),
            'cuda': self.check_cuda(),
            'opencl': self.check_opencl(),
            'permissions': self.check_permissions(),
            'dependencies': self.check_dependencies(),
            'network': self.check_network(),
            'system_info': self.get_system_info()
        }
        
        # Calcular puntuación general
        score = 0
        max_score = 0
        
        if results['python_version']:
            score += 20
        max_score += 20
        
        if results['memory']:
            score += 15
        max_score += 15
        
        if results['cuda'] or results['opencl']:
            score += 10
        max_score += 10
        
        deps_ok = sum(1 for ok in results['dependencies'].values() if ok)
        total_deps = len(results['dependencies'])
        score += (deps_ok / total_deps) * 25
        max_score += 25
        
        if results['permissions']['write_permission']:
            score += 10
        max_score += 10
        
        if results['network']:
            score += 5
        max_score += 5
        
        score_percentage = (score / max_score) * 100
        
        self.logger.info(f"📊 Puntuación del sistema: {score_percentage:.1f}%")
        
        if score_percentage >= 80:
            self.logger.info("✅ Sistema óptimo para Desencriptador Supremo")
        elif score_percentage >= 60:
            self.logger.info("⚠️ Sistema aceptable, puede haber limitaciones de rendimiento")
        else:
            self.logger.warning("❌ Sistema por debajo de requisitos mínimos")
        
        results['score'] = score_percentage
        return results
