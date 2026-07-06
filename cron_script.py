import os
import json
import feedparser
import re
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from datetime import datetime

# Mapeamento de Fontes Mundiais e suas Categorias e Subcategorias
FONTES_RSS = {
    "Al Jazeera (Oriente Médio)": {"url": "https://www.aljazeera.com/xml/rss/all.xml", "categoria": "Política", "subcategoria": "Ásia Ocidental", "termo_img": "middle east politics"},
    "RT News (Rússia/Leste Europeu)": {"url": "https://actualidad.rt.com/feeds/all.xml", "categoria": "Política", "subcategoria": "Europa Oriental", "termo_img": "russia"},
    "BBC News": {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "categoria": "Política", "subcategoria": "Internacional", "termo_img": "world news"},
    "Xinhua Net (China)": {"url": "http://www.xinhuanet.com/english/rss/worldrss.xml", "categoria": "Economia", "subcategoria": "Ásia Oriental", "termo_img": "china economy"},
    "Valor Econômico": {"url": "https://valor.globo.com/rss/valor/", "categoria": "Economia", "subcategoria": "Nacional", "termo_img": "finance"},
    "Infomoney": {"url": "https://www.infomoney.com.br/feed/", "categoria": "Economia", "subcategoria": "Mercado", "termo_img": "stock market"},
    "CBC News (Canadá)": {"url": "https://rss.cbc.ca/lineup/world.xml", "categoria": "Cotidiano", "subcategoria": "América do Norte", "termo_img": "canada"},
    "G1 Brasil": {"url": "https://g1.globo.com/rss/g1/brasil/", "categoria": "Cotidiano", "subcategoria": "Nacional", "termo_img": "brazil"},
    "Globo Esporte (GE)": {"url": "https://ge.globo.com/rss/ge/", "categoria": "Esportes", "subcategoria": "Futebol/Nacional", "termo_img": "soccer"},
    "UOL Esporte": {"url": "http://rss.uol.com.br/feed/esporte.xml", "categoria": "Esportes", "subcategoria": "Geral", "termo_img": "sports"},
    "Telesur (América Latina/Chile)": {"url": "https://www.telesurtv.net/rss/RssAll.html", "categoria": "Cultura & Pop", "subcategoria": "América do Sul", "termo_img": "latin america"},
    "Aristegui Noticias (México)": {"url": "https://aristeguinoticias.com/feed/", "categoria": "Cultura & Pop", "subcategoria": "América Central", "termo_img": "mexico"},
    "Omelete": {"url": "https://www.omelete.com.br/feed", "categoria": "Cultura & Pop", "subcategoria": "Cinema & Séries", "termo_img": "movie movie"},
    "UOL Entretenimento": {"url": "http://rss.uol.com.br/feed/entretenimento.xml", "categoria": "Cultura & Pop", "subcategoria": "Tendências", "termo_img": "pop culture"},
    "NHK World (Japão)": {"url": "https://www3.nhk.or.jp/nhkworld/nhknews/rss/index.xml", "categoria": "Tech & Ciência", "subcategoria": "Ásia Oriental", "termo_img": "japan technology"},
    "Canaltech": {"url": "https://canaltech.com.br/rss/", "categoria": "Tech & Ciência", "subcategoria": "Inovação", "termo_img": "technology"},
    "G1 Bem Estar": {"url": "https://g1.globo.com/rss/g1/saude/", "categoria": "Viver Bem", "subcategoria": "Saúde e Medicina", "termo_img": "health"}
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

def extrair_dados_da_pagina(url_da_noticia, termo_seguranca):
    dados = {"resumo": "Resumo longo indisponível para o layout desta fonte.", "url_imagem": ""}
    try:
        # Mimetiza perfeitamente um navegador real atualizado para furar os bloqueios de segurança
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
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
                
            # 2. Extração de Imagem Real
            meta_img = sopa.find("meta", property="og:image") or sopa.find("meta", attrs={"name": "twitter:image"})
            if meta_img and meta_img.get("content"):
                url_detectada = meta_img["content"].strip()
                if url_detectada.startswith("http"):
                    dados["url_imagem"] = url_detectada

    except Exception as e:
        print(f"Aviso de raspagem em {url_da_noticia}: {e}")
        
    # BACKUP INTELIGENTE ANTI-CAIXA-VAZIA: Se o site bloqueou ou não achou imagem, gera uma imagem jornalística dinâmica e única baseada na fonte/termo
    if not dados["url_imagem"]:
        hash_id = int(datetime.now().microsecond)
        dados["url_imagem"] = f"https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600&auto=format&fit=crop&q=60" # Foto padrão jornalismo caso falhe o termo
        if termo_seguranca:
            termo_url = termo_seguranca.replace(" ", "-")
            dados["url_imagem"] = f"https://source.unsplash.com/featured/600x400/?{termo_url}&sig={hash_id}"
            
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
        termo_img = dados_fonte.get("termo_img", "news")
            
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
                
                dados_pagina = extrair_dados_da_pagina(link, termo_img)
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
