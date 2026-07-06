import streamlit as st
import json
import urllib.request
import streamlit.components.v1 as components

st.set_page_config(
    page_title="horizont.news — Conectando Gerações e Culturas",
    page_icon="🌐",
    layout="wide"
)

# ESTILIZAÇÃO PREMIUM, MODERNA E INCLUSIVA
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif !important;
        }
        .block-container {
            padding-top: 1.5rem !important;
        }
        #MainMenu {visibility: hidden;} 
        [data-testid='stSidebar'] {display: none;}
        
        /* Customização dos Cards para torná-los escaneáveis e atraentes */
        div[data-testid="stContainer"] {
            background-color: #0b1329 !important;
            border: 1px solid #1c2541 !important;
            border-radius: 16px !important;
            padding: 20px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        div[data-testid="stContainer"]:hover {
            transform: translateY(-2px);
            border-color: #00f5d4 !important;
        }
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

# DESIGN DO CABEÇALHO: Sofisticado para o profissional, moderno para o jovem
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding:25px; border-radius:16px; margin-bottom:20px; text-align:center; border: 1px solid #334155;">
        <h1 style="color:#00f5d4; margin:0; font-weight:700; letter-spacing: -0.5px; font-size: 36px;">🌐 horizont.news</h1>
        <p style="color:#94a3b8; font-size:14px; margin:6px 0 0 0; font-weight:400; letter-spacing: 0.2px;">
            Informação sem fronteiras — Perspectivas globais para mentes conectadas
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# TICKER DINÂMICO
st.markdown("""
<marquee style='width: 100%; color: #0b1329; background-color: #00f5d4; padding: 10px; font-size: 13px; font-weight: 700; border-radius: 30px; margin-bottom: 25px;'>
    ⚡ AGORA NO MUNDO: Cobertura integrada multiplataforma • Geopolítica, Economia, Cotidiano, Tendências Pop e Inovação Tecnológica em tempo real direto das principais agências globais...
</marquee>
""", unsafe_allow_html=True)

noticias = ler_banco_dados_fresco()

# Função auxiliar para gerar cores vibrantes nas tags por assunto (Aquece o visual do site)
def obter_cor_categoria(cat):
    cores = {
        "Política": "#ff5c5c",
        "Economia": "#4caf50",
        "Cotidiano": "#2196f3",
        "Esportes": "#ff9800",
        "Cultura & Pop": "#e91e63",
        "Tech & Ciência": "#9c27b0",
        "Viver Bem": "#00bcd4"
    }
    return cores.get(cat, "#607d8b")

if not noticias:
    st.info("📢 Sincronizando feeds mundiais. A sua janela para o planeta está carregando...")
else:
    # FILTROS LADO A LADO: Visual limpo e responsivo para smartphones
    col_lang, col_filtro = st.columns(2)

    with col_lang:
        idioma = st.selectbox("🌎 Escolha seu Idioma / Language", ["Português", "English", "Español"])
        sufixo = {"Português": "pt", "English": "en", "Español": "es"}[idioma]
        lang_audio = {"Português": "pt-BR", "English": "en-US", "Español": "es-ES"}[idioma]

    categorias_dinamicas = sorted(list(set(item.get("categoria", "Política") for item in noticias)))
    opcoes_filtro = ["Feed Completo (Todos os Assuntos)"] + categorias_dinamicas
    
    with col_filtro:
        categoria_selecionada = st.selectbox("🎯 Filtrar Canal", opcoes_filtro)

    sub_selecionada = "Todas as Subcategorias"
    
    if categoria_selecionada != "Feed Completo (Todos os Assuntos)":
        subcategorias_dinamicas = sorted(list(set(
            item.get("subcategoria", "") for item in noticias 
            if item.get("categoria") == categoria_selecionada and item.get("subcategoria")
        )))
        if subcategorias_dinamicas:
            sub_selecionada = st.selectbox(f"🏷️ Refinar Tópico em {categoria_selecionada}", ["Todas as Subcategorias"] + subcategorias_dinamicas)

    # PROCESSAMENTO DE EXIBIÇÃO
    noticias_recentes = list(reversed(noticias))
    
    if categoria_selecionada != "Feed Completo (Todos os Assuntos)":
        noticias_recentes = [n for n in noticias_recentes if n.get("categoria", "Política") == categoria_selecionada]
        if sub_selecionada != "Todas as Subcategorias":
            noticias_recentes = [n for n in noticias_recentes if n.get("subcategoria", "") == sub_selecionada]
    
    if not noticias_recentes:
        st.warning(f"Sem registros novos para este canal no momento. Tente mudar o filtro acima.")
    else:
        col1, col2 = st.columns(2)
        
        for index, item in enumerate(noticias_recentes):
            coluna_atual = col1 if index % 2 == 0 else col2
            
            titulo = item.get(f"titulo_{sufixo}", item.get("titulo_pt", "Sem Título"))
            texto = item.get(f"texto_{sufixo}", item.get("texto_pt", "Sem Conteúdo"))
            categoria = item.get("categoria", "Política")
            subcategoria = item.get("subcategoria", "")
            link_origem = item.get("link_origem", "#")
            chave_unica = item.get('id', str(index))
            
            # Cálculo de tempo de leitura (Média: 150 palavras por minuto)
            total_palavras = len(texto.split()) + len(item.get('resumo_longo', '').split())
            tempo_leitura = max(1, round(total_palavras / 150))
            
            cor_tag = obter_cor_categoria(categoria)
            tag_html = f"<span style='background-color:{cor_tag}; color:white; padding:4px 10px; border-radius:20px; font-size:11px; font-weight:700; text-transform:uppercase; margin-right:8px;'>{categoria}</span>"
            if subcategoria:
                tag_html += f"<span style='background-color:#1c2541; color:#94a3b8; padding:4px 10px; border-radius:20px; font-size:11px; font-weight:600;'>{subcategoria}</span>"

            with coluna_atual:
                with st.container(border=True):
                    # Tags e metadados com design moderno
                    st.markdown(f"<div style='margin-bottom:12px;'>{tag_html}</div>", unsafe_allow_html=True)
                    
                    st.subheader(titulo)
                    
                    # Linha de utilidades (Data + Tempo de leitura para atrair Geração Z e profissionais ágeis)
                    st.markdown(f"<p style='color:#64748b; font-size:12px; margin-bottom:14px;'>📅 {item.get('data')} • ⏱️ {tempo_leitura} min de leitura • 🏛️ {item.get('fonte_origem')}</p>", unsafe_allow_html=True)
                    
                    st.markdown(f"<p style='color:#cbd5e1; font-size:15px; line-height:1.6;'>{texto}</p>", unsafe_allow_html=True)
                    
                    st.divider()
                    
                    # PLAYER DE ÁUDIO ACESSÍVEL
                    texto_limpo = texto.replace('"', '').replace("'", "").replace('\n', ' ')
                    titulo_limpo = titulo.replace('"', '').replace("'", "")
                    html_audio = f"""
                    <div style="display: flex; justify-content: center; margin-bottom: 5px;">
                        <button onclick="window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{titulo_limpo}. {texto_limpo}'); msg.lang='{lang_audio}'; window.speechSynthesis.speak(msg);" 
                        style="background-color:#00f5d4; color:#0b1329; border: none; padding: 8px 20px; border-radius: 25px; cursor: pointer; font-size: 13px; font-weight: 700; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                            🔊 Ouvir Notícia
                        </button>
                        <button onclick="window.speechSynthesis.cancel();" 
                        style="background-color:transparent; color:#f43f5e; border: none; margin-left: 15px; cursor: pointer; font-size: 13px; font-weight: 600;">
                            ⏹️ Parar
                        </button>
                    </div>
                    """
                    components.html(html_audio, height=45)
                    
                    # INTERATIVIDADE: Sistema rápido de votação para engajar os leitores
                    st.markdown("<p style='color:#64748b; font-size:12px; margin-bottom:6px; font-weight:600;'>Qual o impacto dessa matéria para você?</p>", unsafe_allow_html=True)
                    reacao = st.radio(
                        "Avaliação", 
                        ["📈 Impacto Alto", "⚠️ Requer Atenção", "🔍 Neutro / Análise"], 
                        key=f"reacao_{chave_unica}_universal", 
                        horizontal=True, 
                        label_visibility="collapsed"
                    )
                    
                    # ACORDEÃO DE LEITURA COMPLETA
                    with st.expander("📝 Expandir Matéria Completa e Contexto"):
                        resumo_denso = item.get('resumo_longo', item.get('texto_pt', 'O detalhamento completo desta matéria está sendo processado pelas agências integradas.'))
                        st.markdown(f"<p style='color:#e2e8f0; font-size:16px; font-weight:600; margin-bottom:10px;'>{item.get('titulo_pt', 'Matéria de Capa')}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color:#94a3b8; font-size:14.5px; line-height:1.6; font-style:italic;'>{resumo_denso}</p>", unsafe_allow_html=True)
                        st.markdown(f"<div style='margin-top:15px; text-align:right;'><a href='{link_origem}' target='_blank' style='color:#00f5d4; text-decoration:none; font-size:13px; font-weight:700;'>Acessar Fonte Oficial ↗</a></div>", unsafe_allow_html=True)
