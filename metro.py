import requests

URL = "https://api.tfl.gov.uk/Line/Mode/tube/Status"


def buscar_metro():
    try:
        resposta = requests.get(URL, timeout=10)
        if resposta.status_code == 200:
            return [
                {
                    "linha": item["name"],
                    "status": item["lineStatuses"][0]["statusSeverityDescription"],
                }
                for item in resposta.json()
            ]
        print(f"Erro ao buscar metrô. Status code: {resposta.status_code}")
        return None
    except requests.exceptions.RequestException as erro:
        print(
            f"Aviso: não foi possível buscar as informações do metrô. Detalhe: {erro}"
        )
        return None


if __name__ == "__main__":
    dados = buscar_metro()
    if dados is not None:
        for item in dados:
            print(f"{item['linha']}: {item['status']}")
