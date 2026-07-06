import streamlit as st
import json
import urllib.request
import streamlit.components.v1 as components

st.set_page_config(
    page_title="horizont.news — Conectando Gerações",
    page_icon="🌐",
    layout="wide"
)

# ESTILIZAÇÃO DO PORTAL: Foco total em legibilidade, contraste e componentes visuais
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif !important;
        }
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
        }
        #MainMenu {visibility: hidden;} 
        [data-testid='stSidebar'] {display: none;}
        
        .texto-noticia {
            color: #1e293b !important;
            font-size: 15px !important;
            line-height: 1.6 !important;
            font-weight: 400 !important;
        }
        
        .titulo-noticia {
            color: #0f172a !important;
            font-weight: 700 !important;
            font-size: 20px !important;
            line-height: 1.3 !important;
            margin-top: 8px !important;
            margin-bottom: 5px !important;
        }

        /* Acordeão HTML Nativo sem bugs */
        details {
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            margin-top: 15px !important;
        }
        summary {
            font-weight: 600 !important;
            color: #0f172a !important;
            cursor: pointer !important;
            font-size: 14px !important;
            list-style: none !important;
        }
        summary::-webkit-details-marker { display: none !important; }
        summary::before { content: "📝 " !important; }
        
        /* Ajuste fino para imagens integradas nas notícias */
        .img-noticia {
            width: 100%;
            height: 180px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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

# 1. IDENTIDADE VISUAL (HEADER COM LOGO E CRÉDITO)
# Substitua a URL abaixo pela URL da sua imagem final hospedada no GitHub quando criá-la.
# Enquanto não criar sua logo, este bloco simula uma marca em vetor perfeitamente limpa.
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding:25px; border-radius:14px; margin-bottom:20px; text-align:center; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
        <h1 style="color:#00f5d4; margin:0; font-weight:800; letter-spacing: -1px; font-size: 34px; display:inline-block; vertical-align:middle;">🌐 horizont.news</h1>
        <p style="color:#94a3b8; font-size:13px; margin:6px 0 0 0; font-weight:400; letter-spacing: 0.5px;">
            Informação Sem Fronteiras — Perspectivas Globais Para Mentes Conectadas
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# TICKER
st.markdown("""
<marquee style='width: 100%; color: #0f172a; background-color: #00f5d4; padding: 8px; font-size: 13px; font-weight: 700; border-radius: 8px; margin-bottom: 25px;'>
    ⚡ AGORA NO MUNDO: Cobertura integrada multiplataforma • Geopolítica, Economia, Cotidiano, Tendências Pop e Inovação Tecnológica em tempo real direto das principais agências globais...
</marquee>
""", unsafe_allow_html=True)

noticias = ler_banco_dados_fresco()

def obter_cor_categoria(cat):
    cores = {
        "Política": "#e11d48", "Economia": "#16a34a", "Cotidiano": "#2563eb",
        "Esportes": "#ea580c", "Cultura & Pop": "#db2777", "Tech & Ciência": "#7c3aed", "Viver Bem": "#0d9488"
    }
    return cores.get(cat, "#4b5563")

# Dicionário de Imagens de Backup Baseadas na Categoria (Evita que o card fique sem imagem)
def obter_imagem_backup(cat):
    imagens = {
        "Economia": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=600&q=80",
        "Esportes": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=600&q=80",
        "Política": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=600&q=80",
        "Tech & Ciência": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=600&q=80",
        "Cultura & Pop": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80"
    }
    return imagens.get(cat, "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=600&q=80")

if not noticias:
    st.info("📢 Sincronizando feeds mundiais. A sua janela para o planeta está carregando...")
else:
    # FILTROS
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
            sub_selecionada = st.selectbox(f"🏷️ Refinar em {categoria_selecionada}", ["Todas as Subcategorias"] + subcategorias_dinamicas)

    # FILTRAGEM
    noticias_recentes = list(reversed(noticias))
    if categoria_selecionada != "Feed Completo (Todos os Assuntos)":
        noticias_recentes = [n for n in noticias_recentes if n.get("categoria", "Política") == categoria_selecionada]
        if sub_selecionada != "Todas as Subcategorias":
            noticias_recentes = [n for n in noticias_recentes if n.get("subcategoria", "") == sub_selecionada]
    
    if not noticias_recentes:
        st.warning(f"Sem registros novos para este canal no momento.")
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
            
            # Puxa a URL do JSON ou atribui uma imagem linda de backup livre de direitos autorais
            url_foto = item.get("url_imagem", obter_imagem_backup(categoria))
            
            total_palavras = len(texto.split()) + len(item.get('resumo_longo', '').split())
            tempo_leitura = max(1, round(total_palavras / 150))
            
            cor_tag = obter_cor_categoria(categoria)
            tag_html = f"<span style='background-color:{cor_tag}; color:white; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:700; text-transform:uppercase; margin-right:6px;'>{categoria}</span>"
            if subcategoria:
                tag_html += f"<span style='background-color:#f1f5f9; color:#475569; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:600; border: 1px solid #e2e8f0;'>{subcategoria}</span>"

            with coluna_atual:
                with st.container(border=True):
                    # 2. IMPLEMENTAÇÃO DA IMAGEM DA NOTÍCIA
                    st.markdown(f'<img src="{url_foto}" class="img-noticia" alt="Imagem da notícia">', unsafe_allow_html=True)
                    
                    # Tags Editoriais
                    st.markdown(f"<div style='margin-bottom:8px;'>{tag_html}</div>", unsafe_allow_html=True)
                    
                    # Título
                    st.markdown(f"<h3 class='titulo-noticia'>{titulo}</h3>", unsafe_allow_html=True)
                    
                    # Metadados / Crédito do Veículo Original
                    st.markdown(f"<p style='color:#64748b; font-size:12px; margin-top:2px; margin-bottom:12px;'>📅 {item.get('data')} • ⏱️ {tempo_leitura} min • 🏛️ Fonte original: <b>{item.get('fonte_origem')}</b></p>", unsafe_allow_html=True)
                    
                    # Texto Principal
                    st.markdown(f"<p class='texto-noticia'>{texto}</p>", unsafe_allow_html=True)
                    
                    st.divider()
                    
                    # PLAYER DE ÁUDIO
                    texto_limpo = texto.replace('"', '').replace("'", "").replace('\n', ' ')
                    titulo_limpo = titulo.replace('"', '').replace("'", "")
                    html_audio = f"""
                    <div style="display: flex; justify-content: center; margin-bottom: 5px;">
                        <button onclick="window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{titulo_limpo}. {texto_limpo}'); msg.lang='{lang_audio}'; window.speechSynthesis.speak(msg);" 
                        style="background-color:#0f172a; color:#00f5d4; border: none; padding: 8px 18px; border-radius: 20px; cursor: pointer; font-size: 13px; font-weight: 700;">
                            🔊 Ouvir Notícia
                        </button>
                        <button onclick="window.speechSynthesis.cancel();" 
                        style="background-color:transparent; color:#e11d48; border: none; margin-left: 12px; cursor: pointer; font-size: 13px; font-weight: 600;">
                            ⏹️ Parar
                        </button>
                    </div>
                    """
                    components.html(html_audio, height=42)
                    
                    # Interação
                    st.markdown("<p style='color:#475569; font-size:12px; margin-bottom:6px; font-weight:600;'>Qual o impacto dessa matéria?</p>", unsafe_allow_html=True)
                    reacao = st.radio("Avaliação", ["📈 Alto", "⚠️ Atenção", "🔍 Neutro"], key=f"reacao_{chave_unica}_v5", horizontal=True, label_visibility="collapsed")
                    
                    # Acordeão Seguro
                    resumo_denso = item.get('resumo_longo', item.get('texto_pt', 'O detalhamento completo desta matéria está sendo processado.'))
                    html_acordeao = f"""
                    <details>
                        <summary>Matéria Completa e Contexto</summary>
                        <div style="margin-top: 10px; color: #334155; font-size: 14.5px; line-height: 1.6; font-style: italic;">
                            <strong style="color: #0f172a; font-style: normal; display: block; margin-bottom: 6px;">{titulo}</strong>
                            {resumo_denso}
                            <div style="margin-top: 12px; text-align: right;">
                                <a href="{link_origem}" target="_blank" style="color: #2563eb; text-decoration: none; font-size: 13px; font-weight: 700;">Acessar Fonte Oficial ↗</a>
                            </div>
                        </div>
                    </details>
                    """
                    st.markdown(html_acordeao, unsafe_allow_html=True)

# 3. CRÉDITOS DO VEÍCULO (RODAPÉ INSTITUCIONAL)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center; color: #64748b; font-size: 12px;">
        <p style="margin: 0; font-weight: 600;">🌐 horizont.news — Portal de Agregação de Conteúdo Internacional Inteligente</p>
        <p style="margin: 4px 0 0 0;">Conteúdos compilados automaticamente via robô de fontes públicas respeitáveis (G1, UOL, Al Jazeera, Valor Econômico). Todos os direitos reservados aos respectivos veículos originais.</p>
        <p style="margin: 4px 0 0 0; color: #94a3b8;">Desenvolvido com Streamlit e Python para leitura multiplataforma adaptada e acessível.</p>
    </div>
    """, 
    unsafe_allow_html=True
)
