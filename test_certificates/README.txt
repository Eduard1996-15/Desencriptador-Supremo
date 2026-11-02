CERTIFICADOS DE PRUEBA PARA EXTRACTOR DE CLAVES PRIVADAS

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
