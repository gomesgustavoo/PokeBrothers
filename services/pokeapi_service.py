import requests
from uuid import uuid4
import math

from models.Carta import Carta
from services.dollarapi_service import ExchangeService
# substitua pela sua chave
API_KEY = "b85a009f-df35-4234-aa2d-0f4b6799a776"
BASE_URL = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": API_KEY}

def fetch_card_data(name: str, page: int = 1, tipo: str = "", raridade: str = "", colecao: str = "") -> tuple[list[dict], int]:


    query_parts = [f'name:*{name.title()}*']
    if tipo:
        query_parts.append(f'types:{tipo}')
    if raridade:
        query_parts.append(f'rarity:"{raridade}"')
    if colecao:
        query_parts.append(f'set.name:"{colecao}"')

    query = " AND ".join(query_parts)
    params = {
        "q": query,
        "pageSize": 20,
        "page": page
    }
    resp = requests.get(f"{BASE_URL}/cards", headers=HEADERS, params=params)
    if resp.status_code != 200:
        return [], 1

    data = resp.json()

    dollar_to_real = ExchangeService.fetch_usd_to_brl()
    print("Valor do dollar:" + str(dollar_to_real))
    
    items = data.get("data", [])
    total_count = data.get("totalCount", len(items))
    total_pages = math.ceil(total_count / 20)

    cards = []
    for c in items:

        cards = [Carta.from_api_data(c, dollar_to_real) for c in items]

    
    return cards, total_pages

def fetch_all_collections() -> list[str]:
    resp = requests.get(f"{BASE_URL}/sets", headers=HEADERS)
    if resp.status_code != 200:
        return []

    data = resp.json()
    return sorted([item["name"] for item in data.get("data", [])])

def fetch_all_types() -> list[str]:
    resp = requests.get(f"{BASE_URL}/types", headers=HEADERS)
    if resp.status_code != 200:
        return []
    data = resp.json()
    return sorted(item for item in data.get("data", []) )

def fetch_all_rarities() -> list[str]:
    resp = requests.get(f"{BASE_URL}/rarities", headers=HEADERS)
    if resp.status_code != 200:
        return []
    
    data = resp.json()
    return sorted(item for item in data.get("data", []) )


def import_card_to_db(name: str) -> bool:
    """
    Se encontrar a carta na API, grava via add_carta().
    Retorna True se gravou, False caso contrário.
    """
    data = fetch_card_data(name)
    if not data:
        return False

    # add_carta(
    #     nome=data["nome"],
    #     tipo=data["tipo"],
    #     raridade=data["raridade"],
    #     colecao=data["colecao"],
    #     preco_dolar=data["preco_dolar"],
    #     preco_real=data["preco_real"]
    # )
    return True
