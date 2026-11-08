import requests

url = "https://api.frankfurter.dev/v1/latest?base=GBP&symbols=BRL,EUR,USD"
resposta = requests.get(url)
dados = resposta.json()

brl = dados['rates']['BRL']
usd = dados['rates']['USD']
eur = dados['rates']['EUR']

print(f"1 GBP = {brl} BRL")
print(f"1 GBP = {usd} USD")
print(f"1 GBP = {eur} EUR")