# models/item_troca.py
from uuid import uuid4
from models.Carta import Carta

class ItemTroca:
    """
    Representa um item em uma troca, associando uma Carta à quantidade desejada.
    """
    def __init__(self, carta: Carta, quantidade: int = 1):
        self.id = str(uuid4())  # identificador único do item de troca
        self.carta = carta
        self.quantidade = quantidade

    def preco_total(self) -> float:
        """
        Retorna o preço total deste item (preço da carta em reais * quantidade).
        """
        return self.carta.get_preco_real() * self.quantidade