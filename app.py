import streamlit as st
import json
import urllib.request
import re

st.set_page_config(
    page_title="horizont.news — Conectando Gerações",
    page_icon="🌐",
    layout="wide"
)

# 🎨 ESTILIZAÇÃO COMPLETA E COMPACTAÇÃO DE LAYOUT (Estilo Capa de Grande Jornal)
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

        /* Moldura Proporcional para Imagens do Feed */
        .web-img-container {
            width: 100%;
            height: 220px;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 12px;
            background-color: #0f172a;
        }
        .web-img-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        /* Moldura Gigante de Manchete (Capa O Globo) */
        .web-img-destaque {
            width: 100%;
            height: 390px;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 16px;
            background-color: #0f172a;
        }
        .web-img-destaque img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        /* Sanfona / Acordeão Nativo HTML */
        details { background-color: #f8fafc !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; padding: 10px 14px !important; margin-top: 12px !important; }
        summary { font-weight: 600 !important; color: #0f172a !important; cursor: pointer !important; font-size: 14px !important; list-style: none !important; }
        summary::-webkit-details-marker { display: none !important; }
        summary::before { content: "📖 " !important; }

        /* Box de Monetização de Afiliados */
        .box-afiliado {
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border: 1px dashed #22c55e;
            border-radius: 8px;
            padding: 12px;
            margin-top: 15px;
            font-size: 13px;
            color: #14532d;
        }

        /* Botão de Áudio Injetado Seguro */
        .btn-audio-container {
            width: 100% !important;
            overflow: hidden !important;
            display: block !important;
            margin-top: 5px !important;
            margin-bottom: 5px !important;
        }
        
        .btn-audio-player {
            background-color: #0f172a !important; 
            color: #00f5d4 !important; 
            border: none !important; 
            padding: 11px 16px !important; 
            border-radius: 20px !important; 
            cursor: pointer !important; 
            font-size: 13px !important; 
            font-weight: 700 !important; 
            width: 100% !important; 
            text-align: center !important;
            display: block !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            text-decoration: none !important;
            box-sizing: border-box !important;
        }
        .btn-audio-player:hover {
            background-color: #1e293b !important;
        }

        /* Widget Copa do Mundo (Estilo Al Jazeera Live) */
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
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.7; }
            50% { opacity: 1; }
            100% { opacity: 0.7; }
        }
    </style>
    """, 
    unsafe_allow_html=True
)

URL_BANCO_RAW = "https://raw.githubusercontent.com/horizontpostnews-hue/portal-horizont/refs/heads/main/banco_noticias.json"

@st.cache_data(ttl=60)
def ler_banco_dados_fresco():
    try:
        req = urllib.request.Request(URL_BANCO_RAW, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception:
        return []

# BANNER PRINCIPAL (HEADER DO PORTAL)
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding:25px; border-radius:14px; margin-bottom:15px; text-align:center; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
        <h1 style="color:#00f5d4; margin:0; font-weight:800; letter-spacing: -1px; font-size: 34px; display:inline-block; vertical-align:middle;">🌐 horizont.news</h1>
        <p style="color:#94a3b8; font-size:13px; margin:6px 0 0 0; font-weight:400; letter-spacing: 0.5px;">Informação Sem Fronteiras — Pluralidade Global e Independente para Mentes Conectadas</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# MARQUEE INICIAL DE COBERTURA
st.markdown("<marquee style='width: 100%; color: #0f172a; background-color: #00f5d4; padding: 8px; font-size: 13px; font-weight: 700; border-radius: 8px; margin-bottom: 10px;'>⚡ PERSPECTIVAS EM FOCO: Cobertura internacional integrada em equilíbrio com as mídias regionais e independentes do Brasil...</marquee>", unsafe_allow_html=True)

noticias = ler_banco_dados_fresco()

# GIRO GLOBAL TICKER (ÚLTIMAS NOTÍCIAS DINÂMICAS)
if noticias and isinstance(noticias, list):
    ultimas_noticias_titulos = [item.get("titulo_pt", "Nova matéria integrada") for item in noticias[-5:] if isinstance(item, dict)]
    string_ticker = " &nbsp;&nbsp;&nbsp;&nbsp; 🔴 &nbsp;&nbsp;&nbsp;&nbsp; ".join(ultimas_noticias_titulos)
    
    html_segundo_banner = f"""
    <div style="width: 100%; background-color: #1e293b; padding: 8px; border-radius: 8px; margin-bottom: 25px; display: flex; align-items: center; border: 1px solid #334155;">
        <span style="background-color: #e11d48; color: white; font-size: 11px; font-weight: 800; padding: 2px 8px; border-radius: 4px; margin-right: 12px; text-transform: uppercase; white-space: nowrap;">Giro Global</span>
        <marquee style="color: #f8fafc; font-size: 13px; font-weight: 500;" scrollamount="5" onmouseover="this.stop();" onmouseout="this.start();">
            {string_ticker}
        </marquee>
    </div>
    """
    st.markdown(html_segundo_banner, unsafe_allow_html=True)
else:
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

# 🏆 SECTION: COPA DO MUNDO WIDGET (ESTILO LIVE BLOCK DA AL JAZEERA)
st.markdown(
    """
    <div class="copa-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 8px;">
            <span style="font-weight: 800; font-size: 14px; letter-spacing: 0.5px; display: flex; align-items: center; gap: 6px;">🏆 COPA DO MUNDO 2026 — COBERTURA INTEGRADA</span>
            <span class="badge-ao-vivo">🔴 AO VIVO</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 15px;">
            <div class="copa-jogo-card">
                <div style="font-size: 11px; color: #cbd5e1; margin-bottom: 4px; text-transform: uppercase; font-weight: 600;">Grupo A • Rodada 2</div>
                <div style="font-weight: 700; font-size: 15px; color: #fff;">🇧🇷 Brasil &nbsp;<span style="background:#0f172a; padding:2px 8px; border-radius:4px; font-size:14px; margin: 0 2px;">2</span>&nbsp; vs &nbsp;<span style="background:#0f172a; padding:2px 8px; border-radius:4px; font-size:14px; margin: 0 2px;">1</span>&nbsp; 🇫🇷 França</div>
                <div style="font-size: 11px; color: #00f5d4; font-weight: 700; margin-top: 5px;">FIM DE JOGO</div>
            </div>
            <div class="copa-jogo-card">
                <div style="font-size: 11px; color: #cbd5e1; margin-bottom: 4px; text-transform: uppercase; font-weight: 600;">Grupo B • Rodada 2</div>
                <div style="font-weight: 700; font-size: 15px; color: #fff;">🇦🇷 Argentina &nbsp;<span style="background:#e11d48; padding:2px 8px; border-radius:4px; font-size:14px; margin: 0 2px;">0</span>&nbsp; vs &nbsp;<span style="background:#e11d48; padding:2px 8px; border-radius:4px; font-size:14px; margin: 0 2px;">0</span>&nbsp; 🇩🇪 Alemanha</div>
                <div style="font-size: 11px; color: #ffb703; font-weight: 700; margin-top: 5px;">⏱️ 2º TEMPO — 68'</div>
            </div>
            <div class="copa-jogo-card">
                <div style="font-size: 11px; color: #cbd5e1; margin-bottom: 4px; text-transform: uppercase; font-weight: 600;">Próximo Confronto • Hoje 16:00</div>
                <div style="font-weight: 700; font-size: 15px; color: #fff;">🇵🇹 Portugal &nbsp; vs &nbsp; 🇯🇵 Japão</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 5px;">Estádio Icônico de Lusail</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

