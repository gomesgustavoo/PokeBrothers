import customtkinter as ctk
from tkinter import messagebox

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_login_success, show_register_callback):
        super().__init__(master, corner_radius=20)
        self.on_login_success = on_login_success
        self.show_register = show_register_callback
        
        # Variáveis de controle
        self.var_email = ctk.StringVar()
        self.var_pwd = ctk.StringVar()
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Frame principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Título
        ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=18)) \
            .grid(row=0, column=0, columnspan=2, pady=(20, 10))
        
        # Campos de entrada
        ctk.CTkLabel(self, text="Email:").grid(row=1, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self, width=200, textvariable=self.var_email) \
            .grid(row=1, column=1, pady=5)
            
        ctk.CTkLabel(self, text="Senha:").grid(row=2, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self, width=200, show="*", textvariable=self.var_pwd) \
            .grid(row=2, column=1, pady=5)
        
        # Botão de login
        ctk.CTkButton(
            self, text="Entrar", width=250, command=self._on_login
        ).grid(row=3, column=0, columnspan=2, pady=(15, 5))
        
        # Rodapé com link para registro
        rodape = ctk.CTkFrame(self, fg_color="transparent")
        rodape.grid(row=4, column=0, columnspan=2, pady=(10, 20))
        
        ctk.CTkLabel(rodape, text="Não registrado?").grid(row=0, column=0)
        ctk.CTkButton(
            rodape, text="Registrar", width=80, command=self.show_register
        ).grid(row=0, column=1, padx=5)
        
        ctk.CTkLabel(self, text="Esqueceu sua senha?").grid(row=5, column=0, columnspan=2, pady=(5,10))
    
    def _on_login(self):
        """Lida com a tentativa de login"""
        email = self.var_email.get().strip()
        password = self.var_pwd.get().strip()
        
        if not email or not password:
            messagebox.showerror("Login", "Por favor, preencha todos os campos")
            return
        
        # Chama a função de callback passada pelo main
        self.on_login_success(email, password)
    
    def clear_fields(self):
        """Limpa os campos de entrada"""
        self.var_email.set("")
        self.var_pwd.set("")