from typing import List
from models.ItemTroca import ItemTroca

class SimulacaoTroca:
    """
    Modelo para gerenciar o estado de uma simulação de troca,
    com listas de itens oferecidos e recebidos.
    """
    def __init__(self, limite_percentual: float = 10.0):
        # listas privadas de itens ofertados e recebidos
        self._ofertados: List[ItemTroca] = []
        self._recebidos: List[ItemTroca] = []
        # limite percentual para considerar a troca desequilibrada
        self._limite_percentual: float = limite_percentual
        # atributo de equilíbrio percentual, sempre recalculado
        self._equilibrio: float = 0.0

    @property
    def ofertados(self) -> List[ItemTroca]:
        return list(self._ofertados)

    @property
    def recebidos(self) -> List[ItemTroca]:
        return list(self._recebidos)

    @property
    def limite_percentual(self) -> float:
        return self._limite_percentual

    @limite_percentual.setter
    def limite_percentual(self, valor: float):
        self._limite_percentual = valor
        self._recalcular_equilibrio()

    @property
    def equilibrio(self) -> float:
        """
        Diferença percentual entre o total ofertado e recebido,
        arredondada com duas casas decimais.
        """
        return self._equilibrio

    def adicionar_ofertado(self, item: ItemTroca):
        """
        Adiciona um item à lista de itens ofertados e atualiza equilíbrio.
        """
        self._ofertados.append(item)
        self._recalcular_equilibrio()

    def remover_ofertado(self, item_id: str):
        """
        Remove um item dos ofertados pelo seu ID e atualiza equilíbrio.
        """
        self._ofertados = [i for i in self._ofertados if i.get_id() != item_id]
        self._recalcular_equilibrio()

    def adicionar_recebido(self, item: ItemTroca):
        """
        Adiciona um item à lista de itens recebidos e atualiza equilíbrio.
        """
        self._recebidos.append(item)
        self._recalcular_equilibrio()

    def remover_recebido(self, item_id: str):
        """
        Remove um item dos recebidos pelo seu ID e atualiza equilíbrio.
        """
        self._recebidos = [i for i in self._recebidos if i.get_id() != item_id]
        self._recalcular_equilibrio()

    def total_ofertados(self) -> float:
        """
        Soma dos preços de todos os itens ofertados.
        """
        return sum(item.preco_total() for item in self._ofertados)

    def total_recebidos(self) -> float:
        """
        Soma dos preços de todos os itens recebidos.
        """
        return sum(item.preco_total() for item in self._recebidos)

    def diferenca_percentual(self) -> float:
        """
        Calcula a diferença percentual entre o total ofertado e recebido:
        (ofertado - recebido) / recebido * 100.
        Retorna 0.0 se o total recebido for zero.
        O valor é arredondado para duas casas decimais.
        """
        total_r = self.total_recebidos()
        if total_r == 0:
            return 0.0
        total_o = self.total_ofertados()
        diff = (total_o - total_r) / total_r * 100
        return round(diff, 2)

    def esta_desequilibrada(self) -> bool:
        """
        Verifica se a troca ultrapassa o limite percentual configurado.
        """
        return abs(self._equilibrio) > self._limite_percentual

    def _recalcular_equilibrio(self):
        """
        Atualiza o atributo de equilíbrio com base nos totais atuais.
        """
        self._equilibrio = self.diferenca_percentual()
