# FUNCAO: BUSCAR DADOS DAS APIs

import requests  # request: biblioteca que permite fazer requisições HTTP em Python, ou seja, enviar solicitações para servidores web e receber respostas. É amplamente utilizada para interagir com APIs (Application Programming Interfaces) e obter dados de serviços online.

URL = (
    "https://api.open-meteo.com/v1/forecast"  # URL que fornece os valores de temperatura, precipitação e probabilidade de chuva para Woking, Inglaterra
    "?latitude=51.3190&longitude=-0.5589"  # coordenadas geográficas de Woking, Inglaterra (latitude e longitude) / latitude=51.3190&longitude=-0.5589
    "&current=temperature_2m,precipitation"  # parâmetros que indicam que queremos os valores de temperatura e precipitação atuais (em °C e mm, respectivamente)
    "&hourly=precipitation_probability&forecast_hours=6"  # parâmetros que indicam que queremos os valores de probabilidade de chuva nas próximas 6 horas (em %) / forecast_hours=6 indica que queremos os valores das próximas 6 horas
)


def buscar_clima():  # vai na API e pega os valores de temperatura, precipitação e probabilidade de chuva para Woking, Inglaterra
    try:
        resposta = requests.get(
            URL, timeout=10
        )  # TIMEOUT: caso a API demore mais de 10 segundos para responder, vai cair no except
        if (
            resposta.status_code == 200
        ):  # O status code 200 significa que a requisição foi bem sucedida e o servidor respondeu com sucesso (nao significa que o dado estaja bom)
            dados = resposta.json()  # converte a resposta da API em um dicionário Python (JSON) / dados é um dicionário com as informações do clima para Woking, Inglaterra
            return {  # retorna um dicionário com os valores de temperatura, precipitação e probabilidade de chuva para Woking, Inglaterra
                "temperatura": dados["current"][
                    "temperature_2m"
                ],  # pega o valor da temperatura atual em Woking, Inglaterra (em °C)
                "precipitacao": dados["current"][
                    "precipitation"
                ],  # pega o valor da precipitação atual em Woking, Inglaterra (em mm)
                "chance_chuva": max(
                    dados["hourly"]["precipitation_probability"]
                ),  # pega o valor máximo da probabilidade de chuva nas próximas 6 horas em Woking, Inglaterra (em %) / max() retorna o maior valor de uma lista
            }
        print(f"Erro ao buscar clima. Status code: {resposta.status_code}")
        return None  # Retorna None se o status code não for 200 (servidor respondeu mas disse nao ter conseguido processar a requisição)
    except requests.exceptions.RequestException:  # caso esteja fora de ar, sem internet ou qualquer outro problema de conexão, vai cair aqui
        print("Aviso: não foi possível buscar as informações do clima.")
        return None  # Retorna None se não conseguir buscar as informações do clima (servidor sem resposta, sem internet, etc)


if (
    __name__ == "__main__"
):  # se o arquivo for executado diretamente, vai buscar os valores de temperatura, precipitação e probabilidade de chuva para Woking, Inglaterra e imprimir os resultados
    clima = buscar_clima()
    if (
        clima is not None
    ):  # se os valores de temperatura, precipitação e probabilidade de chuva forem diferentes de None (ou seja, se a API respondeu com sucesso)
        print(f"Temperatura atual em Woking: {clima['temperatura']}°C")
        print(f"Precipitação atual em Woking: {clima['precipitacao']} mm")
        print(f"Probabilidade de chuva (6h): {clima['chance_chuva']}%")

# RODAR: python3 clima.py
