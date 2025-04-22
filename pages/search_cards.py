import customtkinter as ctk
from tkinter import messagebox
from services.pokeapi_service import fetch_card_data
from PIL import Image
import requests
from io import BytesIO


class SearchCardsPage(ctk.CTkFrame):
    """
    Página responsável por buscar cartas na Pokémon TCG API e exibir seus dados em grade.
    """
    def __init__(self, master):
        super().__init__(master, corner_radius=12)
        self.current_page = 1
        self.total_pages = 1
        self.current_search_term = ""
        self.var_search = ctk.StringVar()
        self._build()

    def _build(self):
        # Título
        ctk.CTkLabel(
            self,
            text="Buscar Cartas",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=(0, 15))

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
        self.results_frame = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.results_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(15, 0))

        # Permitir expansão da área de resultados
        self.rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

    def on_search(self):
        self.current_search_term = self.var_search.get().strip()
        if not self.current_search_term:
            return messagebox.showwarning("Buscar", "Digite o nome da carta.")
        self.current_page = 1
        self.load_page(self.current_page)

    def load_page(self, page):
        cards, self.total_pages = fetch_card_data(self.current_search_term, page)

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not cards:
            if page == 1:
                return messagebox.showinfo("Resultados", f"Nenhuma carta encontrada para “{self.current_search_term.title()}”.")
            else:
                return messagebox.showinfo("Fim", "Você chegou ao fim dos resultados.")

        # Frame de grade
        grid_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        grid_frame.pack(anchor="center", padx=10, pady=10)

        columns = 3
        for index, card in enumerate(cards):
            row = index // columns
            col = index % columns
            self.create_card_widget(grid_frame, card, row, col)

        # Navegação
        nav_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        nav_frame.pack(pady=10)

        if self.current_page > 1:
            ctk.CTkButton(nav_frame, text="Anterior", command=self.go_previous_page).pack(side="left", padx=10)

        # Texto da página atual
        ctk.CTkLabel(
            nav_frame,
            text=f"Página {self.current_page}/{self.total_pages}",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=10)

        if self.current_page < self.total_pages:
            ctk.CTkButton(nav_frame, text="Próxima", command=self.go_next_page).pack(side="left", padx=10)


    def go_next_page(self):
        self.current_page += 1
        self.load_page(self.current_page)

    def go_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_page(self.current_page)

    @staticmethod
    def load_image_from_url(url, size=(150, 210)):
        try:
            response = requests.get(url, timeout=5)
            image = Image.open(BytesIO(response.content))
            return ctk.CTkImage(light_image=image, dark_image=image, size=size)
        except Exception:
            return None

    @staticmethod
    def create_card_widget(parent, card, row, column):
        # Card Frame geral
        card_frame = ctk.CTkFrame(parent, corner_radius=12, fg_color="#1a1a1a")
        card_frame.grid(row=row, column=column, padx=10, pady=10, sticky="n")

        # Imagem da carta
        img = SearchCardsPage.load_image_from_url(card['imagem_url'], size=(120, 168))
        if img:
            img_label = ctk.CTkLabel(card_frame, image=img, text="")
            img_label.image = img
            img_label.pack(side="left", padx=10, pady=10)
        else:
            ctk.CTkLabel(card_frame, text="[imagem]").pack(side="left", padx=10, pady=10)

        # Bloco de informações ao lado da imagem
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        ctk.CTkLabel(
            info_frame,
            text=card["nome"],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            info_frame,
            text=f'Preço de mercado: US${card["preco_dolar"]:.2f}',
            font=ctk.CTkFont(size=13),
            anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            info_frame,
            text=f'Coleção: {card["colecao"]}',
            font=ctk.CTkFont(size=12),
            anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            info_frame,
            text=f'Raridade: {card["raridade"] or "Desconhecida"}',
            font=ctk.CTkFont(size=12),
            anchor="w"
        ).pack(anchor="w")

