import requests

class ExchangeService:
    """
    Serviço para obter taxa de câmbio USD → BRL usando a API AwesomeAPI.
    """
    API_URL = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'

    @staticmethod
    def fetch_usd_to_brl(timeout: float = 5.0) -> float:
        
        response = requests.get(ExchangeService.API_URL, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        # Estrutura: { "USDBRL": { "bid": "5.1234", ... } }
        usdbrl = data.get('USDBRL') or data.get('USDBRL', {})
        bid_str = usdbrl.get('bid')
        if bid_str is None:
            raise ValueError("Resposta da API não contém campo 'bid'")
        return float(bid_str)
