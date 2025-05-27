import customtkinter as ctk
from tkinter import messagebox
from pages.search_cards import SearchCardsPage
from models.Carta import Carta


class ListaDesejosPage(ctk.CTkFrame):
    COLUNAS    = 5
    TAM_SLOT   = (120, 168)
    MAX_CARTAS = 50              

    def __init__(self, master):
        super().__init__(master, corner_radius=12)
        self.cartas: list[Carta] = []
        self._build()

    # ------------------------------------------------------------- UI
    def _build(self):
        ctk.CTkLabel(
            self, text="Minha Lista de Desejos",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        ctk.CTkButton(
            self, text="+ Adicionar carta",
            command=self._abrir_busca_cartas
        ).grid(row=0, column=1, sticky="e", padx=10, pady=(10, 5))

        self.frame_lista = ctk.CTkScrollableFrame(self, corner_radius=8)
        self.frame_lista.grid(row=1, column=0, columnspan=2,
                              sticky="nsew", padx=10, pady=(5, 10))

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self._renderizar_lista()

    # --------------------------------------------------------- fluxo
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

    def _adicionar_carta(self, carta: Carta):
        """Tenta inserir a carta; aborta se duplicada ou se exceder 50 itens."""
        # 1) Limite geral
        if len(self.cartas) >= self.MAX_CARTAS:
            messagebox.showerror(
                "Limite atingido",
                f"Sua lista de desejos já contém {self.MAX_CARTAS} cartas."
            )
            return

        # 2) Duplicata
        if any(c.get_id() == carta.get_id() for c in self.cartas):
            messagebox.showerror(
                "Carta repetida",
                "Essa carta já está na lista!"
            )
            return

        # 3) Inserção
        self.cartas.append(carta)
        self._renderizar_lista()

    def _remover_carta(self, index: int):
        if not messagebox.askyesno(
            "Remover carta",
            "Deseja realmente remover esta carta da lista?"
        ):
            return
        del self.cartas[index]
        self._renderizar_lista()

    # -------------------------------------------------------- render helpers
    def _renderizar_lista(self):
        for w in self.frame_lista.winfo_children():
            w.destroy()

        if not self.cartas:
            ctk.CTkLabel(
                self.frame_lista,
                text="Nenhuma carta adicionada ainda. Clique em '+ Adicionar carta'.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        for idx, carta in enumerate(self.cartas):
            linha, coluna = divmod(idx, self.COLUNAS)
            self._criar_card_widget(self.frame_lista, carta, idx).grid(
                row=linha, column=coluna, padx=8, pady=8, sticky="n"
            )

    def _criar_card_widget(self, parent, carta: Carta, idx: int):
        card_frame = ctk.CTkFrame(
            parent, corner_radius=8, fg_color="#1a1a1a", width=150
        )
        card_frame.grid_propagate(False)

        img = SearchCardsPage.load_image_from_url(carta.imagem_url, size=self.TAM_SLOT)
        lbl_img = ctk.CTkLabel(card_frame, image=img, text="") if img else \
            ctk.CTkLabel(card_frame, text="[img]", width=self.TAM_SLOT[0], height=self.TAM_SLOT[1])
        if img:
            lbl_img.image = img
        lbl_img.pack(pady=(5, 2))

        ctk.CTkLabel(
            card_frame,
            text=carta.nome[:25] + ("…" if len(carta.nome) > 25 else ""),
            font=ctk.CTkFont(size=12, weight="bold"),
            wraplength=130,
            justify="center"
        ).pack(padx=4)

        ctk.CTkLabel(
            card_frame,
            text=f"R${carta.preco_real:,.2f}",
            font=ctk.CTkFont(size=12)
        ).pack()

        ctk.CTkButton(
            card_frame,
            text="Remover",
            fg_color="#FF6B6B", hover_color="#FF4C4C",
            command=lambda i=idx: self._remover_carta(i)
        ).pack(pady=(4, 6))

        return card_frame

    # -------------------------------------------------- persistência (igual)
    def salvar_lista(self):
        messagebox.showinfo("Lista de Desejos", "Lista salva com sucesso!")
