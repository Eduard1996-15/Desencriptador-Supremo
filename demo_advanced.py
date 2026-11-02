"""
🔑 Demo de Extracción Avanzada de Claves Privadas
Demuestra las nuevas capacidades del Desencriptador Supremo
"""

import os
import sys
from pathlib import Path

# Añadir paths al sistema
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / 'certificates'))

# Evitar que se ejecute main.py automáticamente
os.environ['DEMO_MODE'] = '1'

def demo_advanced_extraction():
    """Demostración del extractor avanzado de claves privadas"""
    
    print("🔑 DEMO: EXTRACCIÓN AVANZADA DE CLAVES PRIVADAS")
    print("=" * 60)
    
    try:
        from certificates.advanced_extractor import AdvancedPrivateKeyExtractor
        
        extractor = AdvancedPrivateKeyExtractor()
        
        # Certificados de ejemplo disponibles
        cert_files = [
            "./data/certificates/test-private-key-protected.pem",
            "./data/certificates/test-private-key.der"
        ]
        
        passwords = {
            "test-private-key-protected.pem": "certificado123",
            "test-private-key.der": "dertest123"
        }
        
        print("\n📄 CERTIFICADOS DISPONIBLES PARA DEMO:")
        for cert_file in cert_files:
            if os.path.exists(cert_file):
                filename = os.path.basename(cert_file)
                password = passwords.get(filename, "Desconocida")
                size = os.path.getsize(cert_file)
                print(f"  • {filename}")
                print(f"    📁 Ruta: {cert_file}")
                print(f"    📏 Tamaño: {size} bytes")
                print(f"    🔑 Contraseña: {password}")
                print()
        
        print("\n🎯 MÉTODOS DE EXTRACCIÓN DISPONIBLES:")
        methods = [
            ("🎯 Automático", "auto", "Prueba múltiples estrategias automáticamente"),
            ("🔑 Contraseña específica", "password", "Usa una contraseña conocida"),
            ("📚 Ataque de diccionario", "dictionary", "Prueba contraseñas de diccionarios"),
            ("⚡ Fuerza bruta", "bruteforce", "Genera y prueba todas las combinaciones"),
            ("🔄 Ataque híbrido", "hybrid", "Combina diccionario con variaciones")
        ]
        
        for emoji, method, description in methods:
            print(f"  {emoji} {method.upper()}")
            print(f"    {description}")
            print()
        
        print("\n💡 EJEMPLO DE USO PROGRAMÁTICO:")
        print("-" * 40)
        
        example_code = '''
from certificates.advanced_extractor import AdvancedPrivateKeyExtractor

# Crear extractor
extractor = AdvancedPrivateKeyExtractor()

# Extracción automática (recomendado)
result = extractor.extract_private_key(
    cert_path="./data/certificates/test-private-key-protected.pem",
    method="auto",
    allow_bruteforce=True,
    max_length=6
)

if result['success']:
    print(f"🎉 Clave extraída!")
    print(f"🔑 Contraseña: {result.get('password_found')}")
    print(f"📝 Clave PEM: {result['private_key_pem'][:100]}...")
else:
    print(f"❌ Error: {result['error']}")
'''
        
        print(example_code)
        
        print("\n🚀 DEMO EN VIVO:")
        print("-" * 40)
        
        # Demo real con un certificado
        demo_cert = "./data/certificates/test-private-key-protected.pem"
        if os.path.exists(demo_cert):
            print(f"📄 Probando con: {demo_cert}")
            print("🎯 Método: Contraseña específica")
            
            # Función de progreso para demo
            def demo_progress(current, total):
                if total > 0:
                    percent = (current / total) * 100
                    print(f"  📊 Progreso: {current}/{total} ({percent:.1f}%)")
            
            result = extractor.extract_private_key(
                demo_cert, 
                method="password", 
                password="certificado123",
                progress_callback=demo_progress
            )
            
            if result['success']:
                print("🎉 ¡ÉXITO! Clave privada extraída")
                print(f"🔐 Tipo: {result.get('key_type')}")
                print(f"📏 Tamaño: {result.get('key_size')} bits")
                print(f"📋 Formato: {result.get('format')}")
                print("📝 Clave PEM (primeros 200 caracteres):")
                print(result['private_key_pem'][:200] + "...")
            else:
                print(f"❌ Error: {result['error']}")
        else:
            print("❌ Certificado de demo no encontrado")
        
        print("\n🎯 CASOS DE USO RECOMENDADOS:")
        print("-" * 40)
        
        use_cases = [
            {
                "scenario": "🏢 Certificado corporativo olvidado",
                "method": "auto",
                "description": "Deja que el sistema pruebe automáticamente contraseñas comunes corporativas"
            },
            {
                "scenario": "🔐 Certificado personal conocido",
                "method": "password",
                "description": "Usa contraseña específica si la conoces"
            },
            {
                "scenario": "📱 Certificado con contraseña simple",
                "method": "bruteforce",
                "description": "Fuerza bruta para contraseñas de 4-6 caracteres"
            },
            {
                "scenario": "🎯 Certificado con patrones conocidos",
                "method": "hybrid",
                "description": "Combina diccionarios con variaciones (años, números)"
            }
        ]
        
        for case in use_cases:
            print(f"{case['scenario']}")
            print(f"  🎯 Método recomendado: {case['method']}")
            print(f"  💡 {case['description']}")
            print()
        
        print("\n⚠️ CONSIDERACIONES DE SEGURIDAD:")
        print("-" * 40)
        print("• Solo usar en certificados propios o con autorización")
        print("• Cambiar contraseñas después de extracción exitosa")
        print("• Proteger claves privadas extraídas")
        print("• Usar solo para fines educativos y testing autorizado")
        
        print("\n✨ NUEVAS FUNCIONALIDADES:")
        print("-" * 40)
        print("• Extracción multihilo para mayor velocidad")
        print("• Soporte para múltiples formatos (PEM, DER, PKCS#12)")
        print("• Generación inteligente de contraseñas basada en archivos")
        print("• Reportes detallados de intentos y métodos")
        print("• Capacidad de detener extracción en tiempo real")
        print("• Estimación de tiempo y progreso visual")
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("💡 Asegúrate de que todos los módulos estén instalados")
    except Exception as e:
        print(f"❌ Error en demo: {e}")

