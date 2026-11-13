import requests

from datetime import date, timedelta

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


def buscar_historico_brl():
    fim = date.today()
    inicio = fim - timedelta(days=30)
    url = f"https://api.frankfurter.dev/v1/{inicio.isoformat()}..{fim.isoformat()}?base=GBP&symbols=BRL"
    try:
        resposta = requests.get(url, timeout=10)
        if resposta.status_code == 200:
            return resposta.json()["rates"]
        print(f"Erro ao buscar histórico do câmbio. Status code: {resposta.status_code}")
        return None
    except requests.exceptions.RequestException:
        print("Aviso: não foi possível buscar o histórico das taxas de câmbio.")
        return None


if __name__ == "__main__":
    rates = buscar_cambio()
    if rates is not None:
        for moeda, valor in rates.items():
            print(f"1 GBP = {valor} {moeda}")

    historico = buscar_historico_brl()


def resumo_brl():
    rates = buscar_cambio()
    historico = buscar_historico_brl()
    if rates is None or historico is None:
        return None
    valores = [dia["BRL"] for dia in historico.values()]
    media = sum(valores) / len(valores)
    hoje = rates["BRL"]
    variacao = (hoje - media) / media * 100
    return {"hoje": hoje, "media": media, "variacao": variacao}


if __name__ == "__main__":
    resumo = resumo_brl()
    if resumo is not None:
        print(
            f"BRL hoje: {resumo['hoje']} | média 30 dias: "
            f"{resumo['media']:.2f} | {resumo['variacao']:+.1f}%"
        )