from uuid import uuid4
from models.Carta import Carta

class ItemListadeDesejos:
    """
    Representa um item na lista de desejos, associando uma Carta, um id único e uma quantidade desejada.
    """

    def __init__(self, carta: Carta, quantidade: int = 1, id: str = None):
        """
        Inicializa um item da lista de desejos.

        Args:
            carta (Carta): O objeto da carta desejada.
            quantidade (int): A quantidade de cópias da carta desejada.
            id (str, optional): O ID único do item. Se não for fornecido, um novo UUID será gerado.
        """
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

