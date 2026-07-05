import streamlit as st
import json
import urllib.request
import streamlit.components.v1 as components

st.set_page_config(
    page_title="horizont.news — Notícias do Mundo",
    page_icon="🌐",
    layout="wide"
)

URL_BANCO_RAW = "https://raw.githubusercontent.com/horizontpostnews-hue/portal-horizont/refs/heads/main/banco_noticias.json"

# Cache de 60 segundos adicionado para que as reações funcionem rapidamente
@st.cache_data(ttl=60)
def ler_banco_dados_fresco():
    try:
        req = urllib.request.Request(
            URL_BANCO_RAW, 
            headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'}
        )
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return []

def obtener_tag_categoria(titulo, texto):
    conteudo = f"{titulo} {texto}".lower()
    if any(w in conteudo for w in ["banco", "tax", "gold", "ouro", "trade", "mercado", "comércio", "celebrate"]):
        return "💰 ECONOMIA / CULTURA"
    elif any(w in conteudo for w in ["trump", "biden", "president", "election", "governo", "ministro", "un", "onu"]):
        return "🏛️ GEOPOLÍTICA"
    elif any(w in conteudo for w in ["bomba", "atack", "ataque", "guerra", "war", "morreu", "fogo", "weather", "alerta"]):
        return "🚨 URGENTE / ALERTA"
    return "📌 INTERNACIONAL"

st.markdown(
    "<style>#MainMenu {visibility: hidden;} [data-testid='stSidebar'] {display: none;}</style>", 
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="background-color:#0f172a; padding:25px; border-radius:12px; margin-bottom:25px; text-align:center; border: 1px solid #1e293b;">
        <h1 style="color:#f8fafc; margin:0; font-family: 'Helvetica Neue', sans-serif; letter-spacing: 1px;">🌐 horizont.news</h1>
        <p style="color:#38bdf8; font-size:15px; margin:5px 0 0 0; font-weight:500;">Feed Internacional Geopolítico em Tempo Real</p>
    </div>
    """, 
    unsafe_allow_html=True
)

idioma = st.selectbox("🌎 Idioma Padrão de Leitura", ["Português", "English", "Español"])
sufixo = {"Português": "pt", "English": "en", "Español": "es"}[idioma]

noticias = ler_banco_dados_fresco()

if not noticias:
    st.info("📢 Atualizando a central de notícias mundiais. Volte em instantes!")
else:
    noticias_recentes = list(reversed(noticias))
    
    for i in range(0, len(noticias_recentes), 2):
        cols = st.columns(2)
        for idx, col in enumerate(cols):
            if i + idx < len(noticias_recentes):
                item = noticias_recentes[i + idx]
                
                titulo = item.get(f"titulo_{sufixo}", item.get("titulo_pt", "Sem Título"))
                texto = item.get(f"texto_{sufixo}", item.get("texto_pt", "Sem Conteúdo"))
                tag = obtener_tag_categoria(titulo, texto)
                link_origem = item.get("link_origem", "#")
                
                # Identificador único para os botões não darem conflito
                chave_unica = item.get('id', f"{i}_{idx}")
                
                with col:
                    with st.container(border=True):
                        st.caption(f"**{tag}**")
                        st.subheader(titulo)
                        st.caption(f"📅 {item.get('data')} | 🏛️ Fonte: {item.get('fonte_origem')}")
                        st.markdown(texto)
                        
                        st.divider() # Linha divisória fina
                        
                        # --- 1. BOTÃO DE OUVIR (Text-to-Speech nativo do navegador) ---
                        texto_limpo = texto.replace('"', '').replace("'", "").replace('\n', ' ')
                        titulo_limpo = titulo.replace('"', '').replace("'", "")
                        html_audio = f"""
                        <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                            <button onclick="window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{titulo_limpo}. {texto_limpo}'); msg.lang='pt-BR'; window.speechSynthesis.speak(msg);" 
                            style="background-color:#0f172a; color:#38bdf8; border: 1px solid #38bdf8; padding: 6px 16px; border-radius: 20px; cursor: pointer; font-size: 14px; font-weight: bold;">
                                🔊 Ouvir Notícia
                            </button>
                            <button onclick="window.speechSynthesis.cancel();" 
                            style="background-color:transparent; color:#ef4444; border: none; margin-left: 10px; cursor: pointer; font-size: 14px;">
                                ⏹️ Parar
                            </button>
                        </div>
                        """
                        components.html(html_audio, height=45)
                        
                        # --- 2. REAÇÕES (Emojis) ---
                        st.caption("O que você achou desta matéria?")
                        r1, r2, r3, r4, r5 = st.columns(5)
                        r1.button("👍", key=f"like_{chave_unica}")
                        r2.button("❤️", key=f"love_{chave_unica}")
                        r3.button("😮", key=f"wow_{chave_unica}")
                        r4.button("😢", key=f"sad_{chave_unica}")
                        r5.button("😡", key=f"angry_{chave_unica}")
                        
                        # --- 3. LINK PARA VERSÃO BRASILEIRA (Expander) ---
                        with st.expander("🇧🇷 Versão e Fonte Original"):
                            st.markdown(f"**{item.get('titulo_pt', 'Título Indisponível')}**")
                            st.markdown(item.get('texto_pt', 'Resumo indisponível.'))
                            st.markdown(f"**[🔗 Acessar matéria na agência original (Link Externo)]({link_origem})**")
