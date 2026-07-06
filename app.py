import streamlit as st
import json
import urllib.request

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
            overflow: hidden !important; /* Remove qualquer scrollbar do card */
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
        summary::before { content: "📝 " !important; }

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

        /* Botão de Áudio Nativo Otimizado (Sem vazamento de tamanho) */
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
            box-sizing: border-box !important; /* Garante que padding não aumente o botão */
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

# HEADER DO PORTAL
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding:25px; border-radius:14px; margin-bottom:20px; text-align:center; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
        <h1 style="color:#00f5d4; margin:0; font-weight:800; letter-spacing: -1px; font-size: 34px; display:inline-block; vertical-align:middle;">🌐 horizont.news</h1>
        <p style="color:#94a3b8; font-size:13px; margin:6px 0 0 0; font-weight:400; letter-spacing: 0.5px;">Informação Sem Fronteiras — Perspectivas Globais Para Mentes Conectadas</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# TICKER
st.markdown("<marquee style='width: 100%; color: #0f172a; background-color: #00f5d4; padding: 8px; font-size: 13px; font-weight: 700; border-radius: 8px; margin-bottom: 25px;'>⚡ AGORA NO MUNDO: Cobertura internacional integrada da Ásia, Europa, Américas e Oriente Médio...</marquee>", unsafe_allow_html=True)

noticias = ler_banco_dados_fresco()

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


if not noticias:
    st.info("📢 Sincronizando feeds mundiais...")
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
            texto = item.get(f"texto_{sufixo}", item.get("texto_pt", "Sem Conteúdo"))
            categoria = item.get("categoria", "Política")
            subcategoria = item.get("subcategoria", "")
            link_origem = item.get("link_origem", "#")
            url_foto = item.get("url_imagem")
            
            cor_tag = obter_cor_categoria(categoria)
            
            tag_html = f"<span style='background-color:{cor_tag}; color:white; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:700; text-transform:uppercase; margin-right:6px;'>{categoria}</span>"
            if subcategoria:
                tag_html += f"<span style='background-color:#e2e8f0; color:#475569; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:600; text-transform:uppercase;'>📍 {subcategoria}</span>"
            
            oferta = obter_oferta_afiliado(categoria)

            with coluna_atual:
                with st.container(border=True):
                    # Renderização de imagem limpa
                    if url_foto and str(url_foto).strip() != "":
                        st.markdown(f'<div class="web-img-container"><img src="{url_foto}" alt="Notícia"></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="web-img-container" style="display: flex; align-items: center; justify-content: center;"><div style="color: #00f5d4; font-weight: 800; font-size: 20px;">🌐 horizont.news</div></div>', unsafe_allow_html=True)
                    
                    # Bloco superior empacotado para alinhar as alturas verticais
                    st.markdown(
                        f"""
                        <div class="noticia-header-bloco">
                            <div style='margin-bottom:8px;'>{tag_html}</div>
                            <h3 class='titulo-noticia'>{titulo}</h3>
                            <p style='color:#64748b; font-size:12px; margin-bottom:12px;'>📅 {item.get('data')} • 🏛️ Fonte: <b>{item.get('fonte_origem')}</b></p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    st.markdown(f"<p class='texto-noticia'>{texto}</p>", unsafe_allow_html=True)
                    st.divider()
                    
                    # CORREÇÃO DO ÁUDIO: Adicionado contêiner para blindar tamanho e overflow
                    texto_limpo = str(texto).replace('"', '&quot;').replace("'", "\\'").replace('\n', ' ')
                    titulo_limpo = str(titulo).replace('"', '&quot;').replace("'", "\\'")
                    
                    html_audio_direto = f"""
                    <div class="btn-audio-container">
                        <button class="btn-audio-player" onclick="window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{titulo_limpo}. {texto_limpo}'); msg.lang='{lang_audio}'; window.speechSynthesis.speak(msg);">
                            🔊 Ouvir Matéria em Áudio
                        </button>
                    </div>
                    """
                    st.markdown(html_audio_direto, unsafe_allow_html=True)
                    
                    # ACORDEÃO
                    resumo_denso = item.get('resumo_longo', item.get('texto_pt', 'O detalhamento completo desta matéria está sendo processado.'))
                    html_acordeao = f"""
                    <details>
                        <summary>Matéria Completa e Contexto</summary>
                        <div style="margin-top: 10px; color: #334155; font-size: 14.5px; line-height: 1.6; font-style: italic;">
                            <strong style="color: #0f172a; font-style: normal; display: block; margin-bottom: 6px;">{titulo}</strong>
                            {resumo_denso}
                            
                            <div class="box-afiliado">
                                {oferta['texto']}<br>
                                <span style="background-color:#22c55e; color:white; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:700; font-style:normal; margin-top:5px; display:inline-block;">CUPOM: {oferta['cupom']}</span>
                                <div style="margin-top:8px; text-align:right;">
                                    <a href="{oferta['link']}" target="_blank" style="background-color:#14532d; color:#ffffff; padding:4px 10px; border-radius:6px; text-decoration:none; font-size:12px; font-weight:700; font-style:normal;">Aproveitar Oferta ↗</a>
                                </div>
                            </div>

                            <div style="margin-top: 15px; text-align: right; border-top: 1px solid #e2e8f0; padding-top:10px;">
                                <a href="{link_origem}" target="_blank" style="color: #2563eb; text-decoration: none; font-size: 13px; font-weight: 700; font-style:normal;">Acessar Fonte Oficial ↗</a>
                            </div>
                        </div>
                    </details>
                    """
                    st.markdown(html_acordeao, unsafe_allow_html=True)

# RODAPÉ
st.markdown("<br><br><div style='border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center; color: #64748b; font-size: 12px;'><p style='margin: 0;'>🌐 horizont.news — Todos os direitos reservados.</p></div>", unsafe_allow_html=True)
