# FUNCAO: CRIAR BANCO DE DADOS SQLITE E SALVAR DADOS DAS APIS

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
            precipitacao REAL NOT NULL,
            chance_chuva INTEGER NOT NULL,
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
    cursor.execute(
        "INSERT INTO clima (temperatura, precipitacao, chance_chuva, coletado_em) "
        "VALUES (?, ?, ?, ?)",
        (clima["temperatura"], clima["precipitacao"], clima["chance_chuva"], agora),
    )
    conexao.commit()
    conexao.close()
    print(f"Temperatura atual de {clima['temperatura']}°C salva")


def salvar_metro(dados):
    conexao = sqlite3.connect("cambio.db")
    cursor = conexao.cursor()
    agora = datetime.now().isoformat(timespec="seconds")
    for item in dados:
        cursor.execute(
            "INSERT INTO metro (linha, status, coletado_em) VALUES (?, ?, ?)",
            (item["linha"], item["status"], agora),
        )
    conexao.commit()
    conexao.close()
    print(f"{len(dados)} informações do metrô salvas")

## RODAR: python3 database.py