"""
Script para crear archivos de ejemplo encriptados para testing
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import hashlib

def create_aes_example():
    """Crea un archivo de ejemplo encriptado con AES"""
    # Datos de ejemplo
    data = b"""Este es un archivo de ejemplo para testing del Desencriptador Supremo.

Contenido:
- Informacion confidencial de prueba
- Datos de ejemplo para verificar desencriptacion
- Password utilizada: "test123"

El Desencriptador Supremo es una herramienta educativa para aprender sobre criptografia.
Solo debe usarse para fines educativos y testing autorizado.
"""
    
    password = "test123"
    
    # Generar IV aleatorio
    iv = os.urandom(16)
    
    # Derivar clave de la contraseña
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=iv,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    
    # Aplicar padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    # Encriptar
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    # Combinar IV + datos encriptados
    final_data = iv + encrypted
    
    # Guardar archivo
    with open("./data/ejemplo-aes.enc", "wb") as f:
        f.write(final_data)
    
    print("✅ Archivo AES creado: ./data/ejemplo-aes.enc")
    print("🔑 Contraseña: test123")

def create_simple_examples():
    """Crea ejemplos simples con diferentes algoritmos"""
    examples = [
        ("admin", "Archivo administrativo secreto con credenciales del sistema."),
        ("password", "Documento con información confidencial de la empresa."),
        ("123456", "Base de datos con información de usuarios y contraseñas."),
        ("qwerty", "Backup de configuración del servidor principal."),
        ("secret", "Manual de procedimientos de seguridad clasificado.")
    ]
    
    for password, content in examples:
        # Crear hash simple como "encriptación"
        data = content.encode()
        
        # Simular encriptación simple (solo para demo)
        encrypted = bytearray()
        key_bytes = hashlib.md5(password.encode()).digest()
        
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
        
        filename = f"./data/ejemplo-{password}.enc"
        with open(filename, "wb") as f:
            f.write(bytes(encrypted))
        
        print(f"✅ Archivo creado: {filename} (contraseña: {password})")

if __name__ == "__main__":
    # Crear directorio de datos si no existe
    os.makedirs("./data", exist_ok=True)
    
    print("🔧 Creando archivos de ejemplo encriptados...")
    
    create_aes_example()
    create_simple_examples()
    
    print("\n📁 Archivos de ejemplo creados en ./data/")
    print("🎯 Usa estos archivos para probar el Desencriptador Supremo")
