import os
import json
import feedparser
import re
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from datetime import datetime

# Mapeamento de Fontes e suas Categorias
FONTES_RSS = {
    # == GEOPOLÍTICA E GLOBAIS ==
    "Al Jazeera": {"url": "https://www.aljazeera.com/xml/rss/all.xml", "categoria": "GEOPOLÍTICA"},
    "BBC News (Reino Unido)": {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "categoria": "INTERNACIONAL"},
    
    # == ECONOMIA E NEGÓCIOS ==
    "Infomoney": {"url": "https://www.infomoney.com.br/feed/", "categoria": "ECONOMIA"},
    "Valor Econômico": {"url": "https://valor.globo.com/rss/valor/", "categoria": "ECONOMIA"},
    
    # == ESPORTES ==
    "Globo Esporte (GE)": {"url": "https://ge.globo.com/rss/ge/", "categoria": "ESPORTE"},
    "UOL Esporte": {"url": "http://rss.uol.com.br/feed/esporte.xml", "categoria": "ESPORTE"},
    
    # == SAÚDE, CULTURA E VARIEDADES ==
    "G1 Bem Estar": {"url": "https://g1.globo.com/rss/g1/saude/", "categoria": "SAÚDE E BEM-ESTAR"},
    "Omelete": {"url": "https://www.omelete.com.br/feed", "categoria": "CULTURA E LAZER"},
    "UOL Entretenimento": {"url": "http://rss.uol.com.br/feed/entretenimento.xml", "categoria": "VARIEDADES"}
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

def extrair_resumo_longo(url_da_noticia):
    """Entra no link original e raspa os primeiros 800 caracteres do texto."""
    try:
        # Disfarça o robô de navegador humano para evitar bloqueios das agências
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resposta = requests.get(url_da_noticia, headers=headers, timeout=15)
        
        # Transforma o site num formato que o Python consegue ler
        sopa = BeautifulSoup(resposta.content, 'html.parser')
        
        # Pega todos os blocos de texto (parágrafos)
        paragrafos = sopa.find_all('p')
        
        # Junta tudo num texto só
        texto_completo = " ".join([p.get_text().strip() for p in paragrafos])
        
        # Limpa espaços em branco duplicados e corta nos 800 caracteres
        texto_limpo = " ".join(texto_completo.split())
        resumo_final = texto_limpo[:800]
        
        if len(resumo_final) < 50:
            return "Resumo longo indisponível para o layout desta fonte."
            
        return resumo_final + "..."
        
    except Exception as e:
        return "Instabilidade ao acessar a matéria completa na fonte original."

def traduzir_noticia(titulo_org, texto_org, resumo_longo_org):
    try:
        # PROTEÇÃO 1: Evita que o tradutor trave se a notícia não tiver texto
        if not titulo_org: titulo_org = "Sem título"
        if not texto_org: texto_org = "Sem descrição disponível."
        if not resumo_longo_org: resumo_longo_org = "Sem resumo detalhado disponível."
        
        # PROTEÇÃO 2: 'auto' permite ler tanto fontes em PT quanto em EN sem misturar tudo
        tradutor_pt = GoogleTranslator(source='auto', target='pt')
        tradutor_es = GoogleTranslator(source='auto', target='es')
        tradutor_en = GoogleTranslator(source='auto', target='en')
        
        titulo_pt = tradutor_pt.translate(titulo_org)
        texto_pt = tradutor_pt.translate(texto_org)
        
        # Traduz o texto longo raspado do site original para o Português
        resumo_pt = tradutor_pt.translate(resumo_longo_org)
        
        titulo_es = tradutor_es.translate(titulo_org)
        texto_es = tradutor_es.translate(texto_org)
        
        titulo_en = tradutor_en.translate(titulo_org)
        texto_en = tradutor_en.translate(texto_org)
        
        return {
            "titulo_pt": titulo_pt, "texto_pt": texto_pt,
            "titulo_en": titulo_en, "texto_en": texto_en,
            "titulo_es": titulo_es, "texto_es": texto_es,
            "resumo_longo": resumo_pt # <--- Salva o super resumo no banco!
        }
    except Exception as e:
        print(f"Erro no tradutor: {e}")
        # Se a tradução falhar, retorna o texto original com aviso em vez de quebrar o site
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
    # Nova estrutura de iteração lendo o Dicionário completo
    for nome_fonte, dados_fonte in FONTES_RSS.items():
        if cont_processadas >= 12: # Limite aumentado para cobrir mais fontes
            break
            
        url_rss = dados_fonte["url"]
        categoria = dados_fonte["categoria"]
            
        try:
            feed = feedparser.parse(url_rss)
            # Pega apenas a 1ª notícia do topo para ser ágil e não dar Timeout no GitHub
            for entry in feed.entries[:1]:
                link = entry.get("link", "")
                if not link or link in links_existentes:
                    continue
                    
                titulo_original = entry.get("title", "")
                resumo_cru = entry.get("summary", entry.get("description", ""))
                texto_original = limpar_html(resumo_cru)
                
                print(f"Processando: {nome_fonte} | {categoria}...")
                
                # O robô entra na matéria original e raspa o texto
                texto_denso = extrair_resumo_longo(link)
                
                # Passamos o título, o lide e o texto denso para o tradutor
                dados_traduzidos = traduzir_noticia(titulo_original, texto_original, texto_denso)
                
                item_noticia = {
                    "id": len(banco_atual) + len(novas_noticias) + 1,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "fonte_origem": nome_fonte,
                    "categoria": categoria,
                    "link_origem": link,
                    "status": "APROVADO",
                    **dados_traduzidos
                }
                
                novas_noticias.append(item_noticia)
                links_existentes.add(link)
                cont_processadas += 1
                
        except Exception as erro_fonte:
            # PROTEÇÃO 3: Se uma fonte inteira cair, o robô pula para a próxima sem travar
            print(f"Erro ao processar a fonte {nome_fonte}: {erro_fonte}")
                
    if novas_noticias:
        banco_atual.extend(novas_noticias)
        # Proteção 4: Mantém apenas as últimas 150 matérias para o arquivo não ficar gigante
        banco_atual = banco_atual[-150:] 
        salvar_banco(banco_atual)
        print(f"Sucesso! {len(novas_noticias)} matérias processadas e categorizadas.")
    else:
        print("Nenhuma notícia nova encontrada.")

if __name__ == "__main__":
    rodar_robo()
