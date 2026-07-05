import streamlit as st
import json
import os

# Configuração da página do portal
st.set_page_config(
    page_title="horizont.news — Painel",
    page_icon="🌐",
    layout="wide"
)

ARQUIVO_BANCO = "banco_noticias.json"

# Função ultra-rápida que apenas lê o banco de dados atualizado pelo robô
def carregar_noticias_locais():
    if os.path.exists(ARQUIVO_BANCO):
        try:
            with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# Título Principal do Portal
st.title("🌐 horizont.news — Painel de Controle Integrado")
st.markdown("---")

# Botão de atualização rápida da interface
if st.button("🔄 Atualizar Feed de Notícias"):
    st.rerun()

# Carrega os dados coletados de forma segura
noticias = carregar_noticias_locais()

if not noticias:
    st.info("📢 O robô está processando os dados geopolíticos globais. Aguarde a próxima rodada automática ou verifique os logs no GitHub Actions.")
else:
    # Seletor de Idioma para o usuário internacional
    idioma = st.selectbox("🌎 Selecione o Idioma / Select Language / Seleccione el Idioma", ["Português", "English", "Español"])
    
    # Mapeamento de sufixos do nosso banco JSON
    sufixos = {
        "Português": "pt",
        "English": "en",
        "Español": "es"
    }
    sufixo = sufixos[idioma]
    
    # Exibe as notícias em formato de cards elegantes
    # Mostra primeiro as notícias mais recentes (ordem inversa)
    for item in reversed(noticias):
        titulo_chave = f"titulo_{sufixo}"
        texto_chave = f"texto_{sufixo}"
        
        # Garante que a tradução exista no banco, senão usa português como segurança
        titulo_exibir = item.get(titulo_chave, item.get("titulo_pt", "Sem Título"))
        texto_exibir = item.get(texto_chave, item.get("texto_pt", "Sem Conteúdo disponível."))
        
        with st.container():
            st.subheader(titulo_exibir)
            st.caption(f"📅 Coletado em: {item.get('data')} | 🏛️ Fonte de Origem: {item.get('fonte_origem')}")
            st.markdown(texto_exibir)
            st.markdown("---")
