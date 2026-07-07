import streamlit as st
import json
import urllib.request
import re

st.set_page_config(
    page_title="horizont.news — Conectando Gerações",
    page_icon="🌐",
    layout="wide"
)

# ESTILIZAÇÃO DO PORTAL (OTIMIZADA PARA ELIMINAR SCROLLBARS INDESEJADAS)
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;600;700&display=swap');
        
        * { font-family: 'Inter', sans-serif !important; }
        .block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; }
        #MainMenu {visibility: hidden;} 
        [data-testid='stSidebar'] {display: none;}
        
        /* Forçar todos os cards a terem uma estrutura vertical alinhada */
        [data-testid="stVerticalBlockBorder"] {
            display: flex !important;
            flex-direction: column !important;
            height: 100% !important;
            justify-content: space-between !important;
            overflow: hidden !important;
        }

        /* Limitar o tamanho do bloco de texto superior para alinhar as colunas */
        .noticia-header-bloco {
            min-height: 110px;
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

        /* Imagem Proporcional */
        .web-img-container {
            width: 100%;
            height: 210px;
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

        /* Acordeão HTML Nativo */
        details { background-color: #f8fafc !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; padding: 10px 14px !important; margin-top: 12px !important; }
        summary { font-weight: 600 !important; color: #0f172a !important; cursor: pointer !important; font-size: 14px !important; list-style: none !important; }
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

        /* Botão de Áudio Nativo */
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
            padding: 10px 16px !important; 
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

# BANNER PRINCIPAL (HEADER)
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding:25px; border-radius:14px; margin-bottom:15px; text-align:center; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
        <h1 style="color:#00f5d4; margin:0; font-weight:800; letter-spacing: -1px; font-size: 34px; display:inline-block; vertical-align:middle;">🌐 horizont.news</h1>
        <p style="color:#94a3b8; font-size:13px; margin:6px 0 0 0; font-weight:400; letter-spacing: 0.5px;">Informação Sem Fronteiras — Pluralidade Global e Independente para Mentes Conectadas</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# PRIMEIRO BANNER: PERSPECTIVAS E INTRODUÇÃO
st.markdown("<marquee style='width: 100%; color: #0f172a; background-color: #00f5d4; padding: 8px; font-size: 13px; font-weight: 700; border-radius: 8px; margin-bottom: 10px;'>⚡ PERSPECTIVAS EM FOCO: Cobertura internacional integrada em equilíbrio com as mídias regionais e independentes do Brasil...</marquee>", unsafe_allow_html=True)

# CARREGAMENTO DO BANCO DE DADOS
noticias = ler_banco_dados_fresco()

# SEGUNDO BANNER: ÚLTIMAS NOTÍCIAS DINÂMICAS DO BANCO (COR DIFERENTE)
if noticias and isinstance(noticias, list):
    # Obtém os títulos das últimas 5 notícias adicionadas para rodar no carrossel de texto
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
            "texto": "👟 <b>Alta Performance:</b> Renove seus equipamentos e roupas esportivas diretamente nas lojas oficiais parceiras com discounts exclusivos.",
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

def limpar_tags_vazadas(texto_bruto):
    if not texto_bruto:
        return ""
    texto_limpo = re.sub(r'<div class="box-afiliado">.*?</div>', '', texto_bruto, flags=re.DOTALL)
    texto_limpo = re.sub(r'<div style=.*?</div>', '', texto_limpo, flags=re.DOTALL)
    texto_limpo = re.sub(r'<.*?/?>', '', texto_limpo)
    return texto_limpo.strip()

if not noticias:
    st.info("📢 Sincronizando feeds mundiais e regionais...")
else:
    # FILTROS
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
        col1, col2 = st.columns(2)
        
        for index, item in enumerate(noticias_recentes):
            if not isinstance(item, dict):
                continue
                
            coluna_atual = col1 if index % 2 == 0 else col2
            
            titulo = item.get(f"titulo_{sufixo}", item.get("titulo_pt", "Sem Título"))
            texto_base = item.get(f"texto_{sufixo}", item.get("texto_pt", "Sem Conteúdo"))
            texto = limpar_tags_vazadas(texto_base)
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
                    
                    # RENDERIZAÇÃO E ATIVAÇÃO DO BOTÃO DE ÁUDIO CORRIGIDO
                    texto_limpo = str(texto).replace('"', '&quot;').replace("'", "\\'").replace('\n', ' ')
                    titulo_limpo = str(titulo).replace('"', '&quot;').replace("'", "\\'")
                    
                    html_audio_direto = f"""
                    <div class="btn-audio-container">
                        <button class="btn-audio-player" onclick="window.speechSynthesis.cancel(); setTimeout(function(){{ var msg = new SpeechSynthesisUtterance('{titulo_limpo}. {texto_limpo}'); msg.lang='{lang_audio}'; window.speechSynthesis.speak(msg); }}, 50);">
                            🔊 Ouvir a matéria em áudio
                        </button>
                    </div>
                    """
                    st.markdown(html_audio_direto, unsafe_allow_html=True)
                    
                    # ACORDEÃO DE LEITURA COMPLETA
                    resumo_bruto = item.get('resumo_longo', item.get('texto_pt', ''))
                    resumo_denso = limpar_tags_vazadas(resumo_bruto)
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

                            <div style="margin-top: 15px; text-align: right; border-top: 1px solid #e2e8f0; padding-top:10px;">
                                <a href="{link_origem}" target="_blank" style="background-color: #2563eb; color: white; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 700;">Acessar Fonte Oficial ↗</a>
                            </div>
                        </div>
                    </details>
                    """
                    st.markdown(html_acordeao, unsafe_allow_html=True)

# RODAPÉ
st.markdown("<br><br><div style='border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center; color: #64748b; font-size: 12px;'><p style='margin: 0;'>🌐 horizont.news — Todos os direitos reservados.</p></div>", unsafe_allow_html=True)
