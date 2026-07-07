import os
import json
import feedparser
import re
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from datetime import datetime

# 1. FONTES ESTRANGEIRAS QUE DEVEM PREDOMINAR (Conforme regiões solicitadas)
FONTES_INTERNACIONAIS = {
    "Al Jazeera (Oriente Médio)": {
        "url": "https://www.aljazeera.com/xml/rss/all.xml", "categoria": "Política", "subcategoria": "Ásia Ocidental", 
        "img_backup": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=600"
    },
    "RT News (Rússia/Leste Europeu)": {
        "url": "https://actualidad.rt.com/feeds/all.xml", "categoria": "Política", "subcategoria": "Europa Oriental", 
        "img_backup": "https://images.unsplash.com/photo-1513326738677-b964603b136d?w=600"
    },
    "BBC News (Reino Unido)": {
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml", "categoria": "Política", "subcategoria": "Reino Unido", 
        "img_backup": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600"
    },
    "Xinhua Net (China)": {
        "url": "http://www.xinhuanet.com/english/rss/worldrss.xml", "categoria": "Economia", "subcategoria": "China", 
        "img_backup": "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=600"
    },
    "Deutsche Welle (União Europeia)": {
        "url": "https://rss.dw.com/rdf/rss_de_all", "categoria": "Economia", "subcategoria": "União Europeia", 
        "img_backup": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600"
    },
    "Associated Press (EUA)": {
        "url": "https://apnews.com/apf-topnews?format=rss", "categoria": "Política", "subcategoria": "EUA", 
        "img_backup": "https://images.unsplash.com/photo-1541185933-ef5d8ed016c2?w=600"
    },
    "CBC News (Canadá)": {
        "url": "https://rss.cbc.ca/lineup/world.xml", "categoria": "Cotidiano", "subcategoria": "Canadá", 
        "img_backup": "https://images.unsplash.com/photo-1507608869274-d3177c8bb4c7?w=600"
    },
    "Aristegui Noticias (México)": {
        "url": "https://aristeguinoticias.com/feed/", "categoria": "Cotidiano", "subcategoria": "México", 
        "img_backup": "https://images.unsplash.com/photo-1512813583145-baaa340ef29f?w=600"
    },
    "Telesur (Chile/América Latina)": {
        "url": "https://www.telesurtv.net/rss/RssAll.html", "categoria": "Cultura & Pop", "subcategoria": "Chile", 
        "img_backup": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=600"
    },
    "NHK World (Japão)": {
        "url": "https://www3.nhk.or.jp/nhkworld/nhknews/rss/index.xml", "categoria": "Tech & Ciência", "subcategoria": "Japão", 
        "img_backup": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=600"
    }
}

