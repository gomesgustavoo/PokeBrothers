from PIL import Image
from io import BytesIO
import customtkinter as ctk
from typing import List

import requests
from models.Carta import Carta
from pages.search_cards import SearchCardsPage


TIPO_CORES = {
    "Grass": "#78C850",
    "Fire": "#F08030",
    "Water": "#6890F0",
    "Lightning": "#F8D030",
    "Psychic": "#F85888",
    "Fighting": "#C03028",
    "Colorless": "#A8A878",
    "Darkness": "#705848",
    "Metal": "#B8B8D0",
    "Fairy": "#EE99AC",
    "Dragon": "#7038F8",
}
class LocalSearchCardsPage(ctk.CTkFrame):
    """Exibe uma lista de cartas locais permitindo filtrar pelo nome."""
    def __init__(self, master, cartas: List[Carta], on_card_select=None):
        super().__init__(master, corner_radius=12)
        self.cartas = cartas
        self.on_card_select = on_card_select
        self.var_search = ctk.StringVar()
        self._build()
        self._renderiza_cartas(self.cartas)

    def _build(self):
        ctk.CTkLabel(
            self,
            text="Buscar Cartas",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        ctk.CTkEntry(
            self,
            textvariable=self.var_search,
            width=250
        ).grid(row=1, column=0, pady=5, padx=10, sticky="w")
        ctk.CTkButton(
            self,
            text="Buscar",
            command=self.on_pesquisa
        ).grid(row=1, column=1, padx=5)

        self.results_frame = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.results_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(10,0))
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

    def on_pesquisa(self):
        term = self.var_search.get().strip().lower()
        if term:
            filtered = [c for c in self.cartas if term in c.nome.lower()]
        else:
            filtered = list(self.cartas)
        self._renderiza_cartas(filtered)

    def _renderiza_cartas(self, cartas: List[Carta]):
        for w in self.results_frame.winfo_children():
            w.destroy()
        if not cartas:
            ctk.CTkLabel(self.results_frame, text="Nenhuma carta encontrada.").pack(pady=20)
            return
        grid_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        grid_frame.pack(anchor="center", padx=10, pady=10)
        columns = 4
        for idx, card in enumerate(cartas):
            row = idx // columns
            col = idx % columns
            self.create_card_widget(grid_frame, card, row, col)

    def load_image_from_url(self,url, size=(150, 210)):
        try:
            response = requests.get(url, timeout=5)
            image = Image.open(BytesIO(response.content))
            return ctk.CTkImage(light_image=image, dark_image=image, size=size)
        except Exception:
            return None

    def create_card_widget(self, parent, card:Carta, row, column):
        # Card Frame geral
        card_frame = ctk.CTkFrame(parent, corner_radius=12, fg_color="#1a1a1a")
        card_frame.grid(row=row, column=column, padx=10, pady=10, sticky="n")

        # Imagem da carta
        img = self.load_image_from_url(card.get_imagem_url(), size=(120, 168))
        if img:
            img_label = ctk.CTkLabel(card_frame, image=img, text="")
            img_label.image = img
            img_label.pack(side="left", padx=10, pady=10)
        else:
            ctk.CTkLabel(card_frame, text="[imagem]").pack(side="left", padx=10, pady=10)

        if self.on_card_select:
            def _on_click(evt=None, c=card):
                # devolve o dict da carta
                self.on_card_select(c)
            # binder no frame e em todos os filhos (imagem + labels)
            card_frame.bind("<Button-1>", _on_click)
            for filho in card_frame.winfo_children():
                filho.bind("<Button-1>", _on_click)

        # Bloco de informações ao lado da imagem
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        ctk.CTkLabel(
            info_frame,
            text=card.get_nome(),
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            info_frame,
            text=f'Preço de mercado: R${card.get_preco_real():.2f}',
            font=ctk.CTkFont(size=12),
            anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            info_frame,
            text=f'Coleção: {card.get_colecao()}',
            font=ctk.CTkFont(size=12),
            anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            info_frame,
            text=f'Raridade: {card.get_raridade() or "Desconhecida"}',
            font=ctk.CTkFont(size=12),
            anchor="w"
        ).pack(anchor="w")
        # Tag de tipo com cor
        tipo = card.get_tipo().split(",")[0] if card.get_tipo() else "Desconhecido"
        cor = TIPO_CORES.get(tipo, "#666666")  # cor padrão se não mapeado

        ctk.CTkLabel(
            info_frame,
            text=f"Tipo: {tipo}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white",
            fg_color=cor,
            corner_radius=6,
            padx=6,
            pady=2
        ).pack(anchor="w", pady=(4, 0))