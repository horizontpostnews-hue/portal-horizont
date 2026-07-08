import streamlit as st
import streamlit.components.v1 as components
import time

# -----------------------------------------------------------------------------
# Configuração da Página e Reset de Layout
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="horizont.news — Conectando Gerações",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injeção de CSS Premium com Correção Absoluta de Quebras Mobile
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
        color: #1e293b !important;
    }
    
    h1, h2, h3 {
        color: #0b1329 !important;
        font-weight: 700 !important;
    }
    p {
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        color: #1e293b !important;
    }
    
    .premium-header {
        background: linear-gradient(135deg, #0b1329 0%, #1e293b 100%);
        padding: 30px 20px;
        text-align: center;
        border-bottom: 4px solid #00f5d4;
        border-radius: 8px;
        margin-bottom: 0px;
        box-shadow: 0 4px 20px rgba(11, 19, 41, 0.15);
    }
    .premium-logo-area {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        margin-bottom: 10px;
    }
    .premium-logo-globe { color: #00f5d4; font-size: 2.8rem; }
    .premium-title {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px;
        margin: 0 !important;
    }
    .premium-title span { color: #00f5d4; }
    .premium-tagline {
        color: #ffbc42 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        letter-spacing: 1px;
        margin-top: 5px !important;
    }

    /* Correção Estrita das Colunas de Reação para Forçar Linha Horizontal Sempre */
    div[data-testid="stHorizontalBlockHasColumns"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
        width: 100% !important;
    }
    
    div[data-testid="column"] {
        flex: unset !important;
        width: auto !important;
        min-width: unset !important;
    }

    /* Estilização Geral dos Botões de Reação Nativos */
    div[data-testid="column"] button {
        background-color: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        color: #334155 !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease-in-out !important;
        width: auto !important;
        display: inline-flex !important;
    }
    
    div[data-testid="column"] button:hover {
        background-color: #e2e8f0 !important;
        color: #0b1329 !important;
        border-color: #cbd5e1 !important;
    }

    /* Destaque para o Botão de Compartilhar Individualizado pela Key */
    div[data-testid="column"] button[key^="sh_"] {
        background-color: #0b1329 !important;
        color: #ffffff !important;
        border: none !important;
    }

    /* Otimização Responsiva do Player de Áudio Nativo */
    audio {
        max-width: 100% !important;
        width: 100% !important;
        margin-bottom: 10px;
    }

    .stDetails { border: 1px solid #e2e8f0 !important; background-color: #ffffff !important; border-radius: 6px !important; }
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAPEAMENTO DE INTERAÇÕES E BANCO DE DADOS
# -----------------------------------------------------------------------------
if "engagement" not in st.session_state:
    st.session_state.engagement = {
        "news_1": {"Alta Relevância": 14, "Crítico": 3, "Emocionante": 0, "Inspirador": 8, "Exige reflexão": 5},
        "news_2": {"Alta Relevância": 22, "Crítico": 11, "Emocionante": 2, "Inspirador": 19, "Exige reflexão": 7},
        "news_3": {"Alta Relevância": 45, "Crítico": 1, "Emocionante": 38, "Inspirador": 29, "Exige reflexão": 12}
    }

# -----------------------------------------------------------------------------
# 1. BARRA DE IDENTIDADE VISUAL OFICIAL E ASSINATURA CLÁSSICA
# -----------------------------------------------------------------------------
st.markdown("""
<div class="premium-header">
    <div class="premium-logo-area">
        <span class="premium-logo-globe">🌐</span>
        <h1 class="premium-title">horizont<span>.news</span></h1>
    </div>
    <div class="premium-tagline">Conectando Gerações — Informação Sem Fronteiras</div>
</div>
""", unsafe_allow_html=True)

# Banners Institucionais e Carrosséis Fluidos
html_ticker_institutional = """
<div style="background-color: #00f5d4; color: #0b1329; padding: 10px 0; overflow: hidden; white-space: nowrap; font-weight: 700; font-size: 0.95rem; border-bottom: 2px solid #0b1329;">
    <div style="display: inline-block; padding-left: 100%; animation: marquee-inst 28s linear infinite;">
        ⚡ CONEXÃO DIRETA COM AS PRINCIPAIS AGÊNCIAS DE NOTÍCIAS INDEPENDENTES DO MUNDO • COBERTURA INTERNACIONAL INTEGRADA DA ÁSIA, EUROPA, AMÉRICAS E ORIENTE MÉDIO • CONECTANDO GERAÇÕES COM PLURALIDADE E INDEPENDÊNCIA ⚡
    </div>
</div>
<style> @keyframes marquee-inst { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } } </style>
"""
components.html(html_ticker_institutional, height=42)

html_ticker_news = """
<div style="display: flex; background-color: #0b1329; border-radius: 4px; overflow: hidden; margin-top: 15px; margin-bottom: 20px; align-items: center;">
    <div style="background-color: #ffbc42; color: #0b1329; padding: 10px 15px; font-weight: 800; font-size: 0.85rem; white-space: nowrap; text-transform: uppercase; letter-spacing: 0.5px;">ÚLTIMAS NOTÍCIAS</div>
    <div style="overflow: hidden; white-space: nowrap; width: 100%; display: flex; align-items: center;">
        <div style="display: inline-block; padding-left: 100%; color: #ffffff; font-size: 0.95rem; font-weight: 500; animation: marquee-news 35s linear infinite;">
            Analistas apontam redirecionamento estratégico em acordos multilaterais e fortalecimento de blocos emergentes (Fonte: Agência Global) &nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp;
            Congresso Nacional pauta nova votação sobre diretrizes econômicas e de fomento à inovação tecnológica (Fonte: Folha de Brasília)
        </div>
    </div>
</div>
<style> @keyframes marquee-news { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } } </style>
"""
components.html(html_ticker_news, height=45)

# -----------------------------------------------------------------------------
# 11. SESSÃO COPA DO MUNDO 2026
# -----------------------------------------------------------------------------
st.markdown("### 🏆 COPA DO MUNDO FIFA 2026 — BASTIDORES & CURIOSIDADES")
with st.container():
    col_vid_left, col_vid_right = st.columns([1.2, 1])
    with col_vid_left:
        st.video("https://www.youtube.com/watch?v=Jm9n_Zcl_iE", start_time=0)
    with col_vid_right:
        st.markdown(
            "<div style='background-color: #f1f5f9; padding: 20px; border-left: 4px solid #ffbc42; border-radius: 4px; height: 100%;'>"
            "<h4 style='margin-top:0; color:#0b1329;'>Giro Técnico Diário: Infraestrutura e Sedes</h4>"
            "<p style='font-size: 0.95rem !important; margin-bottom:0;'>Confira os detalhes cruciais das arenas que receberão as próximas fases eliminatórias da Copa do Mundo de 2026. "
            "A preparação de cidades-sede como Seattle, Nova York e Cidade do México redefine os parâmetros logísticos globais do futebol moderno.</p>"
            "</div>", 
            unsafe_allow_html=True
        )

st.markdown("---")

# -----------------------------------------------------------------------------
# 18. ÁRVORE DE CATEGORIZAÇÃO E FILTRAGEM DINÂMICA
# -----------------------------------------------------------------------------
categories_tree = {
    "Selecione uma Categoria": [],
    "Política": ["Nacional", "Internacional/Geopolítica", "Eleições"],
    "Economia": ["Mercado", "Finanças Pessoais", "Negócios"],
    "Cotidiano": ["Cidades", "Polícia", "Educação", "Clima"],
    "Esportes": ["Futebol", "Basquete", "Variedades"],
    "Entretenimento": ["Cinema & Séries", "Música", "Pop/Tendências"],
    "Tech & Ciência": ["Gadgets", "Espaço", "Inovação"]
}

col_f1, col_f2 = st.columns(2)
with col_f1:
    main_choice = st.selectbox("📂 Selecione a Categoria Principal:", list(categories_tree.keys()))

sub_choice = None
if main_choice != "Selecione uma Categoria":
    with col_f2:
        sub_choice = st.selectbox("❯ Selecione a Subcategoria Específica:", categories_tree[main_choice])

tag_colors = {
    "Política": {"bg": "#e0f2fe", "text": "#0369a1"},
    "Economia": {"bg": "#dcfce7", "text": "#15803d"},
    "Cotidiano": {"bg": "#fef3c7", "text": "#b45309"},
    "Esportes": {"bg": "#f3e8ff", "text": "#6b21a8"},
    "Entretenimento": {"bg": "#fce7f3", "text": "#be185d"},
    "Tech & Ciência": {"bg": "#e0f2fe", "text": "#1d4ed8"}
}

# -----------------------------------------------------------------------------
# BASE DE DADOS INTEGRADA
# -----------------------------------------------------------------------------
news_database = [
    {
        "id": "news_1",
        "title": "Os novos rumos geopolíticos da Inteligência Artificial e a disputa de mercado soberano",
        "category": "Tech & Ciência",
        "subcategory": "Inovação",
        "date_source": "07/07/2026 23:37 • Veículo: Outras Palavras",
        "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
        "lead": "A corrida pelo controle dos ecossistemas digitais avançados ganha contornos dramáticos à medida que blocos governamentais passam a exigir infraestruturas proprietárias de dados. A dependência de soluções terceirizadas de software de poucas corporações ocidentais acendeu o alerta máximo sobre a autonomia e a segurança cibernética de países em desenvolvimento. O redesenho deste mercado global redefine não apenas relações financeiras bilaterais, mas o próprio conceito de soberania tecnológica internacional moderna.",
        "extended_summary": "O atual cenário das ferramentas computacionais e redes neurais de larga escala reflete um espelhamento das assimetrias econômicas tradicionais. Ao acumularem volumes imensos de capital por meio de licenças fechadas de software, um grupo restrito de grandes corporações cria barreiras intransponíveis de entrada, forçando governos inteiros a transferirem ativos intelectuais valiosos para servidores centralizados externos.<br><br>Especialistas apontam que a saída sustentável e madura para esta dependência sistêmica envolve o fomento rigoroso a modelos de código aberto e servidores locais geridos de forma pública."
    },
    {
        "id": "news_2",
        "title": "Decisão estratégica: Escolha de Geraldo Rufino como vice ganha força em articulação política",
        "category": "Política",
        "subcategory": "Nacional",
        "date_source": "07/07/2026 23:36 • Fonte: Brasil 247",
        "image": "https://images.unsplash.com/photo-1540910419892-4a36d2c3266c?auto=format&fit=crop&w=800&q=80",
        "lead": "Nos bastidores das principais coalizões partidárias para o próximo pleito majoritário, o nome do empresário Geraldo Rufino surge como um forte elemento agregador de centro-direita. A indicação atende à demanda explícita de governadores do bloco por uma figura de ampla aceitação no ecossistema de micro e pequenas empresas regionais. A costura final depende unicamente do aval formal das executivas nacionais, que analisam o impacto e o ganho de capilaridade em coligações do Sudeste.",
        "extended_summary": "A aproximação do nome de Rufino para a chapa majoritária representa um movimento técnico calculado para suavizar discursos excessivamente corporativistas e trazer uma narrativa focada em resiliência socioeconômica e empreendedorismo de base. Setores estratégicos do Podemos sinalizam positivamente, enxergando na imagem pública do empresário um forte canal de diálogo direto."
    },
    {
        "id": "news_3",
        "title": "Governo do RN sanciona Lei Lucy para proteção de animais e regulamenta manejo comunitário",
        "category": "Cotidiano",
        "subcategory": "Cidades",
        "date_source": "07/07/2026 23:36 • Fonte: Tribuna do Norte (RN)",
        "image": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=800&q=80",
        "lead": "O Governo do Estado do Rio Grande do Norte promulgou em Diário Oficial a legislação que institui diretrizes rígidas para a tutela de animais em áreas urbanas de convívio social. Inspirada em uma mobilização popular após um caso emblemático ocorrido em Mossoró, a medida descentraliza recursos para o atendimento veterinário emergencial de livre acesso. A lei obriga os municípios do estado a organizarem conselhos ativos voltados à fiscalização e ao controle populacional ético.",
        "extended_summary": "A instituição da nova política de bem-estar animal representa um marco regulatório civilizatório para a região e soluciona impasses históricos de saúde pública. O texto establishes punições severas para casos de negligência em ambientes públicos e cria a figura jurídica do 'Protetor Credenciado', garantindo amparo legal para ações independentes."
    }
]

filtered_news = [n for n in news_database if (main_choice == "Selecione uma Categoria" or n["category"] == main_choice) and (not sub_choice or n["subcategory"] == sub_choice)]
if not filtered_news:
    filtered_news = news_database

# -----------------------------------------------------------------------------
# RENDERIZAÇÃO RESPONSIVA DAS MATÉRIAS
# -----------------------------------------------------------------------------
st.markdown("### 📰 COBERTURA INTEGRADA GLOBAL")

for item in filtered_news:
    colors = tag_colors.get(item["category"], {"bg": "#e2e8f0", "text": "#475569"})
    
    st.markdown(f"""
    <div style="background-color: white; border-radius: 8px; padding: 20px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); border: 1px solid #e2e8f0;">
        <span style="background-color: {colors['bg']}; color: {colors['text']}; display: inline-block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; padding: 4px 10px; border-radius: 4px; margin-bottom: 10px; letter-spacing: 0.5px;">
            {item['category'].upper()} ❯ {item['subcategory']}
        </span>
        <h2 style="font-size: 1.5rem !important; line-height: 1.3 !important; color: #0b1329; margin: 0 0 6px 0; font-weight:700;">{item['title']}</h2>
        <div style="font-size: 0.85rem; color: #64748b;">📅 {item['date_source']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_img, col_txt = st.columns([1, 1.8])
    with col_img:
        st.image(item["image"], use_container_width=True)
        
    with col_txt:
        st.markdown(f"<p style='font-size:1.08rem !important; font-weight:500; color:#1e293b; line-height:1.6; margin-top:0; margin-bottom:12px; text-align:justify;'>{item['lead']}</p>", unsafe_allow_html=True)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        
        with st.expander("📖 LER A MATÉRIA COMPLETA — ANÁLISE EDITORIAL"):
            st.markdown(f"""
            <div style="background-color: #fafafa; border-left: 4px solid #0b1329; padding: 15px; font-size: 1.05rem !important; line-height: 1.6; color: #1e293b; text-align: justify;">
                <p style="margin-top:0; font-weight:700; color:#0b1329;">Análise de Conjuntura — Conselho Editorial Horizont</p>
                <p style="color:#1e293b !important; margin-bottom:0;">{item['extended_summary']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # -----------------------------------------------------------------
        # BOTÕES NATIVOS DISPOSTOS LADO A LADO VIA CSS INLINE-FLEX REATIVO
        # -----------------------------------------------------------------
        st.markdown("<div style='margin-top:14px; margin-bottom:4px; font-size:0.8rem; font-weight:600; color:#64748b; text-transform:uppercase;'>Avaliação de Relevância Editorial:</div>", unsafe_allow_html=True)
        
        reactions_list = ["Alta Relevância", "Crítico", "Emocionante", "Inspirador", "Exige reflexão"]
        
        # Geramos n+1 colunas para acomodar botões nativos que serão interceptados pelo CSS global flexível
        react_cols = st.columns(len(reactions_list) + 1)
        
        for idx, r_name in enumerate(reactions_list):
            with react_cols[idx]:
                current_count = st.session_state.engagement[item["id"]][r_name]
                if st.button(f"{r_name} ({current_count})", key=f"btn_{item['id']}_{idx}"):
                    st.session_state.engagement[item["id"]][r_name] += 1
                    st.toast(f"Reação registada: {r_name}", icon="✅")
                    time.sleep(0.1)
                    st.rerun()
                    
        with react_cols[len(reactions_list)]:
            if st.button("📢 Compartilhar", key=f"sh_{item['id']}"):
                components.html(f"""
                <script>
                navigator.clipboard.writeText("https://horizont.news/noticia/{item['id']}");
                alert("Link corporativo copiado para a área de transferência!");
                </script>
                """, height=0, width=0)
                st.success("Copiado!")

    st.markdown("<br><hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 10px 0;'><br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CRÉDITOS DO VEÍCULO (RODAPÉ)
# -----------------------------------------------------------------------------
st.markdown("""
<div style="background-color: #0b1329; color: #94a3b8; padding: 40px 20px; border-top: 4px solid #ffbc42; border-radius: 8px 8px 0 0; font-size: 0.9rem; margin-top: 40px;">
    <div style="max-width: 1200px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 30px;">
        <div style="flex: 1; min-width: 280px;">
            <h4 style="color: #ffffff; margin-bottom: 12px; font-weight:700;">horizont.news</h4>
            <p style="color: #94a3b8 !important; font-size: 0.85rem !important;">Portal jornalístico independente focado no cruzamento geracional de dados e cobertura global.</p>
        </div>
    </div>
    <hr style="border-color: #1e293b; margin: 30px 0;">
    <div style="text-align: center; font-size: 0.8rem; color: #64748b;">
        © 2026 horizont.news — Desenvolvido em conformidade com as diretrizes editoriais Premium Universal.
    </div>
</div>
""", unsafe_allow_html=True)
