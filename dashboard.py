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
df_metro = pd.read_sql_query("SELECT * FROM metro", conexao)
conexao.close()

st.header("Clima")
if df_clima.empty:
    st.warning("Sem dados de clima. Rode run_pipeline.py.")
else:
    st.metric("Temperatura atual", f"{df_clima['temperatura'][0]} °C")

st.header("Câmbio (base GBP)")
df_pivot = df_cambio.pivot(index="coletado_em", columns="moeda", values="valor")

st.line_chart(df_pivot)

st.header("Metrô de Londres")
st.dataframe(df_metro)