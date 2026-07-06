import os
import json
import feedparser
import re
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from datetime import datetime

# Mapeamento de Fontes Mundiais e URLs estáticas e seguras de backup (Unsplash Imagens Reais)
FONTES_RSS = {
    "Al Jazeera (Oriente Médio)": {
        "url": "https://www.aljazeera.com/xml/rss/all.xml", "categoria": "Política", "subcategoria": "Ásia Ocidental", 
        "img_backup": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=600&auto=format&fit=crop&q=60"
    },
    "RT News (Rússia/Leste Europeu)": {
        "url": "https://actualidad.rt.com/feeds/all.xml", "categoria": "Política", "subcategoria": "Europa Oriental", 
        "img_backup": "https://images.unsplash.com/photo-1513326738677-b964603b136d?w=600&auto=format&fit=crop&q=60"
    },
    "BBC News": {
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml", "categoria": "Política", "subcategoria": "Internacional", 
        "img_backup": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600&auto=format&fit=crop&q=60"
    },
    "Xinhua Net (China)": {
        "url": "http://www.xinhuanet.com/english/rss/worldrss.xml", "categoria": "Economia", "subcategoria": "Ásia Oriental", 
        "img_backup": "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=600&auto=format&fit=crop&q=60"
    },
    "Valor Econômico": {
        "url": "https://valor.globo.com/rss/valor/", "categoria": "Economia", "subcategoria": "Nacional", 
        "img_backup": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=600&auto=format&fit=crop&q=60"
    },
    "Infomoney": {
        "url": "https://www.infomoney.com.br/feed/", "categoria": "Economia", "subcategoria": "Mercado", 
        "img_backup": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&auto=format&fit=crop&q=60"
    },
    "CBC News (Canadá)": {
        "url": "https://rss.cbc.ca/lineup/world.xml", "categoria": "Cotidiano", "subcategoria": "América do Norte", 
        "img_backup": "https://images.unsplash.com/photo-1507608869274-d3177c8bb4c7?w=600&auto=format&fit=crop&q=60"
    },
    "G1 Brasil": {
        "url": "https://g1.globo.com/rss/g1/brasil/", "categoria": "Cotidiano", "subcategoria": "Nacional", 
        "img_backup": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=600&auto=format&fit=crop&q=60"
    },
    "Globo Esporte (GE)": {
        "url": "https://ge.globo.com/rss/ge/", "categoria": "Esportes", "subcategoria": "Futebol/Nacional", 
        "img_backup": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=600&auto=format&fit=crop&q=60"
    },
    "UOL Esporte": {
        "url": "http://rss.uol.com.br/feed/esporte.xml", "categoria": "Esportes", "subcategoria": "Geral", 
        "img_backup": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&auto=format&fit=crop&q=60"
    },
    "Telesur (América Latina/Chile)": {
        "url": "https://www.telesurtv.net/rss/RssAll.html", "categoria": "Cultura & Pop", "subcategoria": "América do Sul", 
        "img_backup": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=600&auto=format&fit=crop&q=60"
    },
    "Aristegui Noticias (México)": {
        "url": "https://aristeguinoticias.com/feed/", "categoria": "Cultura & Pop", "subcategoria": "América Central", 
        "img_backup": "https://images.unsplash.com/photo-1512813583145-baaa340ef29f?w=600&auto=format&fit=crop&q=60"
    },
    "Omelete": {
        "url": "https://www.omelete.com.br/feed", "categoria": "Cultura & Pop", "subcategoria": "Cinema & Séries", 
        "img_backup": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=60"
    },
    "UOL Entretenimento": {
        "url": "http://rss.uol.com.br/feed/entretenimento.xml", "categoria": "Cultura & Pop", "subcategoria": "Tendências", 
        "img_backup": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&auto=format&fit=crop&q=60"
    },
    "NHK World (Japão)": {
        "url": "https://www3.nhk.or.jp/nhkworld/nhknews/rss/index.xml", "categoria": "Tech & Ciência", "subcategoria": "Ásia Oriental", 
        "img_backup": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=600&auto=format&fit=crop&q=60"
    },
    "Canaltech": {
        "url": "https://canaltech.com.br/rss/", "categoria": "Tech & Ciência", "subcategoria": "Inovação", 
        "img_backup": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop&q=60"
    },
    "G1 Bem Estar": {
        "url": "https://g1.globo.com/rss/g1/saude/", "categoria": "Viver Bem", "subcategoria": "Saúde e Medicina", 
        "img_backup": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&auto=format&fit=crop&q=60"
    }
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
    return re.sub('<[^<]+?>', '', str(texto)).strip()

def extrair_dados_da_pagina(url_da_noticia, url_backup):
    dados = {"resumo": "Resumo longo indisponível para o layout desta fonte.", "url_imagem": ""}
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        resposta = requests.get(url_da_noticia, headers=headers, timeout=10)
        
        if resposta.status_code == 200:
            sopa = BeautifulSoup(resposta.content, 'html.parser')
            
            # 1. Extração de texto
            paragrafos = sopa.find_all('p')
            texto_completo = " ".join([p.get_text().strip() for p in paragrafos])
            texto_limpo = " ".join(texto_completo.split())
            if len(texto_limpo) >= 50:
                dados["resumo"] = texto_limpo[:800] + "..."
                
            # 2. Extração de Imagem Real do Artigo
            meta_img = sopa.find("meta", property="og:image") or sopa.find("meta", attrs={"name": "twitter:image"})
            if meta_img and meta_img.get("content"):
                url_detectada = meta_img["content"].strip()
                if url_detectada.startswith("http") and not any(x in url_detectada.lower() for x in ["logo", "fallback", "default"]):
                    dados["url_imagem"] = url_detectada

    except Exception as e:
        print(f"Aviso de raspagem em {url_da_noticia}: {e}")
        
    # BACKUP SEGURO E ESTÁTICO: Evita links dinâmicos e redirecionamentos que quebram o Streamlit
    if not dados["url_imagem"]:
        dados["url_imagem"] = url_backup
            
    return dados

def traduzir_noticia(titulo_org, texto_org, resumo_longo_org):
    try:
        if not titulo_org: titulo_org = "Sem título"
        if not texto_org: texto_org = "Sem descrição disponível."
        
        tradutor_pt = GoogleTranslator(source='auto', target='pt')
        tradutor_es = GoogleTranslator(source='auto', target='es')
        tradutor_en = GoogleTranslator(source='auto', target='en')
        
        titulo_pt = tradutor_pt.translate(titulo_org)
        texto_pt = tradutor_pt.translate(texto_org)
        resumo_pt = tradutor_pt.translate(resumo_longo_org) if resumo_longo_org else texto_pt
        
        titulo_es = tradutor_es.translate(titulo_org)
        texto_es = tradutor_es.translate(texto_org)
        
        titulo_en = tradutor_en.translate(titulo_org)
        texto_en = tradutor_en.translate(texto_org)
        
        return {
            "titulo_pt": titulo_pt, "texto_pt": texto_pt,
            "titulo_en": titulo_en, "texto_en": texto_en,
            "titulo_es": titulo_es, "texto_es": texto_es,
            "resumo_longo": resumo_pt 
        }
    except Exception as e:
        return {
            "titulo_pt": titulo_org, "texto_pt": texto_org,
            "titulo_en": titulo_org, "texto_en": texto_org,
            "titulo_es": titulo_org, "texto_es": texto_org,
            "resumo_longo": resumo_longo_org if resumo_longo_org else texto_org
        }

def rodar_robo():
    banco_atual = ler_banco()
    links_existentes = {item.get("link_origem") for item in banco_atual}
    novas_noticias = []
    
    cont_processadas = 0
    for nome_fonte, dados_fonte in FONTES_RSS.items():
        if cont_processadas >= 25: 
            break
            
        url_rss = dados_fonte["url"]
        categoria = dados_fonte["categoria"]
        subcategoria = dados_fonte.get("subcategoria", "Geral")
        img_backup = dados_fonte["img_backup"]
            
        try:
            feed = feedparser.parse(url_rss)
            for entry in feed.entries[:1]:
                link = entry.get("link", "")
                if not link or link in links_existentes:
                    continue
                    
                titulo_original = entry.get("title", "")
                resumo_cru = entry.get("summary", entry.get("description", ""))
                texto_original = limpar_html(resumo_cru)
                
                print(f"Processando Global: {nome_fonte} | {categoria} > {subcategoria}...")
                
                dados_pagina = extrair_dados_da_pagina(link, img_backup)
                dados_traduzidos = traduzir_noticia(titulo_original, texto_original, dados_pagina["resumo"])
                
                item_noticia = {
                    "id": len(banco_atual) + len(novas_noticias) + 1,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "fonte_origem": nome_fonte,
                    "categoria": categoria,
                    "subcategoria": subcategoria,
                    "link_origem": link,
                    "url_imagem": dados_pagina["url_imagem"],
                    "status": "APROVADO",
                    **dados_traduzidos
                }
                
                novas_noticias.append(item_noticia)
                links_existentes.add(link)
                cont_processadas += 1
                
        except Exception as erro_fonte:
            print(f"Erro ao processar a fonte {nome_fonte}: {erro_fonte}")
                
    if novas_noticias:
        banco_atual.extend(novas_noticias)
        banco_atual = banco_atual[-150:] 
        salvar_banco(banco_atual)
        print(f"Sucesso! {len(novas_noticias)} matérias globais integradas.")
    else:
        print("Nenhuma notícia nova encontrada.")

if __name__ == "__main__":
    rodar_robo()
