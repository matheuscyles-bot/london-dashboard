import requests

url = "https://api.frankfurter.dev/v1/latest?base=GBP&symbols=BRL,EUR,USD"
resposta = requests.get(url)
dados = resposta.json()

for moeda, valor in dados["rates"].items():
    print(f"1 GBP = {valor} {moeda}")

