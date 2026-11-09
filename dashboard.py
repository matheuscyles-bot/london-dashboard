import sqlite3
import pandas as pd
import streamlit as st

st.title ("London Daily Dashboard")

conexao = sqlite3.connect("cambio.db")
df = pd.read_sql_query("SELECT * FROM cambio", conexao)
conexao.close()

st.dataframe(df)