def obter_cor_categoria(cat):
    cores = {"Política": "#e11d48", "Economia": "#16a34a", "Cotidiano": "#2563eb", "Esportes": "#ea580c", "Cultura & Pop": "#db2777", "Tech & Ciência": "#7c3aed", "Viver Bem": "#0d9488"}
    return cores.get(cat, "#4b5563")

def obter_oferta_afiliado(categoria):
    campanhas = {
        "Economia": {
            "texto": "📚 <b>Leitura Recomendada:</b> Entenda os ciclos financeiros globais com os livros mais vendidos da Amazon sobre macroeconomia.",
            "cupom": "FRETE GRÁTIS PRIME",
            "link": "https://www.amazon.com.br?tag=seu_id_afiliado-20"
        },
        "Tech & Ciência": {
            "texto": "💻 <b>Upgrade Tecnológico:</b> Procurando gadgets para aumentar a produtividade? Confira a seleção semanal com até 20% OFF.",
            "cupom": "TECHHORIZONT",
            "link": "https://www.amazon.com.br?tag=seu_id_afiliado-20"
        },
        "Cultura & Pop": {
            "texto": "🎟️ <b>Cinema & Streaming:</b> Assine o Amazon Prime e tenha acesso a milhares de filmes, séries e músicas. Teste grátis por 30 dias.",
            "cupom": "TESTE_GRATIS_30D",
            "link": "https://www.amazon.com.br?tag=seu_id_afiliado-20"
        },
        "Esportes": {
            "texto": "👟 <b>Alta Performance:</b> Renove seus equipamentos e roupas esportivas diretamente nas lojas oficiais parceiras com descontos exclusivos.",
            "cupom": "FITNESS10",
            "link": "https://www.amazon.com.br?tag=seu_id_afiliado-20"
        }
    }
    padrao = {
        "texto": "📖 <b>Mantenha-se Informado:</b> Dispositivos Kindle com condições especiais de parcelamento na Amazon para ler em qualquer lugar.",
        "cupom": "KINDLE2026",
        "link": "https://www.amazon.com.br?tag=seu_id_afiliado-20"
    }
    return campanhas.get(categoria, padrao)

