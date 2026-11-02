"""
🔑 Demo Simple de Funcionalidades Avanzadas
"""

def show_demo():
    print("🚀 DESENCRIPTADOR SUPREMO - NUEVAS FUNCIONALIDADES")
    print("=" * 60)
    
    print("\n🔑 EXTRACCIÓN AVANZADA DE CLAVES PRIVADAS:")
    print("-" * 50)
    print("✅ Sistema multi-método implementado")
    print("✅ Soporte para múltiples formatos (PEM, DER, PKCS#12)")
    print("✅ Ataques inteligentes con progreso en tiempo real")
    print("✅ Detección automática de contraseñas débiles")
    
    print("\n🛠️ HERRAMIENTAS IMPLEMENTADAS:")
    print("-" * 50)
    print("✅ 🔐 Generador de Claves - Crea claves RSA, DSA, Ed25519")
    print("✅ 🔄 Conversor de Formatos - PEM ↔ DER conversión")
    print("✅ 📝 Editor Hexadecimal - Visualizador de archivos binarios")
    print("✅ 🧮 Calculadora Hash - MD5, SHA256, SHA512, BLAKE2b")
    print("🔄 🔍 Buscador de Claves - En desarrollo")
    print("🔄 📊 Análisis de Bits - En desarrollo")
    print("🔄 🎯 Generador de Wordlists - En desarrollo")
    print("🔄 🛡️ Test de Seguridad - En desarrollo")
    
    print("\n📄 ARCHIVOS DE EJEMPLO DISPONIBLES:")
    print("-" * 50)
    
    import os
    
    # Archivos encriptados
    data_dir = "./data"
    if os.path.exists(data_dir):
        print("🔐 Archivos Encriptados:")
        enc_files = [f for f in os.listdir(data_dir) if f.endswith('.enc')]
        for enc_file in enc_files:
            password = {
                'ejemplo-admin.enc': 'admin',
                'ejemplo-password.enc': 'password',
                'ejemplo-123456.enc': '123456',
                'ejemplo-qwerty.enc': 'qwerty',
                'ejemplo-secret.enc': 'secret',
                'ejemplo-aes.enc': 'test123'
            }.get(enc_file, 'Desconocida')
            
            print(f"  📄 {enc_file} → Contraseña: {password}")
    
    # Certificados
    cert_dir = "./data/certificates"
    if os.path.exists(cert_dir):
        print("\n🏆 Certificados:")
        cert_files = os.listdir(cert_dir)
        for cert_file in cert_files:
            if 'protected' in cert_file:
                password = {
                    'test-private-key-protected.pem': 'certificado123',
                    'test-private-key.der': 'dertest123'
                }.get(cert_file, 'Desconocida')
                print(f"  📜 {cert_file} → Contraseña: {password}")
            else:
                print(f"  📜 {cert_file} → Sin protección")
    
    print("\n🎯 CÓMO PROBAR LAS NUEVAS FUNCIONALIDADES:")
    print("-" * 50)
    print("1. 🚀 Ejecuta: python main.py")
    print("2. 📜 Ve a la pestaña 'Certificados'")
    print("3. 📂 Selecciona: data/certificates/test-private-key-protected.pem")
    print("4. 🔑 Haz clic en 'Extraer Clave Privada'")
    print("5. 🎯 Prueba diferentes métodos:")
    print("   • Automático (recomendado)")
    print("   • Contraseña específica: certificado123")
    print("   • Ataque de diccionario")
    print("   • Fuerza bruta (longitud corta)")
    print("6. 🛠️ Explora las herramientas en la pestaña 'Herramientas'")
    
    print("\n💡 EJEMPLOS DE USO:")
    print("-" * 50)
    print("🔐 Desencriptación básica:")
    print("   → Archivo: data/ejemplo-admin.enc")
    print("   → Contraseña: admin")
    
    print("\n🏆 Extracción de certificados:")
    print("   → Archivo: data/certificates/test-private-key-protected.pem")
    print("   → Método: Automático")
    print("   → Resultado: Clave privada extraída exitosamente")
    
    print("\n🧮 Cálculo de hashes:")
    print("   → Herramientas → Calculadora Hash")
    print("   → Ingresa texto o selecciona archivo")
    print("   → Obtén MD5, SHA256, etc.")
    
    print("\n🔐 Generación de claves:")
    print("   → Herramientas → Generador de Claves")
    print("   → Selecciona RSA 2048 bits")
    print("   → Opcional: proteger con contraseña")
    
    print("\n⚠️ RECORDATORIO DE SEGURIDAD:")
    print("-" * 50)
    print("🔒 Solo usar para fines educativos y testing autorizado")
    print("🔒 No usar en sistemas ajenos sin autorización")
    print("🔒 Cambiar contraseñas después de extracción exitosa")
    print("🔒 Proteger claves privadas extraídas")
    
    print("\n🎉 ¡LISTO PARA USAR!")
    print("=" * 60)
    print("Ejecuta: python main.py para comenzar")

if __name__ == "__main__":
    show_demo()
