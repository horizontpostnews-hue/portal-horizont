import streamlit as st
import feedparser
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÕES INICIAIS E SEGURANÇA
# ==========================================
st.set_page_config(page_title="horizont.news - Painel Editorial", layout="wide")

# Insira sua chave gratuita do Gemini nas configurações do Streamlit ou abaixo
# Para obter uma chave grátis: https://aistudio.google.com/
GEMINI_API_KEY = st.sidebar.text_input("Gemini API Key", type="password")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Banco de dados temporário em memória (Simulado para simplificar em 1 arquivo)
if 'banco_noticias' not in st.session_state:
    st.session_state.banco_noticias = []

# Fontes Globais Gratuitas e Sem Paywall (RSS Open-Access)
FONTES_RSS = {
    "Reuters World": "https://news.google.com/rss/search?q=reuters+world&hl=en-US&gl=US&ceid=US:en",
    "Deutsche Welle (EN)": "https://rss.dw.com/rdf/rss-en-all",
    "El País (ES)": "https://elpais.com/rss/elpais/portada.xml",
    "Agência Brasil (PT)": "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml"
}

# Terceirização das regras do Guardrail de Sensibilidade
TERMOS_SENSIVEIS = ['tragédia', 'crime', 'violência', 'morreu', 'assassinato', 'guerra', 'míssil', 'processo judicial', 'atentado', 'suicídio']

# ==========================================
# 2. FUNÇÕES DE INTELIGÊNCIA ARTIFICIAL (IA)
# ==========================================

def classificar_sensibilidade(titulo, texto):
    """Filtro de Sensibilidade (Guardrail)"""
    conteudo = (titulo + " " + texto).lower()
    for termo in TERMOS_SENSIVEIS:
        if termo in conteudo:
            return "RETIDO", f"Contém termo sensível: '{termo}'"
    return "APROVADO", "Seguro para publicação automática"

