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

if __name__ == "__main__":
    from cambio import buscar_cambio

    criar_tabela()
    rates = buscar_cambio()
    if rates is not None:
        salvar_cambio(rates)


