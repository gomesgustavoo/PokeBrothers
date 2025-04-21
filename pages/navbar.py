import customtkinter as ctk

class NavBar(ctk.CTkFrame):
    def __init__(self, master, commands):
        super().__init__(master, corner_radius=0)
        for i, (text, cmd) in enumerate(commands):
            btn = ctk.CTkButton(self, text=text, command=cmd, width=140)
            btn.grid(row=i, column=0, pady=(10 if i==0 else 5), padx=10, sticky="ew")