def pipeline_escrita_ia(titulo_original, link_original, fonte_nome):
    """Técnica de Síntese Cruzada, Paráfrase Radical e Tradução"""
    if not GEMINI_API_KEY:
        return None
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Você é o redator-chefe do portal internacional horizont.news. 
    Seu público vai desde jovens da Geração Z até adultos maduros de várias culturas.
    Com base na seguinte notícia da fonte {fonte_nome}: "{titulo_original}".
    
    Execute as seguintes tarefas estritamente:
    1. Crie um título inédito, chamativo e proprietário (Anti-Plágio).
    2. Aplique Paráfrase Radical: reescreva os fatos puros no formato de Pirâmide Invertida jornalística. Linguagem fluida, leve e instigante.
    3. Escreva a matéria original em Português.
    4. Traduza a matéria criada perfeitamente para Inglês e Espanhol.
    
    Formate sua resposta EXACTAMENTE assim, separando por tags:
    [TITULO_PT] Texto aqui
    [TEXTO_PT] Texto aqui
    [TITULO_EN] Texto aqui
    [TEXTO_EN] Texto aqui
    [TITULO_ES] Texto aqui
    [TEXTO_ES] Texto aqui
    """
    try:
        response = model.generate_content(prompt)
        res = response.text
        
        # Parsing simples da resposta da IA
        dados = {}
        for idioma in ['PT', 'EN', 'ES']:
            dados[f'titulo_{idioma.lower()}'] = res.split(f'[TITULO_{idioma}]')[1].split(f'[TEXTO_{idioma}]')[0].strip()
            if idioma == 'ES':
                dados[f'texto_{idioma.lower()}'] = res.split(f'[TEXTO_{idioma}]')[1].strip()
            else:
                proxima_tag = 'EN' if idioma == 'PT' else 'ES'
                dados[f'texto_{idioma.lower()}'] = res.split(f'[TEXTO_{idioma}]')[1].split(f'[TITULO_{proxima_tag}]')[0].strip()
        
        # Injeção Automática de Créditos e Links
        credito = f"\n\n*Este artigo foi produzido de forma autoral pelo horizont.news, com informações cruzadas de {fonte_nome}. [Acesse a fonte original]({link_original}).*"
        for idioma in ['pt', 'en', 'es']:
            dados[f'texto_{idioma}'] += credito
            
        return dados
    except:
        return None

# ==========================================
# 3. INTERFACE VISUAL (FRONT-END)
# ==========================================

st.title("🌐 horizont.news — Painel de Controle Integrado")
st.markdown("Paleta de cores configurada: **Azul Royal** para estrutura e **Coral/Laranja** para ações urgentes.")

# Botão para capturar notícias do mundo via RSS Agregador
if st.button("🔄 Capturar e Processar Novas Notícias do Mundo"):
    if not GEMINI_API_KEY:
        st.error("Por favor, insira sua Gemini API Key na barra lateral.")
    else:
        com_sucesso = 0
        for nome_fonte, url_rss in FONTES_RSS.items():
            feed = feedparser.parse(url_rss)
            for entrada in feed.entries[:2]: # Captura as 2 mais recentes de cada para não estourar limites
                # Verificar se já existe no nosso banco para evitar duplicidade
                if any(x['link_origem'] == entrada.link for x in st.session_state.banco_noticias):
                    continue
                
                status, motivo = classificar_sensibilidade(entrada.title, entrada.get('description', ''))
                
                # Processa na IA
                dados_ia = pipeline_escrita_ia(entrada.title, entrada.link, nome_fonte)
                
                if dados_ia:
                    nova_noticia = {
                        "id": len(st.session_state.banco_noticias) + 1,
                        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "fonte_origem": nome_fonte,
                        "link_origem": entrada.link,
                        "status": status,
                        "motivo_retencao": motivo,
                        **dados_ia
                    }
                    st.session_state.banco_noticias.append(nova_noticia)
                    com_sucesso += 1
        st.success(f"Processamento concluído! {com_sucesso} novas notícias triadas pelo Guardrail.")

# Abas do Painel Administrativo de Homologação Humana
aba_publicadas, aba_retidas, aba_visualizacao_site = st.tabs([
    "🟢 Feed de Monitoramento (Automáticas/Aprovadas)", 
    "🟠 Mesa de Edição (Retidas pelo Guardrail)", 
    "💻 Visualização do Site (Como o Público Vê)"
])

# ---- ABA 1: FEED DE MONITORAMENTO ----
with aba_publicadas:
    st.subheader("Notícias Publicadas Automaticamente (Livres de Gatilhos)")
    noticias_ok = [n for n in st.session_state.banco_noticias if n['status'] == 'APROVADO']
    if not noticias_ok:
        st.info("Nenhuma notícia automática publicada ainda.")
    else:
        df = pd.DataFrame(noticias_ok)[['id', 'data', 'fonte_origem', 'titulo_pt']]
        st.dataframe(df, use_container_width=True)

# ---- ABA 2: MESA DE EDIÇÃO (RETIDOS) ----
with aba_retidas:
    st.subheader("Fila Visual de Notícias Bloqueadas por Segurança")
    noticias_retidas = [n for n in st.session_state.banco_noticias if n['status'] == 'RETIDO']
    
    if not noticias_retidas:
        st.success("Limpo! Nenhuma notícia retida aguardando revisão.")
    else:
        for idx, noti in enumerate(noticias_retidas):
            with st.expander(f"⚠️ BLOQUEADA: {noti['titulo_pt']} (Motivo: {noti['motivo_retencao']})"):
                st.warning(f"**Motivo do Alerta:** {noti['motivo_retencao']} | **Fonte Original:** {noti['fonte_origem']}")
                
                # Permitir edição rápida pelo humano (Human-in-the-Loop)
                novo_titulo = st.text_input("Editar Título", noti['titulo_pt'], key=f"t_{noti['id']}")
                novo_texto = st.text_area("Editar Texto", noti['texto_pt'], key=f"x_{noti['id']}")
                
                col1, col2, col3 = st.columns(3)
                if col1.button("✅ Aprovar com Edições", key=f"ap_{noti['id']}", help="Aprova a matéria corrigida"):
                    st.session_state.banco_noticias[st.session_state.banco_noticias.index(noti)]['status'] = 'APROVADO'
                    st.session_state.banco_noticias[st.session_state.banco_noticias.index(noti)]['titulo_pt'] = novo_titulo
                    st.session_state.banco_noticias[st.session_state.banco_noticias.index(noti)]['texto_pt'] = novo_texto
                    st.rerun()
                
                if col2.button("🔓 Forçar Aprovação Direta", key=f"f_{noti['id']}", help="Ignorar o alerta (Falso Positivo)"):
                    st.session_state.banco_noticias[st.session_state.banco_noticias.index(noti)]['status'] = 'APROVADO'
                    st.rerun()
                    
                if col3.button("❌ Descartar Matéria", key=f"d_{noti['id']}"):
                    st.session_state.banco_noticias.remove(noti)
                    st.rerun()

# ---- ABA 3: VISUALIZAÇÃO DO SITE (O FEED INFINITO MULTITEMÁTICO) ----
with aba_visualizacao_site:
    st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>horizont.news</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic;'>O cenário global em um clique</p>", unsafe_allow_html=True)
    st.write("---")
    
    idioma_selecionado = st.radio("Selecione o Idioma do Portal / Select Language", ["Português", "English", "Español"], horizontal=True)
    lang_code = "pt" if idioma_selecionado == "Português" else "en" if idioma_selecionado == "English" else "es"

    noticias_para_exibir = [n for n in st.session_state.banco_noticias if n['status'] == 'APROVADO']
    
    if not noticias_para_exibir:
        st.info("O portal está pronto. Use o botão no topo para carregar e simular o feed de notícias!")
    else:
        # Simulação de Feed Infinito Organizado
        for n in reversed(noticias_para_exibir):
            st.markdown(f"<h3 style='color: #1e3a8a;'>{n[f'titulo_{lang_code}']}</h3>", unsafe_allow_html=True)
            st.caption(f"📅 Publicado em: {n['data']} | Fonte: {n['fonte_origem']}")
            st.write(n[f'texto_{lang_code}'])
            
            # Recursos de Engajamento por Faixa Etária
            col_audio, col_emoji = st.columns([1, 1])
            with col_audio:
                # Funcionalidade para adultos e profissionais: Ouvir texto via Áudio (Simulado nativo do navegador)
                st.caption("🔊 Ouvir esta matéria (Recurso de acessibilidade ativado)")
            with col_emoji:
                # Sistema de Reações por Emojis para Jovens (Geração Z)
                st.write("Reações: 👍 | 🔥 | 💡 | 🧠")
            
            st.markdown("<hr style='border: 1px dashed #f97316;' />", unsafe_allow_html=True) # Linha divisória na cor Coral