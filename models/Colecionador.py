from uuid import uuid4
from typing import List
from models.ItemInventario import ItemInventario
from models.Carta import Carta
# from models.Troca import Troca  # Descomente se existir a classe Troca

class Colecionador:
    """
    Representa um colecionador de cartas, com informações pessoais, inventário, histórico de trocas e lista de desejos.
    """

    def __init__(
        self,
        nome: str,
        email: str,
        senha: str,
        id: str = None,
        inventario: List[ItemInventario] = None,
        listaDesejos: List[Carta] = None,
        historicoTrocas: list = None  # Troque para List[Troca] se a classe Troca existir
    ):
        self.__id = id if id is not None else str(uuid4())
        self.__nome = nome
        self.__email = email
        self.__senha = senha
        self.__inventario = inventario if inventario is not None else []
        self.__listaDesejos = listaDesejos if listaDesejos is not None else []
        self.__historicoTrocas = historicoTrocas if historicoTrocas is not None else []

    # Getters e Setters ID
    def get_id(self) -> str:
        return self.__id

    def set_id(self, id: str):
        self.__id = id

    # Getters e Setters Nome
    def get_nome(self) -> str:
        return self.__nome

    def set_nome(self, nome: str):
        self.__nome = nome

    # Getters e Setters Email
    def get_email(self) -> str:
        return self.__email

    def set_email(self, email: str):
        self.__email = email

    # Getters e Setters Senha
    def get_senha(self) -> str:
        return self.__senha

    def set_senha(self, senha: str):
        self.__senha = senha

    # Getters e Setters Inventário
    def get_inventario(self) -> List[ItemInventario]:
        return self.__inventario

    def set_inventario(self, inventario: List[ItemInventario]):
        self.__inventario = inventario

    # Getters e Setters Lista de Desejos
    def get_listaDesejos(self) -> List[Carta]:
        return self.__listaDesejos

    def set_listaDesejos(self, listaDesejos: List[Carta]):
        self.__listaDesejos = listaDesejos

    # Getters e Setters Histórico de Trocas
    def get_historicoTrocas(self) -> list:  # Troque para List[Troca] se a classe Troca existir
        return self.__historicoTrocas

    def set_historicoTrocas(self, historicoTrocas: list):  # Troque para List[Troca] se a classe Troca existir
        self.__historicoTrocas = historicoTrocas

    def adicionar_item_inventario(self, item: ItemInventario):
        """
        Adiciona um ItemInventario ao final do inventário do colecionador.
        """
        self.__inventario.append(item)