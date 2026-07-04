import streamlit as st
import feedparser
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import json

# ==========================================
# 1. CONFIGURAÇÕES INICIAIS E SEGURANÇA
# ==========================================
st.set_page_config(page_title="horizont.news - Painel Editorial", layout="wide")

GEMINI_API_KEY = st.sidebar.text_input("Gemini API Key", type="password")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

if 'banco_noticias' not in st.session_state:
    st.session_state.banco_noticias = []

# Fontes RSS variadas e com alto fluxo de atualização
FONTES_RSS = {
    "G1 Globo (PT)": "https://g1.globo.com/rss/g1/",
    "BBC News World (EN)": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "El Mundo Portada (ES)": "https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml",
    "CNN International (EN)": "http://rss.cnn.com/rss/edition.rss"
}

TERMOS_SENSIVEIS = ['tragédia', 'crime', 'violência', 'morreu', 'assassinato', 'guerra', 'míssil', 'processo judicial', 'atentado', 'suicídio', 'mortes', 'acidente']

# ==========================================
# 2. FUNÇÕES DE INTELIGÊNCIA ARTIFICIAL (IA)
# ==========================================

def classificar_sensibilidade(titulo, texto):
    conteudo = (titulo + " " + texto).lower()
    for termo in TERMOS_SENSIVEIS:
        if termo in conteudo:
            return "RETIDO", f"Contém termo sensível: '{termo}'"
    return "APROVADO", "Seguro para publicação automática"

