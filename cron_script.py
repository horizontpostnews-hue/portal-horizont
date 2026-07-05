import os
import json
import feedparser
import google.generativeai as genai
from datetime import datetime

# Configuração da API do Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Dicionário de fontes RSS de geopolítica e notícias internacionais
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
    Você é um tradutor e jornalista sênior internacional. Receba a notícia em inglês e retorne STRICTLY um objeto JSON estruturado.
    
    Notícia original:
    Título: {titulo_org}
    Texto: {texto_org}
    
    Retorne exatamente este modelo JSON (Não adicione markdown ou blocos de código ```json):
    {{
        "titulo_pt": "Tradução jornalística impecável do título para o Português",
        "texto_pt": "Resumo analítico focado em geopolítica da notícia em Português com até 3 parágrafos",
        "titulo_en": "{titulo_org}",
        "texto_en": "Um resumo curto de 2 linhas em inglês da notícia",
        "titulo_es": "Tradução jornalística do título para o Espanhol",
        "texto_es": "Resumo analítico focado em geopolítica da notícia em Espanhol"
    }}
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text.strip())
    except Exception as e:
        print(f"Erro na API Gemini: {e}")
        # Retorna estrutura de segurança em português caso a API falhe, evitando dados nulos
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
        if cont_processadas >= 4: # Limita a 4 notícias por rodada para evitar estouro de limite de tempo
            break
            
        feed = feedparser.parse(url_rss)
        
        for entry in feed.entries[:3]: # Analisa as 3 mais recentes de cada fonte
            link = entry.link
            if link in links_existentes:
                continue
                
            print(f"Processando nova matéria de: {nome_fonte}")
            titulo_original = entry.title
            texto_original = entry.get("summary", entry.get("description", ""))
            
            # Chama a inteligência artificial para estruturar e traduzir os idiomas
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
        print(f"Sucesso! {len(novas_noticias)} novas matérias traduzidas adicionadas.")
    else:
        print("Nenhuma notícia nova encontrada nas agências mundiais.")

if __name__ == "__main__":
    rodar_robo()
