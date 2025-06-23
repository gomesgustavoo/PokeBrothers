import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import traceback

# Presume-se que a classe Colecionador seja importada se for usada para type hinting
# from models.Colecionador import Colecionador 
from models.Carta import Carta
from models.ItemListadeDesejos import ItemListadeDesejos
from services.pokeapi_service import buscar_carta_por_id
from pages.search_cards import SearchCardsPage

# O nome da variável global para o banco de dados deve ser consistente
INVENTARIO_DB = "inventario.db"

class ListaDesejosPage(ctk.CTkFrame):
    COLUNAS = 5
    TAM_SLOT = (120, 168)
    MAX_CARTAS = 50

    def __init__(self, master, colecionador):
        """
        Versão funcional que recebe o objeto 'colecionador' completo.
        """
        super().__init__(master, corner_radius=12)
        
        try:
            if not colecionador or not colecionador.get_id():
                raise ValueError("O objeto 'colecionador' ou seu ID não foi fornecido para a Lista de Desejos.")
            
            self.colecionador = colecionador
            self.lista_de_desejos: list[ItemListadeDesejos] = []
            
            self._carregar_lista_db()
            self._build()

        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro ao carregar a página:\n\n{e}")
            ctk.CTkLabel(self, text=f"Erro ao carregar a página.\nVerifique o console para mais detalhes.", text_color="red").pack(pady=20, padx=10)


    def _build(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, columnspan=2, sticky="we", pady=(10, 5))
        toolbar.columnconfigure(0, weight=1)
        ctk.CTkButton(
            toolbar, text="+ adicionar carta",
            command=self._abrir_busca_cartas
        ).grid(row=0, column=0, sticky="w", padx=10)

        ctk.CTkLabel(
            self, text="Minha Lista de Desejos",
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

        # Assume que SearchCardsPage tem uma assinatura que aceita on_card_select
        SearchCardsPage(
            master=topo,
            on_card_select=lambda carta: (
                topo.destroy(),
                self._adicionar_carta(carta)
            )
        ).pack(fill="both", expand=True)

    def _adicionar_carta(self, carta: Carta):
        if len(self.lista_de_desejos) >= self.MAX_CARTAS:
            messagebox.showerror("Limite atingido", f"Sua lista de desejos já contém {self.MAX_CARTAS} cartas.")
            return
        # 2) Duplicata
        if any(c.get_id() == carta.get_id() for c in self.lista_de_desejos):
            messagebox.showerror(
                "Carta repetida",
                "Essa carta já está na lista!"
            )

            return

        novo_item = ItemListadeDesejos(carta, quantidade=1)
        self._adicionar_item_db(novo_item)
        self.lista_de_desejos.append(novo_item)
        self._renderizar_lista()

    def _remover_carta(self, item_id_para_remover: str):
        if not messagebox.askyesno("Remover carta", "Deseja realmente remover esta carta da lista?"):
            return

        item_encontrado = next((item for item in self.lista_de_desejos if item.get_id() == item_id_para_remover), None)
        
        if item_encontrado:
            self._remover_item_db(item_id_para_remover)
            self.lista_de_desejos.remove(item_encontrado)
            self._renderizar_lista()

    def _renderizar_lista(self):
        for w in self.frame_lista.winfo_children():
            w.destroy()

        if not self.lista_de_desejos:
            ctk.CTkLabel(
                self.frame_lista,
                text="Nenhuma carta adicionada ainda. Clique em '+ Adicionar carta'.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        for idx, item in enumerate(self.lista_de_desejos):
            linha, coluna = divmod(idx, self.COLUNAS)
            self._criar_card_widget(self.frame_lista, item).grid(
                row=linha, column=coluna, padx=8, pady=8, sticky="n"
            )

    def _criar_card_widget(self, parent, item: ItemListadeDesejos):
        carta = item.get_carta()
        card_frame = ctk.CTkFrame(parent, corner_radius=8, fg_color="#1a1a1a")
        
        img_label = ctk.CTkLabel(card_frame, text="")
        if hasattr(SearchCardsPage, 'load_image_from_url'):
            img = SearchCardsPage.load_image_from_url(carta.get_imagem_url(), size=self.TAM_SLOT)
            if img:
                img_label.configure(image=img)
            else:
                img_label.configure(text="[img]", width=self.TAM_SLOT[0], height=self.TAM_SLOT[1])
        else:
             img_label.configure(text="[img loader n/a]", width=self.TAM_SLOT[0], height=self.TAM_SLOT[1])
        
        img_label.pack(padx=6, pady=6)

        ctk.CTkLabel(card_frame, text=carta.get_nome(), font=ctk.CTkFont(size=13, weight="bold"), wraplength=140).pack(padx=6, pady=(0,2))
        
        if hasattr(carta, 'get_preco_real') and carta.get_preco_real() is not None:
             ctk.CTkLabel(card_frame, text=f"R${carta.get_preco_real():,.2f}", font=ctk.CTkFont(size=12)).pack(padx=6, pady=(0,4))

        ctk.CTkButton(
            card_frame, text="Remover", height=28, fg_color="#FF3B3B", hover_color="#E32B2B",
            command=lambda item_id=item.get_id(): self._remover_carta(item_id)
        ).pack(padx=6, pady=(0, 6), fill='x')

        return card_frame

    def _carregar_lista_db(self):
        """Carrega a lista de desejos usando o ID do objeto colecionador."""
        conn = sqlite3.connect(INVENTARIO_DB)
        cur = conn.cursor()
        # Usa o ID armazenado no objeto da classe
        cur.execute("SELECT id, carta_id, quantidade FROM lista_desejos WHERE colecionador_id=?", (self.colecionador.get_id(),))
        rows = cur.fetchall()
        conn.close()
        
        lista_carregada = []
        for row in rows:
            id_item, carta_id, quantidade = row
            carta = buscar_carta_por_id(carta_id)
            if carta:
                lista_carregada.append(ItemListadeDesejos(carta, quantidade=quantidade, id=id_item))
        self.lista_de_desejos = lista_carregada

    def _adicionar_item_db(self, item: ItemListadeDesejos):
        """Salva um item no DB usando o ID do objeto colecionador."""
        conn = sqlite3.connect(INVENTARIO_DB)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO lista_desejos (id, colecionador_id, carta_id, quantidade) VALUES (?, ?, ?, ?)",
            (item.get_id(), self.colecionador.get_id(), item.get_carta().get_id(), item.get_quantidade())
        )
        conn.commit()
        conn.close()

    def _remover_item_db(self, item_id: str):
        """Remove um item do banco de dados (não precisa do ID do colecionador)."""
        conn = sqlite3.connect(INVENTARIO_DB)
        cur = conn.cursor()
        cur.execute("DELETE FROM lista_desejos WHERE id=?", (item_id,))
        conn.commit()
        conn.close()
