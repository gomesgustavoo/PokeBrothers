# models/item_troca.py
from uuid import uuid4
from models.Carta import Carta

class ItemTroca:
    """
    Representa um item em uma troca, associando uma Carta à quantidade desejada.
    """
    def __init__(self, carta: Carta, quantidade: int = 1):
        self.__id = str(uuid4())  # identificador único do item de troca
        self.__carta = carta
        self.__quantidade = quantidade

    def get_id(self):
        return self.__id

    def set_id(self, id: str):
        self.__id = id

    def get_carta(self):
        return self.__carta

    def set_carta(self, carta: Carta):
        self.__carta = carta

    def get_quantidade(self):
        return self.__quantidade

    def set_quantidade(self, quantidade: int):
        self.__quantidade = quantidade

    def preco_total(self) -> float:
        """
        Retorna o preço total deste item (preço da carta em reais * quantidade).
        """
        return self.__carta.get_preco_real() * self.__quantidade