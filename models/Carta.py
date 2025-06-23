from uuid import uuid4


class Carta:
    """
    Modelo que representa uma carta de Pokémon,
    seguindo o padrão MVC para separar domínio da UI e serviços.
    """
    def __init__(
        self,
        id: str,
        nome: str,
        tipo: str,
        raridade: str,
        colecao: str,
        preco_dolar: float,
        preco_real: float,
        imagem_url: str
    ):
        self.__id = id
        self.__nome = nome
        self.__tipo = tipo
        self.__raridade = raridade
        self.__colecao = colecao
        self.__preco_dolar = preco_dolar
        self.__preco_real = preco_real
        self.__imagem_url = imagem_url

    def get_id(self):
        return self.__id

    def set_id(self, id: str):
        self.__id = id

    def get_nome(self):
        return self.__nome

    def set_nome(self, nome: str):
        self.__nome = nome

    def get_tipo(self):
        return self.__tipo

    def set_tipo(self, tipo: str):
        self.__tipo = tipo

    def get_raridade(self):
        return self.__raridade

    def set_raridade(self, raridade: str):
        self.__raridade = raridade

    def get_colecao(self):
        return self.__colecao

    def set_colecao(self, colecao: str):
        self.__colecao = colecao

    def get_preco_dolar(self):
        return self.__preco_dolar

    def set_preco_dolar(self, preco: float):
        self.__preco_dolar = preco

    def get_preco_real(self):
        return self.__preco_real

    def set_preco_real(self, preco: float):
        self.__preco_real = preco

    def get_imagem_url(self):
        return self.__imagem_url

    def set_imagem_url(self, url: str):
        self.__imagem_url = url

    @classmethod
    def from_api_data(cls, c: dict, dollar_to_real) -> "Carta":
        """
        Cria uma instância de Carta a partir do JSON retornado pela API.
        """
        tipos = ", ".join(c.get("types", []))
        prices = c.get("tcgplayer", {}).get("prices", {})
        price_info = prices.get("holofoil") or prices.get("normal") or {}
        usd = price_info.get("market") or price_info.get("mid") or 0.0
        brl = usd * dollar_to_real

        return cls(
            id=c.get("id", str(uuid4())),
            nome=c.get("name", ""),
            tipo=tipos,
            raridade=c.get("rarity", ""),
            colecao=c.get("set", {}).get("name", ""),
            preco_dolar=usd,
            preco_real=brl,
            imagem_url=c.get("images", {}).get("small", "")
        )