"""
Ventana Principal del Desencriptador Supremo
Interfaz gráfica moderna con múltiples pestañas y funcionalidades avanzadas
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from pathlib import Path

# Importar módulos internos
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'crypto'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'attacks'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'certificates'))

try:
    from crypto_engine import CryptoEngine
    from attack_engine import AttackEngine
    from certificate_handler import CertificateHandler
    from hash_cracker import HashCracker
except ImportError as e:
    print(f"Error importing modules: {e}")
    # Si no se pueden importar, crear clases dummy
    class CryptoEngine:
        def __init__(self): pass
        def decrypt_with_password(self, data, password): return None, None
        def detect_encryption_type(self, data): return [('Unknown', 0.0)]
    class AttackEngine:
        def __init__(self): pass
    class CertificateHandler:
        def __init__(self): pass
        def load_certificate(self, path): return None
    class HashCracker:
        def __init__(self): pass
        def crack_hash(self, hash_str): return {'success': False}

class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_window()
        self.setup_style()
        self.create_widgets()
        self.setup_engines()
        
    def setup_window(self):
        """Configuración básica de la ventana"""
        self.root.title("🔓 Desencriptador Supremo - Ultra Powerful Edition")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Centrar ventana
        self.center_window()
        
        # Configurar cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_style(self):
        """Configuración de estilos y temas"""
        # Configurar tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Colores personalizados
        self.colors = {
            'primary': '#1e1e2e',
            'secondary': '#313244',
            'accent': '#89b4fa',
            'success': '#a6e3a1',
            'warning': '#f9e2af',
            'danger': '#f38ba8',
            'text': '#cdd6f4'
        }
        
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self.create_header()
        
        # Notebook para pestañas
        self.create_tabview()
        
        # Status bar
        self.create_status_bar()
        
    def create_header(self):
        """Crea el header de la aplicación"""
        header_frame = ctk.CTkFrame(self.main_frame, height=80)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Logo y título
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🔓 DESENCRIPTADOR SUPREMO",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        # Botones de acción rápida
        action_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        action_frame.pack(side="right", padx=20, pady=10)
        
        self.emergency_stop_btn = ctk.CTkButton(
            action_frame,
            text="🛑 STOP",
            command=self.emergency_stop,
            fg_color=self.colors['danger'],
            hover_color="#e64553",
            width=80
        )
        self.emergency_stop_btn.pack(side="right", padx=5)
        
        self.quick_scan_btn = ctk.CTkButton(
            action_frame,
            text="⚡ QUICK SCAN",
            command=self.quick_scan,
            width=120
        )
        self.quick_scan_btn.pack(side="right", padx=5)
        
    def create_tabview(self):
        """Crea el sistema de pestañas"""
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.tab_decrypt = self.tabview.add("🔓 Desencriptar")
        self.tab_certificates = self.tabview.add("📜 Certificados")
        self.tab_bruteforce = self.tabview.add("💥 Fuerza Bruta")
        self.tab_hashes = self.tabview.add("🔐 Hashes")
        self.tab_analysis = self.tabview.add("🔍 Análisis")
        self.tab_tools = self.tabview.add("🛠️ Herramientas")
        self.tab_docs = self.tabview.add("📚 Documentación")
        self.tab_settings = self.tabview.add("⚙️ Configuración")
        
        # Configurar contenido de cada pestaña
        self.setup_decrypt_tab()
        self.setup_certificates_tab()
        self.setup_bruteforce_tab()
        self.setup_hashes_tab()
        self.setup_analysis_tab()
        self.setup_tools_tab()
        self.setup_documentation_tab()
        self.setup_settings_tab()
        
    def setup_decrypt_tab(self):
        """Configura la pestaña de desencriptación"""
        # Frame principal de desencriptación
        main_frame = ctk.CTkFrame(self.tab_decrypt)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sección de archivo
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(file_frame, text="📁 Archivo a Desencriptar:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        file_input_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_input_frame.pack(fill="x", padx=10, pady=5)
        
        self.file_entry = ctk.CTkEntry(file_input_frame, placeholder_text="Selecciona un archivo...")
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(file_input_frame, text="Examinar", 
                     command=self.browse_file, width=100).pack(side="right")
        
        # Sección de algoritmos
        algo_frame = ctk.CTkFrame(main_frame)
        algo_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(algo_frame, text="🔐 Algoritmo de Encriptación:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        self.algorithm_var = ctk.StringVar(value="Auto-detectar")
        algorithms = ["Auto-detectar", "AES-256", "AES-128", "RSA", "DES", "3DES", 
                     "Blowfish", "Twofish", "ChaCha20", "Salsa20", "RC4"]
        
        self.algorithm_menu = ctk.CTkOptionMenu(algo_frame, variable=self.algorithm_var, 
                                               values=algorithms)
        self.algorithm_menu.pack(anchor="w", padx=10, pady=5)
        
        # Sección de métodos de ataque
        method_frame = ctk.CTkFrame(main_frame)
        method_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(method_frame, text="⚔️ Método de Ataque:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # Checkboxes para métodos
        self.method_vars = {}
        methods = ["Diccionario", "Fuerza Bruta", "Híbrido", "Reglas", "Máscara", "Tabla Arcoíris"]
        
        methods_container = ctk.CTkFrame(method_frame, fg_color="transparent")
        methods_container.pack(fill="x", padx=10, pady=5)
        
        for i, method in enumerate(methods):
            var = ctk.BooleanVar()
            self.method_vars[method] = var
            checkbox = ctk.CTkCheckBox(methods_container, text=method, variable=var)
            checkbox.grid(row=i//3, column=i%3, sticky="w", padx=10, pady=2)
        
        # Botón de inicio
        self.start_decrypt_btn = ctk.CTkButton(
            main_frame,
            text="🚀 INICIAR DESENCRIPTACIÓN",
            command=self.start_decryption,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['accent']
        )
        self.start_decrypt_btn.pack(fill="x", padx=10, pady=20)
        
        # Progress bar
        self.decrypt_progress = ctk.CTkProgressBar(main_frame)
        self.decrypt_progress.pack(fill="x", padx=10, pady=(0, 10))
        self.decrypt_progress.set(0)
        
    def setup_certificates_tab(self):
        """Configura la pestaña de certificados"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_certificates)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame de carga de certificado
        load_frame = ctk.CTkFrame(main_frame)
        load_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(load_frame, text="📜 Cargar Certificado:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        cert_input_frame = ctk.CTkFrame(load_frame, fg_color="transparent")
        cert_input_frame.pack(fill="x", padx=10, pady=5)
        
        self.cert_entry = ctk.CTkEntry(cert_input_frame, placeholder_text="Selecciona un certificado...")
        self.cert_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(cert_input_frame, text="Examinar", 
                     command=self.browse_certificate, width=100).pack(side="right")
        
        # Información del certificado
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(info_frame, text="ℹ️ Información del Certificado:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        self.cert_info_text = ctk.CTkTextbox(info_frame, height=200)
        self.cert_info_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botones de acción
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(action_frame, text="🔍 Analizar Certificado", 
                     command=self.analyze_certificate).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="🔓 Extraer Clave Privada", 
                     command=self.extract_private_key).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="🛡️ Validar Certificado", 
                     command=self.validate_certificate).pack(side="left", padx=5)
        
    def setup_bruteforce_tab(self):
        """Configura la pestaña de fuerza bruta"""
        main_frame = ctk.CTkFrame(self.tab_bruteforce)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configuración de ataque
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(config_frame, text="💥 Configuración de Fuerza Bruta:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # Configuraciones específicas
        settings_grid = ctk.CTkFrame(config_frame, fg_color="transparent")
        settings_grid.pack(fill="x", padx=10, pady=5)
        
        # Longitud mínima/máxima
        ctk.CTkLabel(settings_grid, text="Longitud mínima:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.min_length = ctk.CTkEntry(settings_grid, width=80)
        self.min_length.insert(0, "1")
        self.min_length.grid(row=0, column=1, padx=5, pady=2)
        
        ctk.CTkLabel(settings_grid, text="Longitud máxima:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.max_length = ctk.CTkEntry(settings_grid, width=80)
        self.max_length.insert(0, "8")
        self.max_length.grid(row=0, column=3, padx=5, pady=2)
        
        # Charset
        ctk.CTkLabel(settings_grid, text="Conjunto de caracteres:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.charset_var = ctk.StringVar(value="alfanumérico")
        charset_menu = ctk.CTkOptionMenu(settings_grid, variable=self.charset_var,
                                        values=["alfanumérico", "solo letras", "solo números", 
                                               "ascii completo", "personalizado"])
        charset_menu.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=2)
        
        # Hilos
        ctk.CTkLabel(settings_grid, text="Número de hilos:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.threads_slider = ctk.CTkSlider(settings_grid, from_=1, to=32, number_of_steps=31)
        self.threads_slider.set(8)
        self.threads_slider.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=2)
        
        self.threads_label = ctk.CTkLabel(settings_grid, text="8")
        self.threads_label.grid(row=2, column=3, padx=5, pady=2)
        self.threads_slider.configure(command=lambda x: self.threads_label.configure(text=str(int(x))))
        
        # Estadísticas en tiempo real
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(stats_frame, text="📊 Estadísticas en Tiempo Real:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=10, pady=5)
        
        # Labels de estadísticas
        self.stats_labels = {}
        stats_items = ["Contraseñas probadas", "Velocidad (p/s)", "Tiempo transcurrido", 
                      "Tiempo estimado", "CPU Usage", "RAM Usage"]
        
        for i, item in enumerate(stats_items):
            label = ctk.CTkLabel(stats_grid, text=f"{item}:")
            label.grid(row=i//2, column=(i%2)*2, sticky="w", padx=10, pady=2)
            
            value_label = ctk.CTkLabel(stats_grid, text="0", fg_color=self.colors['secondary'])
            value_label.grid(row=i//2, column=(i%2)*2+1, sticky="w", padx=10, pady=2)
            self.stats_labels[item] = value_label
        
        # Botón de inicio/parada
        self.bruteforce_btn = ctk.CTkButton(
            main_frame,
            text="💥 INICIAR ATAQUE DE FUERZA BRUTA",
            command=self.toggle_bruteforce,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['danger']
        )
        self.bruteforce_btn.pack(fill="x", padx=10, pady=20)
        
    def setup_hashes_tab(self):
        """Configura la pestaña de cracking de hashes"""
        main_frame = ctk.CTkFrame(self.tab_hashes)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Input de hash
        hash_frame = ctk.CTkFrame(main_frame)
        hash_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(hash_frame, text="🔐 Hash a Crackear:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        self.hash_entry = ctk.CTkEntry(hash_frame, placeholder_text="Ingresa el hash aquí...")
        self.hash_entry.pack(fill="x", padx=10, pady=5)
        
        # Tipo de hash
        type_frame = ctk.CTkFrame(hash_frame, fg_color="transparent")
        type_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(type_frame, text="Tipo de hash:").pack(side="left", padx=5)
        self.hash_type_var = ctk.StringVar(value="Auto-detectar")
        hash_types = ["Auto-detectar", "MD5", "SHA1", "SHA256", "SHA512", "bcrypt", "scrypt", "NTLM", "LM"]
        hash_type_menu = ctk.CTkOptionMenu(type_frame, variable=self.hash_type_var, values=hash_types)
        hash_type_menu.pack(side="left", padx=5)
        
        # Botón de detección
        ctk.CTkButton(type_frame, text="🔍 Auto-detectar", 
                     command=self.auto_detect_hash, width=120).pack(side="left", padx=5)
        
        # Diccionarios
        dict_frame = ctk.CTkFrame(main_frame)
        dict_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(dict_frame, text="📚 Diccionarios:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # Lista de diccionarios disponibles
        dict_list_frame = ctk.CTkFrame(dict_frame)
        dict_list_frame.pack(fill="x", padx=10, pady=5)
        
        self.dict_listbox = tk.Listbox(dict_list_frame, selectmode="multiple", height=4)
        self.dict_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Cargar diccionarios por defecto
        default_dicts = ["rockyou.txt", "common-passwords.txt", "spanish.txt", "numbers.txt", "custom.txt"]
        for d in default_dicts:
            self.dict_listbox.insert(tk.END, d)
        
        dict_buttons = ctk.CTkFrame(dict_list_frame)
        dict_buttons.pack(side="right", fill="y", padx=5, pady=5)
        
        ctk.CTkButton(dict_buttons, text="Agregar", command=self.add_dictionary, width=80).pack(pady=2)
        ctk.CTkButton(dict_buttons, text="Remover", command=self.remove_dictionary, width=80).pack(pady=2)
        ctk.CTkButton(dict_buttons, text="Generar", command=self.generate_dictionary, width=80).pack(pady=2)
        
        # Resultados
        results_frame = ctk.CTkFrame(main_frame)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(results_frame, text="✅ Resultados:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        self.hash_results_text = ctk.CTkTextbox(results_frame, height=150)
        self.hash_results_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botón de crack
        self.crack_hash_btn = ctk.CTkButton(
            main_frame,
            text="🔓 CRACKEAR HASH",
            command=self.crack_hash,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['accent']
        )
        self.crack_hash_btn.pack(fill="x", padx=10, pady=20)
        
    def setup_analysis_tab(self):
        """Configura la pestaña de análisis"""
        main_frame = ctk.CTkFrame(self.tab_analysis)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Selector de archivo para análisis
        file_selector_frame = ctk.CTkFrame(main_frame)
        file_selector_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(file_selector_frame, text="📁 Archivo para analizar:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        file_input_frame = ctk.CTkFrame(file_selector_frame, fg_color="transparent")
        file_input_frame.pack(fill="x", padx=10, pady=5)
        
        self.analysis_file_entry = ctk.CTkEntry(file_input_frame, placeholder_text="Selecciona un archivo para analizar...")
        self.analysis_file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_analysis_btn = ctk.CTkButton(
            file_input_frame, 
            text="📂 Examinar", 
            command=self.browse_analysis_file,
            width=100
        )
        browse_analysis_btn.pack(side="right")
        
        # Análisis de archivos
        file_analysis_frame = ctk.CTkFrame(main_frame)
        file_analysis_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(file_analysis_frame, text="🔍 Análisis Criptográfico:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # Resultados del análisis
        self.analysis_text = ctk.CTkTextbox(file_analysis_frame)
        self.analysis_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botones de análisis
        analysis_buttons = ctk.CTkFrame(file_analysis_frame, fg_color="transparent")
        analysis_buttons.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(analysis_buttons, text="🔍 Detectar Encriptación", 
                     command=self.detect_encryption_analysis).pack(side="left", padx=5)
        ctk.CTkButton(analysis_buttons, text="📊 Análisis de Entropía", 
                     command=self.entropy_analysis_analysis).pack(side="left", padx=5)
        ctk.CTkButton(analysis_buttons, text="🔬 Análisis Forense", 
                     command=self.forensic_analysis_analysis).pack(side="left", padx=5)
        
    def setup_documentation_tab(self):
        """Configura la pestaña de documentación con guías y sugerencias"""
        main_frame = ctk.CTkScrollableFrame(self.tab_docs)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título principal
        title_label = ctk.CTkLabel(
            main_frame, 
            text="📚 GUÍA DE ATAQUES Y ESTRATEGIAS",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Sección: Tipos de archivos y estrategias
        self.create_doc_section(main_frame, "🎯 ESTRATEGIAS POR TIPO DE ARCHIVO", [
            ("📄 Archivos ZIP/RAR protegidos", [
                "• Usar diccionarios comunes primero (rockyou, common-passwords)",
                "• Aplicar reglas de transformación (años, mayúsculas, números)",
                "• Probar contraseñas relacionadas con el nombre del archivo",
                "• Usar ataque híbrido con años (2020-2025)",
                "• Si falla: fuerza bruta incremental (4-8 caracteres)"
            ]),
            ("🔐 Certificados PKCS#12 (.p12, .pfx)", [
                "• Probar contraseñas por defecto: 'changeit', 'password', ''",
                "• Usar diccionarios de contraseñas corporativas",
                "• Probar nombre de dominio/empresa",
                "• Fechas importantes (creación, vencimiento)",
                "• Combinaciones: empresa+año, dominio+123"
            ]),
            ("🔑 Claves privadas SSH/PEM", [
                "• Diccionarios específicos para SSH",
                "• Contraseñas relacionadas con el usuario/servidor",
                "• Frases comunes en inglés",
                "• Nombres + años de nacimiento",
                "• Palabras técnicas + números"
            ]),
            ("💾 Bases de datos encriptadas", [
                "• Contraseñas relacionadas con el proyecto/app",
                "• Credenciales por defecto del SGBD",
                "• Diccionarios de contraseñas de bases de datos",
                "• Nombres de tablas/campos comunes",
                "• Versiones del software + números"
            ]),
            ("📱 Backups de dispositivos móviles", [
                "• Códigos PIN comunes (1234, 0000, 1111)",
                "• Fechas de cumpleaños",
                "• Números de teléfono parciales",
                "• Patrones de desbloqueo convertidos a números",
                "• Combinaciones familiares comunes"
            ])
        ])
        
        # Sección: Algoritmos de encriptación
        self.create_doc_section(main_frame, "🛡️ ESTRATEGIAS POR ALGORITMO", [
            ("AES (Advanced Encryption Standard)", [
                "• Algoritmo muy seguro, enfocarse en contraseñas débiles",
                "• Verificar si usa sal/IV predecible",
                "• Probar implementaciones débiles (ECB mode)",
                "• Diccionarios + reglas de transformación",
                "• Máximo 12 caracteres en fuerza bruta"
            ]),
            ("RSA (Rivest-Shamir-Adleman)", [
                "• Buscar claves con factores débiles",
                "• Verificar tamaño de clave (1024 bits = vulnerable)",
                "• Ataques específicos: Factorización, Common Modulus",
                "• Buscar reutilización de primos",
                "• Herramientas: RsaCtfTool, factordb.com"
            ]),
            ("DES/3DES", [
                "• Algoritmos débiles, fuerza bruta factible",
                "• Diccionarios extensivos primero",
                "• Fuerza bruta hasta 8-10 caracteres",
                "• Verificar modo de operación (ECB vulnerable)",
                "• Aprovechar debilidades conocidas"
            ]),
            ("Hashes (MD5, SHA1, SHA256)", [
                "• MD5/SHA1: Usar tablas rainbow",
                "• Diccionarios masivos (rockyou, wordlists específicas)",
                "• Reglas de Hashcat/John the Ripper",
                "• Ataques de máscara para patrones conocidos",
                "• Considerar sal si es hash salado"
            ])
        ])
        
        # Sección: Diccionarios recomendados
        self.create_doc_section(main_frame, "📚 DICCIONARIOS RECOMENDADOS", [
            ("Diccionarios Básicos", [
                "• rockyou.txt (14M contraseñas) - Descarga automática",
                "• common-passwords.txt - Incluido",
                "• spanish.txt - Incluido",
                "• 10k-most-common.txt",
                "• probable-v2-top12000.txt"
            ]),
            ("Diccionarios Especializados", [
                "• corporate-passwords.txt - Entornos empresariales",
                "• leaked-databases.txt - Bases filtradas",
                "• technology-terms.txt - Términos técnicos",
                "• names-surnames.txt - Nombres y apellidos",
                "• dates-years.txt - Fechas y años"
            ]),
            ("Generación de Diccionarios", [
                "• Usar información OSINT del objetivo",
                "• Generar con CeWL (web crawling)",
                "• Combinar diccionarios existentes",
                "• Crear patrones específicos con Crunch",
                "• Usar mutaciones de contraseñas conocidas"
            ])
        ])
        
        # Sección: Optimización de rendimiento
        self.create_doc_section(main_frame, "⚡ OPTIMIZACIÓN DE RENDIMIENTO", [
            ("Configuración de Hardware", [
                "• GPU: 1000x más rápido para hashes",
                "• CPU: Usar todos los núcleos disponibles",
                "• RAM: Mínimo 8GB para diccionarios grandes",
                "• SSD: Mejora carga de diccionarios",
                "• Refrigeración: Evitar throttling térmico"
            ]),
            ("Estrategia de Ataque", [
                "• Empezar con diccionarios pequeños y rápidos",
                "• Usar reglas simples antes que fuerza bruta",
                "• Paralelizar múltiples ataques",
                "• Guardar progreso para ataques largos",
                "• Establecer timeouts razonables"
            ]),
            ("Configuración de Software", [
                "• Ajustar número de hilos según CPU",
                "• Habilitar aceleración GPU si disponible",
                "• Optimizar uso de memoria",
                "• Usar formatos de diccionario optimizados",
                "• Configurar prioridad de proceso"
            ])
        ])
        
        # Sección: Aspectos legales y éticos
        self.create_doc_section(main_frame, "⚖️ CONSIDERACIONES LEGALES", [
            ("Uso Autorizado Únicamente", [
                "• Solo en sistemas propios o con autorización escrita",
                "• Pentesting autorizado y bug bounties",
                "• Investigación académica con permisos",
                "• Recuperación de contraseñas propias",
                "• Cumplir leyes locales e internacionales"
            ]),
            ("Buenas Prácticas", [
                "• Documentar todas las actividades",
                "• Obtener autorizaciones por escrito",
                "• Respetar alcance de pruebas",
                "• Reportar vulnerabilidades responsablemente",
                "• No acceder a datos no autorizados"
            ]),
            ("Prohibido", [
                "• Acceso no autorizado a sistemas",
                "• Robo de información confidencial",
                "• Daño a sistemas o datos",
                "• Uso para actividades ilegales",
                "• Violación de términos de servicio"
            ])
        ])
        
        # Botones de acción
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkButton(
            action_frame, 
            text="📥 Descargar Diccionarios Populares", 
            command=self.download_dictionaries,
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame, 
            text="🔗 Enlaces Útiles", 
            command=self.show_useful_links,
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame, 
            text="📖 Manual Completo", 
            command=self.open_manual,
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)

    def create_doc_section(self, parent, title, items):
        """Crea una sección de documentación"""
        # Título de sección
        section_frame = ctk.CTkFrame(parent)
        section_frame.pack(fill="x", padx=5, pady=10)
        
        title_label = ctk.CTkLabel(
            section_frame, 
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(anchor="w", padx=15, pady=10)
        
        # Contenido
        for item_title, item_content in items:
            item_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=15, pady=5)
            
            # Subtítulo
            subtitle_label = ctk.CTkLabel(
                item_frame, 
                text=item_title,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            subtitle_label.pack(fill="x", padx=10, pady=(5, 0))
            
            # Lista de puntos
            for point in item_content:
                point_label = ctk.CTkLabel(
                    item_frame, 
                    text=point,
                    font=ctk.CTkFont(size=12),
                    anchor="w",
                    wraplength=800
                )
                point_label.pack(fill="x", padx=20, pady=1)

    def setup_tools_tab(self):
        """Configura la pestaña de herramientas"""
        main_frame = ctk.CTkFrame(self.tab_tools)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Grid de herramientas
        tools_grid = ctk.CTkFrame(main_frame)
        tools_grid.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Herramientas disponibles
        tools = [
            ("🔐 Generador de Claves", self.generate_keys),
            ("🔄 Conversor de Formatos", self.convert_formats),
            ("📝 Editor Hexadecimal", self.hex_editor),
            ("🧮 Calculadora Hash", self.hash_calculator),
            ("🔍 Buscador de Claves", self.key_finder),
            ("📊 Análisis de Bits", self.bit_analysis),
            ("🎯 Generador de Wordlists", self.wordlist_generator),
            ("🛡️ Test de Seguridad", self.security_test)
        ]
        
        for i, (name, command) in enumerate(tools):
            row = i // 2
            col = i % 2
            
            tool_btn = ctk.CTkButton(
                tools_grid,
                text=name,
                command=command,
                height=60,
                font=ctk.CTkFont(size=14)
            )
            tool_btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        tools_grid.grid_columnconfigure(0, weight=1)
        tools_grid.grid_columnconfigure(1, weight=1)
        
    def setup_settings_tab(self):
        """Configura la pestaña de configuración"""
        main_frame = ctk.CTkFrame(self.tab_settings)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configuraciones generales
        general_frame = ctk.CTkFrame(main_frame)
        general_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(general_frame, text="⚙️ Configuración General:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # Tema
        theme_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(theme_frame, text="Tema:").pack(side="left", padx=5)
        self.theme_var = ctk.StringVar(value="Oscuro")
        theme_menu = ctk.CTkOptionMenu(theme_frame, variable=self.theme_var, 
                                      values=["Oscuro", "Claro", "Sistema"],
                                      command=self.change_theme)
        theme_menu.pack(side="left", padx=5)
        
        # Performance
        perf_frame = ctk.CTkFrame(main_frame)
        perf_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(perf_frame, text="🚀 Configuración de Rendimiento:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # Max threads slider
        threads_frame = ctk.CTkFrame(perf_frame, fg_color="transparent")
        threads_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(threads_frame, text="Hilos máximos:").pack(side="left", padx=5)
        self.max_threads_slider = ctk.CTkSlider(threads_frame, from_=1, to=16, number_of_steps=15)
        self.max_threads_slider.set(4)
        self.max_threads_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        self.threads_label = ctk.CTkLabel(threads_frame, text="4")
        self.threads_label.pack(side="right", padx=5)
        
        def update_threads_label(value):
            self.threads_label.configure(text=str(int(value)))
        
        self.max_threads_slider.configure(command=update_threads_label)
        
        # Timeout slider
        timeout_frame = ctk.CTkFrame(perf_frame, fg_color="transparent")
        timeout_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(timeout_frame, text="Timeout (segundos):").pack(side="left", padx=5)
        self.timeout_slider = ctk.CTkSlider(timeout_frame, from_=10, to=300, number_of_steps=29)
        self.timeout_slider.set(30)
        self.timeout_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        self.timeout_label = ctk.CTkLabel(timeout_frame, text="30")
        self.timeout_label.pack(side="right", padx=5)
        
        def update_timeout_label(value):
            self.timeout_label.configure(text=str(int(value)))
        
        self.timeout_slider.configure(command=update_timeout_label)
        
        # GPU acceleration
        self.use_gpu = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(perf_frame, text="Usar aceleración GPU (CUDA)", 
                       variable=self.use_gpu).pack(anchor="w", padx=10, pady=2)
        
        # Multithreading
        self.use_multithread = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(perf_frame, text="Usar multithreading", 
                       variable=self.use_multithread).pack(anchor="w", padx=10, pady=2)
        
        # Memory optimization
        self.memory_opt = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(perf_frame, text="Optimización de memoria (más lento)", 
                       variable=self.memory_opt).pack(anchor="w", padx=10, pady=2)
        
        # Paths
        paths_frame = ctk.CTkFrame(main_frame)
        paths_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(paths_frame, text="📁 Rutas de Archivos:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # Dictionary path
        dict_path_frame = ctk.CTkFrame(paths_frame, fg_color="transparent")
        dict_path_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(dict_path_frame, text="Diccionarios:").pack(side="left", padx=5)
        self.dict_path_entry = ctk.CTkEntry(dict_path_frame, placeholder_text="./data/dictionaries/")
        self.dict_path_entry.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(dict_path_frame, text="...", width=30, 
                     command=self.browse_dict_path).pack(side="right", padx=5)
        
        # Botones de acción
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkButton(action_frame, text="💾 Guardar Configuración", 
                     command=self.save_settings).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="🔄 Restaurar Defaults", 
                     command=self.restore_defaults).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="📊 Ver Logs", 
                     command=self.view_logs).pack(side="left", padx=10)
        
    def create_status_bar(self):
        """Crea la barra de estado"""
        self.status_frame = ctk.CTkFrame(self.main_frame, height=30)
        self.status_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="✅ Listo", 
                                        font=ctk.CTkFont(size=12))
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Indicadores de sistema
        self.cpu_label = ctk.CTkLabel(self.status_frame, text="CPU: 0%", 
                                     font=ctk.CTkFont(size=12))
        self.cpu_label.pack(side="right", padx=10, pady=5)
        
        self.ram_label = ctk.CTkLabel(self.status_frame, text="RAM: 0MB", 
                                     font=ctk.CTkFont(size=12))
        self.ram_label.pack(side="right", padx=10, pady=5)
        
    def setup_engines(self):
        """Inicializa los motores de criptografía"""
        try:
            self.crypto_engine = CryptoEngine()
            self.attack_engine = AttackEngine()
            self.cert_handler = CertificateHandler()
            self.hash_cracker = HashCracker()
            self.update_status("✅ Motores inicializados")
        except Exception as e:
            self.update_status(f"❌ Error inicializando motores: {e}")
    
    # Métodos de eventos
    def browse_file(self):
        """Abre diálogo para seleccionar archivo"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo a desencriptar",
            filetypes=[
                ("Todos los archivos", "*.*"),
                ("Archivos encriptados", "*.enc *.aes *.gpg"),
                ("Certificados", "*.pem *.der *.p12 *.pfx"),
                ("Archivos de claves", "*.key *.priv")
            ]
        )
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
            
    def browse_certificate(self):
        """Abre diálogo para seleccionar certificado"""
        filename = filedialog.askopenfilename(
            title="Seleccionar certificado",
            filetypes=[
                ("Certificados", "*.pem *.der *.crt *.cer"),
                ("PKCS#12", "*.p12 *.pfx"),
                ("Java KeyStore", "*.jks"),
                ("Todos los archivos", "*.*")
            ]
        )
        if filename:
            self.cert_entry.delete(0, tk.END)
            self.cert_entry.insert(0, filename)
            
    def start_decryption(self):
        """Inicia el proceso de desencriptación"""
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Selecciona un archivo primero")
            return
            
        self.update_status("🚀 Iniciando desencriptación...")
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self._decrypt_worker, args=(file_path,))
        thread.daemon = True
        thread.start()
        
    def _decrypt_worker(self, file_path):
        """Worker para desencriptación en hilo separado"""
        try:
            self.update_status("🔍 Analizando archivo...")
            self.decrypt_progress.set(0.1)
            
            # Leer archivo
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            self.update_status("🔍 Detectando tipo de encriptación...")
            self.decrypt_progress.set(0.2)
            
            # Detectar tipo de encriptación
            detected_types = self.crypto_engine.detect_encryption_type(encrypted_data)
            
            if not detected_types or detected_types[0][1] < 0.3:
                self.update_status("❌ No se pudo detectar el tipo de encriptación")
                messagebox.showerror("Error", "No se pudo detectar el tipo de encriptación del archivo")
                return
            
            algorithm = detected_types[0][0]
            confidence = detected_types[0][1]
            
            self.update_status(f"🎯 Detectado: {algorithm} (confianza: {confidence:.2f})")
            self.decrypt_progress.set(0.3)
            
            # Obtener métodos seleccionados
            selected_methods = [method for method, var in self.method_vars.items() if var.get()]
            
            if not selected_methods:
                selected_methods = ["Diccionario"]  # Por defecto
            
            success = False
            result_password = None
            decrypted_data = None
            
            # Intentar cada método seleccionado
            for i, method in enumerate(selected_methods):
                if success:
                    break
                    
                progress_base = 0.3 + (i / len(selected_methods)) * 0.6
                self.update_status(f"🔓 Probando método: {method}")
                self.decrypt_progress.set(progress_base)
                
                if method == "Diccionario":
                    result = self._try_dictionary_attack(encrypted_data, algorithm, progress_base)
                elif method == "Fuerza Bruta":
                    result = self._try_bruteforce_attack(encrypted_data, algorithm, progress_base)
                elif method == "Híbrido":
                    result = self._try_hybrid_attack(encrypted_data, algorithm, progress_base)
                else:
                    continue
                
                if result and result['success']:
                    success = True
                    result_password = result['password']
                    decrypted_data = result['data']
                    break
            
            self.decrypt_progress.set(1.0)
            
            if success:
                self.update_status(f"✅ ¡Desencriptación exitosa! Contraseña: {result_password}")
                self._show_decryption_results(file_path, result_password, decrypted_data, algorithm)
            else:
                self.update_status("❌ No se pudo desencriptar el archivo")
                messagebox.showerror("Error", "No se pudo desencriptar el archivo con los métodos seleccionados")
            
        except Exception as e:
            self.update_status(f"❌ Error: {e}")
            messagebox.showerror("Error", f"Error durante desencriptación: {e}")
    
    def _try_dictionary_attack(self, encrypted_data, algorithm, progress_base):
        """Intenta ataque de diccionario"""
        try:
            dictionaries = [
                "./data/common-passwords.txt",
                "./data/spanish.txt"
            ]
            
            # Verificar que existan diccionarios
            existing_dicts = [d for d in dictionaries if os.path.exists(d)]
            if not existing_dicts:
                return None
            
            password_count = 0
            for dict_path in existing_dicts:
                try:
                    with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            password = line.strip()
                            if not password:
                                continue
                            
                            # Probar contraseña
                            decrypted_data, used_algorithm = self.crypto_engine.decrypt_with_password(
                                encrypted_data, password, algorithm
                            )
                            
                            if decrypted_data:
                                # Verificar si la desencriptación es válida
                                is_valid, reason = self.crypto_engine.verify_decryption(decrypted_data)
                                if is_valid:
                                    return {
                                        'success': True,
                                        'password': password,
                                        'data': decrypted_data,
                                        'algorithm': used_algorithm
                                    }
                            
                            password_count += 1
                            if password_count % 100 == 0:
                                progress = progress_base + (password_count / 10000) * 0.1
                                self.decrypt_progress.set(min(progress, 0.9))
                                self.update_status(f"🔓 Probando: {password} ({password_count} intentos)")
                                self.root.update()
                
                except Exception as e:
                    self.logger.error(f"Error leyendo diccionario {dict_path}: {e}")
                    continue
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error en ataque de diccionario: {e}")
            return None
    
    def _try_bruteforce_attack(self, encrypted_data, algorithm, progress_base):
        """Intenta ataque de fuerza bruta"""
        try:
            charset = "abcdefghijklmnopqrstuvwxyz0123456789"
            max_length = 6  # Límite razonable para demo
            
            from itertools import product
            
            for length in range(1, max_length + 1):
                self.update_status(f"🔓 Fuerza bruta: longitud {length}")
                
                count = 0
                for password_tuple in product(charset, repeat=length):
                    password = ''.join(password_tuple)
                    
                    # Probar contraseña
                    decrypted_data, used_algorithm = self.crypto_engine.decrypt_with_password(
                        encrypted_data, password, algorithm
                    )
                    
                    if decrypted_data:
                        is_valid, reason = self.crypto_engine.verify_decryption(decrypted_data)
                        if is_valid:
                            return {
                                'success': True,
                                'password': password,
                                'data': decrypted_data,
                                'algorithm': used_algorithm
                            }
                    
                    count += 1
                    if count % 1000 == 0:
                        self.update_status(f"🔓 Probando: {password} ({count} intentos)")
                        self.root.update()
                    
                    # Límite de intentos para demo
                    if count > 50000:
                        break
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error en ataque de fuerza bruta: {e}")
            return None
    
    def _try_hybrid_attack(self, encrypted_data, algorithm, progress_base):
        """Intenta ataque híbrido"""
        try:
            # Combinar diccionario con transformaciones
            base_passwords = ["password", "admin", "123456", "qwerty", "abc123"]
            transformations = ["", "1", "123", "2024", "2025", "!", "01"]
            
            count = 0
            for base in base_passwords:
                for transform in transformations:
                    for case_variant in [base, base.upper(), base.capitalize()]:
                        password = case_variant + transform
                        
                        # Probar contraseña
                        decrypted_data, used_algorithm = self.crypto_engine.decrypt_with_password(
                            encrypted_data, password, algorithm
                        )
                        
                        if decrypted_data:
                            is_valid, reason = self.crypto_engine.verify_decryption(decrypted_data)
                            if is_valid:
                                return {
                                    'success': True,
                                    'password': password,
                                    'data': decrypted_data,
                                    'algorithm': used_algorithm
                                }
                        
                        count += 1
                        if count % 50 == 0:
                            progress = progress_base + (count / 500) * 0.1
                            self.decrypt_progress.set(min(progress, 0.9))
                            self.update_status(f"🔓 Probando: {password}")
                            self.root.update()
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error en ataque híbrido: {e}")
            return None
    
    def _show_decryption_results(self, original_file, password, decrypted_data, algorithm):
        """Muestra los resultados de la desencriptación"""
        # Crear ventana de resultados
        result_window = ctk.CTkToplevel(self.root)
        result_window.title("🎉 Desencriptación Exitosa")
        result_window.geometry("800x600")
        result_window.transient(self.root)
        result_window.grab_set()
        
        # Información general
        info_frame = ctk.CTkFrame(result_window)
        info_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(info_frame, text="🎉 ¡DESENCRIPTACIÓN EXITOSA!", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        info_text = f"""
📁 Archivo original: {os.path.basename(original_file)}
🔐 Algoritmo detectado: {algorithm}
🔑 Contraseña encontrada: {password}
📊 Tamaño original: {len(decrypted_data)} bytes
        """
        
        ctk.CTkLabel(info_frame, text=info_text, 
                    font=ctk.CTkFont(size=12), justify="left").pack(pady=10)
        
        # Vista previa del contenido
        preview_frame = ctk.CTkFrame(result_window)
        preview_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(preview_frame, text="👁️ Vista Previa del Contenido:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # Determinar tipo de contenido
        preview_text = self._generate_content_preview(decrypted_data)
        
        preview_textbox = ctk.CTkTextbox(preview_frame, height=300)
        preview_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        preview_textbox.insert("1.0", preview_text)
        preview_textbox.configure(state="disabled")
        
        # Botones de acción
        button_frame = ctk.CTkFrame(result_window)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        def save_decrypted():
            save_path = filedialog.asksaveasfilename(
                title="Guardar archivo desencriptado",
                defaultextension=".txt",
                filetypes=[
                    ("Todos los archivos", "*.*"),
                    ("Archivo de texto", "*.txt"),
                    ("Archivo original", "*" + os.path.splitext(original_file)[1])
                ]
            )
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(decrypted_data)
                messagebox.showinfo("Guardado", f"Archivo guardado como:\n{save_path}")
        
        def copy_password():
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Copiado", "Contraseña copiada al portapapeles")
        
        ctk.CTkButton(button_frame, text="💾 Guardar Archivo", 
                     command=save_decrypted).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(button_frame, text="📋 Copiar Contraseña", 
                     command=copy_password).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(button_frame, text="❌ Cerrar", 
                     command=result_window.destroy).pack(side="right", padx=10, pady=10)
    
    def _generate_content_preview(self, data):
        """Genera vista previa del contenido desencriptado"""
        try:
            # Intentar decodificar como texto
            try:
                text_content = data.decode('utf-8')
                if len(text_content) > 2000:
                    text_content = text_content[:2000] + "\n\n... (contenido truncado)"
                return f"📄 CONTENIDO DE TEXTO:\n\n{text_content}"
            except UnicodeDecodeError:
                pass
            
            # Si no es texto, mostrar información del archivo
            preview = "🔍 ANÁLISIS DE ARCHIVO BINARIO:\n\n"
            
            # Información básica
            preview += f"📊 Tamaño: {len(data)} bytes\n"
            preview += f"🔢 Tipo de datos: Binario\n\n"
            
            # Análisis de headers
            if len(data) >= 4:
                header = data[:4]
                if header == b'\x50\x4B\x03\x04':
                    preview += "📦 Detectado: Archivo ZIP\n"
                elif header == b'\x89\x50\x4E\x47':
                    preview += "🖼️ Detectado: Imagen PNG\n"
                elif header[:2] == b'\xFF\xD8':
                    preview += "📸 Detectado: Imagen JPEG\n"
                elif header == b'%PDF':
                    preview += "📄 Detectado: Documento PDF\n"
                else:
                    preview += f"❓ Header desconocido: {header.hex().upper()}\n"
            
            # Vista hexadecimal de los primeros bytes
            preview += "\n🔍 VISTA HEXADECIMAL (primeros 256 bytes):\n\n"
            hex_data = data[:256]
            
            for i in range(0, len(hex_data), 16):
                chunk = hex_data[i:i+16]
                hex_str = ' '.join(f'{b:02X}' for b in chunk)
                ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
                preview += f"{i:08X}: {hex_str:<48} |{ascii_str}|\n"
            
            if len(data) > 256:
                preview += "\n... (datos adicionales truncados)"
            
            return preview
            
        except Exception as e:
            return f"❌ Error generando vista previa: {e}"
    
    def emergency_stop(self):
        """Detiene todas las operaciones inmediatamente"""
        self.update_status("🛑 PARADA DE EMERGENCIA")
        # Aquí se implementaría la lógica para detener todos los procesos
        
    def quick_scan(self):
        """Realiza un escaneo rápido"""
        self.update_status("⚡ Escaneando...")
        # Implementar escaneo rápido
        
    def toggle_bruteforce(self):
        """Alterna el ataque de fuerza bruta"""
        current_text = self.bruteforce_btn.cget("text")
        if "INICIAR" in current_text:
            self.bruteforce_btn.configure(text="🛑 DETENER ATAQUE")
            self.start_bruteforce_attack()
        else:
            self.bruteforce_btn.configure(text="💥 INICIAR ATAQUE DE FUERZA BRUTA")
            self.stop_bruteforce_attack()
    
    def start_bruteforce_attack(self):
        """Inicia ataque de fuerza bruta"""
        self.update_status("💥 Iniciando ataque de fuerza bruta...")
        # Implementar lógica de fuerza bruta
        
    def stop_bruteforce_attack(self):
        """Detiene ataque de fuerza bruta"""
        self.update_status("🛑 Deteniendo ataque...")
        # Implementar parada de fuerza bruta
    
    def analyze_certificate(self):
        """Analiza el certificado cargado"""
        cert_path = self.cert_entry.get()
        if not cert_path:
            messagebox.showerror("Error", "Selecciona un certificado primero")
            return
        
        try:
            # Cargar certificado
            cert_info = self.cert_handler.load_certificate(cert_path)
            
            if not cert_info:
                messagebox.showerror("Error", "No se pudo cargar el certificado")
                return
            
            # Mostrar información en el textbox
            info_text = self._format_certificate_info(cert_info)
            
            self.cert_info_text.delete("1.0", tk.END)
            self.cert_info_text.insert("1.0", info_text)
            
            self.update_status("✅ Certificado analizado exitosamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error analizando certificado: {e}")
    
    def _format_certificate_info(self, cert_info):
        """Formatea la información del certificado"""
        info_lines = []
        
        info_lines.append("🔍 INFORMACIÓN DEL CERTIFICADO")
        info_lines.append("=" * 50)
        info_lines.append(f"📋 Tipo: {cert_info.get('type', 'Desconocido')}")
        
        if 'version' in cert_info:
            info_lines.append(f"📝 Versión: {cert_info['version']}")
        
        if 'serial_number' in cert_info:
            info_lines.append(f"🔢 Número de serie: {cert_info['serial_number']}")
        
        if 'subject' in cert_info:
            info_lines.append("\n👤 SUJETO:")
            for key, value in cert_info['subject'].items():
                info_lines.append(f"  • {key}: {value}")
        
        if 'issuer' in cert_info:
            info_lines.append("\n🏢 EMISOR:")
            for key, value in cert_info['issuer'].items():
                info_lines.append(f"  • {key}: {value}")
        
        if 'not_valid_before' in cert_info:
            info_lines.append(f"\n📅 Válido desde: {cert_info['not_valid_before']}")
        
        if 'not_valid_after' in cert_info:
            info_lines.append(f"📅 Válido hasta: {cert_info['not_valid_after']}")
            
            if cert_info.get('is_expired'):
                info_lines.append("⚠️ CERTIFICADO EXPIRADO")
        
        if 'signature_algorithm' in cert_info:
            info_lines.append(f"\n🔐 Algoritmo de firma: {cert_info['signature_algorithm']}")
        
        if 'public_key_info' in cert_info:
            pk_info = cert_info['public_key_info']
            info_lines.append(f"🔑 Clave pública: {pk_info.get('algorithm', 'Desconocido')}")
            if 'key_size' in pk_info:
                info_lines.append(f"📏 Tamaño de clave: {pk_info['key_size']} bits")
        
        if 'sha256_fingerprint' in cert_info:
            info_lines.append(f"\n🔍 Huella SHA256: {cert_info['sha256_fingerprint']}")
        
        if 'extensions' in cert_info and cert_info['extensions']:
            info_lines.append("\n📋 EXTENSIONES:")
            for ext_name, ext_info in cert_info['extensions'].items():
                critical = " (CRÍTICA)" if ext_info.get('critical') else ""
                info_lines.append(f"  • {ext_name}{critical}")
        
        if 'file_path' in cert_info:
            info_lines.append(f"\n📁 Archivo: {cert_info['file_path']}")
            info_lines.append(f"📊 Tamaño: {cert_info.get('file_size', 0)} bytes")
        
        return "\n".join(info_lines)
    
    def extract_private_key(self):
        """Extrae clave privada del certificado con opciones avanzadas"""
        cert_path = self.cert_entry.get()
        if not cert_path:
            messagebox.showerror("Error", "Selecciona un certificado primero")
            return
        
        # Crear ventana de opciones de extracción
        extract_window = ctk.CTkToplevel(self.root)
        extract_window.title("🔑 Extracción Avanzada de Clave Privada")
        extract_window.geometry("600x500")
        extract_window.transient(self.root)
        extract_window.grab_set()
        
        main_frame = ctk.CTkFrame(extract_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="🔑 EXTRACCIÓN AVANZADA DE CLAVE PRIVADA", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Mostrar archivo seleccionado
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(file_frame, text=f"📄 Archivo: {cert_path}", 
                    font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=5)
        
        # Método de extracción
        method_frame = ctk.CTkFrame(main_frame)
        method_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(method_frame, text="Método de extracción:").pack(anchor="w", padx=10, pady=5)
        method_var = ctk.StringVar(value="auto")
        
        methods = [
            ("🎯 Automático (Recomendado)", "auto"),
            ("🔑 Contraseña específica", "password"),
            ("📚 Ataque de diccionario", "dictionary"),
            ("⚡ Fuerza bruta", "bruteforce"),
            ("🔄 Ataque híbrido", "hybrid")
        ]
        
        for text, value in methods:
            ctk.CTkRadioButton(method_frame, text=text, variable=method_var, 
                              value=value).pack(anchor="w", padx=20, pady=2)
        
        # Opciones específicas
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        # Contraseña específica
        password_frame = ctk.CTkFrame(options_frame)
        password_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(password_frame, text="Contraseña (si la conoces):").pack(anchor="w", padx=10, pady=2)
        password_entry = ctk.CTkEntry(password_frame, placeholder_text="Contraseña...", show="*")
        password_entry.pack(fill="x", padx=10, pady=2)
        
        # Opciones de fuerza bruta
        bf_frame = ctk.CTkFrame(options_frame)
        bf_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(bf_frame, text="Opciones de fuerza bruta:").pack(anchor="w", padx=10, pady=2)
        
        bf_options_frame = ctk.CTkFrame(bf_frame)
        bf_options_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(bf_options_frame, text="Longitud máxima:").pack(side="left", padx=5)
        max_length_var = ctk.StringVar(value="6")
        length_entry = ctk.CTkEntry(bf_options_frame, textvariable=max_length_var, width=60)
        length_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(bf_options_frame, text="Caracteres:").pack(side="left", padx=5)
        charset_var = ctk.StringVar(value="abcdefghijklmnopqrstuvwxyz0123456789")
        charset_entry = ctk.CTkEntry(bf_options_frame, textvariable=charset_var)
        charset_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Progreso
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", padx=10, pady=10)
        
        progress_label = ctk.CTkLabel(progress_frame, text="Listo para extraer...")
        progress_label.pack(anchor="w", padx=10, pady=5)
        
        progress_bar = ctk.CTkProgressBar(progress_frame)
        progress_bar.pack(fill="x", padx=10, pady=5)
        progress_bar.set(0)
        
        # Botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        extraction_thread = None
        extractor = None
        
        def start_extraction():
            nonlocal extraction_thread, extractor
            
            try:
                # Importar el extractor avanzado
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'certificates'))
                from advanced_extractor import AdvancedPrivateKeyExtractor
                
                extractor = AdvancedPrivateKeyExtractor()
                
                method = method_var.get()
                kwargs = {}
                
                if method == "password":
                    kwargs['password'] = password_entry.get()
                elif method == "bruteforce":
                    kwargs['max_length'] = int(max_length_var.get())
                    kwargs['charset'] = charset_var.get()
                    kwargs['allow_bruteforce'] = True
                elif method == "auto":
                    kwargs['allow_bruteforce'] = True
                    kwargs['max_length'] = 6  # Limitado para demo
                
                # Función de progreso
                def update_progress(current, total):
                    if total > 0:
                        progress = current / total
                        progress_bar.set(progress)
                        progress_label.configure(text=f"Progreso: {current:,}/{total:,} ({progress*100:.1f}%)")
                    extract_window.update_idletasks()
                
                kwargs['progress_callback'] = update_progress
                
                # Deshabilitar botón de inicio
                start_btn.configure(state="disabled")
                stop_btn.configure(state="normal")
                
                progress_label.configure(text=f"Iniciando extracción con método: {method}...")
                
                # Ejecutar en hilo separado
                def extraction_worker():
                    try:
                        result = extractor.extract_private_key(cert_path, method, **kwargs)
                        
                        # Mostrar resultado en el hilo principal
                        extract_window.after(0, lambda: show_extraction_result(result))
                        
                    except Exception as e:
                        extract_window.after(0, lambda: messagebox.showerror("Error", f"Error en extracción: {e}"))
                    finally:
                        extract_window.after(0, lambda: (
                            start_btn.configure(state="normal"),
                            stop_btn.configure(state="disabled"),
                            progress_label.configure(text="Extracción completada."),
                            progress_bar.set(0)
                        ))
                
                extraction_thread = threading.Thread(target=extraction_worker, daemon=True)
                extraction_thread.start()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error iniciando extracción: {e}")
                start_btn.configure(state="normal")
                stop_btn.configure(state="disabled")
        
        def stop_extraction():
            if extractor:
                extractor.stop_extraction()
                progress_label.configure(text="Deteniendo extracción...")
                stop_btn.configure(state="disabled")
        
        def show_extraction_result(result):
            if result['success']:
                # Mostrar ventana con la clave privada extraída
                result_window = ctk.CTkToplevel(extract_window)
                result_window.title("🎉 Clave Privada Extraída")
                result_window.geometry("700x600")
                
                result_text = ctk.CTkTextbox(result_window)
                result_text.pack(fill="both", expand=True, padx=20, pady=20)
                
                content = f"""🎉 CLAVE PRIVADA EXTRAÍDA EXITOSAMENTE!

📄 Archivo: {cert_path}
🔑 Método usado: {result.get('method_used', 'Desconocido')}
🔐 Tipo de clave: {result.get('key_type', 'Desconocido')}
📏 Tamaño: {result.get('key_size', 'Desconocido')} bits
📋 Formato: {result.get('format', 'PEM')}

"""
                
                if result.get('password_found'):
                    content += f"🔑 Contraseña encontrada: {result['password_found']}\n"
                
                if result.get('attempts_made'):
                    content += f"🎯 Intentos realizados: {result['attempts_made']:,}\n"
                
                content += f"""
==================== CLAVE PRIVADA ====================
{result.get('private_key_pem', 'Error obteniendo clave PEM')}

⚠️ IMPORTANTE: 
• Guarda esta clave en un lugar seguro
• La clave privada debe mantenerse confidencial
• Considera cambiar la contraseña del certificado"""
                
                result_text.insert("0.0", content)
                result_text.configure(state="disabled")
                
                # Botón para guardar
                save_frame = ctk.CTkFrame(result_window)
                save_frame.pack(fill="x", padx=20, pady=10)
                
                def save_key():
                    file_path = filedialog.asksaveasfilename(
                        title="Guardar clave privada",
                        defaultextension=".pem",
                        filetypes=[("Archivo PEM", "*.pem"), ("Todos", "*.*")]
                    )
                    if file_path:
                        try:
                            with open(file_path, 'w') as f:
                                f.write(result['private_key_pem'])
                            messagebox.showinfo("Éxito", f"Clave guardada en:\n{file_path}")
                        except Exception as e:
                            messagebox.showerror("Error", f"Error guardando clave: {e}")
                
                ctk.CTkButton(save_frame, text="💾 Guardar Clave", command=save_key).pack(pady=10)
                
            else:
                # Mostrar error detallado
                error_msg = result.get('error', 'Error desconocido')
                
                if 'detailed_results' in result:
                    detailed = result['detailed_results']
                    attempts_info = f"\n\nDetalles de intentos:\n"
                    for attempt in detailed.get('attempts', []):
                        attempts_info += f"• {attempt.get('method', 'N/A')}: {'Éxito' if attempt.get('result', {}).get('success') else 'Falló'}\n"
                    error_msg += attempts_info
                
                messagebox.showerror("Error", f"No se pudo extraer la clave privada:\n\n{error_msg}")
        
        start_btn = ctk.CTkButton(button_frame, text="🚀 Iniciar Extracción", 
                                 command=start_extraction, height=40)
        start_btn.pack(side="left", padx=5, pady=10)
        
        stop_btn = ctk.CTkButton(button_frame, text="🛑 Detener", 
                                command=stop_extraction, height=40, state="disabled")
        stop_btn.pack(side="left", padx=5, pady=10)
        
        ctk.CTkButton(button_frame, text="❌ Cerrar", 
                     command=extract_window.destroy, height=40).pack(side="right", padx=5, pady=10)
    
    def _show_private_key_result(self, result):
        """Muestra el resultado de extracción de clave privada"""
        # Crear ventana de resultados
        result_window = ctk.CTkToplevel(self.root)
        result_window.title("🔑 Clave Privada Extraída")
        result_window.geometry("700x500")
        result_window.transient(self.root)
        result_window.grab_set()
        
        # Información
        info_frame = ctk.CTkFrame(result_window)
        info_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(info_frame, text="🔑 CLAVE PRIVADA EXTRAÍDA EXITOSAMENTE", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        info_text = f"🔐 Tipo de clave: {result.get('key_type', 'Desconocido')}\n📏 Tamaño: {result.get('key_size', 'Desconocido')} bits"
        ctk.CTkLabel(info_frame, text=info_text).pack(pady=5)
        
        # Clave privada
        key_frame = ctk.CTkFrame(result_window)
        key_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(key_frame, text="📄 Clave Privada (PEM):", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        key_textbox = ctk.CTkTextbox(key_frame)
        key_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        key_textbox.insert("1.0", result.get('private_key_pem', ''))
        
        # Botones
        button_frame = ctk.CTkFrame(result_window)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        def save_key():
            save_path = filedialog.asksaveasfilename(
                title="Guardar clave privada",
                defaultextension=".pem",
                filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
            )
            if save_path:
                with open(save_path, 'w') as f:
                    f.write(result.get('private_key_pem', ''))
                messagebox.showinfo("Guardado", f"Clave privada guardada en:\n{save_path}")
        
        def copy_key():
            self.root.clipboard_clear()
            self.root.clipboard_append(result.get('private_key_pem', ''))
            messagebox.showinfo("Copiado", "Clave privada copiada al portapapeles")
        
        ctk.CTkButton(button_frame, text="💾 Guardar", command=save_key).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(button_frame, text="📋 Copiar", command=copy_key).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(button_frame, text="❌ Cerrar", command=result_window.destroy).pack(side="right", padx=10, pady=10)
    
    def validate_certificate(self):
        """Valida el certificado"""
        cert_path = self.cert_entry.get()
        if not cert_path:
            messagebox.showerror("Error", "Selecciona un certificado primero")
            return
        
        try:
            validation_result = self.cert_handler.validate_certificate_chain(cert_path)
            
            if validation_result['is_valid']:
                messagebox.showinfo("Validación", "✅ Certificado válido")
            else:
                issues = '\n'.join(validation_result['issues'])
                messagebox.showwarning("Validación", f"⚠️ Problemas encontrados:\n\n{issues}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error validando certificado: {e}")
    
    def download_dictionaries(self):
        """Descarga diccionarios populares de internet"""
        download_window = ctk.CTkToplevel(self.root)
        download_window.title("📥 Descargar Diccionarios")
        download_window.geometry("600x400")
        download_window.transient(self.root)
        download_window.grab_set()
        
        # Lista de diccionarios disponibles
        dictionaries = [
            {
                'name': 'RockYou.txt',
                'size': '133 MB',
                'description': '14M contraseñas más comunes',
                'url': 'https://github.com/danielmiessler/SecLists/raw/master/Passwords/Leaked-Databases/rockyou.txt.tar.gz'
            },
            {
                'name': 'Common Passwords',
                'size': '2 MB', 
                'description': '10K contraseñas más comunes',
                'url': 'https://github.com/danielmiessler/SecLists/raw/master/Passwords/Common-Credentials/10k-most-common.txt'
            },
            {
                'name': 'Probable Wordlist v2',
                'size': '1 MB',
                'description': 'Top 12K contraseñas probables',
                'url': 'https://github.com/berzerk0/Probable-Wordlists/raw/master/Real-Passwords/Top12Thousand-probable-v2.txt'
            }
        ]
        
        # Frame principal
        main_frame = ctk.CTkFrame(download_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="📥 Diccionarios Disponibles", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Lista de diccionarios
        for i, dict_info in enumerate(dictionaries):
            dict_frame = ctk.CTkFrame(main_frame)
            dict_frame.pack(fill="x", padx=10, pady=5)
            
            info_text = f"📚 {dict_info['name']} ({dict_info['size']})\n{dict_info['description']}"
            ctk.CTkLabel(dict_frame, text=info_text, anchor="w").pack(side="left", padx=10, pady=10)
            
            def download_dict(url=dict_info['url'], name=dict_info['name']):
                self._download_dictionary_file(url, name, download_window)
            
            ctk.CTkButton(dict_frame, text="⬇️ Descargar", 
                         command=download_dict, width=100).pack(side="right", padx=10, pady=10)
        
        # Botón cerrar
        ctk.CTkButton(main_frame, text="❌ Cerrar", 
                     command=download_window.destroy).pack(pady=20)
    
    def _download_dictionary_file(self, url, name, parent_window):
        """Descarga un archivo de diccionario"""
        try:
            import requests
            import os
            
            # Crear directorio si no existe
            dict_dir = "./data/downloaded/"
            os.makedirs(dict_dir, exist_ok=True)
            
            # Determinar nombre de archivo
            filename = name.lower().replace(' ', '-') + '.txt'
            file_path = os.path.join(dict_dir, filename)
            
            # Verificar si ya existe
            if os.path.exists(file_path):
                if not messagebox.askyesno("Archivo existe", f"El archivo {filename} ya existe. ¿Sobreescribir?"):
                    return
            
            # Ventana de progreso
            progress_window = ctk.CTkToplevel(parent_window)
            progress_window.title("Descargando...")
            progress_window.geometry("400x150")
            progress_window.transient(parent_window)
            progress_window.grab_set()
            
            status_label = ctk.CTkLabel(progress_window, text=f"Descargando {name}...")
            status_label.pack(pady=20)
            
            progress_bar = ctk.CTkProgressBar(progress_window)
            progress_bar.pack(padx=20, pady=10, fill="x")
            progress_bar.set(0)
            
            def download_thread():
                try:
                    response = requests.get(url, stream=True)
                    response.raise_for_status()
                    
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0
                    
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                
                                if total_size > 0:
                                    progress = downloaded / total_size
                                    progress_bar.set(progress)
                                    status_label.configure(text=f"Descargando {name}... {progress*100:.1f}%")
                                    progress_window.update()
                    
                    progress_window.destroy()
                    messagebox.showinfo("Éxito", f"Diccionario descargado exitosamente:\n{file_path}")
                    
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Error descargando diccionario: {e}")
            
            # Iniciar descarga en hilo separado
            import threading
            download_thread = threading.Thread(target=download_thread)
            download_thread.daemon = True
            download_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error iniciando descarga: {e}")
    
    def show_useful_links(self):
        """Muestra enlaces útiles"""
        links_window = ctk.CTkToplevel(self.root)
        links_window.title("🔗 Enlaces Útiles")
        links_window.geometry("500x400")
        links_window.transient(self.root)
        
        main_frame = ctk.CTkScrollableFrame(links_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="🔗 RECURSOS ÚTILES", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        links = [
            ("🔑 Hashcat", "https://hashcat.net/hashcat/"),
            ("🔓 John the Ripper", "https://www.openwall.com/john/"),
            ("📚 SecLists", "https://github.com/danielmiessler/SecLists"),
            ("🔍 CrackStation", "https://crackstation.net/"),
            ("📖 OWASP Testing Guide", "https://owasp.org/www-project-web-security-testing-guide/"),
            ("🎯 HaveIBeenPwned", "https://haveibeenpwned.com/"),
            ("🔐 CyberChef", "https://gchq.github.io/CyberChef/")
        ]
        
        for name, url in links:
            link_frame = ctk.CTkFrame(main_frame)
            link_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(link_frame, text=name, anchor="w").pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(link_frame, text=url, anchor="w", 
                        text_color="lightblue").pack(side="left", padx=10, pady=10)
    
    def open_manual(self):
        """Abre el manual completo"""
        try:
            import subprocess
            import sys
            
            manual_path = "./MANUAL.md"
            if os.path.exists(manual_path):
                if sys.platform.startswith('win'):
                    subprocess.run(['start', manual_path], shell=True)
                elif sys.platform.startswith('darwin'):
                    subprocess.run(['open', manual_path])
                else:
                    subprocess.run(['xdg-open', manual_path])
            else:
                messagebox.showerror("Error", "Manual no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Error abriendo manual: {e}")
    
    # Métodos adicionales implementados
    def auto_detect_hash(self):
        """Detecta automáticamente el tipo de hash"""
        hash_value = self.hash_entry.get().strip()
        if not hash_value:
            messagebox.showerror("Error", "Ingresa un hash para detectar")
            return
        
        # Detectar por longitud y formato
        hash_length = len(hash_value)
        detection_results = []
        
        # Verificar si es hexadecimal
        try:
            int(hash_value, 16)
            is_hex = True
        except ValueError:
            is_hex = False
        
        if is_hex:
            if hash_length == 32:
                detection_results.append("MD5 (muy probable)")
            elif hash_length == 40:
                detection_results.append("SHA-1 (muy probable)")
            elif hash_length == 64:
                detection_results.append("SHA-256 (muy probable)")
            elif hash_length == 128:
                detection_results.append("SHA-512 (muy probable)")
        
        # Detectar otros formatos
        if hash_value.startswith('$2a$') or hash_value.startswith('$2b$'):
            detection_results.append("bcrypt")
        elif hash_value.startswith('$6$'):
            detection_results.append("SHA-512 crypt")
        elif hash_value.startswith('$5$'):
            detection_results.append("SHA-256 crypt")
        elif hash_value.startswith('$1$'):
            detection_results.append("MD5 crypt")
        elif '{' in hash_value and '}' in hash_value:
            detection_results.append("Formato LDAP/Windows")
        
        if not detection_results:
            detection_results.append("Formato no reconocido")
        
        # Mostrar resultados
        result_msg = f"Hash: {hash_value[:20]}...\n\nPosibles tipos:\n" + "\n".join(f"• {result}" for result in detection_results)
        messagebox.showinfo("🔍 Detección de Hash", result_msg)
    
    def add_dictionary(self):
        """Añade un nuevo diccionario"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar diccionario",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")]
        )
        
        if file_path:
            # Copiar a la carpeta de datos
            import shutil
            from pathlib import Path
            
            dest_dir = Path("./data")
            dest_dir.mkdir(exist_ok=True)
            
            dest_path = dest_dir / Path(file_path).name
            shutil.copy2(file_path, dest_path)
            
            # Actualizar la lista
            self.dict_listbox.insert("end", Path(file_path).name)
            messagebox.showinfo("Éxito", f"Diccionario añadido: {Path(file_path).name}")
    
    def remove_dictionary(self):
        """Elimina un diccionario seleccionado"""
        try:
            selection = self.dict_listbox.curselection()
            if selection:
                dict_name = self.dict_listbox.get(selection[0])
                
                # Confirmar eliminación
                if messagebox.askyesno("Confirmar", f"¿Eliminar {dict_name}?"):
                    # Eliminar archivo
                    dict_path = Path("./data") / dict_name
                    if dict_path.exists():
                        dict_path.unlink()
                    
                    # Actualizar lista
                    self.dict_listbox.delete(selection[0])
                    messagebox.showinfo("Éxito", f"Diccionario eliminado: {dict_name}")
            else:
                messagebox.showwarning("Advertencia", "Selecciona un diccionario para eliminar")
        except Exception as e:
            messagebox.showerror("Error", f"Error eliminando diccionario: {e}")
    
    def generate_dictionary(self):
        """Genera diccionarios personalizados"""
        # Crear ventana del generador
        gen_window = ctk.CTkToplevel(self.root)
        gen_window.title("🎯 Generador de Diccionarios")
        gen_window.geometry("600x500")
        gen_window.transient(self.root)
        gen_window.grab_set()
        
        main_frame = ctk.CTkFrame(gen_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="🎯 GENERADOR DE DICCIONARIOS PERSONALIZADOS", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Tipo de generación
        type_frame = ctk.CTkFrame(main_frame)
        type_frame.pack(fill="x", padx=10, pady=10)
        
        gen_type = ctk.StringVar(value="combinaciones")
        ctk.CTkLabel(type_frame, text="Tipo de generación:").pack(anchor="w", padx=10, pady=5)
        
        types = [
            ("Combinaciones de palabras", "combinaciones"),
            ("Variaciones numéricas", "numericas"),
            ("Patrones de fechas", "fechas"),
            ("Contraseñas corporativas", "corporativas")
        ]
        
        for text, value in types:
            ctk.CTkRadioButton(type_frame, text=text, variable=gen_type, 
                              value=value).pack(anchor="w", padx=20, pady=2)
        
        # Palabras base
        words_frame = ctk.CTkFrame(main_frame)
        words_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(words_frame, text="Palabras base (una por línea):").pack(anchor="w", padx=10, pady=5)
        words_text = ctk.CTkTextbox(words_frame, height=100)
        words_text.pack(fill="x", padx=10, pady=5)
        words_text.insert("0.0", "admin\ntest\nuser\npassword\ncompany")
        
        # Generar
        def generate():
            words = [w.strip() for w in words_text.get("0.0", "end").strip().split('\n') if w.strip()]
            if not words:
                messagebox.showerror("Error", "Ingresa al menos una palabra base")
                return
            
            generated = set()
            gen_type_val = gen_type.get()
            
            if gen_type_val == "combinaciones":
                for word in words:
                    generated.add(word)
                    generated.add(word.upper())
                    generated.add(word.lower())
                    generated.add(word.capitalize())
                    
            elif gen_type_val == "numericas":
                for word in words:
                    for num in range(0, 100):
                        generated.add(f"{word}{num}")
                        generated.add(f"{num}{word}")
                        
            elif gen_type_val == "fechas":
                years = ["2020", "2021", "2022", "2023", "2024", "2025"]
                for word in words:
                    for year in years:
                        generated.add(f"{word}{year}")
                        generated.add(f"{year}{word}")
                        
            elif gen_type_val == "corporativas":
                suffixes = ["123", "2023", "2024", "!", "@", "01", "admin", "user"]
                for word in words:
                    for suffix in suffixes:
                        generated.add(f"{word}{suffix}")
            
            # Guardar
            if generated:
                file_path = filedialog.asksaveasfilename(
                    title="Guardar diccionario",
                    defaultextension=".txt",
                    filetypes=[("Archivo de texto", "*.txt")]
                )
                
                if file_path:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        for entry in sorted(generated):
                            f.write(f"{entry}\n")
                    
                    messagebox.showinfo("Éxito", f"Diccionario generado!\n\nArchivo: {file_path}\nEntradas: {len(generated):,}")
        
        ctk.CTkButton(main_frame, text="🎯 Generar Diccionario", command=generate, 
                     height=40, font=ctk.CTkFont(size=14)).pack(pady=20)
    
    def crack_hash(self):
        """Cracke un hash usando diferentes métodos"""
        hash_value = self.hash_entry.get().strip()
        if not hash_value:
            messagebox.showerror("Error", "Ingresa un hash para crackear")
            return
        
        algorithm = self.hash_type_var.get()
        
        # Crear ventana de progreso
        crack_window = ctk.CTkToplevel(self.root)
        crack_window.title("🔨 Crackeando Hash")
        crack_window.geometry("500x300")
        crack_window.transient(self.root)
        crack_window.grab_set()
        
        main_frame = ctk.CTkFrame(crack_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="🔨 CRACKEANDO HASH", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        status_label = ctk.CTkLabel(main_frame, text=f"Hash: {hash_value[:20]}...")
        status_label.pack(pady=5)
        
        progress_bar = ctk.CTkProgressBar(main_frame)
        progress_bar.pack(fill="x", padx=10, pady=10)
        progress_bar.set(0)
        
        progress_label = ctk.CTkLabel(main_frame, text="Iniciando...")
        progress_label.pack(pady=5)
        
        def crack_worker():
            try:
                # Usar el hash cracker
                result = self.hash_cracker.crack_hash(
                    hash_value, 
                    algorithm, 
                    progress_callback=lambda current, total: crack_window.after(0, lambda: update_progress(current, total))
                )
                
                crack_window.after(0, lambda: show_result(result))
                
            except Exception as e:
                crack_window.after(0, lambda: messagebox.showerror("Error", f"Error crackeando hash: {e}"))
        
        def update_progress(current, total):
            if total > 0:
                progress = current / total
                progress_bar.set(progress)
                progress_label.configure(text=f"Progreso: {current:,}/{total:,} ({progress*100:.1f}%)")
        
        def show_result(result):
            if result['success']:
                messagebox.showinfo("🎉 Hash Crackeado!", 
                                   f"¡Contraseña encontrada!\n\nHash: {hash_value}\nContraseña: {result['password']}\nMétodo: {result.get('method', 'Desconocido')}")
            else:
                messagebox.showerror("❌ Hash no crackeado", 
                                    f"No se pudo crackear el hash.\n\nError: {result.get('error', 'Desconocido')}")
            crack_window.destroy()
        
        # Iniciar en hilo separado
        threading.Thread(target=crack_worker, daemon=True).start()
    
    def detect_encryption(self):
        """Detecta el tipo de encriptación de un archivo"""
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Selecciona un archivo primero")
            return
        
        try:
            # Usar el crypto engine para detectar
            detection_result = self.crypto_engine.detect_encryption_type(file_path)
            
            # Mostrar resultados
            result_window = ctk.CTkToplevel(self.root)
            result_window.title("🔍 Detección de Encriptación")
            result_window.geometry("500x400")
            
            result_text = ctk.CTkTextbox(result_window)
            result_text.pack(fill="both", expand=True, padx=20, pady=20)
            
            content = f"""🔍 ANÁLISIS DE ENCRIPTACIÓN

📄 Archivo: {file_path}
📏 Tamaño: {detection_result.get('file_size', 0):,} bytes

🎯 DETECCIÓN AUTOMÁTICA:
• Tipo detectado: {detection_result.get('detected_type', 'Desconocido')}
• Confianza: {detection_result.get('confidence', 0):.1f}%
• Entropía: {detection_result.get('entropy', 0):.4f}

📊 CARACTERÍSTICAS:
• Es binario: {'Sí' if detection_result.get('is_binary') else 'No'}
• Posiblemente encriptado: {'Sí' if detection_result.get('likely_encrypted') else 'No'}
• Posiblemente comprimido: {'Sí' if detection_result.get('likely_compressed') else 'No'}

💡 RECOMENDACIONES:
{chr(10).join(detection_result.get('recommendations', ['No hay recomendaciones disponibles']))}
"""
            
            result_text.insert("0.0", content)
            result_text.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error detectando encriptación: {e}")
    
    def entropy_analysis(self):
        """Realiza análisis de entropía detallado"""
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Selecciona un archivo primero")
            return
        
        try:
            import math
            from collections import Counter
            
            with open(file_path, 'rb') as f:
                data = f.read()
            
            if not data:
                messagebox.showerror("Error", "Archivo vacío")
                return
            
            # Calcular entropía
            byte_counts = Counter(data)
            entropy = 0
            for count in byte_counts.values():
                probability = count / len(data)
                entropy -= probability * math.log2(probability)
            
            # Análisis por bloques
            block_size = 1024
            block_entropies = []
            
            for i in range(0, len(data), block_size):
                block = data[i:i+block_size]
                if len(block) > 0:
                    block_counts = Counter(block)
                    block_entropy = 0
                    for count in block_counts.values():
                        prob = count / len(block)
                        block_entropy -= prob * math.log2(prob)
                    block_entropies.append(block_entropy)
            
            avg_block_entropy = sum(block_entropies) / len(block_entropies) if block_entropies else 0
            min_entropy = min(block_entropies) if block_entropies else 0
            max_entropy = max(block_entropies) if block_entropies else 0
            
            # Mostrar resultados
            result_window = ctk.CTkToplevel(self.root)
            result_window.title("📊 Análisis de Entropía")
            result_window.geometry("600x500")
            
            result_text = ctk.CTkTextbox(result_window)
            result_text.pack(fill="both", expand=True, padx=20, pady=20)
            
            content = f"""📊 ANÁLISIS DETALLADO DE ENTROPÍA

📄 Archivo: {file_path}
📏 Tamaño: {len(data):,} bytes

🔢 ENTROPÍA GLOBAL:
• Entropía total: {entropy:.6f} bits/byte
• Entropía máxima: 8.000000 bits/byte
• Porcentaje de aleatoriedad: {(entropy/8)*100:.2f}%

📊 ANÁLISIS POR BLOQUES ({block_size} bytes):
• Bloques analizados: {len(block_entropies)}
• Entropía promedio: {avg_block_entropy:.6f}
• Entropía mínima: {min_entropy:.6f}
• Entropía máxima: {max_entropy:.6f}

🎯 INTERPRETACIÓN:
"""
            
            if entropy < 3.0:
                content += "• Entropía muy baja - Datos altamente estructurados o repetitivos\n"
            elif entropy < 5.0:
                content += "• Entropía baja - Texto plano o datos poco aleatorios\n"
            elif entropy < 6.5:
                content += "• Entropía media - Datos comprimidos o parcialmente aleatorios\n"
            elif entropy < 7.5:
                content += "• Entropía alta - Datos comprimidos eficientemente\n"
            else:
                content += "• Entropía muy alta - Datos encriptados o muy aleatorios\n"
            
            # Distribución de bytes
            unique_bytes = len(byte_counts)
            content += f"\n📈 DISTRIBUCIÓN DE BYTES:\n"
            content += f"• Bytes únicos: {unique_bytes}/256 ({(unique_bytes/256)*100:.1f}%)\n"
            
            most_common = byte_counts.most_common(5)
            content += f"• Bytes más frecuentes:\n"
            for byte_val, count in most_common:
                percentage = (count / len(data)) * 100
                content += f"  - 0x{byte_val:02X}: {count:,} veces ({percentage:.2f}%)\n"
            
            result_text.insert("0.0", content)
            result_text.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis de entropía: {e}")
    
    def forensic_analysis(self):
        """Realiza análisis forense básico del archivo"""
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Selecciona un archivo primero")
            return
        
        try:
            import os
            import hashlib
            import time
            from pathlib import Path
            
            file_path_obj = Path(file_path)
            
            # Información básica del archivo
            stat_info = file_path_obj.stat()
            
            # Calcular hashes
            with open(file_path, 'rb') as f:
                data = f.read()
            
            md5_hash = hashlib.md5(data).hexdigest()
            sha1_hash = hashlib.sha1(data).hexdigest()
            sha256_hash = hashlib.sha256(data).hexdigest()
            
            # Análisis de contenido
            null_bytes = data.count(b'\x00')
            printable_chars = sum(1 for b in data if 32 <= b <= 126)
            
            # Magic bytes (firmas de archivo)
            magic_signatures = {
                b'\x50\x4B\x03\x04': 'ZIP Archive',
                b'\x50\x4B\x05\x06': 'ZIP Archive (empty)',
                b'\x50\x4B\x07\x08': 'ZIP Archive (spanned)',
                b'\x89\x50\x4E\x47': 'PNG Image',
                b'\xFF\xD8\xFF': 'JPEG Image',
                b'\x47\x49\x46\x38': 'GIF Image',
                b'\x25\x50\x44\x46': 'PDF Document',
                b'\xD0\xCF\x11\xE0': 'Microsoft Office Document',
                b'\x7F\x45\x4C\x46': 'Linux Executable (ELF)',
                b'\x4D\x5A': 'Windows Executable (PE)',
                b'-----BEGIN': 'PEM Certificate/Key'
            }
            
            detected_type = "Desconocido"
            for signature, file_type in magic_signatures.items():
                if data.startswith(signature):
                    detected_type = file_type
                    break
            
            # Mostrar resultados
            result_window = ctk.CTkToplevel(self.root)
            result_window.title("🕵️ Análisis Forense")
            result_window.geometry("700x600")
            
            result_text = ctk.CTkTextbox(result_window)
            result_text.pack(fill="both", expand=True, padx=20, pady=20)
            
            content = f"""🕵️ ANÁLISIS FORENSE DETALLADO

📄 INFORMACIÓN DEL ARCHIVO:
• Nombre: {file_path_obj.name}
• Ruta completa: {file_path}
• Tamaño: {stat_info.st_size:,} bytes
• Tipo detectado: {detected_type}

⏰ TIMESTAMPS:
• Creado: {time.ctime(stat_info.st_ctime)}
• Modificado: {time.ctime(stat_info.st_mtime)}
• Accedido: {time.ctime(stat_info.st_atime)}

🔐 HASHES CRIPTOGRÁFICOS:
• MD5: {md5_hash}
• SHA-1: {sha1_hash}
• SHA-256: {sha256_hash}

📊 ANÁLISIS DE CONTENIDO:
• Bytes nulos: {null_bytes:,} ({(null_bytes/len(data)*100):.2f}%)
• Caracteres imprimibles: {printable_chars:,} ({(printable_chars/len(data)*100):.2f}%)
• Posiblemente texto: {'Sí' if printable_chars/len(data) > 0.8 else 'No'}
• Posiblemente binario: {'Sí' if null_bytes > len(data)*0.1 else 'No'}

🔍 PRIMEROS 256 BYTES (HEX):
{data[:256].hex().upper()}

🔍 PRIMEROS 256 BYTES (ASCII):
{repr(data[:256].decode('utf-8', errors='replace'))}

💡 RECOMENDACIONES FORENSES:
"""
            
            if detected_type != "Desconocido":
                content += f"• Archivo identificado como {detected_type}\n"
            
            if null_bytes > len(data) * 0.5:
                content += "• Alto contenido de bytes nulos - posible archivo corrupto o con padding\n"
            
            if printable_chars / len(data) > 0.9:
                content += "• Principalmente texto - analizar con herramientas de texto\n"
            elif printable_chars / len(data) < 0.1:
                content += "• Principalmente binario - usar herramientas de análisis binario\n"
            
            content += "• Verificar hashes contra bases de datos de malware\n"
            content += "• Analizar timestamps para línea temporal\n"
            
            result_text.insert("0.0", content)
            result_text.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis forense: {e}")
    
    # Funciones de herramientas implementadas
    def generate_keys(self):
        """Generador de claves criptográficas"""
        # Crear ventana de generación de claves
        key_window = ctk.CTkToplevel(self.root)
        key_window.title("🔐 Generador de Claves")
        key_window.geometry("600x500")
        key_window.transient(self.root)
        key_window.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(key_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="🔐 GENERADOR DE CLAVES CRIPTOGRÁFICAS", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Tipo de clave
        type_frame = ctk.CTkFrame(main_frame)
        type_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(type_frame, text="Tipo de Clave:").pack(anchor="w", padx=10, pady=5)
        key_type_var = ctk.StringVar(value="RSA")
        key_type_menu = ctk.CTkOptionMenu(type_frame, values=["RSA", "DSA", "Ed25519", "AES", "ChaCha20"], 
                                         variable=key_type_var)
        key_type_menu.pack(fill="x", padx=10, pady=5)
        
        # Tamaño de clave
        size_frame = ctk.CTkFrame(main_frame)
        size_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(size_frame, text="Tamaño (bits):").pack(anchor="w", padx=10, pady=5)
        key_size_var = ctk.StringVar(value="2048")
        key_size_menu = ctk.CTkOptionMenu(size_frame, values=["1024", "2048", "3072", "4096"], 
                                         variable=key_size_var)
        key_size_menu.pack(fill="x", padx=10, pady=5)
        
        # Protección con contraseña
        protect_frame = ctk.CTkFrame(main_frame)
        protect_frame.pack(fill="x", padx=10, pady=10)
        
        protect_var = ctk.BooleanVar()
        ctk.CTkCheckBox(protect_frame, text="Proteger con contraseña", 
                       variable=protect_var).pack(anchor="w", padx=10, pady=5)
        
        password_entry = ctk.CTkEntry(protect_frame, placeholder_text="Contraseña (opcional)", show="*")
        password_entry.pack(fill="x", padx=10, pady=5)
        
        # Botón generar
        def generate():
            try:
                from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ed25519
                from cryptography.hazmat.primitives import serialization
                import os
                
                key_type = key_type_var.get()
                key_size = int(key_size_var.get())
                password = password_entry.get() if protect_var.get() else None
                
                if key_type == "RSA":
                    private_key = rsa.generate_private_key(
                        public_exponent=65537,
                        key_size=key_size
                    )
                elif key_type == "DSA":
                    private_key = dsa.generate_private_key(key_size=key_size)
                elif key_type == "Ed25519":
                    private_key = ed25519.Ed25519PrivateKey.generate()
                else:
                    messagebox.showinfo("Info", f"Generación de {key_type} no implementada aún")
                    return
                
                # Serializar clave privada
                encryption = serialization.BestAvailableEncryption(password.encode()) if password else serialization.NoEncryption()
                
                private_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=encryption
                )
                
                # Clave pública
                public_key = private_key.public_key()
                public_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                
                # Mostrar resultado
                result_window = ctk.CTkToplevel(key_window)
                result_window.title("🔑 Claves Generadas")
                result_window.geometry("700x600")
                
                result_text = ctk.CTkTextbox(result_window)
                result_text.pack(fill="both", expand=True, padx=20, pady=20)
                
                result_content = f"""🔐 CLAVES GENERADAS EXITOSAMENTE

🔑 Tipo: {key_type}
📏 Tamaño: {key_size} bits
🔒 Protegida: {'Sí' if password else 'No'}

==================== CLAVE PRIVADA ====================
{private_pem.decode()}

==================== CLAVE PÚBLICA ====================
{public_pem.decode()}

⚠️ IMPORTANTE: Guarda estas claves en un lugar seguro.
La clave privada debe mantenerse confidencial."""
                
                result_text.insert("0.0", result_content)
                result_text.configure(state="disabled")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error generando claves: {e}")
        
        ctk.CTkButton(main_frame, text="🔑 Generar Claves", command=generate, 
                     height=40, font=ctk.CTkFont(size=14)).pack(pady=20)
    
    def convert_formats(self):
        """Conversor de formatos de certificados"""
        # Crear ventana de conversión
        conv_window = ctk.CTkToplevel(self.root)
        conv_window.title("🔄 Conversor de Formatos")
        conv_window.geometry("600x450")
        conv_window.transient(self.root)
        conv_window.grab_set()
        
        main_frame = ctk.CTkFrame(conv_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="🔄 CONVERSOR DE FORMATOS DE CERTIFICADOS", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Archivo de entrada
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(input_frame, text="Archivo de entrada:").pack(anchor="w", padx=10, pady=5)
        input_entry = ctk.CTkEntry(input_frame, placeholder_text="Selecciona archivo...")
        input_entry.pack(fill="x", padx=10, pady=5)
        
        def browse_input():
            file_path = filedialog.askopenfilename(
                title="Seleccionar archivo",
                filetypes=[
                    ("Certificados", "*.pem *.der *.p12 *.pfx *.crt *.cer"),
                    ("Todos los archivos", "*.*")
                ]
            )
            if file_path:
                input_entry.delete(0, "end")
                input_entry.insert(0, file_path)
        
        ctk.CTkButton(input_frame, text="📂 Buscar", command=browse_input).pack(pady=5)
        
        # Formato de salida
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(output_frame, text="Formato de salida:").pack(anchor="w", padx=10, pady=5)
        output_format = ctk.StringVar(value="PEM")
        format_menu = ctk.CTkOptionMenu(output_frame, values=["PEM", "DER", "PKCS#12"], 
                                       variable=output_format)
        format_menu.pack(fill="x", padx=10, pady=5)
        
        # Contraseña si es necesaria
        password_frame = ctk.CTkFrame(main_frame)
        password_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(password_frame, text="Contraseña (si el archivo está protegido):").pack(anchor="w", padx=10, pady=5)
        password_entry = ctk.CTkEntry(password_frame, placeholder_text="Contraseña...", show="*")
        password_entry.pack(fill="x", padx=10, pady=5)
        
        # Convertir
        def convert():
            input_file = input_entry.get()
            if not input_file:
                messagebox.showerror("Error", "Selecciona un archivo de entrada")
                return
            
            output_dir = filedialog.askdirectory(title="Seleccionar directorio de salida")
            if not output_dir:
                return
            
            try:
                from pathlib import Path
                
                input_path = Path(input_file)
                output_ext = ".pem" if output_format.get() == "PEM" else ".der"
                output_file = Path(output_dir) / f"{input_path.stem}_converted{output_ext}"
                
                # Usar el CertificateHandler existente
                result = self.cert_handler.convert_certificate_format(
                    input_file, str(output_file), output_format.get().lower(), 
                    password_entry.get() or None
                )
                
                if result['success']:
                    messagebox.showinfo("Éxito", f"Archivo convertido exitosamente:\n{result['output_path']}")
                else:
                    messagebox.showerror("Error", f"Error en conversión: {result['error']}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        
        ctk.CTkButton(main_frame, text="🔄 Convertir", command=convert, 
                     height=40, font=ctk.CTkFont(size=14)).pack(pady=20)
    
    def hex_editor(self):
        """Editor hexadecimal simple"""
        # Crear ventana del editor hex
        hex_window = ctk.CTkToplevel(self.root)
        hex_window.title("📝 Editor Hexadecimal")
        hex_window.geometry("800x600")
        hex_window.transient(self.root)
        hex_window.grab_set()
        
        main_frame = ctk.CTkFrame(hex_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="📝 EDITOR HEXADECIMAL", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Controles
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        def load_file():
            file_path = filedialog.askopenfilename(title="Cargar archivo")
            if file_path:
                try:
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    
                    # Convertir a hex con formato
                    hex_lines = []
                    for i in range(0, len(data), 16):
                        chunk = data[i:i+16]
                        hex_part = ' '.join(f'{b:02x}' for b in chunk)
                        ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
                        hex_lines.append(f'{i:08x}: {hex_part:<48} {ascii_part}')
                    
                    hex_text.configure(state="normal")
                    hex_text.delete("0.0", "end")
                    hex_text.insert("0.0", '\n'.join(hex_lines))
                    hex_text.configure(state="disabled")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error cargando archivo: {e}")
        
        ctk.CTkButton(controls_frame, text="📂 Cargar Archivo", command=load_file).pack(side="left", padx=5)
        
        def save_file():
            # Implementar guardado desde hex
            messagebox.showinfo("Info", "Función de guardado en desarrollo")
        
        ctk.CTkButton(controls_frame, text="💾 Guardar", command=save_file).pack(side="left", padx=5)
        
        # Área de texto hex
        hex_text = ctk.CTkTextbox(main_frame, font=ctk.CTkFont(family="Courier", size=12))
        hex_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        hex_text.insert("0.0", "Carga un archivo para ver su contenido en hexadecimal...")
    
    def hash_calculator(self):
        """Calculadora de hashes"""
        # Crear ventana de calculadora
        hash_window = ctk.CTkToplevel(self.root)
        hash_window.title("🧮 Calculadora Hash")
        hash_window.geometry("600x500")
        hash_window.transient(self.root)
        hash_window.grab_set()
        
        main_frame = ctk.CTkFrame(hash_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="🧮 CALCULADORA DE HASHES", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Entrada de texto
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(input_frame, text="Texto a hashear:").pack(anchor="w", padx=10, pady=5)
        text_input = ctk.CTkTextbox(input_frame, height=100)
        text_input.pack(fill="x", padx=10, pady=5)
        
        # O cargar archivo
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", padx=10, pady=10)
        
        file_path_var = ctk.StringVar()
        ctk.CTkLabel(file_frame, text="O seleccionar archivo:").pack(anchor="w", padx=10, pady=5)
        
        file_entry = ctk.CTkEntry(file_frame, textvariable=file_path_var)
        file_entry.pack(fill="x", padx=10, pady=5)
        
        def browse_file():
            file_path = filedialog.askopenfilename(title="Seleccionar archivo")
            if file_path:
                file_path_var.set(file_path)
        
        ctk.CTkButton(file_frame, text="📂 Buscar", command=browse_file).pack(pady=5)
        
        # Algoritmos
        algo_frame = ctk.CTkFrame(main_frame)
        algo_frame.pack(fill="x", padx=10, pady=10)
        
        algorithms = ["MD5", "SHA1", "SHA256", "SHA512", "SHA3-256", "BLAKE2b"]
        algo_vars = {}
        
        ctk.CTkLabel(algo_frame, text="Algoritmos:").pack(anchor="w", padx=10, pady=5)
        
        for algo in algorithms:
            var = ctk.BooleanVar(value=True if algo in ["MD5", "SHA256"] else False)
            algo_vars[algo] = var
            ctk.CTkCheckBox(algo_frame, text=algo, variable=var).pack(anchor="w", padx=20, pady=2)
        
        # Calcular
        def calculate():
            import hashlib
            
            # Obtener datos
            text_data = text_input.get("0.0", "end").strip()
            file_path = file_path_var.get()
            
            if text_data and file_path:
                messagebox.showwarning("Advertencia", "Usa solo texto O archivo, no ambos")
                return
            
            if not text_data and not file_path:
                messagebox.showerror("Error", "Ingresa texto o selecciona un archivo")
                return
            
            try:
                if text_data:
                    data = text_data.encode('utf-8')
                else:
                    with open(file_path, 'rb') as f:
                        data = f.read()
                
                # Calcular hashes seleccionados
                results = []
                for algo, var in algo_vars.items():
                    if var.get():
                        if algo == "MD5":
                            hash_val = hashlib.md5(data).hexdigest()
                        elif algo == "SHA1":
                            hash_val = hashlib.sha1(data).hexdigest()
                        elif algo == "SHA256":
                            hash_val = hashlib.sha256(data).hexdigest()
                        elif algo == "SHA512":
                            hash_val = hashlib.sha512(data).hexdigest()
                        elif algo == "SHA3-256":
                            hash_val = hashlib.sha3_256(data).hexdigest()
                        elif algo == "BLAKE2b":
                            hash_val = hashlib.blake2b(data).hexdigest()
                        
                        results.append(f"{algo}: {hash_val}")
                
                # Mostrar resultados
                result_window = ctk.CTkToplevel(hash_window)
                result_window.title("📊 Resultados Hash")
                result_window.geometry("700x400")
                
                result_text = ctk.CTkTextbox(result_window)
                result_text.pack(fill="both", expand=True, padx=20, pady=20)
                
                source = f"Archivo: {file_path}" if file_path else f"Texto: {text_data[:50]}..."
                result_content = f"🧮 HASHES CALCULADOS\n\n📄 Fuente: {source}\n📏 Tamaño: {len(data)} bytes\n\n" + "\n\n".join(results)
                
                result_text.insert("0.0", result_content)
                result_text.configure(state="disabled")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error calculando hashes: {e}")
        
        ctk.CTkButton(main_frame, text="🧮 Calcular Hashes", command=calculate, 
                     height=40, font=ctk.CTkFont(size=14)).pack(pady=20)
    
    def key_finder(self):
        """Buscador avanzado de claves en archivos"""
        messagebox.showinfo("🔍 Buscador de Claves", "Herramienta en desarrollo...\n\nEsta función escaneará directorios buscando:\n• Certificados X.509\n• Claves SSH\n• Claves PGP\n• Archivos de configuración con credenciales")
    
    def bit_analysis(self):
        """Análisis de bits y entropía"""
        messagebox.showinfo("📊 Análisis de Bits", "Herramienta en desarrollo...\n\nEsta función analizará:\n• Entropía de archivos\n• Distribución de bytes\n• Patrones de aleatoriedad\n• Detección de encriptación")
    
    def wordlist_generator(self):
        """Generador de wordlists personalizadas"""
        messagebox.showinfo("🎯 Generador de Wordlists", "Herramienta en desarrollo...\n\nEsta función generará:\n• Wordlists personalizadas\n• Variaciones de contraseñas\n• Combinaciones basadas en patrones\n• Diccionarios específicos por contexto")
    
    def security_test(self):
        """Test de seguridad del sistema"""
        messagebox.showinfo("🛡️ Test de Seguridad", "Herramienta en desarrollo...\n\nEsta función verificará:\n• Configuración SSL/TLS\n• Certificados instalados\n• Vulnerabilidades conocidas\n• Fortaleza de claves")
    def change_theme(self, theme):
        """Cambia el tema de la aplicación"""
        try:
            if theme in ["blue", "green", "dark-blue"]:
                ctk.set_default_color_theme(theme)
                messagebox.showinfo("Tema cambiado", f"Tema cambiado a: {theme}\n\nReinicia la aplicación para aplicar completamente el cambio.")
            else:
                messagebox.showerror("Error", "Tema no válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error cambiando tema: {e}")
    
    def browse_dict_path(self):
        """Selecciona una nueva ruta para los diccionarios"""
        folder_path = filedialog.askdirectory(
            title="Seleccionar carpeta de diccionarios",
            initialdir="./data"
        )
        
        if folder_path:
            self.dict_path_entry.delete(0, "end")
            self.dict_path_entry.insert(0, folder_path)
            messagebox.showinfo("Éxito", f"Ruta de diccionarios actualizada:\n{folder_path}")
    
    def save_settings(self):
        """Guarda la configuración actual"""
        try:
            import json
            
            settings = {
                "max_threads": self.max_threads_slider.get(),
                "dict_path": self.dict_path_entry.get(),
                "timeout": self.timeout_slider.get(),
                "theme": "dark-blue",  # tema actual
                "auto_save": True,
                "log_level": "INFO"
            }
            
            with open("config.json", 'w') as f:
                json.dump(settings, f, indent=4)
            
            messagebox.showinfo("✅ Configuración guardada", 
                               "La configuración se ha guardado correctamente en config.json")
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando configuración: {e}")
    
    def restore_defaults(self):
        """Restaura la configuración por defecto"""
        if messagebox.askyesno("Confirmar", "¿Restaurar configuración por defecto?"):
            try:
                # Restaurar valores por defecto
                self.max_threads_slider.set(4)
                self.dict_path_entry.delete(0, "end")
                self.dict_path_entry.insert(0, "./data")
                self.timeout_slider.set(30)
                
                # Guardar configuración por defecto
                self.save_settings()
                
                messagebox.showinfo("✅ Restaurado", "Configuración restaurada a valores por defecto")
            except Exception as e:
                messagebox.showerror("Error", f"Error restaurando configuración: {e}")
    
    def view_logs(self):
        """Muestra los logs de la aplicación"""
        try:
            import os
            from pathlib import Path
            
            log_dir = Path("./logs")
            if not log_dir.exists():
                messagebox.showwarning("Sin logs", "No se encontraron archivos de log")
                return
            
            log_files = list(log_dir.glob("*.log"))
            if not log_files:
                messagebox.showwarning("Sin logs", "No se encontraron archivos de log")
                return
            
            # Crear ventana del visor de logs
            log_window = ctk.CTkToplevel(self.root)
            log_window.title("📋 Visor de Logs")
            log_window.geometry("800x600")
            
            main_frame = ctk.CTkFrame(log_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(main_frame, text="📋 VISOR DE LOGS", 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
            
            # Selector de archivo de log
            log_frame = ctk.CTkFrame(main_frame)
            log_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(log_frame, text="Archivo de log:").pack(side="left", padx=10)
            
            log_var = ctk.StringVar(value=str(log_files[0]))
            log_combo = ctk.CTkComboBox(log_frame, variable=log_var, 
                                       values=[str(f) for f in log_files])
            log_combo.pack(side="left", padx=10, expand=True, fill="x")
            
            # Área de texto para mostrar logs
            log_text = ctk.CTkTextbox(main_frame)
            log_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            def load_log():
                try:
                    with open(log_var.get(), 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    log_text.delete("0.0", "end")
                    log_text.insert("0.0", content)
                    
                except Exception as e:
                    log_text.delete("0.0", "end")
                    log_text.insert("0.0", f"Error cargando log: {e}")
            
            # Botón para recargar
            ctk.CTkButton(log_frame, text="🔄 Recargar", command=load_log).pack(side="right", padx=10)
            
            # Cargar log inicial
            load_log()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error abriendo visor de logs: {e}")
    
    def update_status(self, message):
        """Actualiza la barra de estado"""
        self.status_label.configure(text=message)
    
    def browse_analysis_file(self):
        """Selecciona un archivo para análisis"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo para análisis",
            filetypes=[
                ("Todos los archivos", "*.*"),
                ("Certificados", "*.pem;*.crt;*.cer;*.der;*.p12;*.pfx"),
                ("Archivos encriptados", "*.enc;*.aes;*.gpg"),
                ("Archivos comprimidos", "*.zip;*.rar;*.7z"),
                ("Documentos", "*.pdf;*.docx;*.xlsx")
            ]
        )
        
        if file_path:
            self.analysis_file_entry.delete(0, "end")
            self.analysis_file_entry.insert(0, file_path)
    
    def detect_encryption_analysis(self):
        """Detecta el tipo de encriptación usando el archivo de análisis"""
        file_path = self.analysis_file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Selecciona un archivo primero")
            return
        
        try:
            # Usar el crypto engine para detectar
            detection_result = self.crypto_engine.detect_encryption_type(file_path)
            
            # Mostrar resultados en el área de texto
            content = f"""🔍 DETECCIÓN DE ENCRIPTACIÓN

📄 Archivo: {file_path}
📏 Tamaño: {detection_result.get('file_size', 0):,} bytes

🎯 DETECCIÓN AUTOMÁTICA:
• Tipo detectado: {detection_result.get('detected_type', 'Desconocido')}
• Confianza: {detection_result.get('confidence', 0):.1f}%
• Entropía: {detection_result.get('entropy', 0):.4f}

📊 CARACTERÍSTICAS:
• Es binario: {'Sí' if detection_result.get('is_binary') else 'No'}
• Posiblemente encriptado: {'Sí' if detection_result.get('likely_encrypted') else 'No'}
• Posiblemente comprimido: {'Sí' if detection_result.get('likely_compressed') else 'No'}

💡 RECOMENDACIONES:
{chr(10).join(detection_result.get('recommendations', ['No hay recomendaciones disponibles']))}
"""
            
            self.analysis_text.delete("0.0", "end")
            self.analysis_text.insert("0.0", content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error detectando encriptación: {e}")
    
    def entropy_analysis_analysis(self):
        """Realiza análisis de entropía usando el archivo de análisis"""
        file_path = self.analysis_file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Selecciona un archivo primero")
            return
        
        try:
            import math
            from collections import Counter
            
            with open(file_path, 'rb') as f:
                data = f.read()
            
            if not data:
                messagebox.showerror("Error", "Archivo vacío")
                return
            
            # Calcular entropía
            byte_counts = Counter(data)
            entropy = 0
            for count in byte_counts.values():
                probability = count / len(data)
                entropy -= probability * math.log2(probability)
            
            # Análisis por bloques
            block_size = 1024
            block_entropies = []
            
            for i in range(0, len(data), block_size):
                block = data[i:i+block_size]
                if len(block) > 0:
                    block_counts = Counter(block)
                    block_entropy = 0
                    for count in block_counts.values():
                        prob = count / len(block)
                        block_entropy -= prob * math.log2(prob)
                    block_entropies.append(block_entropy)
            
            avg_block_entropy = sum(block_entropies) / len(block_entropies) if block_entropies else 0
            min_entropy = min(block_entropies) if block_entropies else 0
            max_entropy = max(block_entropies) if block_entropies else 0
            
            # Mostrar resultados
            content = f"""📊 ANÁLISIS DETALLADO DE ENTROPÍA

📄 Archivo: {file_path}
📏 Tamaño: {len(data):,} bytes

🔢 ENTROPÍA GLOBAL:
• Entropía total: {entropy:.6f} bits/byte
• Entropía máxima: 8.000000 bits/byte
• Porcentaje de aleatoriedad: {(entropy/8)*100:.2f}%

📊 ANÁLISIS POR BLOQUES ({block_size} bytes):
• Bloques analizados: {len(block_entropies)}
• Entropía promedio: {avg_block_entropy:.6f}
• Entropía mínima: {min_entropy:.6f}
• Entropía máxima: {max_entropy:.6f}

🎯 INTERPRETACIÓN:
"""
            
            if entropy < 3.0:
                content += "• Entropía muy baja - Datos altamente estructurados o repetitivos\n"
            elif entropy < 5.0:
                content += "• Entropía baja - Texto plano o datos poco aleatorios\n"
            elif entropy < 6.5:
                content += "• Entropía media - Datos comprimidos o parcialmente aleatorios\n"
            elif entropy < 7.5:
                content += "• Entropía alta - Datos comprimidos eficientemente\n"
            else:
                content += "• Entropía muy alta - Datos encriptados o muy aleatorios\n"
            
            # Distribución de bytes
            unique_bytes = len(byte_counts)
            content += f"\n📈 DISTRIBUCIÓN DE BYTES:\n"
            content += f"• Bytes únicos: {unique_bytes}/256 ({(unique_bytes/256)*100:.1f}%)\n"
            
            most_common = byte_counts.most_common(5)
            content += f"• Bytes más frecuentes:\n"
            for byte_val, count in most_common:
                percentage = (count / len(data)) * 100
                content += f"  - 0x{byte_val:02X}: {count:,} veces ({percentage:.2f}%)\n"
            
            self.analysis_text.delete("0.0", "end")
            self.analysis_text.insert("0.0", content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis de entropía: {e}")
    
    def forensic_analysis_analysis(self):
        """Realiza análisis forense usando el archivo de análisis"""
        file_path = self.analysis_file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Selecciona un archivo primero")
            return
        
        try:
            import os
            import hashlib
            import time
            from pathlib import Path
            
            file_path_obj = Path(file_path)
            
            # Información básica del archivo
            stat_info = file_path_obj.stat()
            
            # Calcular hashes
            with open(file_path, 'rb') as f:
                data = f.read()
            
            md5_hash = hashlib.md5(data).hexdigest()
            sha1_hash = hashlib.sha1(data).hexdigest()
            sha256_hash = hashlib.sha256(data).hexdigest()
            
            # Análisis de contenido
            null_bytes = data.count(b'\x00')
            printable_chars = sum(1 for b in data if 32 <= b <= 126)
            
            # Magic bytes (firmas de archivo)
            magic_signatures = {
                b'\x50\x4B\x03\x04': 'ZIP Archive',
                b'\x50\x4B\x05\x06': 'ZIP Archive (empty)',
                b'\x50\x4B\x07\x08': 'ZIP Archive (spanned)',
                b'\x89\x50\x4E\x47': 'PNG Image',
                b'\xFF\xD8\xFF': 'JPEG Image',
                b'\x47\x49\x46\x38': 'GIF Image',
                b'\x25\x50\x44\x46': 'PDF Document',
                b'\xD0\xCF\x11\xE0': 'Microsoft Office Document',
                b'\x7F\x45\x4C\x46': 'Linux Executable (ELF)',
                b'\x4D\x5A': 'Windows Executable (PE)',
                b'-----BEGIN': 'PEM Certificate/Key',
                b'\x30\x82': 'DER Certificate/Key'
            }
            
            detected_type = "Desconocido"
            for signature, file_type in magic_signatures.items():
                if data.startswith(signature):
                    detected_type = file_type
                    break
            
            # Mostrar resultados
            content = f"""🕵️ ANÁLISIS FORENSE DETALLADO

📄 INFORMACIÓN DEL ARCHIVO:
• Nombre: {file_path_obj.name}
• Ruta completa: {file_path}
• Tamaño: {stat_info.st_size:,} bytes
• Tipo detectado: {detected_type}

⏰ TIMESTAMPS:
• Creado: {time.ctime(stat_info.st_ctime)}
• Modificado: {time.ctime(stat_info.st_mtime)}
• Accedido: {time.ctime(stat_info.st_atime)}

🔐 HASHES CRIPTOGRÁFICOS:
• MD5: {md5_hash}
• SHA-1: {sha1_hash}
• SHA-256: {sha256_hash}

📊 ANÁLISIS DE CONTENIDO:
• Bytes nulos: {null_bytes:,} ({(null_bytes/len(data)*100):.2f}%)
• Caracteres imprimibles: {printable_chars:,} ({(printable_chars/len(data)*100):.2f}%)
• Posiblemente texto: {'Sí' if printable_chars/len(data) > 0.8 else 'No'}
• Posiblemente binario: {'Sí' if null_bytes > len(data)*0.1 else 'No'}

🔍 PRIMEROS 256 BYTES (HEX):
{data[:256].hex().upper()}

🔍 PRIMEROS 256 BYTES (ASCII):
{repr(data[:256].decode('utf-8', errors='replace'))}

💡 RECOMENDACIONES FORENSES:
"""
            
            if detected_type != "Desconocido":
                content += f"• Archivo identificado como {detected_type}\n"
            
            if null_bytes > len(data) * 0.5:
                content += "• Alto contenido de bytes nulos - posible archivo corrupto o con padding\n"
            
            if printable_chars / len(data) > 0.9:
                content += "• Principalmente texto - analizar con herramientas de texto\n"
            elif printable_chars / len(data) < 0.1:
                content += "• Principalmente binario - usar herramientas de análisis binario\n"
            
            content += "• Verificar hashes contra bases de datos de malware\n"
            content += "• Analizar timestamps para línea temporal\n"
            
            if "Certificate" in detected_type or "Key" in detected_type:
                content += "• CERTIFICADO/CLAVE DETECTADA - Usar extractor de claves privadas\n"
            
            self.analysis_text.delete("0.0", "end")
            self.analysis_text.insert("0.0", content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis forense: {e}")
        
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
