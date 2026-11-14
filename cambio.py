from datetime import date, timedelta

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


def buscar_historico(dias=30, moedas="BRL,EUR,USD"):
    fim = date.today()
    inicio = fim - timedelta(days=dias)
    url = (
        f"https://api.frankfurter.dev/v1/{inicio.isoformat()}..{fim.isoformat()}"
        f"?base=GBP&symbols={moedas}"
    )
    try:
        resposta = requests.get(url, timeout=10)
        if resposta.status_code == 200:
            return resposta.json()["rates"]
        print(f"Erro ao buscar histórico. Status code: {resposta.status_code}")
        return None
    except requests.exceptions.RequestException:
        print("Aviso: não foi possível buscar o histórico do câmbio.")
        return None


def calcular_resumos(rates, historico):
    resumos = {}
    for moeda, hoje in rates.items():
        valores = [dia[moeda] for dia in historico.values()]
        media = sum(valores) / len(valores)
        resumos[moeda] = {
            "hoje": hoje,
            "media": media,
            "variacao": (hoje - media) / media * 100,
        }
    return resumos


if __name__ == "__main__":
    rates = buscar_cambio()
    historico = buscar_historico(30)
    if rates is not None and historico is not None:
        for moeda, r in calcular_resumos(rates, historico).items():
            print(
                f"{moeda} hoje: {r['hoje']} | média: {r['media']:.4f} "
                f"| {r['variacao']:+.1f}%"
            )
        print(f"Pontos em 365 dias: {len(buscar_historico(365))}")
