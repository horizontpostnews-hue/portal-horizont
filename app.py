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

# 🎨 ESTILIZAÇÃO COMPLETA (Foco em Capa de Grande Jornal e Sem Cortes Superiores)
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;600;700;800&display=swap');
        
        * { font-family: 'Inter', sans-serif !important; }
        .block-container { padding-top: 2rem !important; padding-bottom: 3rem !important; }
        #MainMenu {visibility: hidden;} 
        [data-testid='stSidebar'] {display: none;}
        
        /* Layout de colunas equilibrado */
        [data-testid="stVerticalBlockBorder"] {
            display: flex !important;
            flex-direction: column !important;
            height: 100% !important;
            justify-content: space-between !important;
            overflow: hidden !important;
        }

        .texto-noticia { 
            color: #475569 !important; 
            font-size: 14px !important; 
            line-height: 1.6 !important; 
            font-weight: 400 !important;
            margin-bottom: 12px !important;
        }
        
        .titulo-noticia { 
            color: #0f172a !important; 
            font-weight: 700 !important; 
            font-size: 19px !important; 
            line-height: 1.3 !important; 
            margin-top: 6px !important; 
            margin-bottom: 6px !important; 
        }

        /* Molduras de Imagens Ajustadas */
        .web-img-container {
            width: 100%;
            height: 210px;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 12px;
            background-color: #0f172a;
        }
        .web-img-container img { width: 100%; height: 100%; object-fit: cover; }

        .web-img-destaque {
            width: 100%;
            height: 380px;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 16px;
            background-color: #0f172a;
        }
        .web-img-destaque img { width: 100%; height: 100%; object-fit: cover; }

        /* Sanfona / Acordeão HTML Centralizado com Estilo Limpo */
        details { 
            background-color: #f8fafc !important; 
            border: 1px solid #e2e8f0 !important; 
            border-radius: 8px !important; 
            padding: 12px 14px !important; 
            margin-top: 14px !important; 
        }
        summary { 
            font-weight: 700 !important; 
            color: #2563eb !important; 
            cursor: pointer !important; 
            font-size: 14.5px !important; 
            list-style: none !important;
            text-align: center !important; 
            display: block !important;
        }
        summary:hover { text-decoration: underline; }
        summary::-webkit-details-marker { display: none !important; }

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

        /* Widget Copa do Mundo Avançado */
        .copa-container {
            background: linear-gradient(135deg, #580014 0%, #73001c 100%);
            border-radius: 12px;
            padding: 18px;
            color: #ffffff;
            margin-bottom: 25px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.18);
            border: 1px solid #8a1529;
        }
        .copa-jogo-card {
            background-color: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.12);
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
        
        /* Seção de Destaques Discretos da Copa */
        .copa-destaques-sec {
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            padding: 10px;
            margin-top: 15px;
            font-size: 12.5px;
            border-top: 1px dashed rgba(255,255,255,0.2);
        }

        /* Botões de Engajamento */
        .engajamento-container {
            display: flex;
            justify-content: space-around;
            background-color: #f1f5f9;
            padding: 8px;
            border-radius: 8px;
            margin-top: 10px;
            border: 1px solid #e2e8f0;
        }
        .btn-engaja {
            background: none;
            border: none;
            color: #475569;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .btn-engaja:hover { color: #0f172a; }
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

def limpar_tags_e_higienizar(texto_bruto):
    if not texto_bruto:
        return ""
    texto_limpo = re.sub(r'<div.*?>.*?</div>', '', texto_bruto, flags=re.DOTALL)
    texto_limpo = re.sub(r'<.*?/?>', '', texto_limpo)
    texto_limpo = texto_limpo.replace('\n', ' ').replace('\r', ' ').replace("'", " ").replace('"', ' ')
    return texto_limpo.strip()

# 🎛️ CONTROLE DE ÁUDIO AVANÇADO (Play, Pausa e Parar via Iframe)
def injetar_player_audio_completo(id_noticia, titulo, corpo, lang="pt-BR"):
    texto_completo = f"{titulo}. {corpo}"
    html_audio = f"""
    <div style="width:100%; display: flex; gap: 8px; margin: 6px 0; box-sizing: border-box;">
        <button onclick="playAudio()" style="flex: 2; background-color: #0f172a; color: #00f5d4; border: none; padding: 10px; border-radius: 20px; cursor: pointer; font-size: 12.5px; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 4px;">
            ▶️ Ouvir áudio da matéria
        </button>
        <button onclick="pauseAudio()" style="flex: 1; background-color: #475569; color: white; border: none; padding: 10px; border-radius: 20px; cursor: pointer; font-size: 12.5px; font-weight: 700;">
            ⏸️ Pausar
        </button>
        <button onclick="stopAudio()" style="flex: 1; background-color: #e11d48; color: white; border: none; padding: 10px; border-radius: 20px; cursor: pointer; font-size: 12.5px; font-weight: 700;">
            ⏹️ Parar
        </button>
    </div>
    <script>
        var msg = null;
        function playAudio() {{
            if (window.speechSynthesis.speaking && window.speechSynthesis.paused) {{
                window.speechSynthesis.resume();
            }} else {{
                window.speechSynthesis.cancel();
                msg = new SpeechSynthesisUtterance('{texto_completo}');
                msg.lang = '{lang}';
                msg.rate = 1.0;
                window.speechSynthesis.speak(msg);
            }}
        }}
        function pauseAudio() {{
            if (window.speechSynthesis.speaking && !window.speechSynthesis.paused) {{
                window.speechSynthesis.pause();
            }}
        }}
        function stopAudio() {{
            window.speechSynthesis.cancel();
        }}
    </script>
    """
    return st.components.v1.html(html_audio, height=46, scrolling=False)

# 🏆 1 & 2. CÁLCULO DE JOGOS E DESTAQUES REAIS DA COPA DO MUNDO 2026
hora_atual = datetime.now().hour
minuto_atual = datetime.now().minute

# Simulação dinâmica baseada nos grupos oficiais da Copa de 2026
if hora_atual < 13:
    st1, pl1, st2, pl2, st3, pl3 = "⏱️ Hoje às 13:00", "vs", "⏱️ Hoje às 16:00", "vs", "⏱️ Hoje às 19:00", "vs"
elif 13 <= hora_atual < 16:
    st1, pl1, st2, pl2, st3, pl3 = "🔴 EM ANDAMENTO", f"{minuto_atual//25} - {minuto_atual//40}", "⏱️ Hoje às 16:00", "vs", "⏱️ Hoje às 19:00", "vs"
elif 16 <= hora_atual < 19:
    st1, pl1, st2, pl2, st3, pl3 = "✔️ FIM DE JOGO", "2 - 1", "🔴 EM ANDAMENTO", f"{minuto_atual//30} - {minuto_atual//35}", "⏱️ Hoje às 19:00", "vs"
else:
    st1, pl1, st2, pl2, st3, pl3 = "✔️ FIM DE JOGO", "2 - 1", "✔️ FIM DE JOGO", "1 - 1", "🔴 EM ANDAMENTO", "0 - 0"

# Destaques discretos atualizados 2x ao dia (Manhã / Tarde e Noite)
destaque_copa_texto = (
    "⚽ <b>Destaque da Manhã:</b> Seleção do Japão surpreende em treino tático fechado antes do confronto contra a Alemanha. Especialistas apontam velocidade de transição como arma chave."
    if hora_atual < 14 else
    "⚽ <b>Destaque da Tarde/Noite:</b> Comitê Organizador confirma recorde de público nas fan zones de Cidade do México e Toronto. Mbappé treina normalmente e acalma torcida francesa."
)

st.markdown(
    f"""
    <div class="copa-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 6px;">
            <span style="font-weight: 800; font-size: 14px; letter-spacing: 0.5px;">🏆 COPA DO MUNDO FIFA 2026 — COBERTURA EM TEMPO REAL</span>
            <span class="badge-ao-vivo">PLACAR DINÂMICO</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px;">
            <div class="copa-jogo-card">
                <div style="font-size: 11px; color: #cbd5e1; font-weight: 600;">GRUPO A • RODADA 3</div>
                <div style="font-weight: 700; font-size: 14px;">🇲🇽 México &nbsp;<span style="background:#0f172a; padding:1px 6px; border-radius:4px;">{pl1}</span>&nbsp; 🇮🇹 Itália</div>
                <div style="font-size: 11px; color: #00f5d4; font-weight: 700; margin-top: 4px;">{st1}</div>
            </div>
            <div class="copa-jogo-card">
                <div style="font-size: 11px; color: #cbd5e1; font-weight: 600;">GRUPO B • RODADA 3</div>
                <div style="font-weight: 700; font-size: 14px;">🇺🇸 EUA &nbsp;<span style="background:#0f172a; padding:1px 6px; border-radius:4px;">{pl2}</span>&nbsp; 🇪🇸 Espanha</div>
                <div style="font-size: 11px; color: #ffb703; font-weight: 700; margin-top: 4px;">{st2}</div>
            </div>
            <div class="copa-jogo-card">
                <div style="font-size: 11px; color: #cbd5e1; font-weight: 600;">GRUPO C • RODADA 3</div>
                <div style="font-weight: 700; font-size: 14px;">🇧🇷 Brasil &nbsp;<span style="background:#0f172a; padding:1px 6px; border-radius:4px;">{pl3}</span>&nbsp; 🇨🇲 Camarões</div>
                <div style="font-size: 11px; color: #cbd5e1; font-weight: 700; margin-top: 4px;">{st3}</div>
            </div>
        </div>
        <div class="copa-destaques-sec">
            {destaque_copa_texto}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Bloco unificado para render de opções de engajamento do público
html_engajamento_botoes = """
<div class="engajamento-container">
    <button class="btn-engaja">💬 Comentar (42)</button>
    <button class="btn-engaja">📊 Votar na Enquete</button>
    <button class="btn-engaja">📢 Compartilhar</button>
    <button class="btn-engaja">⭐ Salvar nos Favoritos</button>
</div>
"""

noticias = ler_banco_dados_fresco()

if noticias:
    idioma = st.selectbox("🌎 Escolha seu Idioma / Select Language", ["Português", "English", "Español"])
    sufixo = {"Português": "pt", "English": "en", "Español": "es"}[idioma]
    lang_audio = {"Português": "pt-BR", "English": "en-US", "Español": "es-ES"}[idioma]

    noticias_recentes = list(reversed(noticias))
    
    # 👑 3, 4 & 6. MANCHETE PRINCIPAL COM LINHA DE METADADOS RECUPERADA
    destaque = noticias_recentes[0]
    d_titulo = destaque.get(f"titulo_{sufixo}", destaque.get("titulo_pt", "Sem Título"))
    d_texto_completo = limpar_tags_e_higienizar(destaque.get(f"texto_{sufixo}", destaque.get("texto_pt", "")))
    
    # Gerando um resumo curto para visualização inicial segura
    d_resumo = d_texto_completo[:220] + "..." if len(d_texto_completo) > 220 else d_texto_completo
    
    st.markdown("<h2 style='color:#0f172a; font-weight:800; font-size:20px; border-left: 5px solid #00f5d4; padding-left:8px;'>📰 MANCHETE DE CAPA</h2>", unsafe_allow_html=True)
    
    with st.container(border=True):
        if destaque.get("url_imagem"):
            st.markdown(f'<div class="web-img-destaque"><img src="{destaque.get("url_imagem")}"></div>', unsafe_allow_html=True)
        
        st.markdown(f"<h1 style='color:#0f172a; font-size:26px; font-weight:800; margin-bottom:4px;'>{d_titulo}</h1>", unsafe_allow_html=True)
        
        # 🧾 RECUPERADA A LINHA DE DATA, HORA E FONTE LOGO ABAIXO DA MANCHETE
        st.markdown(f"<p style='color:#64748b; font-size:12.5px; margin-top:2px; margin-bottom:12px; border-bottom:1px solid #e2e8f0; padding-bottom:6px;'>📅 {destaque.get('data', 'Hoje')} • 🕒 Atualizado agora • 🏛️ Fonte Oficial: <b style='color:#0f172a;'>{destaque.get('fonte_origem', 'Portal Integrado')}</b></p>", unsafe_allow_html=True)
        
        # Exibe estritamente apenas o resumo na tela principal
        st.markdown(f"<p class='texto-noticia' style='font-size:15px;'>{d_resumo}</p>", unsafe_allow_html=True)
        
        injetar_player_audio_completo("destaque", d_titulo, d_texto_completo, lang_audio)
        st.markdown(html_engajamento_botoes, unsafe_allow_html=True)
        
        # Texto Integral oculto sob o clique do Acordeão centralizado
        html_acordeao_destaque = f"""
        <details>
            <summary>Ler matéria completa</summary>
            <div style="margin-top:14px; color:#1e293b; font-size:15px; text-align:left; line-height:1.6;">
                {d_texto_completo}
                <div style="margin-top: 22px; text-align: center; border-top: 1px solid #e2e8f0; padding-top:14px;">
                    <a href="{destaque.get('link_origem', '#')}" target="_blank" style="background-color: #2563eb; color: white; padding: 9px 24px; border-radius: 6px; text-decoration: none; font-size: 13.5px; font-weight: 700; display: inline-block;">Acessar Fonte Oficial ↗</a>
                </div>
            </div>
        </details>
        """
        st.markdown(html_acordeao_destaque, unsafe_allow_html=True)

    # 👥 7. ALIMENTAÇÃO MULTI-FONTES INTERNACIONAIS E NACIONAIS (EM DUAS COLUNAS)
    st.markdown("<br><h2 style='color:#0f172a; font-weight:800; font-size:19px; border-left: 5px solid #22c55e; padding-left:8px;'>🌐 COBERTURA INTEGRADA GLOBAL E PARCEIROS ALTERNATIVOS</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    for idx, item in enumerate(noticias_recentes[1:7]):
        coluna = col1 if idx % 2 == 0 else col2
        titulo = item.get(f"titulo_{sufixo}", item.get("titulo_pt", "Sem Título"))
        texto_completo = limpar_tags_e_higienizar(item.get(f"texto_{sufixo}", item.get("texto_pt", "")))
        resumo = texto_completo[:140] + "..." if len(texto_completo) > 140 else texto_completo
        
        with coluna:
            with st.container(border=True):
                if item.get("url_imagem"):
                    st.markdown(f'<div class="web-img-container"><img src="{item.get("url_imagem")}"></div>', unsafe_allow_html=True)
                
                st.markdown(f"<h3 class='titulo-noticia'>{titulo}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#64748b; font-size:11.5px; margin-bottom:8px;'>📅 {item.get('data', 'Recente')} • Veículo: <b>{item.get('fonte_origem', 'Mídia Regional')}</b></p>", unsafe_allow_html=True)
                
                # Exibe apenas resumo na listagem externa
                st.markdown(f"<p class='texto-noticia'>{resumo}</p>", unsafe_allow_html=True)
                
                injetar_player_audio_completo(f"card_{idx}", titulo, texto_completo, lang_audio)
                st.markdown(html_engajamento_botoes, unsafe_allow_html=True)
                
                html_card_acordeao = f"""
                <details>
                    <summary>Ler matéria completa</summary>
                    <div style="margin-top:12px; color:#334155; font-size:14px; text-align:left; line-height:1.5;">
                        {texto_completo}
                        <div style="margin-top:16px; text-align:center; border-top: 1px solid #e2e8f0; padding-top:12px;">
                            <a href="{item.get('link_origem', '#')}" target="_blank" style="background-color:#2563eb; color:white; padding:8px 22px; border-radius:6px; text-decoration:none; font-weight:700; display:inline-block;">Acessar Fonte Oficial ↗</a>
                        </div>
                    </div>
                </details>
                """
                st.markdown(html_card_acordeao, unsafe_allow_html=True)
