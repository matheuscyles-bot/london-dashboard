# FUNCAO: ORQUESTRAR OS 3 COLETORES DE DADOS (CAMBIO, CLIMA E METRO) E O BANCO DE DADOS SQLITE

from cambio import buscar_cambio
from clima import buscar_clima
from database import criar_tabela, salvar_cambio, salvar_clima, salvar_metro
from metro import buscar_metro

# BUSCOU AS FUNCOES DE CADA ARQUIVO E AGORA VAI EXECUTAR O PIPELINE DE FORMA ORQUESTRADA


def executar_pipeline():
    criar_tabela()  # CRIA AS TABELAS SE NAO EXISTIREM

    # câmbio: buscar, checar None, salvar
    rates = (
        buscar_cambio()
    )  # vai na API e pega os valores de câmbio do dia USD, EUR e BRL em relação à GBP
    if (
        rates is not None
    ):  # se os valores de câmbio do dia forem diferentes de None (ou seja, se a API respondeu com sucesso)
        salvar_cambio(
            rates
        )  # vai salvar os valores de câmbio do dia USD, EUR e BRL em relação à GBP no banco de dados SQLite

    # clima: buscar, checar None, salvar
    clima = buscar_clima()  # vai na API e pega os valores de clima (temperatura, precipitação e chance de chuva) em Woking, Inglaterra
    if (
        clima is not None
    ):  # se os valores de clima forem diferentes de None (ou seja, se a API respondeu com sucesso)
        salvar_clima(
            clima
        )  # vai salvar os valores de clima (temperatura, precipitação e chance de chuva) em Woking, Inglaterra no banco de dados SQLite

    # metrô: buscar, checar None, salvar
    dados_metro = (
        buscar_metro()
    )  # vai na API e pega os status das linhas de metrô de Londres (Tube)
    if (
        dados_metro is not None
    ):  # se os status das linhas de metrô de Londres (Tube) forem diferentes de None (ou seja, se a API respondeu com sucesso)
        salvar_metro(
            dados_metro
        )  # vai salvar os status das linhas de metrô de Londres (Tube) no banco de dados SQLite


# if ... is not None: SO FAZ UMA COISA, CHEGA SE DEVOLVEU ALGO OU DEVOLVEU "NONE"
# None é o sinal que suas funções dão quando falham (API fora do ar, status diferente de 200, sem internet)


if (
    __name__
    == "__main__"  # if __name__ == "__main__": garante que o arquivo so rode sendo executado diretamente com "python3 run_pipeline.py"
):
    executar_pipeline()
# O arquivo tem 2 usos: 1) ser importado por outro arquivo (dashboard.py) e 2) ser executado diretamente (python3 run_pipeline.py).
# A funcao do if __name__ separa esses 2 usos. Se for importado, o if __name__ nao roda. Se for executado diretamente, o if __name__ roda e chama a funcao executar_pipeline()

# RODAR: python3 run_pipeline.py
