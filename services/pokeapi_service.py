import requests
from uuid import uuid4
import math
# substitua pela sua chave
API_KEY = "b85a009f-df35-4234-aa2d-0f4b6799a776"
BASE_URL = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": API_KEY}
# ajuste conforme a cotação real
DOLLAR_TO_REAL = 5.0

def fetch_card_data(name: str, page: int = 1) -> tuple[list[dict], int]:
    params = {
        "q": f'name:*{name.title()}*',
        "pageSize": 20,
        "page": page
    }
    resp = requests.get(f"{BASE_URL}/cards", headers=HEADERS, params=params)
    if resp.status_code != 200:
        return [], 1

    data = resp.json()
    
    items = data.get("data", [])
    total_count = data.get("totalCount", len(items))
    total_pages = math.ceil(total_count / 20)

    cards = []
    for c in items:
        tipos = ", ".join(c.get("types", []))
        prices = c.get("tcgplayer", {}).get("prices", {})
        price_info = prices.get("holofoil") or prices.get("normal") or {}
        usd = price_info.get("market") or price_info.get("mid") or 0.0
        brl = usd * DOLLAR_TO_REAL

        cards.append({
            "id": c["id"],
            "nome": c["name"],
            "tipo": tipos,
            "raridade": c.get("rarity", ""),
            "colecao": c.get("set", {}).get("name", ""),
            "preco_dolar": usd,
            "preco_real": brl,
            "imagem_url": c.get("images", {}).get("small", "")
        })
    
    return cards, total_pages


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