def pipeline_escrita_ia(titulo_original, link_original, fonte_nome):
    if not GEMINI_API_KEY:
        return None
    
    # Usando o modelo genérico atual 'gemini-pro' para estabilidade na conta gratuita
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Você é o redator-chefe do portal internacional horizont.news.
    Com base na notícia da fonte {fonte_nome}: "{titulo_original}".
    
    Gere uma versão proprietária (anti-plágio), com paráfrase radical em formato de pirâmide invertida jornalística.
    Crie o texto original em português e também traduções adaptadas para inglês e espanhol.
    
    Responda RIGOROSAMENTE no formato JSON abaixo, sem qualquer texto descritivo antes ou depois:
    {{
        "titulo_pt": "Seu título inédito em português",
        "texto_pt": "Seu texto jornalístico em português",
        "titulo_en": "Seu título inédito em inglês",
        "texto_en": "Seu texto jornalístico em inglês",
        "titulo_es": "Seu título inédito em espanhol",
        "texto_es": "Seu texto jornalístico em espanhol"
    }}
    """
    try:
        response = model.generate_content(prompt)
        # Limpa possíveis blocos de formatação markdown que a IA coloque
        texto_puro = response.text.strip()
        if "```json" in texto_puro:
            texto_puro = texto_puro.split("```json")[1].split("```")[0].strip()
        elif "```" in texto_puro:
            texto_puro = texto_puro.split("```")[1].split("```")[0].strip()
            
        dados = json.loads(texto_puro)
        
        # Injeção Automática de Créditos e Links
        credito = f"\n\n*Este artigo foi produzido de forma autoral pelo horizont.news, com informações cruzadas de {fonte_nome}. [Acesse a fonte original]({link_original}).*"
        for idioma in ['pt', 'en', 'es']:
            dados[f'texto_{idioma}'] += credito
            
        return dados
    except Exception as e:
        return None

# ==========================================
# 3. INTERFACE VISUAL (FRONT-END)
# ==========================================

st.title("🌐 horizont.news — Painel de Controle Integrado")
st.markdown("Paleta de cores configurada: **Azul Royal** para estrutura e **Coral/Laranja** para ações urgentes.")

if st.button("🔄 Capturar e Processar Novas Notícias do Mundo"):
    if not GEMINI_API_KEY:
        st.error("Por favor, insira sua Gemini API Key na barra lateral.")
    else:
        com_sucesso = 0
        progresso = st.progress(0)
        status_txt = st.empty()
        
        total_fontes = len(FONTES_RSS)
        
        # Limpa o banco da sessão para o teste forçar a captura das notícias atuais do feed
        st.session_state.banco_noticias = []
        
        for i, (nome_fonte, url_rss) in enumerate(FONTES_RSS.items()):
            status_txt.write(f"Lendo notícias de: {nome_fonte}...")
            feed = feedparser.parse(url_rss)
            
            # Pega as 2 notícias mais recentes do topo do feed de cada fonte
            for entrada in feed.entries[:2]:
                status_txt.write(f"Processando no Gemini: {entrada.title[:50]}...")
                
                status, motivo = classificar_sensibilidade(entrada.title, entrada.get('description', ''))
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
            
            progresso.progress((i + 1) / total_fontes)
            
        status_txt.empty()
        if com_sucesso > 0:
            st.success(f"Sucesso! {com_sucesso} novas notícias foram geradas, traduzidas e publicadas pelo Gemini!")
            st.rerun()
        else:
            st.error("O Gemini não conseguiu processar o formato das notícias nesta tentativa. Verifique se sua chave está correta e tente de novo.")

# Abas do Painel Administrativo
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
        for noti in noticias_retidas:
            with st.expander(f"⚠️ BLOQUEADA: {noti['titulo_pt']} ({noti['fonte_origem']})"):
                st.warning(f"**Motivo do Alerta:** {noti['motivo_retencao']}")
                
                novo_titulo = st.text_input("Editar Título", noti['titulo_pt'], key=f"t_{noti['id']}")
                novo_texto = st.text_area("Editar Texto", noti['texto_pt'], key=f"x_{noti['id']}")
                
                col1, col2, col3 = st.columns(3)
                if col1.button("✅ Aprovar com Edições", key=f"ap_{noti['id']}"):
                    idx = st.session_state.banco_noticias.index(noti)
                    st.session_state.banco_noticias[idx]['status'] = 'APROVADO'
                    st.session_state.banco_noticias[idx]['titulo_pt'] = novo_titulo
                    st.session_state.banco_noticias[idx]['texto_pt'] = novo_texto
                    st.rerun()
                
                if col2.button("🔓 Forçar Aprovação", key=f"f_{noti['id']}"):
                    idx = st.session_state.banco_noticias.index(noti)
                    st.session_state.banco_noticias[idx]['status'] = 'APROVADO'
                    st.rerun()
                    
                if col3.button("❌ Descartar", key=f"d_{noti['id']}"):
                    st.session_state.banco_noticias.remove(noti)
                    st.rerun()

# ---- ABA 3: VISUALIZAÇÃO DO SITE ----
with aba_visualizacao_site:
    st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>horizont.news</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic;'>O cenário global em um clique</p>", unsafe_allow_html=True)
    st.write("---")
    
    idioma_selecionado = st.radio("Idioma do Portal / Language", ["Português", "English", "Español"], horizontal=True)
    lang_code = "pt" if idioma_selecionado == "Português" else "en" if idioma_selecionado == "English" else "es"

    noticias_para_exibir = [n for n in st.session_state.banco_noticias if n['status'] == 'APROVADO']
    
    if not noticias_para_exibir:
        st.info("Nenhuma notícia aprovada para exibição no feed público até o momento.")
    else:
        for n in reversed(noticias_para_exibir):
            st.markdown(f"<h3 style='color: #1e3a8a;'>{n[f'titulo_{lang_code}']}</h3>", unsafe_allow_html=True)
            st.caption(f"📅 Publicado em: {n['data']} | Fonte: {n['fonte_origem']}")
            st.write(n[f'texto_{lang_code}'])
            
            col_audio, col_emoji = st.columns([1, 1])
            with col_audio:
                st.caption("🔊 Ouvir esta matéria (Acessibilidade ativada)")
            with col_emoji:
                st.write("Reações: 👍 | 🔥 | 💡 | 🧠")
            
            st.markdown("<hr style='border: 1px dashed #f97316;' />", unsafe_allow_html=True)
