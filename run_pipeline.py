from cambio import buscar_cambio
from clima import buscar_clima
from metro import buscar_metro
from database import criar_tabela, salvar_cambio, salvar_clima, salvar_metro


def executar_pipeline():
    criar_tabela()

    # câmbio: buscar, checar None, salvar
    rates = buscar_cambio()
    if rates is not None:
        salvar_cambio(rates)

    # clima: buscar, checar None, salvar
    clima = buscar_clima()
    if clima is not None:
        salvar_clima(clima)

    # metrô: buscar, checar None, salvar
    dados_metro = buscar_metro()
    if dados_metro is not None:
        salvar_metro(dados_metro)


if __name__ == "__main__":
    executar_pipeline()