import streamlit as st
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# Configuração da Página e Reset de Layout
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="horizont.news — Conectando Gerações",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injeção de CSS Premium Reconstituído e Ajustado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
        color: #1e293b !important;
    }
    
    .premium-header {
        background: linear-gradient(135deg, #0b1329 0%, #1e293b 100%);
        padding: 30px 20px;
        text-align: center;
        border-bottom: 4px solid #00f5d4;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(11, 19, 41, 0.15);
    }
    .premium-logo-area {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
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

    /* Estilização das matérias em formato de Cards */
    .news-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
        height: 100%;
    }

    /* Destaque Principal */
    .destaque-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
    }

    /* Centralização estrita do título do Expander (Botão de Leitura) */
    [data-testid="stExpander"] summary {
        justify-content: center !important;
        text-align: center !important;
    }
    [data-testid="stExpander"] summary span {
        margin: 0 auto !important;
        font-weight: 600 !important;
    }

    /* Ajuste do fluxo de botões de relevância */
    .dynamic-pill-flow div[data-testid="stHorizontalBlockHasColumns"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
    }
    .dynamic-pill-flow div[data-testid="column"] {
        flex: unset !important;
        width: auto !important;
    }
    .dynamic-pill-flow div[data-testid="stButton"] button {
        width: auto !important;
        white-space: nowrap !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 0.85rem !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# ESTADO DE SESSÃO E DICIONÁRIO DE ENGAJAMENTO (CHAVES PADRONIZADAS)
# -----------------------------------------------------------------------------
reactions_list = ["Alta Relevância", "Crítico", "Emocionante", "Inspirador", "Exige reflexão"]
reaction_emojis = {
    "Alta Relevância": "🔥",
    "Crítico": "⚖️",
    "Emocionante": "🎭",
    "Inspirador": "💡",
    "Exige reflexão": "🧠"
}

if "engagement" not in st.session_state:
    st.session_state.engagement = {
        "destaque": {r: 87 if r == "Alta Relevância" else 15 for r in reactions_list},
        "news_1": {r: 12 if r == "Alta Relevância" else 4 for r in reactions_list},
        "news_2": {r: 22 if r == "Alta Relevância" else 9 for r in reactions_list}
    }

# -----------------------------------------------------------------------------
# BARRA DE IDENTIDADE VISUAL
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

# Letreiros Dinâmicos
html_ticker_news = """
<div style="display: flex; background-color: #0b1329; border-radius: 4px; overflow: hidden; margin-bottom: 25px; align-items: center;">
    <div style="background-color: #ffbc42; color: #0b1329; padding: 10px 15px; font-weight: 800; font-size: 0.85rem; white-space: nowrap;">ÚLTIMAS NOTÍCIAS</div>
    <div style="overflow: hidden; white-space: nowrap; width: 100%; display: flex; align-items: center;">
        <div style="display: inline-block; padding-left: 100%; color: #ffffff; font-size: 0.95rem; font-weight: 500; animation: marquee 30s linear infinite;">
            📌 Transição energética global avança com novos subsídios a usinas de hidrogênio verde na Europa &nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp; 📌 Mercado de semicondutores registra alta histórica no segundo trimestre de 2026
        </div>
    </div>
</div>
<style> @keyframes marquee { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } } </style>
"""
components.html(html_ticker_news, height=45)

# -----------------------------------------------------------------------------
# MATÉRIA EM DESTAQUE
# -----------------------------------------------------------------------------
st.markdown("## 🌟 MATÉRIA EM DESTAQUE")
with st.container():
    st.markdown('<div class="destaque-container">', unsafe_allow_html=True)
    col_dest_img, col_dest_txt = st.columns([1, 1.2])
    with col_dest_img:
        st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80", use_container_width=True)
    with col_dest_txt:
        st.markdown("""
        <span style="background-color: #fef3c7; color: #b45309; font-size: 0.8rem; font-weight: 700; padding: 4px 8px; border-radius: 4px;">CONJUNTURA GLOBAL</span>
        <h2 style="margin-top: 10px; font-size: 2rem;">A Grande Convergência Tecnológica de 2026 e o Impacto nos Empregos de Base</h2>
        <p style="font-size: 0.85rem; color: #64748b;">📅 08/07/2026 • Fonte: World Economic Forum (Suíça)</p>
        <p>A automação industrial unificada por sistemas integrados avançados atingiu seu ápice operacional neste semestre. Governos globais iniciaram frentes de contingência para requalificar trabalhadores de setores operacionais tradicionais.</p>
        """, unsafe_allow_html=True)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3")
        
        # Expander centralizado via CSS
        with st.expander("📖 LER MATÉRIA COMPLETA"):
            st.markdown("""
            A reestruturação econômica impulsionada pelos novos arranjos produtivos automatizados está redesenhando as cadeias de suprimentos globais. O relatório emitido nesta semana indica que mais de 45% das funções eminentemente repetitivas na indústria manufatureira passaram por algum nível de substituição ou suporte digital direto no último ano.
            
            O fenômeno, batizado de A Grande Convergência, não se restringe aos países desenvolvidos, afetando significativamente polos produtivos na América Latina e no Sudeste Asiático. Especialistas alertam para a necessidade premente de reformas estruturais nos currículos de ensino técnico profissionalizante, visando preencher as lacunas abertas pela nova demanda de supervisores de sistemas automatizados.
            
            Paralelamente, consórcios internacionais sugerem a criação de fundos de amparo financiados por taxas de produtividade tecnológica para mitigar os impactos sociais de transição nas regiões mais vulneráveis.
            """)
            
        # Reações Destaque Blindadas contra KeyError
        st.markdown('<div class="dynamic-pill-flow">', unsafe_allow_html=True)
        rc_dest = st.columns(5)
        for idx, r_name in enumerate(reactions_list):
            with rc_dest[idx]:
                emoji = reaction_emojis[r_name]
                count = st.session_state.engagement["destaque"][r_name]
                if st.button(f"{emoji} {r_name} ({count})", key=f"btn_dest_{idx}"):
                    st.session_state.engagement["destaque"][r_name] += 1
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAINEL COPA DO MUNDO 2026
# -----------------------------------------------------------------------------
st.markdown("### 🏆 COPA DO MUNDO FIFA 2026 — BASTIDORES & CURIOSIDADES")
with st.container():
    col_vid_left, col_vid_right = st.columns([1.4, 1])
    with col_vid_left:
        components.iframe("https://www.youtube.com/embed/Jm9n_Zcl_iE", height=315)
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
# FEED PRINCIPAL EM DOIS CARDS PARALELOS
# -----------------------------------------------------------------------------
st.markdown("### 📰 COBERTURA INTEGRADA GLOBAL")

col_feed_1, col_feed_2 = st.columns(2)

# ---- CARD 1: TECH & CIÊNCIA ----
with col_feed_1:
    st.markdown('<div class="news-card">', unsafe_allow_html=True)
    st.markdown("""
    <span style="background-color: #e0f2fe; color: #1d4ed8; font-size: 0.75rem; font-weight: 700; padding: 4px 8px; border-radius: 4px;">TECH & CIÊNCIA ❯ INOVAÇÃO</span>
    <h3 style="margin-top:10px; font-size:1.4rem;">Os novos rumos geopolíticos da Inteligência Artificial e a disputa de mercado soberano</h3>
    <p style="font-size: 0.85rem; color: #64748b;">📅 07/07/2026 23:37 • Fonte: Outras Palavras (Brasil)</p>
    """, unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80", use_container_width=True)
    st.markdown("<p>A corrida pelo controle dos ecossistemas digitais avançados ganha contornos dramáticos à medida que blocos governamentais passam a exigir infraestruturas proprietárias de dados.</p>", unsafe_allow_html=True)
    
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    
    with st.expander("📖 LER MATÉRIA COMPLETA"):
        st.markdown("""
        **Resumo Estruturado da Matéria:**
        1. **Cenário Atual:** Ferramentas computacionais de alta performance e redes neurais profundas de larga escala operam como espelhos das assimetrias econômicas globais tradicionais.
        2. **Monopólio Tecnológico:** O acúmulo de capital por meio de licenças fechadas de software cria barreiras intransponíveis para nações emergentes e pequenas produtoras de tecnologia.
        3. **A Ameaça Soberana:** Depender estritamente de soluções proprietárias externas põe em risco direto as salvaguardas civis, infraestruturas críticas de dados e a segurança cibernética de governos soberanos.
        4. **Iniciativas Emergentes:** Blocos regionais começam a articular redes computacionais públicas e bancos de dados abertos para contornar a dependência monopolista.
        5. **O Fator Infraestrutura:** Centros de processamento de dados e fornecimento estável de energia tornam-se ativos estratégicos de segurança nacional em discussões diplomáticas.
        6. **Modelos Alternativos:** Pesquisadores defendem códigos de governança descentralizada e ecossistemas open-source como caminhos viáveis para mitigar a disparidade tecnológica global.
        7. **Regulamentação Rigorosa:** Diretrizes propostas preveem auditorias profundas sobre algoritmos estrangeiros que operam em setores vitais da economia local.
        8. **Perspectivas Futuras:** O equilíbrio geopolítico da próxima década dependerá diretamente da capacidade de desenvolvimento científico próprio de cada nação.
        9. **Conclusão Factual:** Sem investimento massivo e soberano em tecnologia proprietária, países em desenvolvimento correm o risco de se tornarem colônias digitais definitivas.
        """)
        
    st.markdown('<div class="dynamic-pill-flow">', unsafe_allow_html=True)
    rc1 = st.columns(5)
    for idx, r_name in enumerate(reactions_list):
        with rc1[idx]:
            emoji = reaction_emojis[r_name]
            count = st.session_state.engagement["news_1"][r_name]
            if st.button(f"{emoji} {r_name} ({count})", key=f"btn_n1_{idx}"):
                st.session_state.engagement["news_1"][r_name] += 1
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---- CARD 2: POLÍTICA ----
with col_feed_2:
    st.markdown('<div class="news-card">', unsafe_allow_html=True)
    st.markdown("""
    <span style="background-color: #e0f2fe; color: #0369a1; font-size: 0.75rem; font-weight: 700; padding: 4px 8px; border-radius: 4px;">POLÍTICA ❯ NACIONAL</span>
    <h3 style="margin-top:10px; font-size:1.4rem;">Decisão estratégica: Escolha de Geraldo Rufino como vice ganha força em articulação política</h3>
    <p style="font-size: 0.85rem; color: #64748b;">📅 07/07/2026 23:36 • Fonte: Brasil 247 (Brasil)</p>
    """, unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1540910419892-4a36d2c3266c?auto=format&fit=crop&w=800&q=80", use_container_width=True)
    st.markdown("<p>Nos bastidores das coalizões partidárias, o nome do empresário surge como um forte elemento agregador para o equilíbrio de palanques e atração do setor de comércio.</p>", unsafe_allow_html=True)
    
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")
    
    with st.expander("📖 LER MATÉRIA COMPLETA"):
        st.markdown("""
        **Resumo Estruturado da Matéria:**
        1. **Contexto das Articulações:** Coordenadores de campanha de frentes interpartidárias identificaram a necessidade de equilibrar discursos ideológicos com acenos práticos ao mercado.
        2. **O Nome Escolhido:** O empresário Geraldo Rufino desponta como o favorito devido à sua forte interlocução com o setor produtivo de base e o cooperativismo.
        3. **Apelo Popular:** A história de resiliência e a liderança no empreendedorismo popular agregam capilaridade em setores periféricos urbanos onde a chapa tradicional sofria resistência.
        4. **Recepção Empresarial:** Confederações de comércio e associações de microempreendedores emitiram pareceres preliminares favoráveis ao perfil de composição proposto.
        5. **Alinhamento Programático:** Reuniões fechadas tratam de ajustar os planos econômicos, inserindo tópicos fortes de desburocratização e facilitação de crédito para microcrédito.
        6. **Contrapontos Internos:** Setores mais tradicionais da legenda ponderam sobre a necessidade de garantir espaço para quadros orgânicos históricos na Executiva Nacional.
        7. **Estratégia Regional:** A indicação visa neutralizar o avanço de opositores em estados economicamente estratégicos do Sudeste e Sul do país.
        8. **Calendário Político:** A expectativa das lideranças é oficializar o anúncio de composição de chapa até o final da próxima convenção partidária ordinária.
        9. **Conclusão Factual:** A movimentação consolida uma tendência contemporânea de trazer figuras notórias do setor corporativo para conferir pragmatismo às disputas eleitorais.
        """)
        
    st.markdown('<div class="dynamic-pill-flow">', unsafe_allow_html=True)
    rc2 = st.columns(5)
    for idx, r_name in enumerate(reactions_list):
        with rc2[idx]:
            emoji = reaction_emojis[r_name]
            count = st.session_state.engagement["news_2"][r_name]
            if st.button(f"{emoji} {r_name} ({count})", key=f"btn_n2_{idx}"):
                st.session_state.engagement["news_2"][r_name] += 1
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# RODAPÉ DETALHADO
# -----------------------------------------------------------------------------
st.markdown("""
<div style="background-color: #0b1329; color: #94a3b8; padding: 40px 20px; border-top: 4px solid #ffbc42; border-radius: 8px; font-size: 0.9rem; margin-top: 40px;">
    <div style="text-align: center; max-width: 800px; margin: 0 auto; line-height: 1.6;">
        <p style="font-weight: 700; color: #ffffff; margin-bottom: 5px;">© 2026 horizont.news — Portal Independente</p>
        <p style="color: #64748b; font-size: 0.8rem; margin-bottom: 15px;">
            Desenvolvido em conformidade estrita com as diretrizes do Manual de Redação e Princípios Editoriais de Universalidade. "Informação sem Fronteiras" é uma marca registrada sob licença de distribuição jornalística aberta.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
