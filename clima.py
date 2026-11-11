import requests

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=51.3190&longitude=-0.5589"
    "&current=temperature_2m,precipitation"
    "&hourly=precipitation_probability&forecast_hours=6"
)


def buscar_clima():
    try:
        resposta = requests.get(URL, timeout=10)
        if resposta.status_code == 200:
            dados = resposta.json()
            return {
                "temperatura": dados["current"]["temperature_2m"],
                "precipitacao": dados["current"]["precipitation"],
                "chance_chuva": max(dados["hourly"]["precipitation_probability"]),
            }
        print(f"Erro ao buscar clima. Status code: {resposta.status_code}")
        return None
    except requests.exceptions.RequestException:
        print("Aviso: não foi possível buscar as informações do clima.")
        return None


if __name__ == "__main__":
    clima = buscar_clima()
    if clima is not None:
        print(f"Temperatura atual em Woking: {clima['temperatura']}°C")
        print(f"Precipitação atual em Woking: {clima['precipitacao']} mm")
        print(f"Probabilidade de chuva (6h): {clima['chance_chuva']}%")
