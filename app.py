import streamlit as st
import feedparser
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import json
import os
import re

# ==========================================
# 1. CONFIGURAÇÕES E NOVO MAPA MUNDIAL DE FONTES
# ==========================================
st.set_page_config(page_title="horizont.news - Painel Editorial", layout="wide")

GEMINI_API_KEY = st.sidebar.text_input("Gemini API Key", type="password")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

ARQUIVO_BANCO = "banco_noticias.json"

def carregar_dados_permanentes():
    if os.path.exists(ARQUIVO_BANCO):
        try:
            with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def salvar_dados_permanentes(dados):
    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'banco_noticias' not in st.session_state:
    st.session_state.banco_noticias = carregar_dados_permanentes()

# MAPA MUNDIAL EXPANDIDO: Quebrando a bolha ocidental
FONTES_RSS = {
    "Al Jazeera (Ásia Ocidental / Oriente Médio)": "https://www.aljazeera.com/xml/rss/all.xml",
    "TASS Agency (Europa Oriental / Rússia)": "https://tass.com/rss/v2.xml",
    "NHK World (Japão)": "https://www3.nhk.or.jp/nhkworld/nhknewsline/rss/index.xml",
    "Xinhua Net (China)": "https://www.xinhuanet.com/english/rss/worldrss.xml",
    "Clarín (Argentina)": "https://www.clarin.com/rss/mundo/",
    "El Universal (México)": "https://www.eluniversal.com.mx/rss/universal/mundo.xml",
    "CBC News (Canadá)": "https://rss.cbc.ca/lineup/world.xml",
    "G1 Globo (Brasil)": "https://g1.globo.com/rss/g1/",
    "BBC News (Reino Unido)": "http://feeds.bbci.co.uk/news/world/rss.xml"
}

TERMOS_SENSIVEIS = ['tragédia', 'crime', 'violência', 'morreu', 'assassinato', 'guerra', 'míssil', 'atentado', 'suicídio', 'mortes', 'acidente']

# ==========================================
# 2. INTELIGÊNCIA EDITORIAL E EXTRAÇÃO DE CONTEÚDO REAL
# ==========================================

def classificar_sensibilidade(titulo, texto):
    conteudo = (titulo + " " + texto).lower()
    for termo in TERMOS_SENSIVEIS:
        if termo in conteudo:
            return "RETIDO", f"Contém termo sensível: '{termo}'"
    return "APROVADO", "Seguro para publicação automática"

def limpar_html(texto_html):
    """Remove tags HTML comuns que vêm nos feeds RSS para deixar o texto limpo"""
    if not texto_html:
        return ""
    texto_limpo = re.sub('<[^<]+?>', '', texto_html)
    return texto_limpo.strip()

def motor_fallback_real(titulo, resumo_original, fonte_nome):
    """Se a IA estiver sem chave, extrai o conteúdo REAL do RSS em vez de texto fictício"""
    texto_extraido = limpar_html(resumo_original)
    
    if not texto_extraido or len(texto_extraido) < 15:
        texto_extraido = f"Novos desdobramentos importantes foram despachados diretamente pela central de correspondentes da agência {fonte_nome}."

    return {
        "titulo_pt": f"{titulo}",
        "texto_pt": f"{texto_extraido}\n\n*Nota: Transmissão direta da agência parceira.*",
        "titulo_en": f"Global News: {titulo}",
        "texto_en": f"{texto_extraido}\n\n*Note: Direct agency wire transmission.*",
        "titulo_es": f"Reporte: {titulo}",
        "texto_es": f"{texto_extraido}\n\n*Nota: Transmisión directa desde la agencia de origen.*"
    }

