import sqlite3

import pandas as pd
import streamlit as st

st.title("London Daily Dashboard")

conexao = sqlite3.connect("cambio.db")
df_clima = pd.read_sql_query(
    "SELECT temperatura, coletado_em FROM clima ORDER BY id DESC LIMIT 1",
    conexao,
)
df_cambio = pd.read_sql_query("SELECT * FROM cambio", conexao)
df_metro = pd.read_sql_query(
    "SELECT * FROM metro WHERE coletado_em = (SELECT MAX(coletado_em) FROM metro)",
    conexao,
)
conexao.close()
df_problemas = df_metro[df_metro["status"] != "Good Service"]

st.header("Clima")
if df_clima.empty:
    st.warning("Sem dados de clima. Rode run_pipeline.py.")
else:
    st.metric("Temperatura atual", f"{df_clima['temperatura'][0]} °C")

st.header("Câmbio (base GBP)")
if df_cambio.empty:
    st.warning("Sem dados de câmbio. Rode run_pipeline.py.")
else:
    df_cambio = df_cambio.drop_duplicates(subset=["coletado_em", "moeda"])
    df_pivot = df_cambio.pivot(index="coletado_em", columns="moeda", values="valor")
    st.line_chart(df_pivot[["EUR", "USD"]])
    st.line_chart(df_pivot[["BRL"]])

st.header("Metrô de Londres")
st.dataframe(df_metro)
st.header("Problemas no Metrô")
st.write(df_problemas)