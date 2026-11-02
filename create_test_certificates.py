#!/usr/bin/env python3
"""
Generador de certificados de prueba para testing del extractor
Crea certificados RSA 4096 + SHA256 con contraseñas débiles
"""

import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
import datetime

def create_test_certificate():
    """Crea un certificado de prueba vulnerable"""
    
    # Generar clave privada RSA 4096
    print("🔑 Generando clave RSA 4096...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    
    # Crear certificado autofirmado
    print("📜 Creando certificado autofirmado...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Madrid"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Madrid"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Test CA Organization"),
        x509.NameAttribute(NameOID.COMMON_NAME, "test-ca.example.com"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # Certificado válido por 20 años (indicador de debilidad)
        datetime.datetime.utcnow() + datetime.timedelta(days=7300)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("test-ca.example.com"),
            x509.DNSName("localhost"),
        ]),
        critical=False,
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    ).add_extension(
        x509.KeyUsage(
            digital_signature=True,
            content_commitment=False,
            key_encipherment=False,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=True,
            crl_sign=True,
            encipher_only=False,
            decipher_only=False,
        ),
        critical=True,
    ).sign(private_key, hashes.SHA256())
    
    # Crear directorio de pruebas
    test_dir = "test_certificates"
    os.makedirs(test_dir, exist_ok=True)
    
    # Guardar certificado en PEM
    cert_pem_path = os.path.join(test_dir, "test_ca_cert.pem")
    with open(cert_pem_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    print(f"✅ Certificado PEM guardado: {cert_pem_path}")
    
    # Guardar clave privada SIN contraseña
    key_unprotected_path = os.path.join(test_dir, "test_ca_key_unprotected.pem")
    with open(key_unprotected_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print(f"✅ Clave sin protección guardada: {key_unprotected_path}")
    
    # Guardar clave privada CON contraseña débil
    weak_passwords = ["test123", "password", "changeit", "admin", ""]
    
    for i, password in enumerate(weak_passwords):
        if password:  # Solo para contraseñas no vacías
            key_protected_path = os.path.join(test_dir, f"test_ca_key_protected_{i+1}.pem")
            with open(key_protected_path, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
                ))
            print(f"✅ Clave protegida guardada: {key_protected_path} (password: '{password}')")
    
    # Crear PKCS#12 con contraseña débil
    p12_password = "test123"
    p12_path = os.path.join(test_dir, "test_ca.p12")
    p12_data = pkcs12.serialize_key_and_certificates(
        name=b"Test CA",
        key=private_key,
        cert=cert,
        cas=None,
        encryption_algorithm=serialization.BestAvailableEncryption(p12_password.encode())
    )
    
    with open(p12_path, "wb") as f:
        f.write(p12_data)
    print(f"✅ PKCS#12 guardado: {p12_path} (password: '{p12_password}')")
    
    # Crear archivo de información
    info_path = os.path.join(test_dir, "README.txt")
    with open(info_path, "w", encoding="utf-8") as f:
        f.write("""CERTIFICADOS DE PRUEBA PARA EXTRACTOR DE CLAVES PRIVADAS

ARCHIVOS GENERADOS:
• test_ca_cert.pem - Certificado publico
• test_ca_key_unprotected.pem - Clave privada SIN contrasena
• test_ca_key_protected_1.pem - Clave privada con contrasena 'test123'
• test_ca_key_protected_2.pem - Clave privada con contrasena 'password'
• test_ca_key_protected_3.pem - Clave privada con contrasena 'changeit'
• test_ca_key_protected_4.pem - Clave privada con contrasena 'admin'
• test_ca.p12 - PKCS#12 con contrasena 'test123'

CARACTERISTICAS DEL CERTIFICADO:
• RSA 4096 bits (considerado debil para estandares modernos)
• SHA256 (algoritmo de firma legacy)
• Autofirmado (CA propia)
• Validez 20 anos (indicador de certificado de prueba)
• Nombres de prueba (test-ca.example.com, localhost)

PRUEBAS RECOMENDADAS:
1. Extraer clave sin contrasena (deberia ser instantaneo)
2. Probar extraccion automatica con contrasenas debiles
3. Verificar deteccion de certificado vulnerable
4. Probar diferentes metodos de ataque

SOLO PARA TESTING - No usar en produccion
""")
    
    print(f"✅ Información guardada: {info_path}")
    print(f"\n🎉 ¡Certificados de prueba creados exitosamente en: {test_dir}/")
    print("🔓 Usa estos archivos para probar el extractor de claves privadas")

if __name__ == "__main__":
    create_test_certificate()
