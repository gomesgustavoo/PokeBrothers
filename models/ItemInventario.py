from uuid import uuid4
from models.Carta import Carta

class ItemInventario:
    """
    Representa um item no inventário, associando uma Carta, um id único e uma quantidade.
    """

    def __init__(self, carta: Carta, quantidade: int = 1, id: str = None):
        self.__id = id if id is not None else str(uuid4())
        self.__carta = carta
        self.__quantidade = quantidade

    # Getter e Setter para id
    def get_id(self) -> str:
        return self.__id

    def set_id(self, id: str):
        self.__id = id

    # Getter e Setter para carta
    def get_carta(self) -> Carta:
        return self.__carta

    def set_carta(self, carta: Carta):
        self.__carta = carta

    # Getter e Setter para quantidade
    def get_quantidade(self) -> int:
        return self.__quantidade

    def set_quantidade(self, quantidade: int):
        self.__quantidade = quantidade

    def get_carta_id(self):
        """
        Retorna o id da carta associada a este item do inventário.
        """
        return self.__carta.get_id()