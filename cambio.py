#FUNCAO: BUSCAR DADOS DAS APIs 

from datetime import date, timedelta

import requests # request: biblioteca que permite fazer requisições HTTP em Python, ou seja, enviar solicitações para servidores web e receber respostas. É amplamente utilizada para interagir com APIs (Application Programming Interfaces) e obter dados de serviços online.

URL = "https://api.frankfurter.dev/v1/latest?base=GBP&symbols=BRL,EUR,USD" #URL que fornece os valores de câmbio do dia USD, EUR e BRL em relação à GBP


def buscar_cambio(): #vai na API e pega os valores de câmbio do dia USD, EUR e BRL em relação à GBP
    try: 
        resposta = requests.get(URL, timeout=10) #TIMEOUT: caso a API demore mais de 10 segundos para responder, vai cair no except
        if resposta.status_code == 200: # O status code 200 significa que a requisição foi bem sucedida e o servidor respondeu com sucesso (nao significa que o dado estaja bom)
            return resposta.json()["rates"] # retorna os valores de câmbio se o status code for 200 (Servidor respondeu com sucesso) / devolve um dicionario {"BRL": 7.49, "EUR": 1.19, "USD": 1.32} / ["rates"] pega só a parte das cotações.
        print(f"Erro ao buscar câmbio. Status code: {resposta.status_code}") #resposta.status_code é o código de status HTTP retornado pelo servidor. Se não for 200, significa que houve algum problema na requisição. Nesse caso, o código imprime uma mensagem de erro com o status code retornado.
        return None # Retorna None se o status code não for 200 (servidor respondeu mas disse nao ter conseguido processar a requisição)
    except requests.exceptions.RequestException: #caso esteja fora de ar, sem internet ou qualquer outro problema de conexão, vai cair aqui
        print("Aviso: não foi possível buscar as taxas de câmbio.")
        return None # Retorna None se não conseguir buscar as taxas de câmbio (servidor sem resposta, sem internet, etc)


def buscar_historico(dias=30, moedas="BRL,EUR,USD"): # vai na API e pega os valores de câmbio dos últimos 30 dias (ou outro período definido pelo usuário) USD, EUR e BRL em relação à GBP
    fim = date.today() # fim é a data de hoje
    inicio = fim - timedelta(days=dias) # inicio é a data de hoje menos o número de dias definido pelo usuário (padrão 30 dias) / timedelta é uma função que permite calcular a diferença entre datas
    url = (
        f"https://api.frankfurter.dev/v1/{inicio.isoformat()}..{fim.isoformat()}"
        f"?base=GBP&symbols={moedas}"
    )
    try:
        resposta = requests.get(url, timeout=10) # TIMEOUT: caso a API demore mais de 10 segundos para responder, vai cair no except
        if resposta.status_code == 200: # O status code 200 significa que a requisição foi bem sucedida e o servidor respondeu com sucesso (nao significa que o dado estaja bom)
            return resposta.json()["rates"] # retorna os valores de câmbio se o status code for 200 (Servidor respondeu com sucesso) / devolve um dicionario {"2023-06-01": {"BRL": 7.49, "EUR": 1.19, "USD": 1.32}, "2023-06-02": {"BRL": 7.50, "EUR": 1.20, "USD": 1.33}, ...} / ["rates"] pega só a parte das cotações.
        print(f"Erro ao buscar histórico. Status code: {resposta.status_code}") # resposta.status_code é o código de status HTTP retornado pelo servidor. Se não for 200, significa que houve algum problema na requisição. Nesse caso, o código imprime uma mensagem de erro com o status code retornado.
        return None # Retorna None se o status code não for 200 (servidor respondeu mas disse nao ter conseguido processar a requisição)
    except requests.exceptions.RequestException: # caso esteja fora de ar, sem internet ou qualquer outro problema de conexão, vai cair aqui
        print("Aviso: não foi possível buscar o histórico do câmbio.") 
        return None # Retorna None se não conseguir buscar o histórico do câmbio (servidor sem resposta, sem internet, etc)


def calcular_resumos(rates, historico): # calcula a média dos últimos 30 dias e a variação percentual do câmbio de hoje em relação à média dos últimos 30 dias
    resumos = {} # dicionário vazio que vai armazenar os resumos de cada moeda "{}"
    for moeda, hoje in rates.items(): # para cada moeda e seu valor de hoje
        valores = [dia[moeda] for dia in historico.values()] # cria uma lista com os valores de cada dia do histórico para a moeda atual (ex: [7.49, 7.50, 7.51, ...])
        media = sum(valores) / len(valores) # calcula a média dos valores do histórico para a moeda atual (ex: (7.49 + 7.50 + 7.51 + ...) / sum(valoores)) soma todos os valores da lista / len(valores)) devolve o número de elementos na lista valores
        resumos[moeda] = { # adiciona ao dicionário resumos a moeda atual como chave e um dicionário com os valores de hoje, média e variação percentual como valor
            "hoje": hoje,# valor de hoje da moeda atual
            "media": media, # média dos valores do histórico para a moeda atual
            "variacao": (hoje - media) / media * 100, # calcula a variação percentual do câmbio de hoje em relação à média dos últimos 30 dias ((valor de hoje - média) / média * 100)
        }
    return resumos # retorna o dicionário resumos com os valores de hoje, média e variação percentual para cada moeda


if __name__ == "__main__": # se o arquivo for executado diretamente, vai buscar os valores de câmbio do dia e o histórico dos últimos 30 dias e imprimir os resumos de cada moeda
    rates = buscar_cambio() # vai buscar os valores de câmbio do dia USD, EUR e BRL em relação à GBP
    historico = buscar_historico(30) # vai buscar os valores de câmbio dos últimos 30 dias USD, EUR e BRL em relação à GBP
    if rates is not None and historico is not None:# se os valores de câmbio do dia e o histórico dos últimos 30 dias forem diferentes de None (ou seja, se a API respondeu com sucesso)
        for moeda, r in calcular_resumos(rates, historico).items(): # para cada moeda e seu resumo (hoje, média e variação percentual) calculado pela função calcular_resumos
            print( 
                f"{moeda} hoje: {r['hoje']} | média: {r['media']:.4f} " # imprime o valor de hoje e a média dos últimos 30 dias para cada moeda
                f"| {r['variacao']:+.1f}%" # imprime a variação percentual do câmbio de hoje em relação à média dos últimos 30 dias para cada moeda
            )
        print(f"Pontos em 365 dias: {len(buscar_historico(365))}") # imprime o número de pontos de dados disponíveis no histórico dos últimos 365 dias (ou seja, quantos dias a API tem dados de câmbio disponíveis para cada moeda)

# RODAR: python3 cambio.py