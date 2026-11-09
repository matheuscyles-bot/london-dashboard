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

    
if __name__ == "__main__":
    from cambio import buscar_cambio
    from clima import buscar_clima

    criar_tabela()

    rates = buscar_cambio()
    if rates is not None:
        salvar_cambio(rates)

    clima = buscar_clima()
    if clima is not None:
        salvar_clima(clima)