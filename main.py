#!/usr/bin/env python3
"""
Desencriptador Supremo - Aplicación de Escritorio Ultra Potente
Herramienta avanzada para desencriptación de certificados y datos encriptados
Autor: ver LICENSE
Version: 1.0.0
"""

import sys
import os
import threading
import time
from pathlib import Path

# Agregar directorios al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'gui'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'crypto'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'attacks'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'certificates'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

try:
    import customtkinter as ctk
    from gui.main_window import MainWindow
    from utils.logger import Logger
    from utils.config import Config
    from utils.system_check import SystemChecker
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Installing required dependencies...")
    os.system("pip install -r requirements.txt")
    sys.exit(1)

class DesencriptadorSupremo:
    """Clase principal de la aplicación Desencriptador Supremo"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.app_name = "Desencriptador Supremo"
        self.logger = Logger()
        self.config = Config()
        self.system_checker = SystemChecker()
        
    def show_banner(self):
        """Muestra el banner de la aplicación"""
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                    DESENCRIPTADOR SUPREMO                   ║
║                     Ultra Powerful Edition                  ║
║                        Version {self.version}                        ║
║                                                              ║
║          🔓 EXTREME DECRYPTION CAPABILITIES 🔓               ║
║                                                              ║
║  ⚠️  SOLO PARA FINES EDUCATIVOS Y TESTING AUTORIZADO  ⚠️   ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def check_system_requirements(self):
        """Verifica los requisitos del sistema"""
        print("🔍 Verificando requisitos del sistema...")
        
        # Verificar Python version
        if not self.system_checker.check_python_version():
            print("❌ Versión de Python no compatible")
            return False
            
        # Verificar RAM
        if not self.system_checker.check_memory():
            print("⚠️ RAM insuficiente, el rendimiento puede verse afectado")
            
        # Verificar GPU CUDA (opcional)
        if self.system_checker.check_cuda():
            print("✅ GPU CUDA detectada - Aceleración habilitada")
        else:
            print("ℹ️ GPU CUDA no detectada - Usando CPU")
            
        # Verificar permisos
        if not self.system_checker.check_permissions():
            print("⚠️ Permisos limitados detectados")
            
        return True
        
    def initialize_components(self):
        """Inicializa todos los componentes de la aplicación"""
        print("🚀 Inicializando componentes...")
        
        # Configurar CustomTkinter
        ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
        ctk.set_default_color_theme("blue")  # Tema azul
        
        # Inicializar logger
        self.logger.info(f"Iniciando {self.app_name} v{self.version}")
        
        # Cargar configuración
        self.config.load_config()
        
        print("✅ Componentes inicializados correctamente")
        
    def run(self):
        """Ejecuta la aplicación principal"""
        try:
            self.show_banner()
            
            if not self.check_system_requirements():
                input("Presiona Enter para continuar de todos modos...")
            
            self.initialize_components()
            
            print("🎯 Lanzando interfaz gráfica...")
            
            # Crear y ejecutar la ventana principal
            app = MainWindow()
            app.run()
            
        except KeyboardInterrupt:
            print("\n👋 Aplicación cerrada por el usuario")
            self.logger.info("Aplicación cerrada por KeyboardInterrupt")
            
        except Exception as e:
            print(f"\n❌ Error crítico: {e}")
            self.logger.error(f"Error crítico: {e}")
            input("Presiona Enter para salir...")
            
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Limpia recursos antes de cerrar"""
        print("🧹 Limpiando recursos...")
        self.logger.info("Cerrando aplicación")
        

def main():
    """Función principal"""
    # Verificar que se ejecute como script principal
    if __name__ == "__main__":
        app = DesencriptadorSupremo()
        app.run()
    else:
        print("Este archivo debe ejecutarse directamente")


if __name__ == "__main__":
    main()
