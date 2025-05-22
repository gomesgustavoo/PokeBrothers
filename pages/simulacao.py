import customtkinter as ctk
from models.Simulacao import SimulacaoTroca
from pages.search_cards import SearchCardsPage
from models.ItemTroca import ItemTroca
from models.Carta import Carta
from tkinter import messagebox

DOLLAR_TO_REAL = 5.0


class SimulacaoTrocaPage(ctk.CTkFrame):


    SLOTS_POR_PAINEL = 10
    COLUNAS = 5
    """
    Página para simular trocas de cartas entre colecionadores,
    com painéis de cartas oferecidas e recebidas.
    """

    def __init__(self, master):
        super().__init__(master, corner_radius=12)
        self.simulacao = SimulacaoTroca(limite_percentual=10.0)
        self.ofertados_frames = []
        self.recebidos_frames = []
        self.var_total_ofertados = ctk.StringVar(value="Valor total: R$0,00")
        self.var_total_recebidos = ctk.StringVar(value="Valor total: R$0,00")
        self.var_diff_ofertados = ctk.StringVar(value="0%")
        self.var_diff_recebidos = ctk.StringVar(value="0%")
        self.badge_of = None
        self.badge_rc = None
        self.var_status_troca = ctk.StringVar(value="Indefinido (adicione pelo menos uma carta em cada lado da simulação)")
        self._build()

    def _build(self):
        # Título da página
        ctk.CTkLabel(self, text="Simular Troca", font=ctk.CTkFont(size=20, weight="bold")) \
            .grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Layout de colunas
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Painel de cartas ofertadas
        painel_ofertados = ctk.CTkFrame(self, corner_radius=10, fg_color="#2b2b2b")
        painel_ofertados.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self._montar_painel(painel_ofertados, "Cartas Oferecidas", self.ofertados_frames, self._adicionar_ofertado, total_var=self.var_total_ofertados,diff_var=self.var_diff_ofertados)
        # Painel de cartas recebidas
        painel_recebidos = ctk.CTkFrame(self, corner_radius=10, fg_color="#2b2b2b")
        painel_recebidos.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self._montar_painel(painel_recebidos, "Cartas Recebidas", self.recebidos_frames, self._adicionar_recebido, total_var=self.var_total_recebidos, diff_var=self.var_diff_recebidos)

        self.lbl_status = ctk.CTkLabel(
            self,
            textvariable=self.var_status_troca,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4E73D8"
        )
        self.lbl_status.grid(row=2, column=0, columnspan=2, pady=(0,5))

        # Botão de registrar simulação
        botao_salvar = ctk.CTkButton(
            self,
            text="Registrar Simulação",
            command=self._registrar_simulacao
        )
        botao_salvar.grid(row=3, column=0, columnspan=2, pady=(10, 20))

    def _montar_painel(self, painel, titulo, lista_frames, cmd_add, total_var, diff_var):
        # Cabeçalho e total
        ctk.CTkLabel(
            painel,
            text=titulo,
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=self.COLUNAS, pady=(10,5))
        ctk.CTkLabel(
            painel,
            textvariable=total_var,
            anchor="e"
        ).grid(row=1, column=0, columnspan=self.COLUNAS, sticky="e", padx=10)
        # Slots de cartas
        # Grid de slots com 2 linhas e COLUNAS colunas
        frame_grid = ctk.CTkFrame(painel, corner_radius=6, fg_color="#1a1a1a")
        frame_grid.grid(row=2, column=0, columnspan=self.COLUNAS, padx=10, pady=(5,10), sticky="nsew")

        for idx in range(self.SLOTS_POR_PAINEL):
            linha = idx // self.COLUNAS
            coluna = idx % self.COLUNAS
            slot = ctk.CTkFrame(
                frame_grid,
                width=130,
                height=200,
                fg_color="#333333",
                corner_radius=6
            )
            slot.grid(row=linha, column=coluna, padx=5, pady=5)

            btn = ctk.CTkButton(
                slot,
                text="+ Add",
                command=lambda i=idx: cmd_add(i)
            )
            btn.place(relx=0.5, rely=0.5, anchor="center")

            lista_frames.append((slot, total_var))

        # Badge de diferença
        badge = ctk.CTkLabel(
            painel,
            textvariable=diff_var,
            fg_color="#4E73D8",
            text_color="black",
            corner_radius=10,
            padx=8,
            pady=4,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        badge.grid(row=3, column=0, columnspan=self.COLUNAS, pady=(0,10))
        # Armazenar referência para atualizar cor depois
        if "Oferecidas" in titulo:
            self.badge_of = badge
        else:
            self.badge_rc = badge

    def _adicionar_ofertado(self, indice: int):
        self._escolher_fonte_carta(ofertado=True, indice=indice)

    def _adicionar_recebido(self, indice: int):
        self._escolher_fonte_carta(ofertado=False, indice=indice)

    def _escolher_fonte_carta(self, ofertado: bool, indice: int):
        """
        Modal que pergunta ao usuário se ele quer:
          • Buscar cartas na API (SearchCards)
          • Selecionar do Inventário (se ofertado) ou da Lista de Desejos (se ofertante)
        """
        topo = ctk.CTkToplevel(self)
        topo.title("De onde você quer adicionar?")
        topo.geometry("400x150")
        # Escolha o texto e a função correta
        if not ofertado:
            txt_lista = "Selecionar da Lista de Desejos"
            cmd_lista = lambda: self._selecionar_da_lista_desejos(indice, topo)
        else:
            txt_lista = "Selecionar do Inventário"
            cmd_lista = lambda: self._selecionar_do_inventario(indice, topo)

        # Botão buscar na API
        ctk.CTkButton(
            topo,
            text="Pesquisar Cartas",
            command=lambda:
                (topo.destroy(),
                    self._open_search_modal(ofertado, indice))
        ).pack(fill="x", padx=20, pady=(20, 5))

        # Botão listar do inventário ou wishlist
        ctk.CTkButton(
            topo,
            text=txt_lista,
            command=lambda: (topo.destroy(), cmd_lista())
        ).pack(fill="x", padx=20, pady=(0, 20))

    def _open_search_modal(self, ofertado: bool, indice: int):
        """
        Abre diretamente o SearchCardsPage em um novo modal.
        """
        topo = ctk.CTkToplevel(self)
        topo.title("Buscar Carta")
        topo.geometry("1200x800")
        SearchCardsPage(
            master=topo,
            on_card_select=lambda carta:
                (topo.destroy(),
                    self._selecionar_ofertado(carta, indice, topo)
                    if ofertado else
                    self._selecionar_recebido(carta, indice, topo))
        ).pack(fill="both", expand=True)

    def _selecionar_da_lista_desejos(self, indice: int, parent=None):
        """
        Aqui você abre seu modal/próprio componente que lista
        a lista de desejos do usuário e retorna a carta selecionada.
        """
        return

    def _selecionar_do_inventario(self, indice: int, parent=None):
        """
        Abre seu modal de inventário do usuário.
        """
        return

    def _atualizar_totais(self):
        # atualiza totais
        try:
            self.var_total_ofertados.set(f"Valor total: R${self.simulacao.total_ofertados():,.2f}")
            self.var_total_recebidos.set(f"Valor total: R${self.simulacao.total_recebidos():,.2f}")
            # atualiza diffs
            diff = self.simulacao.diferenca_percentual()
            print("DIFERENCA", diff)
            self.var_diff_ofertados.set(f"{diff:.0f}%")
            self.var_diff_recebidos.set(f"{(-diff):.0f}%")
            # aplica cor de alerta se desequilibrado

            if abs(diff) > self.simulacao.limite_percentual:
                self.badge_of.configure(fg_color="#FF6B6B")
                self.badge_rc.configure(fg_color="#FF6B6B")
                self.var_status_troca.set("Desequilibrada ＞﹏＜")
                self.lbl_status.configure(text_color="#FF6B6B")
            else:
                self.badge_of.configure(fg_color="#5EF06A")
                self.badge_rc.configure(fg_color="#5EF06A")
                self.var_status_troca.set("Equilibrada (●'◡'●)")
                self.lbl_status.configure(text_color="#5EF06A")
        except(ZeroDivisionError):
            self.var_status_troca.set("Indefinido (adicione pelo menos uma carta em cada lado da simulação)")
            self.lbl_status.configure(text_color="#4E73D8")

    def _selecionar_ofertado(self, carta:Carta, indice, topo):
        topo.destroy()  
        item = ItemTroca(carta)
        # adiciona na simulação
        self.simulacao.adicionar_ofertado(item)
        # renderiza no slot apropriado
        self._renderizar_slot(ofertado=True, indice=indice, item=item)
        self._atualizar_totais()

    def _selecionar_recebido(self, carta:Carta, indice, topo):
        topo.destroy()
        item = ItemTroca(carta)
        self.simulacao.adicionar_recebido(item)
        self._renderizar_slot(ofertado=False, indice=indice, item=item)
        self._atualizar_totais()

    def _renderizar_slot(self, ofertado: bool, indice: int, item: ItemTroca):
        """
        Limpa o frame do slot, exibe imagem, quantidade e botão de remover.
        """
        lista = self.ofertados_frames if ofertado else self.recebidos_frames
        slot_frame, total_var = lista[indice]

        # limpa conteúdo
        for w in slot_frame.winfo_children():
            w.destroy()

        # imagem clicável (não altera função de seleção já feito)
        img = SearchCardsPage.load_image_from_url(item.carta.imagem_url, size=(100,140))
        if img:
            lbl_img = ctk.CTkLabel(slot_frame, image=img, text="")
            lbl_img.image = img
            lbl_img.pack(pady=(5,0))
        # preco
        preco_formatado = f"R${item.carta.preco_real:,.2f}"
        ctk.CTkLabel(
            slot_frame,
            text=preco_formatado
        ).pack()
        # botão remover
        ctk.CTkButton(
            slot_frame,
            text="X",
            fg_color="red",
            command=lambda i=item.id, o=ofertado: self._remover_item(i, o)
        ).pack(pady=(5,0))

    def _remover_item(self, item_id: str, ofertado: bool):
        # Remove do modelo
        if ofertado:
            self.simulacao.remover_ofertado(item_id)
            items = self.simulacao.ofertados
            frames = self.ofertados_frames
        else:
            self.simulacao.remover_recebido(item_id)
            items = self.simulacao.recebidos
            frames = self.recebidos_frames
        # Re-renderiza todos os slots
        for idx, (frame_slot, total_var) in enumerate(frames):
            for w in frame_slot.winfo_children():
                w.destroy()
            if idx < len(items):
                self._renderizar_slot(ofertado, idx, items[idx])
            else:
                btn = ctk.CTkButton(
                    frame_slot,
                    text="+ Add",
                    command=(lambda i=idx: self._adicionar_ofertado(i) if ofertado else self._adicionar_recebido(i))
                )
                btn.place(relx=0.5, rely=0.5, anchor="center")
        # atualiza totais
        self._atualizar_totais()

    def _registrar_simulacao(self):
        # Verifica desequilíbrio
        if self.simulacao.esta_desequilibrada():
            # TODO: abrir modal de alerta antes de confirmar
            return
        # TODO: persistir simulação em backend ou local
        return messagebox.showinfo("Simulação", "Simulação registrada com sucesso!")
