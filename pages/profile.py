import customtkinter as ctk
from tkinter import messagebox

class ProfilePage(ctk.CTkFrame):
    def __init__(
        self,
        master,
        record_id: str,
        current_name: str,
        current_email: str,
        on_update_callback,
        on_delete_callback,
        on_logout_callback
    ):
        super().__init__(master, corner_radius=12)
        self.record_id = record_id
        self.current_name = current_name
        self.current_email = current_email
        self.on_update = on_update_callback
        self.on_delete = on_delete_callback
        self.on_logout = on_logout_callback

        # Variável para editar o nome
        self.var_name = ctk.StringVar(value=current_name)

        self._build()

    def _build(self):
        # Email (somente leitura)
        ctk.CTkLabel(self, text="Email:").grid(
            row=0, column=0, sticky="e", padx=10, pady=10
        )
        ctk.CTkLabel(self, text=self.current_email).grid(
            row=0, column=1, sticky="w", padx=10, pady=10
        )

        # Nome (editável)
        ctk.CTkLabel(self, text="Nome:").grid(
            row=1, column=0, sticky="e", padx=10, pady=10
        )
        ctk.CTkEntry(self, width=300, textvariable=self.var_name).grid(
            row=1, column=1, pady=10, padx=5
        )

        # Botões de ação (acompanhados de pad menor para aproximar)
        button_padx = 10
        ctk.CTkButton(
            self,
            text="Alterar Nome",
            width=140,
            command=self._on_update_name
        ).grid(row=2, column=0, pady=20, padx=button_padx)

        ctk.CTkButton(
            self,
            text="Excluir Conta",
            width=140,
            fg_color="red",
            hover_color="#AA0000",
            command=self._confirm_delete
        ).grid(row=2, column=1, pady=20, padx=button_padx)

        ctk.CTkButton(
            self,
            text="Sair",
            width=140,
            command=self.on_logout
        ).grid(row=2, column=2, pady=20, padx=button_padx)

    def _on_update_name(self):
        new_name = self.var_name.get().strip()
        if new_name:
            self.on_update(new_name)
        else:
            messagebox.showwarning("Perfil", "O nome não pode ficar vazio.")

    def _confirm_delete(self):
        resp = messagebox.askyesno(
            "Excluir Conta",
            "Tem certeza que deseja excluir sua conta? Esta ação é irreversível."
        )
        if resp:
            self.on_delete()
