import customtkinter as ctk
from models.Simulacao import SimulacaoTroca
from pages.search_cards import SearchCardsPage
from pages.local_search_cards import LocalSearchCardsPage
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

    def __init__(self, master, inventario=None, lista_desejos=None):
        super().__init__(master, corner_radius=12)
        self.inventario = inventario or []
        self.lista_desejos = lista_desejos or []
        self.simulacao = SimulacaoTroca(limite_percentual=10.0)
        self.ofertados_frames = []
        self.recebidos_frames = []
        self.var_total_ofertados = ctk.StringVar(value="Valor total: R$0,00")
        self.var_total_recebidos = ctk.StringVar(value="Valor total: R$0,00")
        self.var_diff_ofertados = ctk.StringVar(value="0%")
        self.var_diff_recebidos = ctk.StringVar(value="0%")
        self.badge_of = None
        self.badge_rc = None
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

        # Botão de registrar simulação
        botao_salvar = ctk.CTkButton(
            self,
            text="Registrar Simulação",
            command=self._registrar_simulacao
        )
        botao_salvar.grid(row=2, column=0, columnspan=2, pady=(10, 20))

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
            pady=4
        )
        badge.grid(row=3, column=0, columnspan=self.COLUNAS, pady=(0,10))
        # Armazenar referência para atualizar cor depois
        if "Oferecidas" in titulo:
            self.badge_of = badge
        else:
            self.badge_rc = badge


    def _adicionar_ofertado(self, indice):
        # abre modal de busca, passando callback
        topo = ctk.CTkToplevel(self)
        topo.title("Buscar Carta Ofertada")
        topo.geometry("800x600")
        SearchCardsPage(
            master=topo,
            on_card_select=lambda carta: self._selecionar_ofertado(carta, indice, topo)
        ).pack(fill="both", expand=True)

    def _adicionar_recebido(self, indice):
        topo = ctk.CTkToplevel(self)
        topo.title("Buscar Carta Recebida")
        topo.geometry("800x600")
        SearchCardsPage(
            master=topo,
            on_card_select=lambda carta: self._selecionar_recebido(carta, indice, topo)
        ).pack(fill="both", expand=True)

    def _selecionar_do_inventario(self, indice):
        """Abre busca limitada às cartas do inventário."""
        if not self.inventario:
            return
        cartas = [item.get_carta() for item in self.inventario]
        topo = ctk.CTkToplevel(self)
        topo.title("Inventário")
        topo.geometry("800x600")
        LocalSearchCardsPage(
            master=topo,
            cards=cartas,
            on_card_select=lambda c: self._selecionar_ofertado(c, indice, topo)
        ).pack(fill="both", expand=True)

    def _selecionar_da_lista_desejos(self, indice):
        """Abre busca limitada às cartas da lista de desejos."""
        if not self.lista_desejos:
            return
        topo = ctk.CTkToplevel(self)
        topo.title("Lista de Desejos")
        topo.geometry("800x600")
        LocalSearchCardsPage(
            master=topo,
            cards=self.lista_desejos,
            on_card_select=lambda c: self._selecionar_recebido(c, indice, topo)
        ).pack(fill="both", expand=True)


    def _atualizar_totais(self):
        # atualiza totais
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
        else:
            self.badge_of.configure(fg_color="#5EF06A")
            self.badge_rc.configure(fg_color="#5EF06A")

    def _selecionar_ofertado(self, carta:Carta, indice, topo):
        topo.destroy()  
        item = ItemTroca(carta)
        # adiciona na simulação
        self.simulacao.adicionar_ofertado(item)
        # renderiza no slot apropriado
        self._renderizar_slot(oferecido=True, indice=indice, item=item)
        self._atualizar_totais()

    def _selecionar_recebido(self, carta:Carta, indice, topo):
        topo.destroy()
        item = ItemTroca(carta)
        self.simulacao.adicionar_recebido(item)
        self._renderizar_slot(oferecido=False, indice=indice, item=item)
        self._atualizar_totais()

    def _renderizar_slot(self, oferecido: bool, indice: int, item: ItemTroca):
        """
        Limpa o frame do slot, exibe imagem, quantidade e botão de remover.
        """
        lista = self.ofertados_frames if oferecido else self.recebidos_frames
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
        ctk.CTkLabel(slot_frame, text=f"R${item.carta.preco_real}").pack()
        # botão remover
        ctk.CTkButton(
            slot_frame,
            text="X",
            fg_color="red",
            command=lambda i=item.id, o=oferecido: self._remover_item(i, o)
        ).pack(pady=(5,0))

    def _remover_item(self, item_id: str, oferecido: bool):
        # Remove do modelo
        if oferecido:
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
                self._renderizar_slot(oferecido, idx, items[idx])
            else:
                btn = ctk.CTkButton(
                    frame_slot,
                    text="+ Add",
                    command=(lambda i=idx: self._adicionar_ofertado(i) if oferecido else self._adicionar_recebido(i))
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
