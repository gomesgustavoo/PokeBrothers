import sqlite3
from models.ItemListadeDesejos import ItemListadeDesejos
from services.pokeapi_service import buscar_carta_por_id

# Usa o mesmo arquivo de DB do inventário
LISTA_DESEJOS_DB = 'inventario.db'

class ListaDesejosRepo:
    def __init__(self, db_path=LISTA_DESEJOS_DB):
        self.__db_path = db_path

    def get_db_path(self):
        return self.__db_path

    def carregar_lista(self, colecionador_id):
        """
        Carrega todos os itens da lista de desejos para um dado colecionador.
        Retorna uma lista de ItemListadeDesejos.
        """
        lista = []
        conn = sqlite3.connect(self.__db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, carta_id FROM lista_desejos WHERE colecionador_id=?",
            (colecionador_id,)
        )
        rows = cur.fetchall()
        conn.close()

        for row in rows:
            item_id, carta_id = row
            carta = buscar_carta_por_id(carta_id)
            if carta:
                lista.append(
                    ItemListadeDesejos(carta, id=item_id)
                )
        return lista

    def adicionar_item(self, item_lista, colecionador_id):
        """
        Insere um novo ItemListadeDesejos na tabela.
        """
        conn = sqlite3.connect(self.__db_path)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO lista_desejos (id, colecionador_id, carta_id) VALUES (?, ?, ?)",
            (
                item_lista.get_id(),
                colecionador_id,
                item_lista.get_carta().get_id(),
            )
        )
        conn.commit()
        conn.close()

    def remover_item(self, item_id):
        """
        Remove um ItemListadeDesejos pelo seu ID.
        """
        conn = sqlite3.connect(self.__db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM lista_desejos WHERE id=?", (item_id,))
        conn.commit()
        conn.close()
