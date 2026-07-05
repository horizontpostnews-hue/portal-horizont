import streamlit as st
import json
import os

st.set_page_config(page_title="Painel Admin — horizont.news", page_icon="⚙️", layout="wide")

st.title("⚙️ Painel de Controle Administrativo")
st.markdown("Use esta página para forçar o recarregamento do banco de dados caso o Streamlit trave.")

if st.button("🗑️ Forçar Limpeza de Cache e Atualizar Dados", use_container_width=True):
    st.cache_data.clear()
    st.success("Cache limpo com sucesso! Verifique a página principal.")
    st.rerun()

if os.path.exists("banco_noticias.json"):
    with open("banco_noticias.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
    st.metric(label="Total de Notícias no Banco de Dados", value=len(dados))
    st.json(dados)
else:
    st.error("Arquivo banco_noticias.json não encontrado.")
