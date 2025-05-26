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
        # ---------- TOOLBAR (linha preta superior do mock) ----------
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, columnspan=2, sticky="we", pady=(10, 5))
        toolbar.columnconfigure(0, weight=1)

        ctk.CTkButton(
            toolbar, text="+ adicionar carta",
            command=self._abrir_busca_cartas
        ).grid(row=0, column=0, sticky="w", padx=10)

        # ---------- Título “Minhas Cartas” logo abaixo -------------
        ctk.CTkLabel(
            self, text="Minhas Cartas",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=10)

        # ---------- Área com as cartas (grade dentro de scroll) ----
        self.frame_lista = ctk.CTkScrollableFrame(self, corner_radius=8)
        self.frame_lista.grid(row=2, column=0, columnspan=2,
                                sticky="nsew", padx=10, pady=(5, 10))

        # expansão
        self.rowconfigure(2, weight=1)
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
        if any(c.id == carta.id for c in self.cartas):
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
        """
        Mini-card agora sem altura fixa (para não cortar a imagem)
        e com o 'X' posicionado no canto inferior direito.
        """
        # ------------------ container ------------------
        card_frame = ctk.CTkFrame(
            parent,
            corner_radius=8,
            fg_color="#1a1a1a",
            width=280            # só fixa a largura
            # -> removemos height=..., para não cortar
        )
        # permitir que o frame ajuste sua altura aos conteúdos
        card_frame.grid_propagate(True)

        # configurações de grid (coluna 1 cresce, coluna 2 = botão)
        card_frame.columnconfigure(1, weight=1)

        # ------------------- imagem --------------------
        img = SearchCardsPage.load_image_from_url(
            carta.imagem_url, size=self.TAM_SLOT
        )
        if img:
            lbl_img = ctk.CTkLabel(card_frame, image=img, text="")
            lbl_img.image = img
        else:
            lbl_img = ctk.CTkLabel(
                card_frame,
                text="[img]",
                width=self.TAM_SLOT[0],
                height=self.TAM_SLOT[1]
            )
        lbl_img.grid(
            row=0, column=0,
            rowspan=2,
            padx=6, pady=6,
            sticky="nw"
        )

        # ------------------- infos --------------------
        info = ctk.CTkFrame(card_frame, fg_color="transparent")
        info.grid(
            row=0, column=1,
            sticky="nw",
            padx=(0, 6), pady=(6, 2)
        )
        ctk.CTkLabel(
            info,
            text=carta.nome,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
            wraplength=150
        ).pack(anchor="w")
        ctk.CTkLabel(
            info,
            text=f"Preço: R${carta.preco_real:,.2f}",
            font=ctk.CTkFont(size=12),
            anchor="w"
        ).pack(anchor="w")

        # --------------- botão “X” --------------------
        ctk.CTkButton(
            card_frame,
            text="X",
            width=28,
            fg_color="#FF3B3B",
            hover_color="#E32B2B",
            command=lambda i=idx: self._remover_carta(i)
        ).grid(
            row=1, column=2,
            padx=(0, 6), pady=(0, 6),
            sticky="se"   # canto inferior direito
        )

        return card_frame


    # -------------------------------------------------- persistência (igual)
    def salvar_lista(self):
        messagebox.showinfo("Lista de Desejos", "Lista salva com sucesso!")
