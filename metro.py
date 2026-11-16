# FUNCAO: BUSCAR DADOS DAS APIs

import requests  # request: biblioteca que permite fazer requisições HTTP em Python, ou seja, enviar solicitações para servidores web e receber respostas. É amplamente utilizada para interagir com APIs (Application Programming Interfaces) e obter dados de serviços online.

URL = "https://api.tfl.gov.uk/Line/Mode/tube/Status"  # URL que fornece os status das linhas de metrô de Londres (Tube)


def buscar_metro():  # vai na API e pega os status das linhas de metrô de Londres (Tube)
    try:
        resposta = requests.get(
            URL, timeout=10
        )  # TIMEOUT: caso a API demore mais de 10 segundos para responder, vai cair no except
        if (
            resposta.status_code == 200
        ):  # O status code 200 significa que a requisição foi bem sucedida e o servidor respondeu com sucesso (nao significa que o dado estaja bom)
            return [  # retorna uma lista de dicionários com os status das linhas de metrô de Londres (Tube) se o status code for 200 (Servidor respondeu com sucesso)
                {
                    "linha": item[
                        "name"
                    ],  # item["name"] pega o nome da linha de metrô (ex: "Bakerloo", "Central", "Circle", etc)
                    "status": item["lineStatuses"][0][
                        "statusSeverityDescription"
                    ],  # item["lineStatuses"][0]["statusSeverityDescription"] pega o status da linha de metrô (ex: "Good Service", "Minor Delays", "Severe Delays", etc)
                }
                for item in resposta.json()  # resposta.json() converte a resposta da API em um dicionário Python (JSON) / item é um dicionário com as informações de cada linha de metrô de Londres (Tube)
            ]
        print(f"Erro ao buscar metrô. Status code: {resposta.status_code}")
        return None  # Retorna None se o status code não for 200 (servidor respondeu mas disse nao ter conseguido processar a requisição)
    except requests.exceptions.RequestException as erro:  # caso esteja fora de ar, sem internet ou qualquer outro problema de conexão, vai cair aqui
        print(
            f"Aviso: não foi possível buscar as informações do metrô. Detalhe: {erro}"
        )
        return None  # Retorna None se não conseguir buscar as informações do metrô (servidor sem resposta, sem internet, etc)


if (
    __name__ == "__main__"
):  # se o arquivo for executado diretamente, vai buscar os status das linhas de metrô de Londres (Tube) e imprimir os resultados
    dados = buscar_metro()
    if (
        dados is not None
    ):  # se os status das linhas de metrô de Londres (Tube) forem diferentes de None (ou seja, se a API respondeu com sucesso)
        for item in dados:  # para cada item (linha de metrô) na lista de status das linhas de metrô de Londres (Tube)
            print(
                f"{item['linha']}: {item['status']}"
            )  # imprime o nome da linha de metrô e o seu status (ex: "Bakerloo: Good Service", "Central: Minor Delays", etc)

# RODAR: python3 metro.py
