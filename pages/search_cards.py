import customtkinter as ctk
from tkinter import messagebox
from services.pokeapi_service import fetch_card_data

class SearchCardsPage(ctk.CTkFrame):
    """
    Página responsável apenas por buscar cartas na Pokémon TCG API e exibir seus dados.
    """
    def __init__(self, master):
        super().__init__(master, corner_radius=12)
        self.current_page = 1
        self.current_search_term = ""
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
        self.current_search_term = self.var_search.get().strip()
        if not self.current_search_term:
            return messagebox.showwarning("Buscar", "Digite o nome da carta.")
        self.current_page = 1
        self.load_page(self.current_page)

    def load_page(self, page):
        cards = fetch_card_data(self.current_search_term, page)

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not cards:
            if page == 1:
                return messagebox.showinfo("Resultados", f"Nenhuma carta encontrada para “{self.current_search_term.title()}”.")
            else:
                return messagebox.showinfo("Fim", "Você chegou ao fim dos resultados.")

        for card in cards:
            info = (
                f"{card['nome']} | Tipo: {card['tipo']} | "
                f"Set: {card['colecao']} | Raridade: {card['raridade']} | "
                f"US${card['preco_dolar']:.2f}"
            )
            ctk.CTkLabel(self.results_frame, text=info, anchor="w", wraplength=400).pack(fill="x", pady=2, padx=5)

        # Adiciona botões de navegação
        nav_frame = ctk.CTkFrame(self.results_frame)
        nav_frame.pack(pady=10)

        if self.current_page > 1:
            ctk.CTkButton(nav_frame, text="Anterior", command=self.go_previous_page).pack(side="left", padx=10)

        ctk.CTkButton(nav_frame, text="Próxima", command=self.go_next_page).pack(side="left", padx=10)

    def go_next_page(self):
        self.current_page += 1
        self.load_page(self.current_page)

    def go_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_page(self.current_page)

