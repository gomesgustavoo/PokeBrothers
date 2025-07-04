from uuid import uuid4
from typing import List
from models.ItemInventario import ItemInventario
from models.Carta import Carta
from models.ItemListadeDesejos import ItemListadeDesejos
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
        historicoTrocas: list = None,  # Troque para List[Troca] se a classe Troca existir
        inventario_repo=None,
        listaDesejos_repo=None
    ):
        from services.inventario_repo import InventarioRepo
        from services.lista_desejos_repo import ListaDesejosRepo
        self.__id = id if id is not None else str(uuid4())
        self.__nome = nome
        self.__email = email
        self.__senha = senha
        self.__inventario = inventario if inventario is not None else []
        self.__listaDesejos = listaDesejos if listaDesejos is not None else []
        self.__historicoTrocas = historicoTrocas if historicoTrocas is not None else []
        self.inventario_repo = inventario_repo or InventarioRepo()
        self.listaDesejos_repo = listaDesejos_repo or ListaDesejosRepo()  # Use o mesmo repo ou crie um específico

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

    def set_listaDesejos(self, listaDesejos):
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

    def atualizar_item_inventario(self, item: ItemInventario):
        # Atualiza em memória e persiste
        for i, it in enumerate(self.__inventario):
            if it.get_id() == item.get_id():
                self.__inventario[i] = item
                break
        self.inventario_repo.atualizar_item(item)

    def adicionar_item_inventario_persistente(self, item: ItemInventario):
        self.__inventario.append(item)
        self.inventario_repo.adicionar_item(item, self.get_id())

    def remover_item_inventario(self, item: ItemInventario):
        self.__inventario = [i for i in self.__inventario if i.get_id() != item.get_id()]
        self.inventario_repo.remover_item(item.get_id())

    def carregar_inventario_persistente(self):
        inventario = self.inventario_repo.carregar_inventario(self.get_id())
        self.set_inventario(inventario)

    def get_lista_desejos(self) -> List[ItemListadeDesejos]:
        return self.__listaDesejos

    def set_lista_desejos(self, lista: List[ItemListadeDesejos]):
        self.__listaDesejos = lista

    def adicionar_item_lista_desejos_persistente(self, item: ItemListadeDesejos):
        """
        Adiciona um ItemListadeDesejos à lista e persiste no banco.
        """
        self.__listaDesejos.append(item)
        self.listaDesejos_repo.adicionar_item(item, self.get_id())

    def atualizar_item_lista_desejos(self, item: ItemListadeDesejos):
        """
        Atualiza em memória e persiste.
        """
        for i, it in enumerate(self.__listaDesejos):
            if it.get_id() == item.get_id():
                self.__listaDesejos[i] = item
                break
        self.listaDesejos_repo.atualizar_item(item)

    def remover_item_lista_desejos(self, item: ItemListadeDesejos):
        """
        Remove da lista em memória e do banco.
        """
        self.__listaDesejos = [
            it for it in self.__listaDesejos if it.get_id() != item.get_id()
        ]
        self.listaDesejos_repo.remover_item(item.get_id())

    def carregar_lista_desejos_persistente(self):
        """
        Carrega do banco a lista de desejos associada a este colecionador.
        """
        lista = self.listaDesejos_repo.carregar_lista(self.get_id())
        self.set_listaDesejos(lista)

    @classmethod
    def from_db(cls, colecionador_id):
        import sqlite3
        DB_NAME = "colecionadores.db"
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT id, nome, email, senha FROM colecionadores WHERE id=?", (colecionador_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        colecionador = cls(
            nome=row[1],
            email=row[2],
            senha=row[3],
            id=row[0]
        )
        colecionador.carregar_inventario_persistente()
        colecionador.carregar_lista_desejos_persistente()
        return colecionador