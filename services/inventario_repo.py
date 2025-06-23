import sqlite3
from models.ItemInventario import ItemInventario
from services.pokeapi_service import buscar_carta_por_id

INVENTARIO_DB = 'inventario.db'

class InventarioRepo:
    def __init__(self, db_path=INVENTARIO_DB):
        self.__db_path = db_path

    def get_db_path(self):
        return self.__db_path

    def carregar_inventario(self, colecionador_id):
        inventario = []
        conn = sqlite3.connect(self.__db_path)
        cur = conn.cursor()
        cur.execute("SELECT id, carta_id, quantidade FROM inventario WHERE colecionador_id=?", (colecionador_id,))
        rows = cur.fetchall()
        conn.close()
        for row in rows:
            carta = buscar_carta_por_id(row[1])
            if carta:
                inventario.append(ItemInventario(carta, quantidade=row[2], id=row[0]))
        return inventario

    def adicionar_item(self, item_inventario, colecionador_id):
        conn = sqlite3.connect(self.__db_path)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO inventario (id, colecionador_id, carta_id, quantidade) VALUES (?, ?, ?, ?)",
            (item_inventario.get_id(), colecionador_id, item_inventario.get_carta().get_id(), item_inventario.get_quantidade())
        )
        conn.commit()
        conn.close()

    def remover_item(self, item_id):
        conn = sqlite3.connect(self.__db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM inventario WHERE id=?", (item_id,))
        conn.commit()
        conn.close()

    def atualizar_item(self, item_inventario):
        conn = sqlite3.connect(self.__db_path)
        cur = conn.cursor()
        cur.execute(
            "UPDATE inventario SET quantidade=? WHERE id=?",
            (item_inventario.get_quantidade(), item_inventario.get_id())
        )
        conn.commit()
        conn.close()