def pipeline_escrita_ia(titulo_original, resumo_original, link_original, fonte_nome):
    # Se não houver chave de API informada, usa o conteúdo real vindo do jornal de origem
    if not GEMINI_API_KEY:
        return motor_fallback_real(titulo_original, resumo_original, fonte_nome)
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        texto_base = limpar_html(resumo_original)
        
        prompt = f"""
        Você é o redator-chefe do portal internacional horizont.news.
        Com base no título "{titulo_original}" e no fato coletado: "{texto_base}" da fonte {fonte_nome}.
        
        Escreva uma matéria jornalística aprofundada e proprietária (mínimo 3 parágrafos) expandindo o contexto.
        Gere três versões completas e traduzidas: português, inglês e espanhol.
        
        Retorne RIGOROSAMENTE apenas um JSON limpo e válido:
        {{
            "titulo_pt": "Manchete forte em português",
            "texto_pt": "Corpo da notícia completo e profissional em português",
            "titulo_en": "Manchete em inglês",
            "texto_en": "Corpo da notícia em inglês",
            "titulo_es": "Manchete em espanhol",
            "texto_es": "Corpo da notícia em espanhol"
        }}
        """
        response = model.generate_content(prompt)
        texto_puro = response.text.strip()
        
        if "```json" in texto_puro:
            texto_puro = texto_puro.split("```json")[1].split("```")[0].strip()
        elif "```" in texto_puro:
            texto_puro = texto_puro.split("```")[1].split("```")[0].strip()
            
        dados = json.loads(texto_puro)
    except Exception:
        dados = motor_fallback_real(titulo_original, resumo_original, fonte_nome)
        
    # Rodapé de transparência editorial
    credito = f"\n\n*Este artigo foi estruturado de forma independente pela redação horizont.news, com dados analíticos de {fonte_nome}. [Leia o despacho original no veículo de origem]({link_original}).*"
    for idioma in ['pt', 'en', 'es']:
        dados[f'texto_{idioma}'] += credito
        
    return dados

# ==========================================
# 3. INTERFACE VISUAL (FRONT-END DO PORTAL)
# ==========================================

st.title("🌐 horizont.news — Painel de Controle Integrado")

if st.button("🔄 Capturar e Processar Novas Notícias do Mundo"):
    com_sucesso = 0
    progresso = st.progress(0)
    status_txt = st.empty()
    
    total_fontes = len(FONTES_RSS)
    banco_atual = carregar_dados_permanentes()
    links_existentes = {n['link_origem'] for n in banco_atual}
    
    for i, (nome_fonte, url_rss) in enumerate(FONTES_RSS.items()):
        status_txt.write(f"📖 Conectando com a agência: **{nome_fonte}**...")
        feed = feedparser.parse(url_rss)
        
        for entrada in feed.entries[:1]: # Coleta a notícia mais quente de cada região
            if entrada.link in links_existentes:
                continue
                
            status_txt.write(f"🤖 IA processando cobertura global de: *{nome_fonte}*")
            
            resumo_cru = entrada.get('summary', entrada.get('description', ''))
            status, motivo = classificar_sensibilidade(entrada.title, resumo_cru)
            dados_ia = pipeline_escrita_ia(entrada.title, resumo_cru, entrada.link, nome_fonte)
            
            if dados_ia:
                nova_noticia = {
                    "id": len(banco_atual) + 1,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "fonte_origem": nome_fonte,
                    "link_origem": entrada.link,
                    "status": status,
                    "motivo_retencao": motivo,
                    **dados_ia
                }
                banco_atual.append(nova_noticia)
                com_sucesso += 1
        
        progresso.progress((i + 1) / total_fontes)
        
    status_txt.empty()
    
    if com_sucesso > 0:
        salvar_dados_permanentes(banco_atual)
        st.session_state.banco_noticias = banco_atual
        st.success(f"Sucesso! {com_sucesso} agências globais integradas ao feed!")
        st.rerun()
    else:
        st.info("Nenhuma matéria inédita nas agências mundiais neste exato segundo.")

# Abas Administrativas e Públicas
aba_publicadas, aba_retidas, aba_visualizacao_site = st.tabs([
    "🟢 Feed de Monitoramento (Automáticas/Aprovadas)", 
    "🟠 Mesa de Edição (Retidas pelo Guardrail)", 
    "💻 Visualização do Site (Como o Público Vê)"
])

