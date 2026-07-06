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

# Esconde o menu lateral do Streamlit para o público
st.markdown(
    "<style>#MainMenu {visibility: hidden;} [data-testid='stSidebar'] {display: none;}</style>", 
    unsafe_allow_html=True
)

# Cabeçalho Premium com as novas cores
st.markdown(
    """
    <div style="background-color:#003366; padding:25px; border-radius:12px; margin-bottom:15px; text-align:center; border: 1px solid #1e293b;">
        <h1 style="color:#ffffff; margin:0; font-family: 'Helvetica Neue', sans-serif; letter-spacing: 1px;">🌐 horizont.news</h1>
        <p style="color:#66b3ff; font-size:15px; margin:5px 0 0 0; font-weight:500;">Feed Internacional Geopolítico em Tempo Real</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# 1. TICKER DE NOTÍCIAS (Barra Rolante)
st.markdown("""
<marquee style='width: 100%; color: #FFFFFF; background-color: #2C3E50; padding: 10px; font-family: sans-serif; font-weight: bold; border-radius: 5px; margin-bottom: 25px;'>
    🔴 ÚLTIMAS ATUALIZAÇÕES: As principais notícias de Geopolítica, Economia e Mundo em Tempo Real direto das agências internacionais...
</marquee>
""", unsafe_allow_html=True)

idioma = st.selectbox("🌎 Idioma Padrão de Leitura", ["Português", "English", "Español"])
sufixo = {"Português": "pt", "English": "en", "Español": "es"}[idioma]

# Mapeamento dinâmico para a voz do narrador acompanhar o idioma escolhido
lang_audio = {"Português": "pt-BR", "English": "en-US", "Español": "es-ES"}[idioma]

noticias = ler_banco_dados_fresco()

if not noticias:
    st.info("📢 Atualizando a central de notícias mundiais. Volte em instantes!")
else:
    noticias_recentes = list(reversed(noticias))
    
    # 2. ORGANIZANDO O LAYOUT EM 2 COLUNAS
    col1, col2 = st.columns(2)
    
    for index, item in enumerate(noticias_recentes):
        # A lógica alterna as notícias: uma vai para a esquerda, a seguinte para a direita
        coluna_atual = col1 if index % 2 == 0 else col2
        
        titulo = item.get(f"titulo_{sufixo}", item.get("titulo_pt", "Sem Título"))
        texto = item.get(f"texto_{sufixo}", item.get("texto_pt", "Sem Conteúdo"))
        
        # Lê a categoria nova que o robô vai enviar
        categoria = item.get("categoria", "INTERNACIONAL") 
        link_origem = item.get("link_origem", "#")
        chave_unica = item.get('id', str(index))
        
        with coluna_atual:
            with st.container(border=True):
                st.caption(f"**📌 {categoria.upper()}** | 🏛️ Fonte: {item.get('fonte_origem')}")
                st.subheader(titulo)
                st.caption(f"📅 {item.get('data')}")
                st.markdown(texto)
                
                st.divider()
                
                # Botão de Áudio Nativo Inteligente (Ajusta a voz automaticamente)
                texto_limpo = texto.replace('"', '').replace("'", "").replace('\n', ' ')
                titulo_limpo = titulo.replace('"', '').replace("'", "")
                html_audio = f"""
                <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                    <button onclick="window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{titulo_limpo}. {texto_limpo}'); msg.lang='{lang_audio}'; window.speechSynthesis.speak(msg);" 
                    style="background-color:#003366; color:#ffffff; border: 1px solid #003366; padding: 6px 16px; border-radius: 20px; cursor: pointer; font-size: 14px; font-weight: bold;">
                        🔊 Ouvir Notícia
                    </button>
                    <button onclick="window.speechSynthesis.cancel();" 
                    style="background-color:transparent; color:#ef4444; border: none; margin-left: 10px; cursor: pointer; font-size: 14px;">
                        ⏹️ Parar
                    </button>
                </div>
                """
                components.html(html_audio, height=45)
                
                # 3. NOVAS REAÇÕES ANALÍTICAS
                st.caption("Avaliação Geopolítica / Mercado:")
                reacao = st.radio(
                    "Avaliação", 
                    ["📈 Alta Relevância", "⚠️ Tensão", "🔍 Exige Análise"], 
                    key=f"reacao_{chave_unica}", 
                    horizontal=True, 
                    label_visibility="collapsed"
                )
                
                # Caixa Sanfona da Fonte Original
                with st.expander("🇧🇷 Versão e Fonte Original"):
                    st.markdown(f"**{item.get('titulo_pt', 'Indisponível')}**")
                    st.markdown(item.get('texto_pt', 'Indisponível'))
                    st.markdown(f"**[🔗 Acessar matéria na agência original (Link Externo)]({link_origem})**")
