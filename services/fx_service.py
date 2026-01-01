import httpx
import asyncio

async def collect_base_currencies():
    base_currencies = ["EUR"]
    rest_of_currencies = await fetch_quotes("EUR")
    base_currencies.extend(list(rest_of_currencies))
    return base_currencies
    

async def fetch_quotes(base_quote: str):
    URL = "https://api.frankfurter.dev/v1/latest"
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(URL, params={"base": base_quote})
        response.raise_for_status()
        data = response.json()
        if "rates" not in data:
            raise ValueError("Invalid API response")
        return data["rates"]
    
async def collect_data():
    list_of_currencies = await collect_base_currencies()
    base = []
    for currency in list_of_currencies:
        currency_rates = await fetch_quotes(currency)
        rates_in = [
            {
                "base_currency": currency,
                "quote_currency": k,
                "rate": v
            }
            for k, v in currency_rates.items()
        ]
        base.extend(rates_in)
    return base