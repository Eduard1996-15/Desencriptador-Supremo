# Manual de Usuario - Desencriptador Supremo

## 🚀 Guía de Inicio Rápido

### Instalación

1. **Clonar o descargar el proyecto**
2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Ejecutar la aplicación:**
   ```bash
   python main.py
   ```

### Primer Uso

1. La aplicación verificará automáticamente los requisitos del sistema
2. Se creará un archivo de configuración por defecto
3. Se abrirá la interfaz gráfica principal

## 📚 Guía de Funcionalidades

### 🔓 Pestaña Desencriptar

**Funciones principales:**
- Selección de archivos encriptados
- Auto-detección de algoritmos de encriptación
- Múltiples métodos de ataque simultáneos
- Barra de progreso en tiempo real

**Algoritmos soportados:**
- AES (128, 256) - CBC, GCM
- RSA (1024, 2048, 4096 bits)
- DES y 3DES
- Blowfish
- ChaCha20 y Salsa20
- RC4
- Detección automática

**Métodos de ataque:**
- **Diccionario:** Usa listas de contraseñas comunes
- **Fuerza Bruta:** Prueba todas las combinaciones posibles
- **Híbrido:** Combina diccionario con transformaciones
- **Reglas:** Aplica reglas de transformación
- **Máscara:** Usa patrones específicos (ej: ?l?l?l?d?d?d)
- **Tabla Arcoíris:** Búsqueda en tablas pre-computadas

### 📜 Pestaña Certificados

**Funciones:**
- Carga de certificados X.509, PEM, DER, PKCS#12
- Análisis detallado de información del certificado
- Extracción de claves privadas
- Validación de cadenas de certificados
- Conversión entre formatos

**Formatos soportados:**
- PEM (.pem, .crt, .cer)
- DER (.der)
- PKCS#12 (.p12, .pfx)
- Java KeyStore (.jks)

### 💥 Pestaña Fuerza Bruta

**Configuraciones avanzadas:**
- Longitud mínima y máxima de contraseñas
- Conjuntos de caracteres personalizados
- Control de hilos de procesamiento
- Estadísticas en tiempo real

**Conjuntos de caracteres:**
- Alfanumérico (a-z, A-Z, 0-9)
- Solo letras
- Solo números
- ASCII completo
- Personalizado

**Estadísticas en tiempo real:**
- Contraseñas probadas
- Velocidad (contraseñas/segundo)
- Tiempo transcurrido
- Tiempo estimado restante
- Uso de CPU y RAM

### 🔐 Pestaña Hashes

**Tipos de hash soportados:**
- MD5
- SHA1, SHA256, SHA512
- bcrypt
- scrypt
- NTLM
- LM Hash

**Funciones:**
- Auto-detección de tipo de hash
- Múltiples diccionarios simultáneos
- Generación de diccionarios personalizados
- Resultados detallados

### 🔍 Pestaña Análisis

**Herramientas de análisis:**
- **Detección de Encriptación:** Identifica el algoritmo usado
- **Análisis de Entropía:** Mide la aleatoriedad de los datos
- **Análisis Forense:** Busca metadatos y patrones ocultos

### 🛠️ Pestaña Herramientas

**Utilidades incluidas:**
- **Generador de Claves:** Crea claves seguras o débiles para testing
- **Conversor de Formatos:** Convierte entre diferentes formatos
- **Editor Hexadecimal:** Visualiza y edita archivos en hexadecimal
- **Calculadora Hash:** Genera hashes de archivos o texto
- **Buscador de Claves:** Busca claves en archivos de texto
- **Análisis de Bits:** Análisis a nivel de bits
- **Generador de Wordlists:** Crea diccionarios personalizados
- **Test de Seguridad:** Evalúa la fortaleza de contraseñas

### ⚙️ Pestaña Configuración

**Configuraciones principales:**
- **Tema:** Oscuro, Claro, Sistema
- **Rendimiento:** GPU, Multithreading, Optimización de memoria
- **Rutas:** Directorios de diccionarios, salida, logs
- **Seguridad:** Logging de contraseñas, borrado seguro

## 💡 Consejos de Uso

### Optimización de Rendimiento

1. **Usar GPU cuando esté disponible**
2. **Ajustar número de hilos según tu CPU**
3. **Habilitar caché para operaciones repetitivas**
4. **Usar diccionarios optimizados**

### Mejores Prácticas

1. **Empezar con diccionarios comunes**
2. **Usar análisis de entropía antes de fuerza bruta**
3. **Configurar timeouts apropiados**
4. **Guardar progreso para ataques largos**

### Seguridad

1. **Nunca registrar contraseñas en logs**
2. **Usar borrado seguro para archivos temporales**
3. **Mantener logs de auditoría**
4. **Seguir principios de uso ético**

## 🔧 Solución de Problemas

### Problemas Comunes

**La aplicación no inicia:**
- Verificar instalación de Python 3.8+
- Instalar dependencias faltantes
- Verificar permisos de escritura

**Rendimiento lento:**
- Reducir número de hilos
- Habilitar optimización de memoria
- Verificar uso de CPU/RAM

**Errores de memoria:**
- Habilitar optimización de memoria
- Reducir tamaño de caché
- Usar diccionarios más pequeños

**GPU no detectada:**
- Instalar drivers NVIDIA actualizados
- Instalar CUDA Toolkit
- Verificar compatibilidad

### Logs y Depuración

Los logs se guardan en el directorio `logs/` con información detallada:
- Errores y excepciones
- Métricas de rendimiento
- Eventos de seguridad
- Progreso de ataques

## 📊 Métricas y Estadísticas

### Interpretación de Resultados

**Velocidad de ataque:**
- MD5: ~10M/s (CPU), ~1B/s (GPU)
- SHA256: ~1M/s (CPU), ~100M/s (GPU)
- bcrypt: ~1K/s (CPU), ~10K/s (GPU)

**Tiempos estimados:**
- Contraseña 6 caracteres: segundos-minutos
- Contraseña 8 caracteres: horas-días
- Contraseña 12 caracteres: años-décadas

## 🚨 Consideraciones Legales

### Uso Autorizado Únicamente

Este software debe usarse ÚNICAMENTE para:
- Fines educativos y de aprendizaje
- Testing de seguridad autorizado
- Investigación en ciberseguridad
- Auditorías de seguridad propias

### Prohibido

- Uso en sistemas sin autorización
- Actividades ilegales o maliciosas
- Violación de términos de servicio
- Acceso no autorizado a datos

### Responsabilidad

El usuario es completamente responsable del uso ético y legal de esta herramienta.

## 📞 Soporte

Para reportar bugs o sugerir mejoras:
1. Revisar la documentación
2. Verificar logs de error
3. Crear un issue en el repositorio
4. Incluir información del sistema

---

**⚠️ RECORDATORIO:** Esta herramienta es solo para fines educativos y testing autorizado. El uso indebido es responsabilidad exclusiva del usuario.
