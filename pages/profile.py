import customtkinter as ctk
from tkinter import messagebox

class ProfilePage(ctk.CTkFrame):
    def __init__(self, master, current_name, current_email):
        super().__init__(master, corner_radius=12)
        self.current_name = current_name
        self.current_email = current_email
        self._build()

    def _build(self):
        labels = ["Nome:", "Email:", "Senha:"]
        values = [self.current_name, self.current_email, ""]
        for i, (lbl, val) in enumerate(zip(labels, values)):
            ctk.CTkLabel(self, text=lbl).grid(row=i, column=0, sticky="e", padx=10, pady=10)
            ent = ctk.CTkEntry(
                self,
                width=300,
                show="*" if lbl == "Senha:" else "",
                textvariable=ctk.StringVar(value=val)
            )
            ent.grid(row=i, column=1, pady=10, padx=5)

        ctk.CTkButton(
            self,
            text="Redefinir Senha",
            width=120,
            command=lambda: messagebox.showinfo("Senha", "Fluxo de redefinição de senha")
        ).grid(row=3, column=0, pady=20)
        ctk.CTkButton(
            self,
            text="Excluir Conta",
            width=120,
            command=lambda: messagebox.showwarning("Excluir", "Conta excluída (stub)")
        ).grid(row=3, column=1, pady=20)
