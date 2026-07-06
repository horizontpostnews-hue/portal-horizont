import os
import json
import feedparser
import re
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from datetime import datetime

# Mapeamento de Fontes e suas Categorias e SUBCATEGORIAS
FONTES_RSS = {
    # ├── Política
    "Al Jazeera": {"url": "https://www.aljazeera.com/xml/rss/all.xml", "categoria": "Política", "subcategoria": "Geopolítica"},
    "BBC News": {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "categoria": "Política", "subcategoria": "Internacional"},
    
    # ├── Economia
    "Infomoney": {"url": "https://www.infomoney.com.br/feed/", "categoria": "Economia", "subcategoria": "Mercado"},
    "Valor Econômico": {"url": "https://valor.globo.com/rss/valor/", "categoria": "Economia", "subcategoria": "Negócios"},
    
    # ├── Cotidiano
    "G1 Brasil": {"url": "https://g1.globo.com/rss/g1/brasil/", "categoria": "Cotidiano", "subcategoria": "Nacional"},
    
    # ├── Esportes
    "Globo Esporte (GE)": {"url": "https://ge.globo.com/rss/ge/", "categoria": "Esportes", "subcategoria": "Futebol/Nacional"},
    "UOL Esporte": {"url": "http://rss.uol.com.br/feed/esporte.xml", "categoria": "Esportes", "subcategoria": "Geral"},
    
    # ├── Cultura & Pop
    "Omelete": {"url": "https://www.omelete.com.br/feed", "categoria": "Cultura & Pop", "subcategoria": "Cinema & Séries"},
    "UOL Entretenimento": {"url": "http://rss.uol.com.br/feed/entretenimento.xml", "categoria": "Cultura & Pop", "subcategoria": "Tendências"},
    
    # ├── Tech & Ciência
    "Canaltech": {"url": "https://canaltech.com.br/rss/", "categoria": "Tech & Ciência", "subcategoria": "Inovação"},
    
    # └── Viver Bem
    "G1 Bem Estar": {"url": "https://g1.globo.com/rss/g1/saude/", "categoria": "Viver Bem", "subcategoria": "Saúde e Medicina"}
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

def extrair_resumo_longo(url_da_noticia):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resposta = requests.get(url_da_noticia, headers=headers, timeout=15)
        sopa = BeautifulSoup(resposta.content, 'html.parser')
        paragrafos = sopa.find_all('p')
        texto_completo = " ".join([p.get_text().strip() for p in paragrafos])
        texto_limpo = " ".join(texto_completo.split())
        resumo_final = texto_limpo[:800]
        
        if len(resumo_final) < 50:
            return "Resumo longo indisponível para o layout desta fonte."
            
        return resumo_final + "..."
        
    except Exception as e:
        return "Instabilidade ao acessar a matéria completa na fonte original."

def traduzir_noticia(titulo_org, texto_org, resumo_longo_org):
    try:
        if not titulo_org: titulo_org = "Sem título"
        if not texto_org: texto_org = "Sem descrição disponível."
        if not resumo_longo_org: resumo_longo_org = "Sem resumo detalhado disponível."
        
        tradutor_pt = GoogleTranslator(source='auto', target='pt')
        tradutor_es = GoogleTranslator(source='auto', target='es')
        tradutor_en = GoogleTranslator(source='auto', target='en')
        
        titulo_pt = tradutor_pt.translate(titulo_org)
        texto_pt = tradutor_pt.translate(texto_org)
        resumo_pt = tradutor_pt.translate(resumo_longo_org)
        
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
        print(f"Erro no tradutor: {e}")
        return {
            "titulo_pt": f"⚠️ [Erro na Tradução] {titulo_org}", "texto_pt": str(e),
            "titulo_en": f"⚠️ [Translation Error] {titulo_org}", "texto_en": str(e),
            "titulo_es": f"⚠️ [Error de Traducción] {titulo_org}", "texto_es": str(e),
            "resumo_longo": resumo_longo_org
        }

def rodar_robo():
    banco_atual = ler_banco()
    links_existentes = {item.get("link_origem") for item in banco_atual}
    novas_noticias = []
    
    cont_processadas = 0
    for nome_fonte, dados_fonte in FONTES_RSS.items():
        if cont_processadas >= 12: 
            break
            
        url_rss = dados_fonte["url"]
        categoria = dados_fonte["categoria"]
        subcategoria = dados_fonte.get("subcategoria", "Geral") # <--- Puxando a nova subcategoria
            
        try:
            feed = feedparser.parse(url_rss)
            for entry in feed.entries[:1]:
                link = entry.get("link", "")
                if not link or link in links_existentes:
                    continue
                    
                titulo_original = entry.get("title", "")
                resumo_cru = entry.get("summary", entry.get("description", ""))
                texto_original = limpar_html(resumo_cru)
                
                print(f"Processando: {nome_fonte} | {categoria} > {subcategoria}...")
                
                texto_denso = extrair_resumo_longo(link)
                dados_traduzidos = traduzir_noticia(titulo_original, texto_original, texto_denso)
                
                item_noticia = {
                    "id": len(banco_atual) + len(novas_noticias) + 1,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "fonte_origem": nome_fonte,
                    "categoria": categoria,
                    "subcategoria": subcategoria, # <--- Salvando no banco
                    "link_origem": link,
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
        print(f"Sucesso! {len(novas_noticias)} matérias processadas e categorizadas.")
    else:
        print("Nenhuma notícia nova encontrada.")

if __name__ == "__main__":
    rodar_robo()
