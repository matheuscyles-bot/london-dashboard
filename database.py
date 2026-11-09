import sqlite3
from datetime import datetime


def criar_tabela():
    conexao = sqlite3.connect("cambio.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cambio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            moeda TEXT NOT NULL,
            valor REAL NOT NULL,
            coletado_em TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clima (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura REAL NOT NULL,
            coletado_em TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            linha TEXT NOT NULL,
            status TEXT NOT NULL,
            coletado_em TEXT NOT NULL
        )
    """)


    conexao.commit()
    conexao.close()
    print("Tabela criada")


def salvar_cambio(rates):
    conexao = sqlite3.connect("cambio.db")
    cursor = conexao.cursor()
    agora = datetime.now().isoformat(timespec="seconds")
    for moeda, valor in rates.items():
        cursor.execute(
            "INSERT INTO cambio (moeda, valor, coletado_em) VALUES (?, ?, ?)",
            (moeda, valor, agora),
        )
    conexao.commit()
    conexao.close()
    print(f"{len(rates)} cotações salvas")


def salvar_clima(clima):
    conexao = sqlite3.connect("cambio.db")
    cursor = conexao.cursor()
    agora = datetime.now().isoformat(timespec="seconds")
    temperatura = clima["current"]["temperature_2m"]
    cursor.execute(
        "INSERT INTO clima (temperatura, coletado_em) VALUES (?, ?)",
        (temperatura, agora),
    )
    conexao.commit()
    conexao.close()
    print(f"Temperatura atual de {temperatura}°C salva")


def salvar_metro(dados):
    conexao = sqlite3.connect("cambio.db")
    cursor = conexao.cursor()
    agora = datetime.now().isoformat(timespec="seconds")
    for linha in dados:
        nome = linha["name"]
        status = linha["lineStatuses"][0]["statusSeverityDescription"]
        cursor.execute(
            "INSERT INTO metro (linha, status, coletado_em) VALUES (?, ?, ?)",
            (nome, status, agora),
        )
    conexao.commit()
    conexao.close()
    print(f"{len(dados)} informações do metrô salvas")


if __name__ == "__main__":
    from cambio import buscar_cambio
    from clima import buscar_clima
    from metro import buscar_metro

    criar_tabela()

    rates = buscar_cambio()
    if rates is not None:
        salvar_cambio(rates)

    clima = buscar_clima()
    if clima is not None:
        salvar_clima(clima)

    dados_metro = buscar_metro()
    if dados_metro is not None:
        salvar_metro(dados_metro)