with aba_publicadas:
    st.subheader("Fila de Distribuição de Conteúdo")
    noticias_ok = [n for n in st.session_state.banco_noticias if n['status'] == 'APROVADO']
    if not noticias_ok:
        st.info("Aguardando novas entradas automáticas desimpedidas.")
    else:
        df = pd.DataFrame(noticias_ok)[['id', 'data', 'fonte_origem', 'titulo_pt']]
        st.dataframe(df, use_container_width=True)

with aba_retidas:
    st.subheader("Mesa de Triagem Crítica (Filtros de Segurança)")
    noticias_retidas = [n for n in st.session_state.banco_noticias if n['status'] == 'RETIDO']
    
    if not noticias_retidas:
        st.success("Nenhum alerta de segurança ou sensibilidade ativo.")
    else:
        for noti in noticias_retidas:
            with st.expander(f"⚠️ FILTRO ATIVO: {noti['titulo_pt']} ({noti['fonte_origem']})"):
                st.warning(f"**Gatilho Identificado:** {noti['motivo_retencao']}")
                novo_titulo = st.text_input("Ajustar Título Editorial", noti['titulo_pt'], key=f"t_{noti['id']}")
                novo_texto = st.text_area("Ajustar Texto Editorial", noti['texto_pt'], key=f"x_{noti['id']}")
                
                col1, col2, col3 = st.columns(3)
                if col1.button("✅ Publicar Matéria", key=f"ap_{noti['id']}"):
                    noti['status'] = 'APROVADO'
                    noti['titulo_pt'] = novo_titulo
                    noti['texto_pt'] = novo_texto
                    salvar_dados_permanentes(st.session_state.banco_noticias)
                    st.rerun()
                if col2.button("🔓 Ignorar Alerta", key=f"f_{noti['id']}"):
                    noti['status'] = 'APROVADO'
                    salvar_dados_permanentes(st.session_state.banco_noticias)
                    st.rerun()
                if col3.button("❌ Arquivar", key=f"d_{noti['id']}"):
                    st.session_state.banco_noticias.remove(noti)
                    salvar_dados_permanentes(st.session_state.banco_noticias)
                    st.rerun()

# --- EXIBIÇÃO FORMATADA COMO JORNAL REAL ---
with aba_visualizacao_site:
    st.markdown("<h1 style='text-align: center; color: #1e3a8a; font-family: Georgia, serif; font-size: 3rem;'>horizont.news</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; color: #6b7280;'>A cobertura geopolítica global descentralizada</p>", unsafe_allow_html=True)
    st.write("---")
    
    idioma_selecionado = st.radio("Selecione a Edição Global / Language", ["Português", "English", "Español"], horizontal=True)
    lang_code = "pt" if idioma_selecionado == "Português" else "en" if idioma_selecionado == "English" else "es"

    noticias_para_exibir = [n for n in st.session_state.banco_noticias if n['status'] == 'APROVADO']
    
    if not noticias_para_exibir:
        st.info("Nenhum artigo publicado no feed público ainda. Forneça a API Key ou clique em 'Capturar' para iniciar o feed permanente.")
    else:
        for n in reversed(noticias_para_exibir):
            st.markdown(f"<h2 style='color: #1e3a8a; font-family: Georgia, serif; line-height: 1.3;'>{n[f'titulo_{lang_code}']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #b45309; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;'>🌐 AGÊNCIA EMISSORA: {n['fonte_origem']} | 📅 DATA DE CHEGADA: {n['data']}</p>", unsafe_allow_html=True)
            
            # Formatação refinada de parágrafos para o público geral
            paragrafos = n[f'texto_{lang_code}'].split("\n\n")
            for parágrafo in paragrafos:
                if parágrafo.strip():
                    st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.6; text-align: justify; font-family: sans-serif; color: #1f2937;'>{parágrafo}</p>", unsafe_allow_html=True)
            
            st.markdown("<div style='display: flex; gap: 15px; margin-top: 10px;'><span style='cursor:pointer;'>👍 Útil</span> | <span style='cursor:pointer;'>🔥 Relevante</span> | <span style='cursor:pointer;'>🧠 Neutro</span></div>", unsafe_allow_html=True)
            st.markdown("<hr style='border: 0; border-top: 1px solid #e5e7eb; margin: 25px 0;' />", unsafe_allow_html=True)
