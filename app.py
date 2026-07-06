import streamlit as st
import json
import urllib.request
import streamlit.components.v1 as components

st.set_page_config(
    page_title="horizont.news — Notícias do Mundo",
    page_icon="🌐",
    layout="wide"
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem !important;
        }
        #MainMenu {visibility: hidden;} 
        [data-testid='stSidebar'] {display: none;}
    </style>
    """, 
    unsafe_allow_html=True
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

st.markdown(
    """
    <div style="background-color:#003366; padding:12px 20px; border-radius:10px; margin-bottom:15px; text-align:center; border: 1px solid #1e293b;">
        <h1 style="color:#ffffff; margin:0; font-family: 'Helvetica Neue', sans-serif; letter-spacing: 1px; font-size: 28px;">🌐 horizont.news</h1>
        <p style="color:#66b3ff; font-size:13px; margin:2px 0 0 0; font-weight:500;">Feed Internacional Geopolítico em Tempo Real</p>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown("""
<marquee style='width: 100%; color: #FFFFFF; background-color: #2C3E50; padding: 8px; font-family: sans-serif; font-size: 14px; font-weight: bold; border-radius: 5px; margin-bottom: 20px;'>
    🔴 ÚLTIMAS ATUALIZAÇÕES: As principais notícias de Geopolítica, Economia e Mundo em Tempo Real direto das agências internacionais...
</marquee>
""", unsafe_allow_html=True)

noticias = ler_banco_dados_fresco()

if not noticias:
    st.info("📢 Atualizando a central de notícias mundiais. Volte em instantes!")
else:
    # 1. LINHA DE CONTROLES PRINCIPAIS
    col_lang, col_filtro = st.columns(2)

    with col_lang:
        idioma = st.selectbox("🌎 Idioma Padrão", ["Português", "English", "Español"])
        sufixo = {"Português": "pt", "English": "en", "Español": "es"}[idioma]
        lang_audio = {"Português": "pt-BR", "English": "en-US", "Español": "es-ES"}[idioma]

    categorias_dinamicas = sorted(list(set(item.get("categoria", "INTERNACIONAL") for item in noticias)))
    opcoes_filtro = ["Todas as Categorias"] + categorias_dinamicas
    
    with col_filtro:
        categoria_selecionada = st.selectbox("🎯 Filtrar por Assunto", opcoes_filtro)

    sub_selecionada = "Todas as Subcategorias"
    
    # 2. FILTRO SECUNDÁRIO (Subcategorias - Só aparece se uma Categoria for selecionada)
    if categoria_selecionada != "Todas as Categorias":
        subcategorias_dinamicas = sorted(list(set(
            item.get("subcategoria", "") for item in noticias 
            if item.get("categoria") == categoria_selecionada and item.get("subcategoria")
        )))
        
        if subcategorias_dinamicas:
            # Cria uma caixa de seleção estilizada para não poluir
            sub_selecionada = st.selectbox(f"🏷️ Refinar {categoria_selecionada}", ["Todas as Subcategorias"] + subcategorias_dinamicas)

    # 3. MOTOR DE BUSCA (Aplica os filtros)
    noticias_recentes = list(reversed(noticias))
    
    if categoria_selecionada != "Todas as Categorias":
        noticias_recentes = [n for n in noticias_recentes if n.get("categoria", "INTERNACIONAL") == categoria_selecionada]
        
        if sub_selecionada != "Todas as Subcategorias":
            noticias_recentes = [n for n in noticias_recentes if n.get("subcategoria", "") == sub_selecionada]
    
    if not noticias_recentes:
        st.warning(f"Nenhuma notícia encontrada com estes filtros no momento.")
    else:
        col1, col2 = st.columns(2)
        
        for index, item in enumerate(noticias_recentes):
            coluna_atual = col1 if index % 2 == 0 else col2
            
            titulo = item.get(f"titulo_{sufixo}", item.get("titulo_pt", "Sem Título"))
            texto = item.get(f"texto_{sufixo}", item.get("texto_pt", "Sem Conteúdo"))
            
            # Puxa a categoria e a subcategoria
            categoria = item.get("categoria", "INTERNACIONAL") 
            subcategoria = item.get("subcategoria", "")
            
            # Formata a tag visual para o leitor
            tag_visual = f"{categoria.upper()} ❯ {subcategoria}" if subcategoria else f"{categoria.upper()}"
            
            link_origem = item.get("link_origem", "#")
            chave_unica = item.get('id', str(index))
            
            with coluna_atual:
                with st.container(border=True):
                    # Agora a Subcategoria aparece brilhando aqui em cima!
                    st.caption(f"**📌 {tag_visual}** | 🏛️ Fonte: {item.get('fonte_origem')}")
                    st.subheader(titulo)
                    st.caption(f"📅 {item.get('data')}")
                    st.markdown(texto)
                    
                    st.divider()
                    
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
                    
                    st.caption("Avaliação Geopolítica / Mercado:")
                    reacao = st.radio(
                        "Avaliação", 
                        ["📈 Alta Relevância", "⚠️ Tensão", "🔍 Exige Análise"], 
                        key=f"reacao_{chave_unica}_sub", 
                        horizontal=True, 
                        label_visibility="collapsed"
                    )
                    
                    with st.expander("📝 Resumo Expandido e Fonte"):
                        resumo_denso = item.get('resumo_longo', item.get('texto_pt', 'O resumo estendido para esta matéria ainda está sendo processado pela nossa IA.'))
                        
                        st.markdown(f"**{item.get('titulo_pt', 'Indisponível')}**")
                        st.markdown(f"*{resumo_denso}*")
                        st.markdown(f"**[🔗 Acessar matéria completa na agência (Link Externo)]({link_origem})**")
