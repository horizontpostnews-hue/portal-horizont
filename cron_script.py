import os
import json
import feedparser
import re
from deep_translator import GoogleTranslator
from datetime import datetime

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

def limpar_html(texto):
    # Remove tags HTML de links ou imagens que possam vir sujas no resumo
    return re.sub('<[^<]+?>', '', texto).strip()

def traduzir_noticia(titulo_org, texto_org):
    try:
        # Traduzindo diretamente para o Português do Brasil
        titulo_pt = GoogleTranslator(source='auto', target='pt').translate(titulo_org)
        texto_pt = GoogleTranslator(source='auto', target='pt').translate(texto_org)
        
        # Traduzindo diretamente para o Espanhol
        titulo_es = GoogleTranslator(source='auto', target='es').translate(titulo_org)
        texto_es = GoogleTranslator(source='auto', target='es').translate(texto_org)
        
        return {
            "titulo_pt": titulo_pt,
            "texto_pt": texto_pt,
            "titulo_en": titulo_org,
            "texto_en": texto_org,
            "titulo_es": titulo_es,
            "texto_es": texto_es
        }
    except Exception as e:
        print(f"Erro no tradutor: {e}")
        return {
            "titulo_pt": titulo_org, "texto_pt": texto_org,
            "titulo_en": titulo_org, "texto_en": texto_org,
            "titulo_es": titulo_org, "texto_es": texto_org
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
            texto_original = limpar_html(entry.get("summary", entry.get("description", "")))
            
            dados_traduzidos = traduzir_noticia(titulo_original, texto_original)
            
            item_noticia = {
                "id": len(banco_atual) + len(novas_noticias) + 1,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "fonte_origem": nome_fonte,
                "link_origem": link,
                "status": "APROVADO",
                **dados_traduzidos
            }
            
            novas_noticias.append(item_noticia)
            cont_processadas += 1
            if cont_processadas >= 4:
                break
                
    if novas_noticias:
        banco_atual.extend(novas_noticias)
        salvar_banco(banco_atual)
        print("Tradução e salvamento concluídos com sucesso!")

if __name__ == "__main__":
    rodar_robo()
