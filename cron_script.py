import os
import json
import feedparser
import google.generativeai as genai
from datetime import datetime

# Configuração da API do Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

FONTES_RSS = {
    "Al Jazeera (Oriente Médio)": "https://www.aljazeera.com/xml/rss/all.xml",
    "BBC News (Reino Unido)": "https://feeds.bbci.co.uk/news/world/rss.xml"
}

ARQUIVO_BANCO = "banco_noticias.json"

def ler_banco():
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

def traduzir_e_resumir(titulo_org, texto_org):
    prompt = f"""
    Você é um tradutor e jornalista. 
    Traduza e resuma a notícia abaixo.
    Título original: {titulo_org}
    Texto original: {texto_org}
    
    Retorne EXATAMENTE este formato JSON (sem crases de formatação Markdown):
    {{
        "titulo_pt": "Título em português",
        "texto_pt": "Resumo em português (2 parágrafos)",
        "titulo_en": "{titulo_org}",
        "texto_en": "Resumo em inglês",
        "titulo_es": "Título em espanhol",
        "texto_es": "Resumo em espanhol"
    }}
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Limpeza pesada caso o Gemini retorne o JSON sujo com crases
        texto_limpo = response.text.strip()
        if texto_limpo.startswith("```json"):
            texto_limpo = texto_limpo[7:-3].strip()
        elif texto_limpo.startswith("```"):
            texto_limpo = texto_limpo[3:-3].strip()
            
        return json.loads(texto_limpo)
    except Exception as e:
        print(f"Erro na IA: {e}")
        return {
            "titulo_pt": titulo_org,
            "texto_pt": texto_org,
            "titulo_en": titulo_org,
            "texto_en": texto_org,
            "titulo_es": titulo_org,
            "texto_es": texto_org
        }

def rodar_robo():
    banco_atual = ler_banco()
    links_existentes = {item.get("link_origem") for item in banco_atual}
    novas_noticias = []
    
    cont_processadas = 0
    
    for nome_fonte, url_rss in FONTES_RSS.items():
        if cont_processadas >= 4:
            break
            
        feed = feedparser.parse(url_rss)
        
        for entry in feed.entries[:3]:
            link = entry.link
            if link in links_existentes:
                continue
                
            titulo_original = entry.title
            texto_original = entry.get("summary", entry.get("description", ""))
            
            dados_traduzidos = traduzir_e_resumir(titulo_original, texto_original)
            
            item_noticia = {
                "id": len(banco_atual) + len(novas_noticias) + 1,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "fonte_origem": nome_fonte,
                "link_origem": link,
                "status": "APROVADO",
                "motivo_retencao": "Seguro",
                **dados_traduzidos
            }
            
            novas_noticias.append(item_noticia)
            cont_processadas += 1
            if cont_processadas >= 4:
                break
                
    if novas_noticias:
        banco_atual.extend(novas_noticias)
        salvar_banco(banco_atual)
        print(f"Sucesso! {len(novas_noticias)} inseridas.")

if __name__ == "__main__":
    rodar_robo()
