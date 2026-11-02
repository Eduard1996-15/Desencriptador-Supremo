"""
Manejador de Certificados para el Desencriptador Supremo
Maneja certificados X.509, PEM, DER, PKCS#12, etc.
"""

import os
import base64
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID
import OpenSSL
from datetime import datetime
import logging

class CertificateHandler:
    """Manejador principal de certificados"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def load_certificate(self, file_path, password=None):
        """Carga un certificado desde archivo"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Intentar diferentes formatos
            cert_info = None
            
            # Intentar PEM
            if b'-----BEGIN CERTIFICATE-----' in data:
                cert_info = self._load_pem_certificate(data)
            elif b'-----BEGIN PRIVATE KEY-----' in data or b'-----BEGIN RSA PRIVATE KEY-----' in data:
                cert_info = self._load_pem_private_key(data, password)
            elif file_path.lower().endswith(('.p12', '.pfx')):
                cert_info = self._load_pkcs12(data, password)
            else:
                # Intentar DER
                cert_info = self._load_der_certificate(data)
            
            if cert_info:
                cert_info['file_path'] = file_path
                cert_info['file_size'] = len(data)
                
            return cert_info
            
        except Exception as e:
            self.logger.error(f"Error cargando certificado: {e}")
            return None
    
    def _load_pem_certificate(self, data):
        """Carga certificado PEM"""
        try:
            cert = x509.load_pem_x509_certificate(data)
            return self._extract_certificate_info(cert)
        except Exception as e:
            self.logger.error(f"Error cargando PEM: {e}")
            return None
    
    def _load_der_certificate(self, data):
        """Carga certificado DER"""
        try:
            cert = x509.load_der_x509_certificate(data)
            return self._extract_certificate_info(cert)
        except Exception as e:
            self.logger.error(f"Error cargando DER: {e}")
            return None
    
    def _load_pem_private_key(self, data, password=None):
        """Carga clave privada PEM"""
        try:
            if password:
                password = password.encode() if isinstance(password, str) else password
            
            private_key = serialization.load_pem_private_key(data, password=password)
            return self._extract_private_key_info(private_key)
        except Exception as e:
            self.logger.error(f"Error cargando clave privada: {e}")
            return None
    
    def _load_pkcs12(self, data, password=None):
        """Carga archivo PKCS#12"""
        try:
            if password:
                password = password.encode() if isinstance(password, str) else password
            
            private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                data, password
            )
            
            info = {
                'type': 'PKCS#12',
                'has_private_key': private_key is not None,
                'has_certificate': certificate is not None,
                'additional_certs_count': len(additional_certificates) if additional_certificates else 0
            }
            
            if certificate:
                cert_info = self._extract_certificate_info(certificate)
                info.update(cert_info)
            
            if private_key:
                key_info = self._extract_private_key_info(private_key)
                info['private_key'] = key_info
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error cargando PKCS#12: {e}")
            return None
    
    def _extract_certificate_info(self, cert):
        """Extrae información detallada del certificado"""
        try:
            info = {
                'type': 'X.509 Certificate',
                'version': cert.version.name,
                'serial_number': str(cert.serial_number),
                'not_valid_before': cert.not_valid_before.isoformat(),
                'not_valid_after': cert.not_valid_after.isoformat(),
                'is_expired': cert.not_valid_after < datetime.now(),
                'signature_algorithm': cert.signature_algorithm_oid._name,
                'public_key_algorithm': cert.public_key().__class__.__name__
            }
            
            # Extraer información del sujeto
            subject = cert.subject
            info['subject'] = self._extract_name_attributes(subject)
            
            # Extraer información del emisor
            issuer = cert.issuer
            info['issuer'] = self._extract_name_attributes(issuer)
            
            # Extraer extensiones
            info['extensions'] = self._extract_extensions(cert)
            
            # Información de la clave pública
            public_key = cert.public_key()
            info['public_key_info'] = self._extract_public_key_info(public_key)
            
            # Huella digital
            info['sha256_fingerprint'] = cert.fingerprint(hashes.SHA256()).hex().upper()
            info['sha1_fingerprint'] = cert.fingerprint(hashes.SHA1()).hex().upper()
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error extrayendo información del certificado: {e}")
            return {'type': 'Certificate', 'error': str(e)}
    
    def _extract_private_key_info(self, private_key):
        """Extrae información de la clave privada"""
        try:
            info = {
                'type': private_key.__class__.__name__,
                'key_size': private_key.key_size if hasattr(private_key, 'key_size') else 'Unknown'
            }
            
            # Información específica por tipo de clave
            if hasattr(private_key, 'public_key'):
                public_key = private_key.public_key()
                info['public_key_info'] = self._extract_public_key_info(public_key)
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error extrayendo información de clave privada: {e}")
            return {'type': 'Private Key', 'error': str(e)}
    
    def _extract_name_attributes(self, name):
        """Extrae atributos del nombre X.509"""
        attributes = {}
        
        oid_names = {
            NameOID.COUNTRY_NAME: 'Country',
            NameOID.STATE_OR_PROVINCE_NAME: 'State/Province',
            NameOID.LOCALITY_NAME: 'Locality',
            NameOID.ORGANIZATION_NAME: 'Organization',
            NameOID.ORGANIZATIONAL_UNIT_NAME: 'Organizational Unit',
            NameOID.COMMON_NAME: 'Common Name',
            NameOID.EMAIL_ADDRESS: 'Email Address'
        }
        
        for attribute in name:
            oid_name = oid_names.get(attribute.oid, str(attribute.oid))
            attributes[oid_name] = attribute.value
        
        return attributes
    
    def _extract_extensions(self, cert):
        """Extrae extensiones del certificado"""
        extensions = {}
        
        try:
            for ext in cert.extensions:
                ext_name = ext.oid._name if hasattr(ext.oid, '_name') else str(ext.oid)
                extensions[ext_name] = {
                    'critical': ext.critical,
                    'value': str(ext.value)
                }
        except Exception as e:
            self.logger.error(f"Error extrayendo extensiones: {e}")
        
        return extensions
    
    def _extract_public_key_info(self, public_key):
        """Extrae información de la clave pública"""
        try:
            info = {
                'algorithm': public_key.__class__.__name__,
                'key_size': getattr(public_key, 'key_size', 'Unknown')
            }
            
            # Información específica para RSA
            if hasattr(public_key, 'public_numbers'):
                numbers = public_key.public_numbers()
                if hasattr(numbers, 'e'):
                    info['public_exponent'] = numbers.e
                if hasattr(numbers, 'n'):
                    info['modulus_bits'] = numbers.n.bit_length()
            
            return info
            
        except Exception as e:
            return {'error': str(e)}
    
    def validate_certificate_chain(self, cert_path, ca_cert_path=None):
        """Valida la cadena de certificados"""
        try:
            with open(cert_path, 'rb') as f:
                cert_data = f.read()
            
            cert = x509.load_pem_x509_certificate(cert_data)
            
            # Verificaciones básicas
            now = datetime.now()
            is_valid = True
            issues = []
            
            if cert.not_valid_before > now:
                is_valid = False
                issues.append("Certificado aún no válido")
            
            if cert.not_valid_after < now:
                is_valid = False
                issues.append("Certificado expirado")
            
            # TODO: Implementar verificación de cadena completa
            
            return {
                'is_valid': is_valid,
                'issues': issues,
                'validation_time': now.isoformat()
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'issues': [f"Error de validación: {e}"],
                'validation_time': datetime.now().isoformat()
            }
    
    def extract_private_key_from_protected(self, cert_path, password):
        """Extrae clave privada de certificado protegido"""
        try:
            with open(cert_path, 'rb') as f:
                data = f.read()
            
            # Intentar diferentes métodos según el formato
            if cert_path.lower().endswith(('.p12', '.pfx')):
                return self._extract_from_pkcs12(data, password)
            else:
                return self._extract_from_pem(data, password)
                
        except Exception as e:
            self.logger.error(f"Error extrayendo clave privada: {e}")
            return None
    
    def _extract_from_pkcs12(self, data, password):
        """Extrae clave privada de PKCS#12"""
        try:
            password_bytes = password.encode() if isinstance(password, str) else password
            private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                data, password_bytes
            )
            
            if private_key:
                # Serializar clave privada
                pem_key = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                
                return {
                    'success': True,
                    'private_key_pem': pem_key.decode(),
                    'key_type': private_key.__class__.__name__,
                    'key_size': getattr(private_key, 'key_size', 'Unknown')
                }
            else:
                return {'success': False, 'error': 'No se encontró clave privada'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _extract_from_pem(self, data, password):
        """Extrae clave privada de PEM"""
        try:
            password_bytes = password.encode() if isinstance(password, str) else password
            private_key = serialization.load_pem_private_key(data, password=password_bytes)
            
            # Serializar sin contraseña
            pem_key = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            return {
                'success': True,
                'private_key_pem': pem_key.decode(),
                'key_type': private_key.__class__.__name__,
                'key_size': getattr(private_key, 'key_size', 'Unknown')
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def convert_certificate_format(self, input_path, output_path, output_format, password=None):
        """Convierte certificado entre formatos"""
        try:
            # Cargar certificado
            cert_info = self.load_certificate(input_path, password)
            if not cert_info:
                return {'success': False, 'error': 'No se pudo cargar el certificado'}
            
            with open(input_path, 'rb') as f:
                data = f.read()
            
            # Determinar conversión necesaria
            if output_format.lower() == 'pem':
                result = self._convert_to_pem(data, password)
            elif output_format.lower() == 'der':
                result = self._convert_to_der(data, password)
            else:
                return {'success': False, 'error': f'Formato no soportado: {output_format}'}
            
            if result['success']:
                with open(output_path, 'wb') as f:
                    f.write(result['data'])
                return {'success': True, 'output_path': output_path}
            else:
                return result
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _convert_to_pem(self, data, password=None):
        """Convierte a formato PEM"""
        try:
            # Si ya es PEM, devolver tal cual
            if b'-----BEGIN CERTIFICATE-----' in data:
                return {'success': True, 'data': data}
            
            # Intentar cargar como DER
            cert = x509.load_der_x509_certificate(data)
            pem_data = cert.public_bytes(serialization.Encoding.PEM)
            
            return {'success': True, 'data': pem_data}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _convert_to_der(self, data, password=None):
        """Convierte a formato DER"""
        try:
            # Si es PEM, convertir
            if b'-----BEGIN CERTIFICATE-----' in data:
                cert = x509.load_pem_x509_certificate(data)
                der_data = cert.public_bytes(serialization.Encoding.DER)
                return {'success': True, 'data': der_data}
            
            # Si ya es DER, devolver tal cual
            return {'success': True, 'data': data}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
