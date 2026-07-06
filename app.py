import streamlit as st
import json
import urllib.request
import streamlit.components.v1 as components

st.set_page_config(
    page_title="horizont.news — Conectando Gerações",
    page_icon="🌐",
    layout="wide"
)

# ESTILIZAÇÃO DO PORTAL
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;600;700&display=swap');
        
        * { font-family: 'Inter', sans-serif !important; }
        .block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; }
        #MainMenu {visibility: hidden;} 
        [data-testid='stSidebar'] {display: none;}
        
        .texto-noticia { color: #1e293b !important; font-size: 15px !important; line-height: 1.6 !important; font-weight: 400 !important; }
        .titulo-noticia { color: #0f172a !important; font-weight: 700 !important; font-size: 20px !important; line-height: 1.3 !important; margin-top: 8px !important; margin-bottom: 5px !important; }

        /* Acordeão HTML Nativo */
        details { background-color: #f8fafc !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; padding: 10px 14px !important; margin-top: 15px !important; }
        summary { font-weight: 600 !important; color: #0f172a !important; cursor: pointer !important; font-size: 14px !important; list-style: none !important; }
        summary::-webkit-details-marker { display: none !important; }
        summary::before { content: "📝 " !important; }

        /* Renderização Direta de Imagem via Navegador (Contorna bloqueios do servidor) */
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

        /* Box de Afiliados / Cupons Premium */
        .box-afiliado {
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border: 1px dashed #22c55e;
            border-radius: 8px;
            padding: 12px;
            margin-top: 15px;
            font-size: 13px;
            color: #14532d;
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

# MOTOR DE MONETIZAÇÃO
def obter_oferta_afiliado(categoria):
    campanhas = {
        "Economia": {
            "texto": "📚 <b>Leitura Recomendada:</b> Entenda os ciclos financeiros globais com os livros mais vendidos da Amazon sobre macroeconomia.",
            "cupom": "FRETE GRÁTIS PRIME",
            "link": "https://www.amazon.com.br?tag=seu_id_afiliado-20"
        },
        "Tech & Ciência": {
            "texto": "💻 <b>Upgrade Tecnológico:</b> Procurando gadgets para aumentar sua produtividade? Confira a seleção semanal com até 20% OFF.",
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

    categorias_dinamicas = sorted(list(set(item.get("categoria", "Política") for item in noticias)))
    with col_filtro:
        categoria_selecionada = st.selectbox("🎯 Filtrar Canal", ["Feed Completo (Todos os Assuntos)"] + categories_dinamicas)

    noticias_recentes = list(reversed(noticias))
    if categoria_selecionada != "Feed Completo (Todos os Assuntos)":
        noticias_recentes = [n for n in noticias_recentes if n.get("categoria", "Política") == categoria_selecionada]
    
    if not noticias_recentes:
        st.warning(f"Sem registros novos para este canal.")
    else:
        col1, col2 = st.columns(2)
        
        for index, item in enumerate(noticias_recentes):
            coluna_atual = col1 if index % 2 == 0 else col2
            
            titulo = item.get(f"titulo_{sufixo}", item.get("titulo_pt", "Sem Título"))
            texto = item.get(f"texto_{sufixo}", item.get("texto_pt", "Sem Conteúdo"))
            categoria = item.get("categoria", "Política")
            subcategoria = item.get("subcategoria", "")
            link_origem = item.get("link_origem", "#")
            
            # CAPTURA DA IMAGEM DO BANCO DE DADOS
            url_foto = item.get("url_imagem")
            
            total_palavras = len(texto.split()) + len(item.get('resumo_longo', '').split())
            tempo_leitura = max(1, round(total_palavras / 150))
            
            cor_tag = obter_cor_categoria(categoria)
            
            tag_html = f"<span style='background-color:{cor_tag}; color:white; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:700; text-transform:uppercase; margin-right:6px;'>{categoria}</span>"
            if subcategoria:
                tag_html += f"<span style='background-color:#e2e8f0; color:#475569; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:600; text-transform:uppercase;'>📍 {subcategoria}</span>"
            
            oferta = obter_oferta_afiliado(categoria)

            with coluna_atual:
                with st.container(border=True):
                    # EXIBIÇÃO DIRETA VIA NAVEGADOR COM FALLBACK SEGURO
                    if url_foto and url_foto.strip() != "":
                        st.markdown(f'<div class="web-img-container"><img src="{url_foto}" alt="Notícia"></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="web-img-container" style="display: flex; align-items: center; justify-content: center;"><div style="color: #00f5d4; font-weight: 800; font-size: 20px;">🌐 horizont.news</div></div>', unsafe_allow_html=True)
                        
                    st.markdown(f"<div style='margin-bottom:8px;'>{tag_html}</div>", unsafe_allow_html=True)
                    st.markdown(f"<h3 class='titulo-noticia'>{titulo}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color:#64748b; font-size:12px; margin-bottom:12px;'>📅 {item.get('data')} • 🏛️ Fonte: <b>{item.get('fonte_origem')}</b></p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='texto-noticia'>{texto}</p>", unsafe_allow_html=True)
                    
                    st.divider()
                    
                    # AUDIO PLAYER
                    texto_limpo = texto.replace('"', '').replace("'", "").replace('\n', ' ')
                    titulo_limpo = titulo.replace('"', '').replace("'", "")
                    html_audio = f"""
                    <div style="display: flex; justify-content: center; margin-bottom: 5px;">
                        <button onclick="window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{titulo_limpo}. {texto_limpo}'); msg.lang='{lang_audio}'; window.speechSynthesis.speak(msg);" 
                        style="background-color:#0f172a; color:#00f5d4; border: none; padding: 8px 18px; border-radius: 20px; cursor: pointer; font-size: 13px; font-weight: 700;">🔊 Ouvir Notícia</button>
                    </div>
                    """
                    components.html(html_audio, height=42)
                    
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
