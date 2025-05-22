import customtkinter as ctk
from tkinter import messagebox
from models.ItemInventario import ItemInventario
from models.Carta import Carta
from pages.search_cards import SearchCardsPage
from PIL import Image
import requests
from io import BytesIO

class InventarioPage(ctk.CTkFrame):
    """
    Página de Inventário do Colecionador: permite adicionar e remover cartas do inventário.
    """
    SLOTS_POR_LINHA = 5

    def __init__(self, master, colecionador):
        super().__init__(master, corner_radius=12)
        self.colecionador = colecionador
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Inventário", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(10, 20))

        btn_add = ctk.CTkButton(self, text="+ Adicionar Carta", command=self._abrir_modal_adicionar)
        btn_add.pack(pady=(0, 15))

        self.frame_cartas = ctk.CTkFrame(self, corner_radius=10)
        self.frame_cartas.pack(fill="both", expand=True, padx=10, pady=10)
        self._renderizar_cartas()

    def _abrir_modal_adicionar(self):
        topo = ctk.CTkToplevel(self)
        topo.title("Adicionar Carta ao Inventário")
        topo.geometry("800x600")
        SearchCardsPage(
            master=topo,
            on_card_select=lambda carta: self._adicionar_carta(carta, topo)
        ).pack(fill="both", expand=True)

    def _adicionar_carta(self, carta: Carta, topo):
        topo.destroy()
        # Verifica se já existe a carta no inventário
        for item in self.colecionador.get_inventario():
            if item.get_carta().id == carta.id:
                item.set_quantidade(item.get_quantidade() + 1)
                break
        else:
            novo_item = ItemInventario(carta, quantidade=1)
            self.colecionador.get_inventario().append(novo_item)
        self._renderizar_cartas()

    def _remover_carta(self, item_id: str):
        inventario = self.colecionador.get_inventario()
        for item in inventario:
            if item.get_id() == item_id:
                if item.get_quantidade() > 1:
                    item.set_quantidade(item.get_quantidade() - 1)
                else:
                    inventario.remove(item)
                break
        self._renderizar_cartas()

    def _renderizar_cartas(self):
        for widget in self.frame_cartas.winfo_children():
            widget.destroy()

        inventario = self.colecionador.get_inventario()
        if not inventario:
            ctk.CTkLabel(self.frame_cartas, text="Nenhuma carta no inventário.").pack(pady=20)
            return

        for idx, item in enumerate(inventario):
            row = idx // self.SLOTS_POR_LINHA
            col = idx % self.SLOTS_POR_LINHA
            self._criar_widget_carta(self.frame_cartas, item, row, col)

    def _criar_widget_carta(self, parent, item: ItemInventario, row, col):
        carta = item.get_carta()
        frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="#232323")
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="n")

        # Imagem da carta
        img = self._carregar_imagem_url(carta.imagem_url)
        if img:
            lbl_img = ctk.CTkLabel(frame, image=img, text="")
            lbl_img.image = img
            lbl_img.pack(pady=(5, 0))
        else:
            ctk.CTkLabel(frame, text="[imagem]").pack(pady=(5, 0))

        # Nome e quantidade
        ctk.CTkLabel(frame, text=carta.nome, font=ctk.CTkFont(size=13, weight="bold")).pack()
        ctk.CTkLabel(frame, text=f"Qtd: {item.get_quantidade()}").pack()

        # Botão de exclusão (ícone pequeno)
        btn_del = ctk.CTkButton(
            frame,
            text="🗑️",
            width=24,
            height=24,
            fg_color="#d9534f",
            text_color="white",
            font=ctk.CTkFont(size=14),
            command=lambda i=item.get_id(): self._remover_carta(i)
        )
        btn_del.pack(pady=(5, 0))

    @staticmethod
    def _carregar_imagem_url(url, size=(90, 126)):
        try:
            response = requests.get(url, timeout=5)
            image = Image.open(BytesIO(response.content))
            return ctk.CTkImage(light_image=image, dark_image=image, size=size)
        except Exception:
            return None