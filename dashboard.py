import sqlite3

import pandas as pd
import streamlit as st

from cambio import buscar_cambio, buscar_historico, calcular_resumos

st.title("London Daily Dashboard")

conexao = sqlite3.connect("cambio.db")
df_clima = pd.read_sql_query(
    "SELECT temperatura, precipitacao, chance_chuva, coletado_em "
    "FROM clima ORDER BY id DESC LIMIT 1",
    conexao,
)
df_clima = pd.read_sql_query(
    "SELECT temperatura, precipitacao, chance_chuva, coletado_em "
    "FROM clima ORDER BY id DESC LIMIT 1",
    conexao,
)
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


@st.cache_data(ttl=3600)
def carregar_cambio(dias):
    return buscar_cambio(), buscar_historico(dias)


st.header("Câmbio (base GBP)")
periodo = st.radio("Período", ["30 dias", "6 meses", "1 ano"], horizontal=True)
dias = {"30 dias": 30, "6 meses": 182, "1 ano": 365}[periodo]

rates, historico = carregar_cambio(dias)
if rates is None or historico is None:
    st.warning("Não foi possível carregar o câmbio.")
else:
    resumos = calcular_resumos(rates, historico)
    colunas = st.columns(3)
    for coluna, (moeda, r) in zip(colunas, resumos.items()):
        coluna.metric(
            f"GBP→{moeda}",
            f"{r['hoje']}",
            f"{r['variacao']:+.1f}% vs média ({r['media']:.4f})",
        )

    df_hist = pd.DataFrame.from_dict(historico, orient="index")
    st.line_chart(df_hist[["EUR", "USD"]])
    st.line_chart(df_hist[["BRL"]])


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
