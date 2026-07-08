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

# Injeção de CSS para o Tema Premium Universal (#0b1329, #00f5d4, #ffbc42)
# Correção do argumento de renderização HTML e calibração de contrastes
st.markdown("""
<style>
    /* Reset e Estilos Globais */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
        color: #1e293b !important;
    }
    
    /* Acessibilidade e Hierarquia de Textos */
    h1, h2, h3 {
        color: #0b1329 !important;
        font-weight: 700 !important;
    }
    p {
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        color: #1e293b !important; /* Contraste aumentado para o público sênior */
    }
    
    /* Barra de Identidade Visual Premium */
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
    .premium-logo-globe {
        color: #00f5d4;
        font-size: 2.8rem;
        animation: pulse 3s infinite ease-in-out;
    }
    .premium-title {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px;
        margin: 0 !important;
        padding: 0 !important;
    }
    .premium-title span {
        color: #00f5d4;
    }
    .premium-tagline {
        color: #ffbc42 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        letter-spacing: 1px;
        margin-top: 5px !important;
    }

    /* Espaçamentos Gerais do Streamlit */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.9; }
        50% { transform: scale(1.05); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True) # CORRIGIDO: Argumento oficial aceito pelo Streamlit

# Inicialização do Estado de Sessão para Reações de Engajamento
if "engagement" not in st.session_state:
    st.session_state.engagement = {}

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

# -----------------------------------------------------------------------------
# 2. BANNER INSTITUCIONAL DINÂMICO (FLUXO MÉDIO EM CSS)
# -----------------------------------------------------------------------------
html_ticker_institutional = """
<div style="background-color: #00f5d4; color: #0b1329; padding: 10px 0; overflow: hidden; white-space: nowrap; font-weight: 700; font-size: 0.95rem; box-shadow: inset 0 -2px 5px rgba(0,0,0,0.1); border-bottom: 2px solid #0b1329;">
    <div style="display: inline-block; padding-left: 100%; animation: marquee-inst 28s linear infinite;">
        ⚡ CONEXÃO DIRETA COM AS PRINCIPAIS AGÊNCIAS DE NOTÍCIAS INDEPENDENTES DO MUNDO • COBERTURA INTERNACIONAL INTEGRADA DA ÁSIA, EUROPA, AMÉRICAS E ORIENTE MÉDIO • CONECTANDO GERAÇÕES COM PLURALIDADE E INDEPENDÊNCIA ⚡
    </div>
</div>
<style>
@keyframes marquee-inst {
    0% { transform: translate3d(0, 0, 0); }
    100% { transform: translate3d(-100%, 0, 0); }
}
</style>
"""
components.html(html_ticker_institutional, height=42)

# -----------------------------------------------------------------------------
# 3. CARROSSEL DINÂMICO DE ÚLTIMAS NOTÍCIAS (FLUXO MODERADO)
# -----------------------------------------------------------------------------
html_ticker_news = """
<div style="display: flex; background-color: #0b1329; border-radius: 4px; overflow: hidden; margin-top: 15px; margin-bottom: 20px; align-items: center;">
    <div style="background-color: #ffbc42; color: #0b1329; padding: 10px 15px; font-weight: 800; font-size: 0.85rem; white-space: nowrap; text-transform: uppercase; letter-spacing: 0.5px;">
        ÚLTIMAS NOTÍCIAS
    </div>
    <div style="overflow: hidden; white-space: nowrap; width: 100%; display: flex; align-items: center;">
        <div style="display: inline-block; padding-left: 100%; color: #ffffff; font-size: 0.95rem; font-weight: 500; animation: marquee-news 35s linear infinite;">
            Analistas apontam redirecionamento estratégico em acordos multilaterais e fortalecimento de blocos emergentes (Fonte: Agência Global) &nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp;
            Congresso Nacional pauta nova votação sobre diretrizes econômicas e de fomento à inovação tecnológica (Fonte: Folha de Brasília) &nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp;
            Mercado financeiro eleva projeção de crescimento industrial puxado por alta histórica em exportações de manufaturados (Fonte: Valor Econômico) &nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp;
            Novas metas climáticas globais exigem reformulação urgente em matrizes de transporte urbano nas metrópoles (Fonte: ClimaInfo) &nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp;
            Principais polos acadêmicos assinam cooperação internacional para desenvolvimento ético e descentralizado de IA (Fonte: TechReview)
        </div>
    </div>
</div>
<style>
@keyframes marquee-news {
    0% { transform: translate3d(0, 0, 0); }
    100% { transform: translate3d(-100%, 0, 0); }
}
</style>
"""
components.html(html_ticker_news, height=45)

# -----------------------------------------------------------------------------
# 11. SESSÃO COPA DO MUNDO 2026 (VÍDEO PÚBLICO INTEGRADO)
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
            "<p style='font-size: 0.95rem !important;'>Confira os detalhes cruciais das arenas que receberão as próximas fases eliminatórias da Copa do Mundo de 2026. "
            "A preparação de cidades-sede como Seattle, Nova York e Cidade do México redefine os parâmetros logísticos globais do futebol moderno. "
            "A movimentação nos bastidores aponta recordes de ocupação hoteleira nas imediações dos complexos esportivos, consolidando a América do Norte como o coração pulsante da torcida mundial nesta edição histórica.</p>"
            "</div>", 
            unsafe_with_allowed_html=True
        )

st.markdown("---")

# -----------------------------------------------------------------------------
# 18. ÁRVORE DE CATEGORIZAÇÃO E FILTRAGEM DINÂMICA CONDICIONAL
# -----------------------------------------------------------------------------
categories_tree = {
    "Selecione uma Categoria": [],
    "Política": ["Nacional", "Internacional/Geopolítica", "Eleições"],
    "Economia": ["Mercado", "Finanças Pessoais", "Negócios"],
    "Cotidiano": ["Cidades", "Polícia", "Educação", "Clima"],
    "Esportes": ["Futebol", "Basquete", "Variedades"],
    "Entretenimento": ["Cinema & Séries", "Música", "Pop/Tendências"],
    "Tech & Ciência": ["Gadgets", "Espaço", "Inovação"],
    "Gastronomia e Culinária": ["Tendências", "Alta Cozinha", "Receitas"],
    "Viver Bem": ["Saúde", "Bem-Estar", "Medicina", "Longevidade"]
}

col_f1, col_f2 = st.columns(2)

with col_f1:
    main_choice = st.selectbox("📂 Selecione a Categoria Principal:", list(categories_tree.keys()))

sub_choice = None
if main_choice != "Selecione uma Categoria":
    with col_f2:
        sub_choice = st.selectbox("❯ Selecione a Subcategoria Específica:", categories_tree[main_choice])

# Paleta Semântica para os Assuntos
tag_colors = {
    "Política": {"bg": "#e0f2fe", "text": "#0369a1"},
    "Economia": {"bg": "#dcfce7", "text": "#15803d"},
    "Cotidiano": {"bg": "#fef3c7", "text": "#b45309"},
    "Esportes": {"bg": "#f3e8ff", "text": "#6b21a8"},
    "Entretenimento": {"bg": "#fce7f3", "text": "#be185d"},
    "Tech & Ciência": {"bg": "#e0f2fe", "text": "#1d4ed8"},
    "Gastronomia e Culinária": {"bg": "#ffedd5", "text": "#c2410c"},
    "Viver Bem": {"bg": "#ccfbf1", "text": "#0f766e"}
}

# -----------------------------------------------------------------------------
# BASE DE DADOS INTEGRADA — LIDES INTRODUTÓRIOS DE 3 A 4 LINHAS (SEM CORTES)
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
        "extended_summary": "O atual cenário das ferramentas computacionais e redes neurais de larga escala reflete um espelhamento das assimetrias econômicas tradicionais. Ao acumularem volumes imensos de capital por meio de licenças fechadas de software, um grupo restrito de grandes corporações cria barreiras intransponíveis de entrada, forçando governos inteiros a transferirem ativos intelectuais valiosos para servidores centralizados externos.\n\nEspecialistas apontam que a saída sustentável e madura para esta dependência sistêmica envolve o fomento rigoroso a modelos de código aberto e servidores locais geridos de forma pública. Essa mudança drástica de postura é o que impede que o desenvolvimento de algoritmos de automação e análise se converta em uma mera engrenagem de extração de valor, devolvendo aos ecossistemas universitários e regionais o protagonismo científico e regulatório imprescindível para as próximas décadas."
    },
    {
        "id": "news_2",
        "title": "Decisão estratégica: Escolha de Geraldo Rufino como vice ganha força em articulação política",
        "category": "Política",
        "subcategory": "Nacional",
        "date_source": "07/07/2026 23:36 • Fonte: Brasil 247",
        "image": "https://images.unsplash.com/photo-1540910419892-4a36d2c3266c?auto=format&fit=crop&w=800&q=80",
        "lead": "Nos bastidores das principais coalizões partidárias para o próximo pleito majoritário, o nome do empresário Geraldo Rufino surge como um forte elemento agregador de centro-direita. A indicação atende à demanda explícita de governadores do bloco por uma figura de ampla aceitação no ecossistema de micro e pequenas empresas regionais. A costura final depende unicamente do aval formal das executivas nacionais, que analisam o impacto e o ganho de capilaridade em coligações do Sudeste.",
        "extended_summary": "A aproximação do nome de Rufino para a chapa majoritária representa um movimento técnico calculado para suavizar discursos excessivamente corporativistas e trazer uma narrativa focada em resiliência socioeconômica e empreendedorismo de base. Setores estratégicos do Podemos sinalizam positivamente, enxergando na imagem pública do empresário um forte canal de diálogo direto com as periferias urbanas e com trabalhadores autônomos.\n\nA estratégia de consolidação eleitoral agora entra na fase de alinhamento com frentes parlamentares de estados fundamentais. A expectativa de analistas é de que o anúncio pacifique as tensões regionais e estabeleça um palanque unificado de forte apelo popular, combinando o rigor de gestão fiscal com propostas focadas na geração orgânica de emprego e renda facilitada por incentivos estaduais."
    },
    {
        "id": "news_3",
        "title": "Governo do RN sanciona Lei Lucy para proteção de animais e regulamenta manejo comunitário",
        "category": "Cotidiano",
        "subcategory": "Cidades",
        "date_source": "07/07/2026 23:36 • Fonte: Tribuna do Norte (RN)",
        "image": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=800&q=80",
        "lead": "O Governo do Estado do Rio Grande do Norte promulgou em Diário Oficial a legislação que institui diretrizes rígidas para a tutela de animais em áreas urbanas de convívio social. Inspirada em uma mobilização popular após um caso emblemático ocorrido em Mossoró, a medida descentraliza recursos para o atendimento veterinário emergencial de livre acesso. A lei obriga os municípios do estado a organizarem conselhos ativos voltados à fiscalização e ao controle populacional ético.",
        "extended_summary": "A instituição da nova política de bem-estar animal representa um marco regulatório civilizatório para a região e soluciona impasses históricos de saúde pública. O texto estabelece punições severas para casos de negligência em ambientes públicos e cria a figura jurídica do 'Protetor Credenciado', garantindo amparo legal para ações independentes.\n\nCom suporte orçamentário previsto em emendas e fundos de desenvolvimento social, secretarias locais agora correm para implantar os primeiros postos regionais de triagem e castração móvel. A mudança, altamente comemorada por coletivos, coloca o estado na vanguarda legislativa do manejo urbano equilibrado, servindo de modelo prático para as demais federações que enfrentam o crescimento desordenado de populações vulneráveis de rua."
    }
]

# Lógica de Filtragem de Notícias
filtered_news = []
for n in news_database:
    if main_choice != "Selecione uma Categoria":
        if n["category"] != main_choice:
            continue
    if sub_choice:
        if n["subcategory"] != sub_choice:
            continue
    filtered_news.append(n)

if not filtered_news:
    st.info("Nenhuma notícia encontrada para este filtro específico. Exibindo o feed geral:")
    filtered_news = news_database

# -----------------------------------------------------------------------------
# RENDERIZAÇÃO RESPONSIVA DO CORPO DE MATÉRIAS
# -----------------------------------------------------------------------------
st.markdown("### 📰 COBERTURA INTEGRADA GLOBAL")

for item in filtered_news:
    colors = tag_colors.get(item["category"], {"bg": "#e2e8f0", "text": "#475569"})
    
    with st.container():
        st.markdown(f"""
        <div style="background-color: white; border-radius: 8px; padding: 24px; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); border: 1px solid #e2e8f0;">
            <span style="background-color: {colors['bg']}; color: {colors['text']}; display: inline-block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; padding: 4px 10px; border-radius: 4px; margin-bottom: 12px; letter-spacing: 0.5px;">
                {item['category'].upper()} ❯ {item['subcategory']}
            </span>
            <h2 style="font-size: 1.6rem !important; line-height: 1.3 !important; color: #0b1329; margin-bottom: 8px; font-weight:700;">{item['title']}</h2>
            <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 15px;">📅 {item['date_source']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_img, col_txt = st.columns([1, 1.8])
        
        with col_img:
            st.image(item["image"], use_container_width=True)
            
        with col_txt:
            # Lide fluido, completo e sem interrupções abruptas (Ajuste de 3 a 4 linhas)
            st.markdown(f"<p style='font-size:1.1rem !important; font-weight:500; color:#1e293b; line-height:1.6; margin-bottom: 15px;'>{item['lead']}</p>", unsafe_with_allowed_html=True)
            
            # Player de áudio da matéria
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
            
            # 19. Resumo Estendido Autoral com tratamento estético e textual refinado
            with st.expander("📖 LER A MATÉRIA COMPLETA — ANÁLISE EDITORIAL"):
                st.markdown(f"""
                <div style="background-color: #fafafa; border-left: 4px solid #0b1329; padding: 20px; font-size: 1.05rem !important; line-height: 1.7; color: #1e293b; text-align: justify; white-space: pre-line;">
                    <strong>Análise de Conjuntura — Conselho Editorial Horizont</strong>
                    
                    {item['extended_summary']}
                </div>
                """, unsafe_allow_html=True)
            
            # -----------------------------------------------------------------
            # 16 e 17. BOTÕES DE ENGAJAMENTO E COMPARTILHAR TOTALMENTE FUNCIONAIS
            # -----------------------------------------------------------------
            st.markdown("<div style='margin-top:15px; margin-bottom:5px; font-size:0.8rem; font-weight:600; color:#64748b;'>AVALIE A RELEVÂNCIA DESTA MATÉRIA:</div>", unsafe_allow_html=True)
            
            reactions = ["Alta Relevância", "Crítico", "Emocionante", "Inspirador", "Exige reflexão"]
            cols_reactions = st.columns([1, 1, 1, 1.2, 1.2, 1.2])
            
            if item["id"] not in st.session_state.engagement:
                st.session_state.engagement[item["id"]] = {r: 0 for r in reactions}
            
            for idx, reaction in enumerate(reactions):
                with cols_reactions[idx]:
                    count = st.session_state.engagement[item["id"]][reaction]
                    if st.button(f"{reaction} ({count})", key=f"btn_{item['id']}_{reaction}"):
                        st.session_state.engagement[item["id"]][reaction] += 1
                        st.toast(f"Reação '{reaction}' registrada!", icon="✅")
                        time.sleep(0.4)
                        st.rerun()
            
            # Botão Compartilhar com Chamada JavaScript Real
            with cols_reactions[5]:
                if st.button("📢 Compartilhar", key=f"share_{item['id']}"):
                    components.html(f"""
                    <script>
                    navigator.clipboard.writeText("https://horizont.news/noticia/{item['id']}");
                    alert("Link da notícia copiado para a área de transferência com sucesso!");
                    </script>
                    """, height=0, width=0)
                    st.success("Link copiado!")
                    
        st.markdown("<br><hr style='border: 0; border-top: 1px solid #e2e8f0;'><br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CRÉDITOS DO VEÍCULO (RODAPÉ INSTITUCIONAL E CONFORMIDADE JURÍDICA)
# -----------------------------------------------------------------------------
st.markdown("""
<div style="background-color: #0b1329; color: #94a3b8; padding: 40px 20px; border-top: 4px solid #ffbc42; border-radius: 8px 8px 0 0; font-size: 0.9rem; margin-top: 50px;">
    <div style="max-width: 1200px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 30px;">
        <div style="flex: 1; min-width: 280px;">
            <h4 style="color: #ffffff; margin-bottom: 12px; font-weight:700;">horizont.news</h4>
            <p style="color: #94a3b8 !important; font-size: 0.85rem !important;">Portal jornalístico independente focado no cruzamento geracional de dados, análises aprofundadas e cobertura global e descentralizada em tempo real.</p>
        </div>
        <div style="flex: 1; min-width: 280px;">
            <h4 style="color: #ffffff; margin-bottom: 12px; font-weight:700;">Segurança Jurídica & Fontes</h4>
            <p style="color: #94a3b8 !important; font-size: 0.85rem !important;">Conteúdos e feeds técnicos integrados em parceria direta com agências de notícias globais independentes. Os direitos autorais de imagem e áudio são integralmente preservados aos respectivos emissores e detentores sob licença pública distribuída.</p>
        </div>
        <div style="flex: 1; min-width: 280px;">
            <h4 style="color: #ffffff; margin-bottom: 12px; font-weight:700;">Termos de Uso Simplificados</h4>
            <p style="color: #94a3b8 !important; font-size: 0.85rem !important;">É expressamente permitida a reprodução e compartilhamento de trechos e lides das matérias informativas, desde que mantidos o link direto para este portal e os devidos créditos às fontes nominais especificadas em cada publicação.</p>
        </div>
    </div>
    <hr style="border-color: #1e293b; margin: 30px 0;">
    <div style="text-align: center; font-size: 0.8rem; color: #64748b;">
        © 2026 horizont.news — Desenvolvido em conformidade com as diretrizes editoriais Premium Universal. Todos os direitos reservados.
    </div>
</div>
""", unsafe_allow_html=True)
