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
    if not texto:
        return ""
    # Remove tags HTML de links ou imagens que possam vir sujas no resumo
    return re.sub('<[^<]+?>', '', str(texto)).strip()

def traduzir_noticia(titulo_org, texto_org):
    try:
        # PROTEÇÃO 1: Evita que o tradutor trave se a notícia não tiver texto
        if not titulo_org: titulo_org = "Sem título"
        if not texto_org: texto_org = "Sem descrição disponível."
        
        # PROTEÇÃO 2: Força a origem como Inglês ('en') para evitar que a detecção falhe
        tradutor_pt = GoogleTranslator(source='en', target='pt')
        tradutor_es = GoogleTranslator(source='en', target='es')
        
        titulo_pt = tradutor_pt.translate(titulo_org)
        texto_pt = tradutor_pt.translate(texto_org)
        
        titulo_es = tradutor_es.translate(titulo_org)
        texto_es = tradutor_es.translate(texto_org)
        
        return {
            "titulo_pt": titulo_pt, "texto_pt": texto_pt,
            "titulo_en": titulo_org, "texto_en": texto_org,
            "titulo_es": titulo_es, "texto_es": texto_es
        }
    except Exception as e:
        print(f"Erro no tradutor: {e}")
        # Se a tradução falhar, retorna o texto original com aviso em vez de quebrar o site
        return {
            "titulo_pt": f"⚠️ [Erro na Tradução] {titulo_org}", "texto_pt": str(e),
            "titulo_en": titulo_org, "texto_en": texto_org,
            "titulo_es": f"⚠️ [Error de Traducción] {titulo_org}", "texto_es": str(e)
        }

def rodar_robo():
    banco_atual = ler_banco()
    links_existentes = {item.get("link_origem") for item in banco_atual}
    novas_noticias = []
    
    cont_processadas = 0
    for nome_fonte, url_rss in FONTES_RSS.items():
        if cont_processadas >= 4:
            break
            
        try:
            feed = feedparser.parse(url_rss)
            for entry in feed.entries[:3]:
                link = entry.get("link", "")
                if not link or link in links_existentes:
                    continue
                    
                titulo_original = entry.get("title", "")
                resumo_cru = entry.get("summary", entry.get("description", ""))
                texto_original = limpar_html(resumo_cru)
                
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
        except Exception as erro_fonte:
            # PROTEÇÃO 3: Se uma fonte inteira cair, o robô pula para a próxima sem travar
            print(f"Erro ao processar a fonte {nome_fonte}: {erro_fonte}")
                
    if novas_noticias:
        banco_atual.extend(novas_noticias)
        salvar_banco(banco_atual)
        print(f"Sucesso! {len(novas_noticias)} matérias processadas.")
    else:
        print("Nenhuma notícia nova encontrada.")

if __name__ == "__main__":
    rodar_robo()
