import requests

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=51.5072&longitude=-0.1276&current=temperature_2m"
)


def buscar_clima():
    try:
        resposta = requests.get(URL, timeout=10)
        if resposta.status_code == 200:
            return resposta.json()
        print(f"Erro ao buscar clima. Status code: {resposta.status_code}")
        return None
    except requests.exceptions.RequestException:
        print("Aviso: não foi possível buscar as informações do clima.")
        return None


if __name__ == "__main__":
    clima = buscar_clima()
    if clima is not None:
        print(clima)