import sqlite3

import pandas as pd
import streamlit as st

from cambio import resumo_brl

st.title("London Daily Dashboard")

conexao = sqlite3.connect("cambio.db")
df_clima = pd.read_sql_query(
    "SELECT temperatura, precipitacao, chance_chuva, coletado_em "
    "FROM clima ORDER BY id DESC LIMIT 1",
    conexao,
)
df_cambio = pd.read_sql_query("SELECT * FROM cambio", conexao)
df_metro = pd.read_sql_query(
    "SELECT * FROM metro WHERE coletado_em = (SELECT MAX(coletado_em) FROM metro)",
    conexao,
)
conexao.close()

st.header("Clima")
if df_clima.empty:
    st.warning("Sem dados de clima. Rode run_pipeline.py.")
else:
    st.metric("Temperatura atual", f"{df_clima['temperatura'][0]} °C")
    st.metric("Precipitação", f"{df_clima['precipitacao'][0]} mm")
    st.metric("Chance de chuva (6h)", f"{df_clima['chance_chuva'][0]}%")

st.header("Câmbio (base GBP)")
resumo = resumo_brl()
if resumo is None:
    st.warning("Não foi possível calcular o resumo do BRL.")
else:
    st.metric(
        "GBP→BRL hoje",
        f"{resumo['hoje']}",
        f"{resumo['variacao']:+.1f}% vs média de 30 dias",
    )

if df_cambio.empty:
    st.warning("Sem dados de câmbio. Rode run_pipeline.py.")
else:
    df_cambio = df_cambio.drop_duplicates(subset=["coletado_em", "moeda"])
    df_pivot = df_cambio.pivot(index="coletado_em", columns="moeda", values="valor")
    st.line_chart(df_pivot[["EUR", "USD"]])
    st.line_chart(df_pivot[["BRL"]])

st.header("Metrô de Londres")
if df_metro.empty:
    st.warning("Sem dados do metrô. Rode run_pipeline.py.")
else:
    df_problemas = df_metro[df_metro["status"] != "Good Service"]
    st.metric("Linhas com problema", len(df_problemas))
    if df_problemas.empty:
        st.success("Todas as linhas com serviço normal")
    else:
        st.dataframe(df_problemas)
    with st.expander("Ver todas as linhas"):
        st.dataframe(df_metro)
