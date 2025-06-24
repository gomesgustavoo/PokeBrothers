import customtkinter as ctk
from tkinter import messagebox
import traceback

from models.Colecionador import Colecionador
from models.ItemListadeDesejos import ItemListadeDesejos
from models.Carta import Carta
from pages.search_cards import SearchCardsPage

class ListaDesejosPage(ctk.CTkFrame):
    COLUNAS = 5
    TAM_SLOT = (120, 168)
    MAX_CARTAS = 50

    def __init__(self, master, colecionador: Colecionador):
        super().__init__(master, corner_radius=12)
        try:
            if not colecionador or not colecionador.get_id():
                raise ValueError("Colecionador inválido para Lista de Desejos.")

            self.colecionador = colecionador
            # Carrega do repo via método de Colecionador
            self.colecionador.carregar_lista_desejos_persistente()

            self._build()
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror(
                "Erro Crítico",
                f"Ocorreu um erro ao carregar a página:\n\n{e}"
            )
            ctk.CTkLabel(
                self,
                text="Erro ao carregar a página.\nVerifique o console para mais detalhes.",
                text_color="red"
            ).pack(pady=20, padx=10)

    def _build(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, columnspan=2, sticky="we", pady=(10, 5))
        toolbar.columnconfigure(0, weight=1)
        ctk.CTkButton(
            toolbar,
            text="+ Adicionar Carta",
            command=self._abrir_busca_cartas
        ).grid(row=0, column=0, sticky="w", padx=10)

        ctk.CTkLabel(
            self,
            text="Minha Lista de Desejos",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=10)

        self.frame_lista = ctk.CTkScrollableFrame(self, corner_radius=8)
        self.frame_lista.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(5, 10))
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self._renderizar_lista()

    def _abrir_busca_cartas(self):
        topo = ctk.CTkToplevel(self)
        topo.title("Buscar carta")
        topo.geometry("1200x800")

        SearchCardsPage(
            master=topo,
            on_card_select=lambda carta: (
                topo.destroy(),
                self._adicionar_carta(carta)
            )
        ).pack(fill="both", expand=True)

    def carta_repetida(self, carta: Carta) -> bool:
        desejos = self.colecionador.get_listaDesejos()
        return any(item.get_carta().get_id() == carta.get_id() for item in desejos)

    def _adicionar_carta(self, carta: Carta):
        desejos = self.colecionador.get_listaDesejos()
        if len(desejos) >= self.MAX_CARTAS:
            messagebox.showerror(
                "Limite atingido",
                f"Sua lista de desejos já contém {self.MAX_CARTAS} cartas."
            )
            return

        if self.carta_repetida(carta):
            messagebox.showerror(
                "Carta repetida",
                "Essa carta já está na lista!"
            )
            return

        novo_item = ItemListadeDesejos(carta)
        # Delegar ao Colecionador
        self.colecionador.adicionar_item_lista_desejos_persistente(novo_item)
        self._renderizar_lista()

    def _remover_carta(self, item_id: str):
        if not messagebox.askyesno(
            "Remover carta",
            "Deseja realmente remover esta carta da lista?"
        ):
            return

        # Busca o item
        item = next(
            (it for it in self.colecionador.get_listaDesejos() if it.get_id() == item_id),
            None
        )
        if item:
            # Delegar ao Colecionador
            self.colecionador.remover_item_lista_desejos(item)
            self._renderizar_lista()

    def _renderizar_lista(self):
        for w in self.frame_lista.winfo_children():
            w.destroy()

        desejos = self.colecionador.get_listaDesejos()
        if not desejos:
            ctk.CTkLabel(
                self.frame_lista,
                text="Nenhuma carta adicionada ainda. Clique em '+ Adicionar Carta'.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        for idx, item in enumerate(desejos):
            row, col = divmod(idx, self.COLUNAS)
            self._criar_card_widget(self.frame_lista, item).grid(
                row=row, column=col, padx=8, pady=8, sticky="n"
            )

    def _criar_card_widget(self, parent, item: ItemListadeDesejos):
        carta = item.get_carta()
        card = ctk.CTkFrame(parent, corner_radius=8, fg_color="#1a1a1a")

        img_label = ctk.CTkLabel(card, text="")
        if hasattr(SearchCardsPage, 'load_image_from_url'):
            img = SearchCardsPage.load_image_from_url(
                carta.get_imagem_url(), size=self.TAM_SLOT
            )
            if img:
                img_label.configure(image=img)
            else:
                img_label.configure(
                    text="[img]", width=self.TAM_SLOT[0], height=self.TAM_SLOT[1]
                )
        else:
            img_label.configure(
                text="[img loader n/a]", width=self.TAM_SLOT[0], height=self.TAM_SLOT[1]
            )
        img_label.pack(padx=6, pady=6)

        ctk.CTkLabel(
            card,
            text=carta.get_nome(),
            font=ctk.CTkFont(size=13, weight="bold"),
            wraplength=140
        ).pack(padx=6, pady=(0,2))

        if hasattr(carta, 'get_preco_real') and carta.get_preco_real() is not None:
            ctk.CTkLabel(
                card,
                text=f"R${carta.get_preco_real():,.2f}",
                font=ctk.CTkFont(size=12)
            ).pack(padx=6, pady=(0,4))

        ctk.CTkButton(
            card,
            text="Remover",
            height=28,
            fg_color="#FF3B3B",
            hover_color="#E32B2B",
            command=lambda i=item: self._remover_carta(i.get_id())
        ).pack(padx=6, pady=(0,6), fill='x')

        return card
