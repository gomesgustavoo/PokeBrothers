import customtkinter as ctk
from tkinter import messagebox
import re

class RegisterPage(ctk.CTkFrame):
    def __init__(self, master, on_register_callback, show_login_callback):
        super().__init__(master, corner_radius=20)
        self.on_register = on_register_callback
        self.show_login = show_login_callback
        
        # Variáveis de controle
        self.var_name = ctk.StringVar()
        self.var_email = ctk.StringVar()
        self.var_pwd = ctk.StringVar()
        self.var_pwd_confirm = ctk.StringVar()
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Frame principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Título
        ctk.CTkLabel(
            self, text="Registro de Colecionador",
            font=ctk.CTkFont(size=18)
        ).grid(row=0, column=0, columnspan=2, pady=(20,10))
        
        # Campos de entrada
        ctk.CTkLabel(self, text="Nome:").grid(row=1, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self, width=200, textvariable=self.var_name) \
            .grid(row=1, column=1, pady=5)
            
        ctk.CTkLabel(self, text="Email:").grid(row=2, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self, width=200, textvariable=self.var_email) \
            .grid(row=2, column=1, pady=5)
            
        ctk.CTkLabel(self, text="Senha:").grid(row=3, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self, width=200, show="*", textvariable=self.var_pwd) \
            .grid(row=3, column=1, pady=5)
            
        ctk.CTkLabel(self, text="Confirme Senha:").grid(row=4, column=0, sticky="e", padx=10)
        ctk.CTkEntry(self, width=200, show="*", textvariable=self.var_pwd_confirm) \
            .grid(row=4, column=1, pady=5)
        
        # Botão de registro
        ctk.CTkButton(
            self, text="Registre-se", width=250, command=self._on_register
        ).grid(row=5, column=0, columnspan=2, pady=(15, 5))
        
        # Rodapé com link para login
        rodape = ctk.CTkFrame(self, fg_color="transparent")
        rodape.grid(row=6, column=0, columnspan=2, pady=(10,20))
        
        ctk.CTkLabel(rodape, text="Já possui conta?").grid(row=0, column=0)
        ctk.CTkButton(
            rodape, text="Login", width=80, command=self.show_login
        ).grid(row=0, column=1, padx=5)
    def _on_register(self):
        """Lida com a tentativa de registro"""

        name = self.var_name.get().strip()
        email = self.var_email.get().strip()
        password = self.var_pwd.get().strip()
        password_confirm = self.var_pwd_confirm.get().strip()
        
        # Validação de email usando regex
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messagebox.showwarning("Cadastro", "Por favor, insira um email válido.")
            return

        # Validação de tamanho da senha
        if len(password) < 6:
            messagebox.showwarning("Cadastro", "A senha deve ter pelo menos 6 caracteres.")
            return

        if password != password_confirm:
            messagebox.showwarning("Cadastro", "As senhas não coincidem.")
            return
        
        # Chama a função de callback passada pelo main
        self.on_register(name, email, password)
    
    def clear_fields(self):
        """Limpa todos os campos de entrada"""
        self.var_name.set("")
        self.var_email.set("")
        self.var_pwd.set("")
        self.var_pwd_confirm.set("")