import os
import json
import feedparser
from datetime import datetime
import re

# Nova importação imune a conflitos de pacotes
try:
    import google.generativeai as genai
    CHAVE_VALIDA = True
except Exception:
    CHAVE_VALIDA = False

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY and len(API_KEY.strip()) > 10 and CHAVE_VALIDA:
    try:
        genai.configure(api_key=API_KEY.strip())
    except:
        CHAVE_VALIDA = False
else:
    CHAVE_VALIDA = False

ARQUIVO_BANCO = "banco_noticias.json"

FONTES_RSS = {
    "Al Jazeera (Oriente Médio)": "https://www.aljazeera.com/xml/rss/all.xml",
    "NHK World (Japão)": "https://www3.nhk.or.jp/nhkworld/nhknewsline/rss/index.xml",
    "BBC News (Reino Unido)": "http://feeds.bbci.co.uk/news/world/rss.xml"
}

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

def limpar_html(texto_html):
    if not texto_html:
        return ""
    return re.sub('<[^<]+?>', '', texto_html).strip()

def motor_fallback(titulo, resumo_original, fonte_nome):
    texto = limpar_html(resumo_original) if resumo_original else "Novos desdobramentos despachados pela central de correspondentes."
    return {
        "titulo_pt": f"[Direto] {titulo}",
        "texto_pt": f"{texto}\n\n*Transmissão direta da agência {fonte_nome}.*",
        "titulo_en": f"{titulo}",
        "texto_en": f"{texto}\n\n*Direct wire transmission.*",
        "titulo_es": f"{titulo}",
        "texto_es": f"{texto}\n\n*Transmisión directa.*"
    }

def pipeline_gemini(titulo_original, resumo_original, link_original, fonte_nome):
    if not CHAVE_VALIDA:
        return motor_fallback(titulo_original, resumo_original, fonte_nome)
        
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        texto_base = limpar_html(resumo_original)
        
        prompt = f"""
        Você é o redator do portal horizont.news. Com base no fato: "{texto_base}" da fonte {fonte_nome},
        escreva uma matéria jornalística simples (2 parágrafos).
        Retorne APENAS um JSON limpo, sem markdown adicionais:
        {{
            "titulo_pt": "{titulo_original}",
            "texto_pt": "Texto em português",
            "titulo_en": "{titulo_original}",
            "texto_en": "Texto em inglês",
            "titulo_es": "{titulo_original}",
            "texto_es": "Texto em espanhol"
        }}
        """
        response = model.generate_content(prompt)
        texto_puro = response.text.strip()
        
        if "```json" in texto_puro:
            texto_puro = texto_puro.split("```json")[1].split("```")[0].strip()
        elif "```" in texto_puro:
            texto_puro = texto_puro.split("```")[1].split("```")[0].strip()
            
        dados = json.loads(texto_puro)
    except:
        dados = motor_fallback(titulo_original, resumo_original, fonte_nome)
        
    for idioma in ['pt', 'en', 'es']:
        dados[f'texto_{idioma}'] += f"\n\n* Fonte original: {fonte_nome} - [Acesse o link]({link_original}) *"
    return dados

def executar_captura():
    print("Iniciando varredura rápida global...")
    banco_atual = carregar_banco()
    links_existentes = {n.get('link_origem') for n in banco_atual if 'link_origem' in n}
    novos_artigos = 0
    
    for nome_fonte, url_rss in FONTES_RSS.items():
        try:
            feed = feedparser.parse(url_rss)
            if not feed.entries:
                continue
                
            entrada = feed.entries[0]
            if entrada.link in links_existentes:
                continue
                
            resumo_cru = entrada.get('summary', entrada.get('description', ''))
            dados_ia = pipeline_gemini(entrada.title, resumo_cru, entrada.link, nome_fonte)
            
            if dados_ia:
                nova_noticia = {
                    "id": len(banco_atual) + 1,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "fonte_origem": nome_fonte,
                    "link_origem": entrada.link,
                    "status": "APROVADO",
                    "motivo_retencao": "Seguro",
                    **dados_ia
                }
                banco_atual.append(nova_noticia)
                novos_artigos += 1
                
        except Exception as e:
            print(f"Erro na fonte {nome_fonte}: {e}")
                
    if novos_artigos > 0:
        salvar_banco(banco_atual)
        print(f"Sucesso! {novos_artigos} novas notícias inseridas.")
    else:
        print("Nenhuma novidade encontrada nesta rodada.")

if __name__ == "__main__":
    executar_captura()
