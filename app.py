import streamlit as st
import feedparser
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import json
import os

# ==========================================
# 1. CONFIGURAÇÕES INICIAIS E MAPA MUNDIAL DE FONTES
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

# Novo ecossistema expandido com diversidade geopolítica e cultural
FONTES_RSS = {
    "Al Jazeera (Oriente Médio)": "https://www.aljazeera.com/xml/rss/all.xml",
    "NHK World (Japão)": "https://www3.nhk.or.jp/nhkworld/nhknewsline/rss/index.xml",
    "Xinhua Net (China)": "https://www.xinhuanet.com/english/rss/worldrss.xml",
    "RT News (Europa Oriental)": "https://www.rt.com/rss/news/",
    "El Universal (México)": "https://www.eluniversal.com.mx/world/rss.xml",
    "Clarín (Argentina)": "https://www.clarin.com/rss/mundo/",
    "CBC News (Canadá)": "https://rss.cbc.ca/lineup/world.xml",
    "G1 Globo (Brasil)": "https://g1.globo.com/rss/g1/",
    "BBC News (Reino Unido)": "http://feeds.bbci.co.uk/news/world/rss.xml"
}

TERMOS_SENSIVEIS = ['tragédia', 'crime', 'violência', 'morreu', 'assassinato', 'guerra', 'míssil', 'atentado', 'suicídio', 'mortes', 'acidente']

# ==========================================
# 2. MOTOR DE IA E GERAÇÃO RESTRUTURADA DE CONTEÚDO
# ==========================================

def classificar_sensibilidade(titulo, texto):
    conteudo = (titulo + " " + texto).lower()
    for termo in TERMOS_SENSIVEIS:
        if termo in conteudo:
            return "RETIDO", f"Contém termo sensível: '{termo}'"
    return "APROVADO", "Seguro para publicação automática"

def motor_traducao_local(titulo, fonte_nome):
    """Gera um artigo legível e limpo para o público caso a API fique offline"""
    return {
        "titulo_pt": f"{titulo}",
        "texto_pt": f"A agência de notícias {fonte_nome} enviou um despacho urgente informando novos desdobramentos sobre este caso na última hora. O bloco de correspondentes internacionais acompanha os impactos comerciais e políticos na região geográfica do ocorrido.",
        "titulo_en": f"Global Report: {titulo}",
        "texto_en": f"International agency {fonte_nome} dispatched urgent updates regarding this development. Global analysts are evaluating the immediate political and economic impacts across the affected territory.",
        "titulo_es": f"Reporte: {titulo}",
        "texto_es": f"La agencia de noticias {fonte_nome} emitió un despacho de última hora sobre este caso. Corresponsales internacionales analizan las implicaciones políticas y comerciales en la región."
    }

def pipeline_escrita_ia(titulo_original, link_original, fonte_nome):
    if not GEMINI_API_KEY:
        return motor_traducao_local(titulo_original, fonte_nome)
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Você é o redator-chefe do portal multilíngue horizont.news.
        Com base no fato coletado da fonte {fonte_nome}: "{titulo_original}".
        
        Escreva uma matéria jornalística proprietária, sem copiar a fonte.
        Gere três versões completas: uma em português, uma em inglês e uma em espanhol.
        
        Retorne RIGOROSAMENTE apenas um JSON limpo e válido:
        {{
            "titulo_pt": " Manchete atraente em português",
            "texto_pt": "Corpo da notícia completo e profissional em português (mínimo de 3 parágrafos)",
            "titulo_en": "Manchete em inglês",
            "texto_en": "Corpo da notícia em inglês (mínimo de 3 parágrafos)",
            "titulo_es": "Manchete em espanhol",
            "texto_es": "Corpo da notícia em espanhol (mínimo de 3 parágrafos)"
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
        dados = motor_traducao_local(titulo_original, fonte_nome)
        
    # Links e notas de transparência editorial
    credito = f"\n\n*Este artigo foi estruturado de forma independente pela redação horizont.news, com dados analíticos de {fonte_nome}. [Leia o documento original no veículo de origem]({link_original}).*"
    for idioma in ['pt', 'en', 'es']:
        dados[f'texto_{idioma}'] += credito
        
    return dados

# ==========================================
# 3. INTERFACE VISUAL (PAINEL + PORTAL DO PÚBLICO)
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
        
        # Pega a notícia mais fresca do topo de cada uma das 9 fontes mundiais
        for entrada in feed.entries[:1]:
            if entrada.link in links_existentes:
                continue
                
            status_txt.write(f"🤖 IA reescrevendo cobertura global de: *{nome_fonte}*")
            status, motivo = classificar_sensibilidade(entrada.title, entrada.get('description', ''))
            dados_ia = pipeline_escrita_ia(entrada.title, entrada.link, nome_fonte)
            
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
        st.success(f"Sucesso! {com_sucesso} correspondentes internacionais integrados ao banco!")
        st.rerun()
    else:
        st.info("Nenhum fato novo ou inédito detectado nos satélites de notícias neste minuto.")

# Estruturação de abas
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

# --- EXIBIÇÃO REAL DO SITE PARA O LEITOR ---
with aba_visualizacao_site:
    st.markdown("<h1 style='text-align: center; color: #1e3a8a; font-family: Georgia, serif;'>horizont.news</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; color: #6b7280;'>A perspectiva geopolítica global em tempo real</p>", unsafe_allow_html=True)
    st.write("---")
    
    idioma_selecionado = st.radio("Selecione a Edição Global / Language", ["Português", "English", "Español"], horizontal=True)
    lang_code = "pt" if idioma_selecionado == "Português" else "en" if idioma_selecionado == "English" else "es"

    noticias_para_exibir = [n for n in st.session_state.banco_noticias if n['status'] == 'APROVADO']
    
    if not noticias_para_exibir:
        st.info("Nenhum artigo publicado nas últimas horas no feed público.")
    else:
        # Exibe as notícias em formato jornalístico limpo de leitura
        for n in reversed(noticias_para_exibir):
            st.markdown(f"<h2 style='color: #1e3a8a; font-family: Georgia, serif;'>{n[f'titulo_{lang_code}']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #854d0e; font-size: 0.85rem; font-weight: bold;'>🌐 CANAL COBERTURA: {n['fonte_origem']} | 📅 REGISTRO: {n['data']}</p>", unsafe_allow_html=True)
            
            # Divide os parágrafos de texto para dar legibilidade de jornal de verdade
            paragrafos = n[f'texto_{lang_code}'].split("\n\n")
            for parágrafo in paragrafos:
                if parágrafo.strip():
                    st.write(parágrafo)
                    
            col_audio, col_emoji = st.columns([1, 1])
            with col_audio:
                st.caption("🔊 Ouvir esta cobertura por áudio")
            with col_emoji:
                st.write("Interagir: 👍 | 🔥 | 🧠")
            st.markdown("<hr style='border: 1px solid #e5e7eb;' />", unsafe_allow_html=True)
