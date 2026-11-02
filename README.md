# Desencriptador Supremo 🔓

Una aplicación de escritorio extremadamente potente para desencriptación de certificados, archivos y datos encriptados.

## Características Principales

- **Interfaz Gráfica Moderna**: GUI elegante con CustomTkinter
- **Múltiples Algoritmos de Encriptación**: AES, RSA, DES, 3DES, Blowfish, Twofish, ChaCha20, y más
- **Manejo de Certificados**: Soporte para X.509, PEM, DER, PKCS#12, JKS
- **Ataques de Fuerza Bruta**: Implementación optimizada con multithreading
- **Ataques de Diccionario**: Carga de diccionarios personalizados
- **Análisis Criptográfico**: Detección automática de tipos de encriptación
- **Soporte GPU**: Aceleración CUDA para operaciones intensivas
- **Generación de Claves**: Creación de claves débiles y fuertes para testing
- **Hash Cracking**: MD5, SHA1, SHA256, SHA512, bcrypt, scrypt
- **Exportación de Resultados**: Múltiples formatos de salida

## Requisitos del Sistema

- Windows 10/11
- Python 3.8+
- 8GB RAM mínimo (16GB recomendado)
- GPU NVIDIA (opcional, para aceleración CUDA)

## Instalación

1. Clona el repositorio
2. Instala las dependencias: `pip install -r requirements.txt`
3. Ejecuta la aplicación: `python main.py`

### Datos de prueba

Los certificados y archivos cifrados de ejemplo **no se versionan** (ver
`.gitignore`). Para regenerarlos antes de usar los demos:

```bash
python create_test_certificates.py   # certificados de prueba en test_certificates/
python create_examples.py            # archivos .enc de ejemplo en data/
python create_certificates.py        # certificados en data/certificates/
```

## Uso

⚠️ **ADVERTENCIA**: Esta herramienta es solo para fines educativos y testing de seguridad autorizado. El usuario es responsable del uso ético de esta aplicación.

## Estructura del Proyecto

```
Desencriptador Supremo/
├── main.py                 # Punto de entrada principal
├── gui/                    # Interfaz gráfica
├── crypto/                 # Módulos de criptografía
├── attacks/                # Módulos de ataques
├── certificates/           # Manejo de certificados
├── utils/                  # Utilidades
├── data/                   # Diccionarios y datos
└── tests/                  # Pruebas unitarias
```

## Contribución

Las contribuciones son bienvenidas. Por favor, sigue las mejores prácticas de seguridad.

## Licencia

MIT License - Ver LICENSE para más detalles.