def demo_gui_features():
    """Demuestra las funcionalidades de la GUI mejorada"""
    
    print("\n🖥️ NUEVAS FUNCIONALIDADES DE LA GUI:")
    print("=" * 60)
    
    gui_features = [
        {
            "name": "🔐 Generador de Claves",
            "description": "Genera claves RSA, DSA, Ed25519 con protección opcional",
            "location": "Pestaña Herramientas"
        },
        {
            "name": "🔄 Conversor de Formatos",
            "description": "Convierte entre PEM, DER y otros formatos",
            "location": "Pestaña Herramientas"
        },
        {
            "name": "📝 Editor Hexadecimal",
            "description": "Visualiza archivos en formato hexadecimal",
            "location": "Pestaña Herramientas"
        },
        {
            "name": "🧮 Calculadora Hash",
            "description": "Calcula MD5, SHA256, SHA512 y otros hashes",
            "location": "Pestaña Herramientas"
        },
        {
            "name": "🔑 Extracción Avanzada",
            "description": "Sistema multi-método para extraer claves privadas",
            "location": "Pestaña Certificados → Extraer Clave Privada"
        },
        {
            "name": "🎯 Generador de Wordlists",
            "description": "Crea wordlists personalizadas para ataques",
            "location": "Pestaña Herramientas"
        }
    ]
    
    for feature in gui_features:
        print(f"{feature['name']}")
        print(f"  📋 {feature['description']}")
        print(f"  📍 Ubicación: {feature['location']}")
        print()
    
    print("\n🎯 CÓMO PROBAR LAS NUEVAS FUNCIONALIDADES:")
    print("-" * 50)
    
    test_steps = [
        "1. Ejecuta: python main.py",
        "2. Ve a la pestaña 'Certificados'",
        "3. Selecciona: data/certificates/test-private-key-protected.pem",
        "4. Haz clic en 'Extraer Clave Privada'",
        "5. Selecciona método 'Automático'",
        "6. Observa el progreso en tiempo real",
        "7. ¡Disfruta viendo la clave extraída!"
    ]
    
    for step in test_steps:
        print(f"  {step}")
    
    print("\n💎 HERRAMIENTAS ADICIONALES:")
    print("-" * 50)
    print("• 🔐 Generador de Claves: Crea nuevas claves criptográficas")
    print("• 🧮 Calculadora Hash: Verifica integridad de archivos")
    print("• 📝 Editor Hex: Inspecciona archivos binarios")
    print("• 🔄 Conversor: Cambia formatos de certificados")

if __name__ == "__main__":
    print("🚀 DEMOSTRACIÓN DEL DESENCRIPTADOR SUPREMO")
    print("   Ultra Powerful Edition - Advanced Features")
    print("=" * 70)
    
    demo_advanced_extraction()
    demo_gui_features()
    
    print("\n" + "=" * 70)
    print("🎉 ¡DEMO COMPLETADA!")
    print("🚀 Ejecuta 'python main.py' para probar la aplicación completa")
    print("=" * 70)
