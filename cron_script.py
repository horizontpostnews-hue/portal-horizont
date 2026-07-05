import os
import json
import feedparser
import google.generativeai as genai
from datetime import datetime
import re

# ==========================================
# 1. CONFIGURAÇÕES E MAPA MUNDIAL DE FONTES
# ==========================================
API_KEY = os.getenv("GEMINI_API_KEY")

# Validação inicial da chave para evitar falhas críticas de Bad Request (400)
CHAVE_VALIDA = False
if API_KEY and len(API_KEY.strip()) > 10:
    try:
        genai.configure(api_key=API_KEY.strip())
        CHAVE_VALIDA = True
    except:
        CHAVE_VALIDA = False

ARQUIVO_BANCO = "banco_noticias.json"

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
# 2. FUNÇÕES EDITORIAIS E LIMPEZA DE TEXTO
# ==========================================
def carregar_banco():
    if os.path.exists(ARQUIVO_BANCO):
        try:
            with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def salvar_banco(dados):
    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def classificar_sensibilidade(titulo, texto):
    conteudo = (titulo + " " + texto).lower()
    for termo in TERMOS_SENSIVEIS:
        if termo in conteudo:
            return "RETIDO", f"Contém termo sensível: '{termo}'"
    return "APROVADO", "Seguro para publicação automática"

def limpar_html(texto_html):
    if not texto_html:
        return ""
    texto_limpo = re.sub('<[^<]+?>', '', texto_html)
    return texto_limpo.strip()

def motor_fallback_real(titulo, resumo_original, fonte_nome):
    texto_extraido = limpar_html(resumo_original)
    if not texto_extraido or len(texto_extraido) < 15:
        texto_extraido = f"Novos desdobramentos importantes foram despachados diretamente pela central de correspondentes da agência {fonte_nome}."

    return {
        "titulo_pt": f"{titulo}",
        "texto_pt": f"{texto_extraido}\n\n*Nota: Transmissão direta da agência parceira por indisponibilidade de IA.*",
        "titulo_en": f"Global News: {titulo}",
        "texto_en": f"{texto_extraido}\n\n*Note: Direct agency wire transmission due to IA fallback.*",
        "titulo_es": f"Reporte: {titulo}",
        "texto_es": f"{texto_extraido}\n\n*Nota: Transmisión directa desde la agencia de origen.*"
    }

def pipeline_gemini(titulo_original, resumo_original, link_original, fonte_nome):
    if not CHAVE_VALIDA:
        return motor_fallback_real(titulo_original, resumo_original, fonte_nome)
        
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        texto_base = limpar_html(resumo_original)
        
        prompt = f"""
        Você é o redator-chefe do portal internacional horizont.news.
        Com base no título "{titulo_original}" e no fato coletado: "{texto_base}" da fonte {fonte_nome}.
        Escreva uma matéria jornalística aprofundada (mínimo 3 parágrafos).
        Gere três versões completas e traduzidas: português, inglês e espanhol.
        
        Retorne RIGOROSAMENTE apenas um JSON limpo:
        {{
            "titulo_pt": "Manchete em português",
            "texto_pt": "Corpo da notícia em português",
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
        
    credito = f"\n\n*Este artigo foi estruturado pela redação horizont.news, com dados analíticos de {fonte_nome}. [Leia o despacho original]({link_original}).*"
    for idioma in ['pt', 'en', 'es']:
        dados[f'texto_{idioma}'] += credito
    return dados

# ==========================================
# 3. EXECUÇÃO DA ROTINA
# ==========================================
def executar_captura():
    print("Iniciando rotina geopolítica global...")
    banco_atual = carregar_banco()
    links_existentes = {n['link_origem'] for n in banco_atual}
    novos_artigos = 0
    
    for nome_fonte, url_rss in FONTES_RSS.items():
        try:
            feed = feedparser.parse(url_rss)
            for entrada in feed.entries[:1]:
                if entrada.link in links_existentes:
                    continue
                    
                resumo_cru = entrada.get('summary', entrada.get('description', ''))
                status, motivo = classificar_sensibilidade(entrada.title, resumo_cru)
                dados_ia = pipeline_gemini(entrada.title, resumo_cru, entrada.link, nome_fonte)
                
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
                    links_existentes.add(entrada.link)
                    novos_artigos += 1
        except Exception as e:
            print(f"Erro ao ler a fonte {nome_fonte}: {e}")
                
    if novos_artigos > 0:
        salvar_banco(banco_atual)
        print(f"Sucesso! {novos_artigos} artigos integrados permanentemente.")
    else:
        print("Nenhum fato inédito encontrado nesta rodada.")

if __name__ == "__main__":
    executar_captura()
