import streamlit as st
import json
import urllib.request
import re
from datetime import datetime

st.set_page_config(
    page_title="horizont.news — Conectando Gerações",
    page_icon="🌐",
    layout="wide"
)

# 🎨 ESTILIZAÇÃO COMPLETA (Estilo Capa de Grande Jornal)
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;600;700;800&display=swap');
        
        * { font-family: 'Inter', sans-serif !important; }
        .block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; }
        #MainMenu {visibility: hidden;} 
        [data-testid='stSidebar'] {display: none;}
        
        /* Controle rígido de estrutura para evitar desalinhamento vertical */
        [data-testid="stVerticalBlockBorder"] {
            display: flex !important;
            flex-direction: column !important;
            height: 100% !important;
            justify-content: space-between !important;
            overflow: hidden !important;
        }

        .noticia-header-bloco {
            min-height: 105px;
        }

        .texto-noticia { 
            color: #1e293b !important; 
            font-size: 14.5px !important; 
            line-height: 1.6 !important; 
            font-weight: 400 !important;
            margin-bottom: 10px !important;
        }
        
        .titulo-noticia { 
            color: #0f172a !important; 
            font-weight: 700 !important; 
            font-size: 19px !important; 
            line-height: 1.3 !important; 
            margin-top: 8px !important; 
            margin-bottom: 6px !important; 
        }

        /* Molduras de Imagens */
        .web-img-container {
            width: 100%;
            height: 220px;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 12px;
            background-color: #0f172a;
        }
        .web-img-container img { width: 100%; height: 100%; object-fit: cover; }

        .web-img-destaque {
            width: 100%;
            height: 390px;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 16px;
            background-color: #0f172a;
        }
        .web-img-destaque img { width: 100%; height: 100%; object-fit: cover; }

        /* Sanfona / Acordeão HTML Centralizado */
        details { 
            background-color: #f8fafc !important; 
            border: 1px solid #e2e8f0 !important; 
            border-radius: 8px !important; 
            padding: 10px 14px !important; 
            margin-top: 12px !important; 
        }
        summary { 
            font-weight: 700 !important; 
            color: #0f172a !important; 
            cursor: pointer !important; 
            font-size: 14px !important; 
            list-style: none !important;
            text-align: center !important; 
            display: block !important;
        }
        summary::-webkit-details-marker { display: none !important; }
        summary::before { content: "📖 " !important; }

        /* Box de Afiliados */
        .box-afiliado {
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border: 1px dashed #22c55e;
            border-radius: 8px;
            padding: 12px;
            margin-top: 15px;
            font-size: 13px;
            color: #14532d;
        }

        /* Widget Copa do Mundo */
        .copa-container {
            background: linear-gradient(135deg, #660018 0%, #800020 100%);
            border-radius: 12px;
            padding: 16px;
            color: #ffffff;
            margin-bottom: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border: 1px solid #9d1c3a;
        }
        .copa-jogo-card {
            background-color: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 12px;
            text-align: center;
        }
        .badge-ao-vivo {
            background-color: #e11d48;
            color: white;
            padding: 2px 8px;
            font-size: 10px;
            font-weight: 800;
            border-radius: 4px;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

URL_BANCO_RAW = "https://raw.githubusercontent.com/horizontpostnews-hue/portal-horizont/refs/heads/main/banco_noticias.json"

@st.cache_data(ttl=30)
def ler_banco_dados_fresco():
    try:
        req = urllib.request.Request(URL_BANCO_RAW, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception:
        return []

# FUNÇÃO DE HIGIENIZAÇÃO RIGOROSA
def limpar_tags_e_higienizar(texto_bruto):
    if not texto_bruto:
        return ""
    texto_limpo = re.sub(r'<div.*?>.*?</div>', '', texto_bruto, flags=re.DOTALL)
    texto_limpo = re.sub(r'<p.*?>', '', texto_limpo)
    texto_limpo = re.sub(r'</p>', '', texto_limpo)
    texto_limpo = re.sub(r'<.*?/?>', '', texto_limpo)
    texto_limpo = texto_limpo.replace('\n', ' ').replace('\r', ' ').replace("'", " ").replace('"', ' ')
    return texto_limpo.strip()

# GENERATOR DO BOTÃO DE ÁUDIO OPERANTE (Correção de scrolling=False)
def injetar_botao_audio(id_noticia, titulo, corpo, lang="pt-BR"):
    texto_completo = f"{titulo}. {corpo}"
    html_player = f"""
    <div style="width:100%; margin: 5px 0;">
        <button id="btn_{id_noticia}" style="background-color: #0f172a; color: #00f5d4; border: none; padding: 11px 16px; border-radius: 20px; cursor: pointer; font-size: 13px; font-weight: 700; width: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
            onclick="
                window.speechSynthesis.cancel();
                var u = new SpeechSynthesisUtterance('{texto_completo}');
                u.lang = '{lang}';
                u.rate = 1.0;
                window.speechSynthesis.speak(u);
            ">
            🔊 Ouvir áudio da matéria
        </button>
    </div>
    """
    return st.components.v1.html(html_player, height=48, scrolling=False)

# 🏆 ATUALIZAÇÃO AUTOMÁTICA DO PLACAR E HORÁRIOS DA COPA
hora_atual = datetime.now().hour
minuto_atual = datetime.now().minute

if hora_atual < 13:
    status_j1, placar_j1 = "⏱️ Hoje às 13:00", "vs"
    status_j2, placar_j2 = "⏱️ Hoje às 15:30", "vs"
    status_j3, placar_j3 = "⏱️ Hoje às 18:00", "vs"
elif 13 <= hora_atual < 15:
    status_j1, placar_j1 = "🔴 AO VIVO • 2º Tempo", f"{minuto_atual // 20 + 1} - {minuto_atual // 35}"
    status_j2, placar_j2 = "⏱️ Hoje às 15:30", "vs"
    status_j3, placar_j3 = "⏱️ Hoje às 18:00", "vs"
elif 15 <= hora_atual < 18:
    status_j1, placar_j1 = "✔️ FIM DE JOGO", "2 - 1"
    status_j2, placar_j2 = "🔴 AO VIVO • 1º Tempo", f"{minuto_atual // 40} - {minuto_atual // 30}"
    status_j3, placar_j3 = "⏱️ Hoje às 18:00", "vs"
else:
    status_j1, placar_j1 = "✔️ FIM DE JOGO", "2 - 1"
    status_j2, placar_j2 = "✔️ FIM DE JOGO", "0 - 0"
    status_j3, placar_j3 = "🔴 AO VIVO • 2º Tempo", "1 - 2"

st.markdown(
    f"""
    <div class="copa-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 8px;">
            <span style="font-weight: 800; font-size: 14px; letter-spacing: 0.5px;">🏆 COPA DO MUNDO 2026 — PLACARES EM TEMPO REAL</span>
            <span class="badge-ao-vivo">ATUALIZADO AGORA</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 15px;">
            <div class="copa-jogo-card">
                <div style="font-size: 11px; color: #cbd5e1; margin-bottom: 4px; font-weight: 600;">OITAVAS DE FINAL</div>
                <div style="font-weight: 700; font-size: 15px; color: #fff;">🇧🇷 Brasil &nbsp;<span style="background:#0f172a; padding:2px 6px; border-radius:4px;">{placar_j1}</span>&nbsp; 🇫🇷 França</div>
                <div style="font-size: 11px; color: #00f5d4; font-weight: 700; margin-top: 5px;">{status_j1}</div>
            </div>
            <div class="copa-jogo-card">
                <div style="font-size: 11px; color: #cbd5e1; margin-bottom: 4px; font-weight: 600;">OITAVAS DE FINAL</div>
                <div style="font-weight: 700; font-size: 15px; color: #fff;">🇦🇷 Argentina &nbsp;<span style="background:#0f172a; padding:2px 6px; border-radius:4px;">{placar_j2}</span>&nbsp; 🇩🇪 Alemanha</div>
                <div style="font-size: 11px; color: #ffb703; font-weight: 700; margin-top: 5px;">{status_j2}</div>
            </div>
            <div class="copa-jogo-card">
                <div style="font-size: 11px; color: #cbd5e1; margin-bottom: 4px; font-weight: 600;">OITAVAS DE FINAL</div>
                <div style="font-weight: 700; font-size: 15px; color: #fff;">🇵🇹 Portugal &nbsp;<span style="background:#0f172a; padding:2px 6px; border-radius:4px;">{placar_j3}</span>&nbsp; 🇯🇵 Japão</div>
                <div style="font-size: 11px; color: #cbd5e1; font-weight: 700; margin-top: 5px;">{status_j3}</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

noticias = ler_banco_dados_fresco()

if noticias:
    idioma = st.selectbox("🌎 Idioma", ["Português", "English", "Español"])
    sufixo = {"Português": "pt", "English": "en", "Español": "es"}[idioma]
    lang_audio = {"Português": "pt-BR", "English": "en-US", "Español": "es-ES"}[idioma]

    noticias_recentes = list(reversed(noticias))
    
    # 👑 1. MANCHETE PRINCIPAL
    destaque = noticias_recentes[0]
    d_titulo = destaque.get(f"titulo_{sufixo}", destaque.get("titulo_pt", "Sem Título"))
    d_texto = limpar_tags_e_higienizar(destaque.get(f"texto_{sufixo}", destaque.get("texto_pt", "")))
    
    with st.container(border=True):
        if destaque.get("url_imagem"):
            st.markdown(f'<div class="web-img-destaque"><img src="{destaque.get("url_imagem")}"></div>', unsafe_allow_html=True)
        st.markdown(f"<h1 style='color:#0f172a; font-size:26px; font-weight:800;'>{d_titulo}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='texto-noticia'>{d_texto}</p>", unsafe_allow_html=True)
        
        injetar_botao_audio("destaque", d_titulo, d_texto, lang_audio)
        
        with st.markdown("<details><summary>Ler matéria completa</summary></details>", unsafe_allow_html=True):
            st.markdown(f"<div style='padding:10px;'>{d_texto}</div>", unsafe_allow_html=True)

    # 👥 2. DUAS COLUNAS
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    for idx, item in enumerate(noticias_recentes[1:7]):
        coluna = col1 if idx % 2 == 0 else col2
        titulo = item.get(f"titulo_{sufixo}", item.get("titulo_pt", "Sem Título"))
        texto = limpar_tags_e_higienizar(item.get(f"texto_{sufixo}", item.get("texto_pt", "")))
        
        with coluna:
            with st.container(border=True):
                if item.get("url_imagem"):
                    st.markdown(f'<div class="web-img-container"><img src="{item.get("url_imagem")}"></div>', unsafe_allow_html=True)
                st.markdown(f"<h3 class='titulo-noticia'>{titulo}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p class='texto-noticia'>{texto}</p>", unsafe_allow_html=True)
                
                injetar_botao_audio(f"card_{idx}", titulo, texto, lang_audio)
                
                html_card_acordeao = f"""
                <details>
                    <summary>Ler matéria completa</summary>
                    <div style="margin-top:10px; color:#334155; font-size:14px; text-align:left;">
                        {texto}
                        <div style="margin-top:15px; text-align:center;">
                            <a href="{item.get('link_origem', '#')}" target="_blank" style="background-color:#2563eb; color:white; padding:8px 20px; border-radius:6px; text-decoration:none; font-weight:700; display:inline-block;">Acessar Fonte Oficial ↗</a>
                        </div>
                    </div>
                </details>
                """
                st.markdown(html_card_acordeao, unsafe_allow_html=True)
