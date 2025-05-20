from typing import List
from models.ItemTroca import ItemTroca

class SimulacaoTroca:
    """
    Modelo para gerenciar o estado de uma simulação de troca,
    com listas de itens oferecidos e recebidos.
    """
    def __init__(self, limite_percentual: float = 10.0):
        # itens que o usuário oferece
        self.ofertados: List[ItemTroca] = []
        # itens que o usuário espera receber
        self.recebidos: List[ItemTroca] = []
        # percentual de tolerância para considerar a troca desequilibrada
        self.limite_percentual = limite_percentual

    def adicionar_ofertado(self, item: ItemTroca):
        """
        Adiciona um item à lista de itens ofertados.
        """
        self.ofertados.append(item)

    def remover_ofertado(self, item_id: str):
        """
        Remove um item dos ofertados pelo seu ID.
        """
        self.ofertados = [i for i in self.ofertados if i.id != item_id]

    def adicionar_recebido(self, item: ItemTroca):
        """
        Adiciona um item à lista de itens recebidos.
        """
        self.recebidos.append(item)

    def remover_recebido(self, item_id: str):
        """
        Remove um item dos recebidos pelo seu ID.
        """
        self.recebidos = [i for i in self.recebidos if i.id != item_id]

    def total_ofertados(self) -> float:
        """
        Soma dos preços de todos os itens ofertados.
        """
        return sum(item.preco_total() for item in self.ofertados)

    def total_recebidos(self) -> float:
        """
        Soma dos preços de todos os itens recebidos.
        """
        return sum(item.preco_total() for item in self.recebidos)

    def diferenca_percentual(self) -> float:
        """
        Calcula a diferença percentual entre o total ofertado e recebido:
        (ofertado - recebido) / recebido * 100.
        Retorna 0 se o total recebido for zero.
        """
        total_r = self.total_recebidos()
        if total_r == 0:
            return 0.0
        total_o = self.total_ofertados()
        return (total_o - total_r) / total_r * 100

    def esta_desequilibrada(self) -> bool:
        """
        Verifica se a troca ultrapassa o limite percentual configurado.
        """
        return abs(self.diferenca_percentual()) > self.limite_percentual
