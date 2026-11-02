"""
Script para crear certificados de ejemplo con contraseñas para testing
"""

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import datetime
import os

def create_sample_certificate():
    """Crea un certificado de ejemplo con clave privada protegida"""
    
    # Generar clave privada
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Información del certificado
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Madrid"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Madrid"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Desencriptador Supremo Test"),
        x509.NameAttribute(NameOID.COMMON_NAME, "test.example.com"),
    ])
    
    # Crear certificado
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
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("test.example.com"),
            x509.DNSName("www.test.example.com"),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256(), default_backend())
    
    # Crear directorio si no existe
    os.makedirs("./data/certificates", exist_ok=True)
    
    # Guardar certificado público
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    with open("./data/certificates/test-cert.pem", "wb") as f:
        f.write(cert_pem)
    
    # Guardar clave privada SIN contraseña
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("./data/certificates/test-private-key.pem", "wb") as f:
        f.write(private_pem)
    
    # Guardar clave privada CON contraseña
    protected_private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(b"certificado123")
    )
    with open("./data/certificates/test-private-key-protected.pem", "wb") as f:
        f.write(protected_private_pem)
    
    print("✅ Certificados creados en ./data/certificates/")
    print("📄 test-cert.pem - Certificado público")
    print("🔓 test-private-key.pem - Clave privada sin contraseña")
    print("🔐 test-private-key-protected.pem - Clave privada protegida")
    print("🔑 Contraseña de la clave privada: certificado123")

def create_pkcs12_example():
    """Crea archivos adicionales de certificado para testing"""
    
    # Crear un archivo DER para testing
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Crear certificado
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Test DER Format"),
        x509.NameAttribute(NameOID.COMMON_NAME, "der.test.com"),
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
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).sign(private_key, hashes.SHA256(), default_backend())
    
    # Guardar en formato DER
    cert_der = cert.public_bytes(serialization.Encoding.DER)
    with open("./data/certificates/test-cert.der", "wb") as f:
        f.write(cert_der)
    
    # Guardar clave privada en formato DER con contraseña
    private_der = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(b"dertest123")
    )
    with open("./data/certificates/test-private-key.der", "wb") as f:
        f.write(private_der)
    
    print("✅ Archivos DER creados:")
    print("📄 test-cert.der - Certificado en formato DER")
    print("🔐 test-private-key.der - Clave privada DER protegida")
    print("🔑 Contraseña: dertest123")

if __name__ == "__main__":
    print("🔧 Creando certificados de ejemplo...")
    
    create_sample_certificate()
    print()
    create_pkcs12_example()
    
    print("\n📁 Todos los certificados creados exitosamente!")
    print("🎯 Usa estos archivos para probar la funcionalidad de certificados")