def limpar_tags_e_higienizar(texto_bruto):
    if not texto_bruto:
        return ""
    texto_limpo = re.sub(r'<div class="box-afiliado">.*?</div>', '', texto_bruto, flags=re.DOTALL)
    texto_limpo = re.sub(r'<div style=.*?</div>', '', texto_limpo, flags=re.DOTALL)
    texto_limpo = re.sub(r'<.*?/?>', '', texto_limpo)
    # Higienização contra quebras de texto e aspas que quebram JavaScript
    texto_limpo = texto_limpo.replace('\n', ' ').replace('\r', ' ').replace("'", "\\'").replace('"', '&quot;')
    return texto_limpo.strip()

if not noticias:
    st.info("📢 Sincronizando feeds mundiais e regionais...")
else:
    # CONFIGURAÇÃO DE SELEÇÃO E FILTROS DO PORTAL
    col_lang, col_filtro = st.columns(2)
    with col_lang:
        idioma = st.selectbox("🌎 Escolha seu Idioma", ["Português", "English", "Español"])
        sufixo = {"Português": "pt", "English": "en", "Español": "es"}[idioma]
        lang_audio = {"Português": "pt-BR", "English": "en-US", "Español": "es-ES"}[idioma]

    opcoes_filtro = ["Feed Completo (Todos os Assuntos)"]
    if isinstance(noticias, list):
        categorias_extraidas = sorted(list(set(item.get("categoria", "Política") for item in noticias if isinstance(item, dict))))
        opcoes_filtro.extend(categorias_extraidas)

    with col_filtro:
        categoria_selecionada = st.selectbox("🎯 Filtrar Canal", opcoes_filtro)

    noticias_recentes = list(reversed(noticias))
    if categoria_selecionada != "Feed Completo (Todos os Assuntos)":
        noticias_recentes = [n for n in noticias_recentes if isinstance(n, dict) and n.get("categoria", "Política") == categoria_selecionada]
    
    if not noticias_recentes:
        st.warning(f"Sem registros novos para este canal.")
    else:
        # 👑 1. MANCHETE DE CAPA (LARGURA TOTAL - ESTILO O GLOBO PRINCIPAL)
        destaque = noticias_recentes[0]
        noticias_restantes = noticias_recentes[1:]
        
        d_titulo = destaque.get(f"titulo_{sufixo}", destaque.get("titulo_pt", "Sem Título"))
        d_texto_bruto = destaque.get(f"texto_{sufixo}", destaque.get("texto_pt", "Sem Conteúdo"))
        d_texto = limpar_tags_e_higienizar(d_texto_bruto)
        d_categoria = destaque.get("categoria", "Política")
        d_subcategoria = destaque.get("subcategoria", "")
        d_link_origem = destaque.get("link_origem", "#")
        d_url_foto = destaque.get("url_imagem")
        d_fonte = destaque.get("fonte_origem", "Fonte Externa")
        
        d_cor = obter_cor_categoria(d_categoria)
        d_tag_html = f"<span style='background-color:{d_cor}; color:white; padding:5px 12px; border-radius:12px; font-size:11px; font-weight:700; text-transform:uppercase; margin-right:6px;'>{d_categoria}</span>"
        if d_subcategoria:
            d_tag_html += f"<span style='background-color:#e2e8f0; color:#475569; padding:5px 12px; border-radius:12px; font-size:11px; font-weight:600; text-transform:uppercase;'>📍 {d_subcategoria}</span>"
        
        st.markdown("<h2 style='color:#0f172a; font-weight:800; font-size:22px; margin-top:10px; margin-bottom:15px; border-left: 5px solid #00f5d4; padding-left:10px; letter-spacing:-0.5px;'>📰 MANCHETE PRINCIPAL</h2>", unsafe_allow_html=True)
        
        with st.container(border=True):
            if d_url_foto and str(d_url_foto).strip() != "":
                st.markdown(f'<div class="web-img-destaque"><img src="{d_url_foto}" alt="Destaque Principal"></div>', unsafe_allow_html=True)
            
            st.markdown(
                f"""
                <div style='margin-bottom:10px;'>{d_tag_html}</div>
                <h1 style='color:#0f172a; font-size:28px; font-weight:800; line-height:1.2; margin-top:8px; margin-bottom:8px; letter-spacing:-0.5px;'>{d_titulo}</h1>
                <p style='color:#64748b; font-size:12px; margin-bottom:15px;'>📅 {destaque.get('data')} • Cobertura Exclusiva por <b>{d_fonte}</b></p>
                <p style='color:#1e293b; font-size:15.5px; line-height:1.7; font-weight:400; margin-bottom:18px;'>{d_texto}</p>
                """, 
                unsafe_allow_html=True
            )
            
            # Botão de Áudio Seguro da Manchete
            html_audio_destaque = f"""
            <div class="btn-audio-container">
                <button class="btn-audio-player" onclick="window.speechSynthesis.cancel(); setTimeout(function(){{ var msg = new SpeechSynthesisUtterance('{d_titulo}. {d_texto}'); msg.lang='{lang_audio}'; window.speechSynthesis.speak(msg); }}, 40);">
                    🔊 Ouvir a manchete em áudio
                </button>
            </div>
            """
            st.markdown(html_audio_destaque, unsafe_allow_html=True)
            
            # Acordeão Expandido da Manchete
            d_resumo = limpar_tags_e_higienizar(destaque.get('resumo_longo', destaque.get('texto_pt', '')))
            if not d_resumo: d_resumo = d_texto
            d_oferta = obter_oferta_afiliado(d_categoria)
            
            html_acordeao_destaque = f"""
            <details>
                <summary>Ler cobertura completa da manchete</summary>
                <div style="margin-top: 10px; color: #334155; font-size: 14.5px; line-height: 1.6;">
                    <p style="font-style: italic; margin-bottom: 15px;">{d_resumo}</p>
                    <p style="font-size: 13px; color: #475569; margin-top: 10px; border-top: 1px dashed #e2e8f0; padding-top: 8px;">🏛️ <b>Fonte verificada:</b> {d_fonte}</p>
                    <div class="box-afiliado">
                        {d_oferta['texto']}<br>
                        <span style="background-color:#22c55e; color:white; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:700; display:inline-block; margin-top:5px;">CUPOM: {d_oferta['cupom']}</span>
                        <div style="margin-top:8px; text-align:right;"><a href="{d_oferta['link']}" target="_blank" style="background-color:#14532d; color:#ffffff; padding:4px 10px; border-radius:6px; text-decoration:none; font-size:12px; font-weight:700;">Aproveitar Oferta ↗</a></div>
                    </div>
                    <div style="margin-top: 20px; text-align: center; border-top: 1px solid #e2e8f0; padding-top:15px;">
                        <a href="{d_link_origem}" target="_blank" style="background-color: #2563eb; color: white; padding: 8px 24px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 700; display: inline-block; max-width: 250px; text-align: center;">Acessar Fonte Oficial ↗</a>
                    </div>
                </div>
            </details>
            """
            st.markdown(html_acordeao_destaque, unsafe_allow_html=True)

        st.markdown("<br><h2 style='color:#0f172a; font-weight:800; font-size:20px; margin-bottom:15px; border-left: 5px solid #16a34a; padding-left:10px; letter-spacing:-0.5px;'>🌐 OUTRAS MATÉRIAS DO FEED</h2>", unsafe_allow_html=True)
        
        # 👥 2. CRIAÇÃO DAS DUAS COLUNAS TRADICIONAIS PARA O RESTANTE DO FEED
        col1, col2 = st.columns(2)
        
        for index, item in enumerate(noticias_restantes):
            if not isinstance(item, dict):
                continue
                
            coluna_atual = col1 if index % 2 == 0 else col2
            
            titulo = item.get(f"titulo_{sufixo}", item.get("titulo_pt", "Sem Título"))
            texto_base = item.get(f"texto_{sufixo}", item.get("texto_pt", "Sem Conteúdo"))
            texto = limpar_tags_e_higienizar(texto_base)
            categoria = item.get("categoria", "Política")
            subcategoria = item.get("subcategoria", "")
            link_origem = item.get("link_origem", "#")
            url_foto = item.get("url_imagem")
            fonte_origem = item.get("fonte_origem", "Fonte Externa")
            
            cor_tag = obter_cor_categoria(categoria)
            
            tag_html = f"<span style='background-color:{cor_tag}; color:white; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:700; text-transform:uppercase; margin-right:6px;'>{categoria}</span>"
            if subcategoria:
                tag_html += f"<span style='background-color:#e2e8f0; color:#475569; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:600; text-transform:uppercase;'>📍 {subcategoria}</span>"
            
            oferta = obter_oferta_afiliado(categoria)

            with coluna_atual:
                with st.container(border=True):
                    if url_foto and str(url_foto).strip() != "":
                        st.markdown(f'<div class="web-img-container"><img src="{url_foto}" alt="Notícia"></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="web-img-container" style="display: flex; align-items: center; justify-content: center;"><div style="color: #00f5d4; font-weight: 800; font-size: 20px;">🌐 horizont.news</div></div>', unsafe_allow_html=True)
                    
                    st.markdown(
                        f"""
                        <div class="noticia-header-bloco">
                            <div style='margin-bottom:8px;'>{tag_html}</div>
                            <h3 class='titulo-noticia'>{titulo}</h3>
                            <p style='color:#64748b; font-size:12px; margin-bottom:12px;'>📅 {item.get('data')} • 🏛️ Fonte: <b>{fonte_origem}</b></p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    st.markdown(f"<p class='texto-noticia'>{texto}</p>", unsafe_allow_html=True)
                    st.divider()
                    
                    # Botão de Áudio do Card Individual
                    html_audio_direto = f"""
                    <div class="btn-audio-container">
                        <button class="btn-audio-player" onclick="window.speechSynthesis.cancel(); setTimeout(function(){{ var msg = new SpeechSynthesisUtterance('{titulo}. {texto}'); msg.lang='{lang_audio}'; window.speechSynthesis.speak(msg); }}, 40);">
                            🔊 Ouvir a matéria em áudio
                        </button>
                    </div>
                    """
                    st.markdown(html_audio_direto, unsafe_allow_html=True)
                    
                    # Acordeão do Card Individual
                    resumo_bruto = item.get('resumo_longo', item.get('texto_pt', ''))
                    resumo_denso = limpar_tags_e_higienizar(resumo_bruto)
                    if not resumo_denso:
                        resumo_denso = texto

                    html_acordeao = f"""
                    <details>
                        <summary>Ler matéria completa</summary>
                        <div style="margin-top: 10px; color: #334155; font-size: 14.5px; line-height: 1.6;">
                            <strong style="color: #0f172a; display: block; margin-bottom: 6px;">{titulo}</strong>
                            <p style="font-style: italic; margin-bottom: 15px;">{resumo_denso}</p>
                            
                            <p style="font-size: 13px; color: #475569; margin-top: 10px; border-top: 1px dashed #e2e8f0; padding-top: 8px;">🏛️ <b>Fonte da notícia:</b> {fonte_origem}</p>
                            
                            <div class="box-afiliado">
                                {oferta['texto']}<br>
                                <span style="background-color:#22c55e; color:white; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:700; display:inline-block; margin-top:5px;">CUPOM: {oferta['cupom']}</span>
                                <div style="margin-top:8px; text-align:right;">
                                    <a href="{oferta['link']}" target="_blank" style="background-color:#14532d; color:#ffffff; padding:4px 10px; border-radius:6px; text-decoration:none; font-size:12px; font-weight:700;">Aproveitar Oferta ↗</a>
                                </div>
                            </div>

                            <div style="margin-top: 20px; text-align: center; border-top: 1px solid #e2e8f0; padding-top:15px;">
                                <a href="{link_origem}" target="_blank" style="background-color: #2563eb; color: white; padding: 8px 24px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 700; display: inline-block; max-width: 250px; text-align: center;">Acessar Fonte Oficial ↗</a>
                            </div>
                        </div>
                    </details>
                    """
                    st.markdown(html_acordeao, unsafe_allow_html=True)

# RODAPÉ ESTÁTICO DO PORTAL
st.markdown("<br><br><div style='border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center; color: #64748b; font-size: 12px;'><p style='margin: 0;'>🌐 horizont.news — Todos os direitos reservados.</p></div>", unsafe_allow_html=True)
