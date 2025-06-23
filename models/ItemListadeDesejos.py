from uuid import uuid4
from models.Carta import Carta

class ItemListadeDesejos:
    """
    Representa um item na lista de desejos, associando uma Carta, um id único.
    """

    def __init__(self, carta: Carta, id: str = None):
        self.__id = id if id is not None else str(uuid4())
        self.__carta = carta

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

