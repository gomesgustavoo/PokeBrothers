import customtkinter as ctk
from tkinter import messagebox
from services.pokeapi_service import fetch_card_data

class SearchCardsPage(ctk.CTkFrame):
    """
    Página responsável apenas por buscar cartas na Pokémon TCG API e exibir seus dados.
    """
    def __init__(self, master):
        super().__init__(master, corner_radius=12)
        self.var_search = ctk.StringVar()
        self._build()

    def _build(self):
        # Título
        ctk.CTkLabel(
            self,
            text="Buscar Cartas",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=(0,15))

        # Campo de busca
        ctk.CTkLabel(self, text="Nome da Carta:").grid(row=1, column=0, sticky="e", padx=10)
        ctk.CTkEntry(
            self,
            textvariable=self.var_search,
            width=250
        ).grid(row=1, column=1, pady=5)
        ctk.CTkButton(
            self,
            text="Buscar",
            command=self.on_search
        ).grid(row=1, column=2, padx=5)

        # Frame de resultados
        self.results_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=12
        )
        self.results_frame.grid(
            row=2, column=0, columnspan=3,
            sticky="nsew", pady=(15,0)
        )

        # Permite expansão da área de resultados
        self.rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

    def on_search(self):
        name = self.var_search.get().strip()
        if not name:
            return messagebox.showwarning("Buscar", "Digite o nome da carta.")

        card = fetch_card_data(name)
        if not card:
            return messagebox.showerror(
                "Buscar", f"Carta “{name.title()}” não encontrada."
            )

        # Limpa resultados anteriores
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Exibe informações da carta
        info = f"{card['nome']} | Set: {card['colecao']} | US${card['preco_dolar']:.2f}"
        ctk.CTkLabel(
            self.results_frame,
            text=info,
            anchor="w"
        ).pack(fill="x", pady=2, padx=5)

        # Opcional: limpar campo de busca
        # self.var_search.set("")
