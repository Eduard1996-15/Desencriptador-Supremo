# 📖 Manual de Usuario - Desencriptador Supremo

## 🎯 Guía de Testing y Validación

### Archivos de Ejemplo Incluidos

La aplicación incluye varios archivos de ejemplo para probar todas las funcionalidades:

#### 📄 Archivos Encriptados
- `data/ejemplo-aes.enc` → Contraseña: `test123` (Encriptación AES-256)
- `data/ejemplo-admin.enc` → Contraseña: `admin`
- `data/ejemplo-password.enc` → Contraseña: `password`
- `data/ejemplo-123456.enc` → Contraseña: `123456`
- `data/ejemplo-qwerty.enc` → Contraseña: `qwerty`
- `data/ejemplo-secret.enc` → Contraseña: `secret`

#### 🔐 Certificados de Ejemplo
- `data/certificates/test-cert.pem` → Certificado público
- `data/certificates/test-private-key.pem` → Clave privada sin protección
- `data/certificates/test-private-key-protected.pem` → Contraseña: `certificado123`
- `data/certificates/test-cert.der` → Certificado en formato DER
- `data/certificates/test-private-key.der` → Contraseña: `dertest123`

---

## 🚀 Cómo Usar la Aplicación

### 1. 📁 Pestaña Principal - Desencriptación

**Proceso recomendado:**
1. Haz clic en "Seleccionar Archivo" 
2. Navega a `data/` y selecciona cualquier archivo `.enc`
3. Introduce la contraseña correspondiente (ver lista arriba)
4. Haz clic en "Desencriptar"
5. Observa la nueva ventana con el contenido desencriptado

**Ejemplo paso a paso:**
```
Archivo: ejemplo-aes.enc
Contraseña: test123
Resultado: Ventana mostrando el contenido del documento
```

### 2. 🔓 Pestaña Ataques

**Tipos de ataque disponibles:**

#### Fuerza Bruta
- **Caracteres personalizados**: Define tu propio conjunto
- **Longitud**: De 1 a 12 caracteres
- **Ejemplo**: Prueba con `ejemplo-admin.enc` usando solo letras minúsculas

#### Ataque de Diccionario
- **Diccionarios incluidos**: common-passwords.txt, spanish.txt
- **Recomendado para**: Contraseñas comunes
- **Ejemplo**: Usa `common-passwords.txt` con cualquier archivo de ejemplo

#### Ataque Híbrido
- **Combina**: Diccionario + variaciones (números, mayúsculas)
- **Más efectivo**: Para contraseñas como "admin123" o "Password!"

### 3. 📋 Pestaña Análisis

**Funcionalidades:**
- **Detección automática** del tipo de encriptación
- **Análisis de entropía** para determinar aleatoriedad
- **Recomendaciones** de ataque según el archivo

**Cómo usar:**
1. Selecciona un archivo encriptado
2. Haz clic en "Analizar"
3. Lee las recomendaciones de ataque sugeridas

### 4. 🏆 Pestaña Certificados

**Tipos soportados:**
- **PEM**: Certificados en texto
- **DER**: Certificados binarios
- **Claves privadas protegidas**

**Proceso:**
1. Selecciona un certificado de `data/certificates/`
2. Si está protegido, introduce la contraseña
3. Observa la información detallada del certificado

### 5. 🔨 Pestaña Hash Cracking

**Algoritmos soportados:**
- MD5, SHA-1, SHA-256, SHA-512
- bcrypt, scrypt, PBKDF2

**Ejemplo de uso:**
1. Introduce un hash MD5: `5d41402abc4b2a76b9719d911017c592`
2. Selecciona "MD5" como algoritmo
3. Usa ataque de diccionario
4. Resultado: "hello"

### 6. 📚 Pestaña Documentación

**Contiene:**
- **Estrategias de ataque** para diferentes tipos de archivos
- **Recomendaciones** de diccionarios
- **Mejores prácticas** de seguridad
- **Descarga automática** de diccionarios adicionales

---

## 🎯 Casos de Uso Específicos

### Escenario 1: Archivo ZIP Protegido
```
Situación: Archivo ZIP con contraseña olvidada
Estrategia: Ataque híbrido
Diccionario: common-passwords.txt
Variaciones: Números 0-999
```

### Escenario 2: Certificado Corporativo
```
Situación: Clave privada de servidor
Estrategia: Ataque de diccionario
Enfoque: Contraseñas corporativas comunes
```

### Escenario 3: Hash de Base de Datos
```
Situación: Hash MD5 de contraseña de usuario
Estrategia: Rainbow tables + diccionario
Herramientas: Hash Cracking tab
```

---

## ⚡ Tips de Optimización

### Rendimiento
- **Multithreading**: Automático en todos los ataques
- **GPU**: Se detecta automáticamente si está disponible
- **Memoria**: Monitoreada para prevenir saturación

### Estrategias Efectivas
1. **Empieza con diccionarios** antes que fuerza bruta
2. **Analiza el archivo primero** para determinar el tipo
3. **Usa ataques híbridos** para contraseñas complejas
4. **Ajusta la longitud** según el contexto del archivo

---

## 🔒 Consideraciones de Seguridad

### ⚠️ USO ÉTICO ÚNICAMENTE
- **Educación**: Aprendizaje de criptografía
- **Testing autorizado**: Solo en sistemas propios
- **Investigación**: Ciberseguridad legítima

### Responsabilidades
- **El usuario es completamente responsable** del uso de esta herramienta
- **No usar en sistemas ajenos** sin autorización explícita
- **Respetar todas las leyes locales** e internacionales

---

## 🛠️ Solución de Problemas

### Errores Comunes
1. **"Archivo no válido"**: Verifica que el archivo esté realmente encriptado
2. **"Contraseña incorrecta"**: Prueba con diferentes ataques
3. **"Error de memoria"**: Reduce el número de hilos o longitud de ataque

### Logs y Depuración
- **Ubicación**: `logs/desencriptador_*.log`
- **Nivel**: INFO, WARNING, ERROR
- **Útil para**: Diagnosticar problemas específicos

---

## 📞 Soporte

Para problemas técnicos o preguntas:
1. Revisa este manual primero
2. Verifica los logs en `logs/`
3. Prueba con archivos de ejemplo incluidos
4. Verifica que todas las dependencias estén instaladas

**¡Disfruta explorando las capacidades del Desencriptador Supremo!** 🚀
