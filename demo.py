"""
🎯 Script de Demostración - Desencriptador Supremo
Muestra todas las capacidades de la aplicación con ejemplos prácticos
"""

import os
import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

def show_banner():
    """Muestra el banner de demostración"""
    print("\n" + "="*70)
    print("🎯 DEMOSTRACIÓN DEL DESENCRIPTADOR SUPREMO")
    print("   Ultra Powerful Edition - Showcase")
    print("="*70)

def demo_file_structure():
    """Muestra la estructura de archivos creados"""
    print("\n📁 ESTRUCTURA DE ARCHIVOS DE EJEMPLO:")
    print("-" * 50)
    
    # Archivos encriptados
    data_dir = Path("./data")
    if data_dir.exists():
        print("\n🔐 Archivos Encriptados:")
        for file in data_dir.glob("*.enc"):
            size = file.stat().st_size
            print(f"  📄 {file.name} ({size} bytes)")
    
    # Certificados
    cert_dir = Path("./data/certificates")
    if cert_dir.exists():
        print("\n🏆 Certificados:")
        for file in cert_dir.iterdir():
            if file.is_file():
                size = file.stat().st_size
                print(f"  📜 {file.name} ({size} bytes)")
    
    # Diccionarios
    print("\n📚 Diccionarios:")
    for dict_file in ["common-passwords.txt", "spanish.txt"]:
        dict_path = data_dir / dict_file
        if dict_path.exists():
            lines = len(dict_path.read_text(encoding='utf-8', errors='ignore').splitlines())
            print(f"  📖 {dict_file} ({lines:,} entradas)")

def demo_test_scenarios():
    """Muestra escenarios de testing"""
    print("\n🎯 ESCENARIOS DE TESTING DISPONIBLES:")
    print("-" * 50)
    
    scenarios = [
        {
            "name": "🔓 Desencriptación Rápida",
            "file": "ejemplo-admin.enc",
            "password": "admin",
            "description": "Prueba básica de desencriptación con contraseña simple"
        },
        {
            "name": "⚡ Ataque de Fuerza Bruta",
            "file": "ejemplo-secret.enc",
            "password": "secret",
            "description": "Ataque con caracteres alfabéticos, longitud 1-6"
        },
        {
            "name": "📖 Ataque de Diccionario",
            "file": "ejemplo-password.enc",
            "password": "password",
            "description": "Usar common-passwords.txt para encontrar la clave"
        },
        {
            "name": "🏆 Análisis de Certificados",
            "file": "test-private-key-protected.pem",
            "password": "certificado123",
            "description": "Extracción de clave privada de certificado"
        },
        {
            "name": "🔐 Encriptación AES Avanzada",
            "file": "ejemplo-aes.enc",
            "password": "test123",
            "description": "Desencriptación de AES-256 con PBKDF2"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   📄 Archivo: {scenario['file']}")
        print(f"   🔑 Contraseña: {scenario['password']}")
        print(f"   💡 {scenario['description']}")

def demo_attack_strategies():
    """Muestra estrategias de ataque recomendadas"""
    print("\n⚔️ ESTRATEGIAS DE ATAQUE RECOMENDADAS:")
    print("-" * 50)
    
    strategies = [
        {
            "type": "📱 Contraseñas Móviles",
            "pattern": "Números, patrones, fechas",
            "approach": "Diccionario + variaciones numéricas",
            "time": "< 1 minuto"
        },
        {
            "type": "🏢 Contraseñas Corporativas",
            "pattern": "Empresa + año/número",
            "approach": "Diccionario corporativo + híbrido",
            "time": "< 5 minutos"
        },
        {
            "type": "🔐 Contraseñas Personales",
            "pattern": "Nombres + fechas significativas",
            "approach": "Diccionario personal + fuerza bruta",
            "time": "Variable"
        },
        {
            "type": "⚡ Contraseñas Simples",
            "pattern": "4-6 caracteres básicos",
            "approach": "Fuerza bruta directa",
            "time": "< 30 segundos"
        }
    ]
    
    for strategy in strategies:
        print(f"\n🎯 {strategy['type']}")
        print(f"   📋 Patrón: {strategy['pattern']}")
        print(f"   ⚔️ Enfoque: {strategy['approach']}")
        print(f"   ⏱️ Tiempo estimado: {strategy['time']}")

def demo_performance_tips():
    """Muestra consejos de optimización"""
    print("\n⚡ CONSEJOS DE OPTIMIZACIÓN:")
    print("-" * 50)
    
    tips = [
        "🧵 Usa multithreading (automático en la app)",
        "📊 Analiza el archivo antes de atacar",
        "📚 Empieza con diccionarios antes que fuerza bruta",
        "🎯 Ajusta la longitud según el contexto",
        "💾 Monitorea el uso de memoria durante ataques largos",
        "🔄 Usa ataques híbridos para máxima efectividad",
        "📝 Revisa los logs para optimizar estrategias"
    ]
    
    for tip in tips:
        print(f"  {tip}")

def demo_legal_reminder():
    """Recordatorio legal importante"""
    print("\n" + "="*70)
    print("⚠️  RECORDATORIO LEGAL IMPORTANTE")
    print("="*70)
    print("""
🔒 ESTE SOFTWARE ES SOLO PARA FINES EDUCATIVOS

✅ Usos Permitidos:
   • Aprendizaje de criptografía y seguridad
   • Testing en sistemas propios
   • Investigación académica autorizada
   • Práctica en entornos controlados

❌ Usos Prohibidos:
   • Acceso no autorizado a sistemas ajenos
   • Violación de la privacidad
   • Actividades ilegales de cualquier tipo
   • Uso comercial sin licencia

👤 RESPONSABILIDAD: El usuario es completamente responsable
   del uso de esta herramienta. Los desarrolladores no se
   hacen responsables del mal uso.

📜 Licencia: MIT con términos de uso ético
""")

def main():
    """Función principal de la demostración"""
    show_banner()
    demo_file_structure()
    demo_test_scenarios()
    demo_attack_strategies()
    demo_performance_tips()
    demo_legal_reminder()
    
    print("\n🚀 Para ejecutar la aplicación:")
    print("   python main.py")
    print("\n📖 Para más información:")
    print("   Ver MANUAL_TESTING.md")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
