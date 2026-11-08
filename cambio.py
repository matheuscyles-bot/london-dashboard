import requests

URL = "https://api.frankfurter.dev/v1/latest?base=GBP&symbols=BRL,EUR,USD"


def buscar_cambio():
    try:
        resposta = requests.get(URL, timeout=10)
        if resposta.status_code == 200:
            return resposta.json()["rates"]
        print(f"Erro ao buscar câmbio. Status code: {resposta.status_code}")
        return None
    except requests.exceptions.RequestException:
        print("Aviso: não foi possível buscar as taxas de câmbio.")
        return None


if __name__ == "__main__":
    rates = buscar_cambio()
    if rates is not None:
        for moeda, valor in rates.items():
            print(f"1 GBP = {valor} {moeda}")


def buscar_clima():
    try:
        resposta = requests.get("https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=London", timeout=10)
        if resposta.status_code == 200:
            return resposta.json()
        print(f"Erro ao buscar clima. Status code: {resposta.status_code}")
        return None
    except requests.exceptions.RequestException:
        print("Aviso: não foi possível buscar as informações do clima.")
        return None