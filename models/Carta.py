from uuid import uuid4

from services.dollarapi_service import ExchangeService


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
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.raridade = raridade
        self.colecao = colecao
        self.preco_dolar = preco_dolar
        self.preco_real = preco_real
        self.imagem_url = imagem_url

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