# 2. FONTES NACIONAIS BRASILEIRAS (Equilíbrio Plural e Pleno)
FONTES_NACIONAIS = {
    # Hegemônicas / Grandes Agências
    "Poder 360": {
        "url": "https://www.poder360.com.br/feed/", "categoria": "Política", "subcategoria": "Nacional",
        "img_backup": "https://images.unsplash.com/photo-1540910419892-4a36d2c3266c?w=600"
    },
    "Jornal do Commercio (PE)": {
        "url": "https://jc.ne10.uol.com.br/rss/", "categoria": "Economia", "subcategoria": "Pernambuco",
        "img_backup": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=600"
    },
    "Diário de Pernambuco": {
        "url": "https://www.diariodepernambuco.com.br/rss", "categoria": "Cotidiano", "subcategoria": "Pernambuco",
        "img_backup": "https://images.unsplash.com/photo-1569336415962-a4bd9f69cd83?w=600"
    },
    "Tribuna do Norte (RN)": {
        "url": "https://www.tribunadonorte.com.br/feed/", "categoria": "Cotidiano", "subcategoria": "Rio Grande do Norte",
        "img_backup": "https://images.unsplash.com/photo-1566241477600-ac026ad43874?w=600"
    },
    # Não Hegemônicas / Alternativas / Independentes
    "Brasil 247": {
        "url": "https://www.brasil247.com/feed", "categoria": "Política", "subcategoria": "Alternativa",
        "img_backup": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600"
    },
    "Jornal GGN": {
        "url": "https://jornalggn.com.br/feed/", "categoria": "Política", "subcategoria": "Alternativa",
        "img_backup": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600"
    },
    "Opera Mundi": {
        "url": "https://operamundi.uol.com.br/rss", "categoria": "Política", "subcategoria": "Internacional",
        "img_backup": "https://images.unsplash.com/photo-1554415707-6e8cfc93fe23?w=600"
    },
    "Outras Palavras": {
        "url": "https://outraspalavras.net/feed/", "categoria": "Cultura & Pop", "subcategoria": "Alternativa",
        "img_backup": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600"
    },
    "Viomundo": {
        "url": "https://www.viomundo.com.br/feed", "categoria": "Cotidiano", "subcategoria": "Alternativa",
        "img_backup": "https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?w=600"
    },
    "Jeduca": {
        "url": "https://jeduca.org.br/rss", "categoria": "Tech & Ciência", "subcategoria": "Educação",
        "img_backup": "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=600"
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

def limpar_html_e_lixo(texto):
    if not texto:
        return ""
    texto_limpo = re.sub(r'<[^<]+?>', '', str(texto))
    texto_limpo = re.sub(r'http\s*\S+|www\.\S+', '', texto_limpo)
    texto_limpo = " ".join(texto_limpo.split())
    return texto_limpo.strip()

def extrair_dados_da_pagina(url_da_noticia, url_backup):
    dados = {"resumo": "", "url_imagem": ""}
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        resposta = requests.get(url_da_noticia, headers=headers, timeout=8)
        
        if resposta.status_code == 200:
            sopa = BeautifulSoup(resposta.content, 'html.parser')
            for lixo in sopa(["script", "style", "nav", "footer", "header", "aside", "form"]):
                lixo.extract()
                
            paragrafos = sopa.find_all('p')
            texto_lista = []
            for p in paragrafos:
                txt = p.get_text().strip()
                if len(txt) > 35 and not any(x in txt.lower() for x in ["javascript", "cookie", "copyright", "termos de uso", "assine"]):
                    texto_lista.append(txt)
            
            texto_completo = " ".join(texto_lista)
            texto_final = limpar_html_e_lixo(texto_completo)
            
            if len(texto_final) >= 100:
                dados["resumo"] = texto_final[:1200] + "..."
                
            meta_img = sopa.find("meta", property="og:image") or sopa.find("meta", attrs={"name": "twitter:image"})
            if meta_img and meta_img.get("content"):
                url_det = meta_img["content"].strip()
                if url_det.startswith("http") and not any(x in url_det.lower() for x in ["logo", "fallback", "default", "avatar"]):
                    dados["url_imagem"] = url_det

    except Exception:
        pass
        
    if not dados["url_imagem"]:
        dados["url_imagem"] = url_backup
    return dados

def traduzir_noticia(titulo_org, texto_org, resumo_longo_org):
    try:
        tradutor_pt = GoogleTranslator(source='auto', target='pt')
        tradutor_es = GoogleTranslator(source='auto', target='es')
        tradutor_en = GoogleTranslator(source='auto', target='en')
        
        titulo_pt = tradutor_pt.translate(titulo_org)
        texto_pt = tradutor_pt.translate(texto_org)
        resumo_pt = tradutor_pt.translate(resumo_longo_org) if resumo_longo_org else texto_pt
        
        return {
            "titulo_pt": titulo_pt, "texto_pt": texto_pt,
            "titulo_en": tradutor_en.translate(titulo_org), "texto_en": tradutor_en.translate(texto_org),
            "titulo_es": tradutor_es.translate(titulo_org), "texto_es": tradutor_es.translate(texto_org),
            "resumo_longo": resumo_pt 
        }
    except Exception:
        return {
            "titulo_pt": titulo_org, "texto_pt": texto_org,
            "titulo_en": titulo_org, "texto_en": texto_org,
            "titulo_es": titulo_org, "texto_es": texto_org,
            "resumo_longo": resumo_longo_org if resumo_longo_org else texto_org
        }

def rodar_robo():
    banco_atual = ler_banco()
    links_existentes = {item.get("link_origem") for item in banco_atual if isinstance(item, dict)}
    novas_noticias = []
    
    # REGRA DE PROPORÇÃO: Coleta até 3 de cada fonte internacional (Predomínio) e 1 de cada nacional (Equilíbrio)
    processador_fontes = [
        {"dicionario": FONTES_INTERNACIONAIS, "limite_por_fonte": 3, "tipo": "Global"},
        {"dicionario": FONTES_NACIONAIS, "limite_por_fonte": 1, "tipo": "Nacional"}
    ]
    
    for bloco in processador_fontes:
        for nome_fonte, dados_fonte in bloco["dicionario"].items():
            try:
                feed = feedparser.parse(dados_fonte["url"])
                coletadas_da_fonte = 0
                
                for entry in feed.entries:
                    if coletadas_da_fonte >= bloco["limite_por_fonte"]:
                        break
                        
                    link = entry.get("link", "")
                    if not link or link in links_existentes:
                        continue
                        
                    titulo_original = entry.get("title", "")
                    resumo_cru = entry.get("summary", entry.get("description", ""))
                    texto_original = limpar_html_e_lixo(resumo_cru)
                    
                    print(f"[{bloco['tipo']}] Mapeando: {nome_fonte} -> {titulo_original[:40]}...")
                    
                    dados_pagina = extrair_dados_da_pagina(link, dados_fonte["img_backup"])
                    resumo_final = dados_pagina["resumo"] if dados_pagina["resumo"] else texto_original
                    
                    dados_traduzidos = traduzir_noticia(titulo_original, texto_original, resumo_final)
                    
                    item_noticia = {
                        "id": len(banco_atual) + len(novas_noticias) + 1,
                        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "fonte_origem": nome_fonte,
                        "categoria": dados_fonte["categoria"],
                        "subcategoria": dados_fonte["subcategoria"],
                        "link_origem": link,
                        "url_imagem": dados_pagina["url_imagem"],
                        "status": "APROVADO",
                        **dados_traduzidos
                    }
                    
                    novas_noticias.append(item_noticia)
                    links_existentes.add(link)
                    coletadas_da_fonte += 1
                    
            except Exception as e:
                print(f"Erro na fonte {nome_fonte}: {e}")
                
    if novas_noticias:
        banco_atual.extend(novas_noticias)
        # Mantém até 150 notícias rodando para preservar a diversidade e a performance
        banco_atual = banco_atual[-150:] 
        salvar_banco(banco_atual)
        print(f"Sucesso! {len(novas_noticias)} matérias mescladas e integradas de forma equilibrada.")
    else:
        print("Nenhuma nova inserção necessária.")

if __name__ == "__main__":
    rodar_robo()
