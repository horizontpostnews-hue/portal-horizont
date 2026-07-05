import os
import json
import feedparser
import google.generativeai as genai
from datetime import datetime

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

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
    if not api_key:
        raise ValueError("Chave GEMINI_API_KEY não foi encontrada no GitHub Secrets!")
        
    prompt = f"""
    Traduza e resuma a notícia a seguir.
    Título original: {titulo_org}
    Texto original: {texto_org}
    
    Retorne APENAS um JSON válido. Não use formatação markdown (```json). Use este formato exato:
    {{
        "titulo_pt": "Título em português",
        "texto_pt": "Resumo em português (2 parágrafos)",
        "titulo_en": "Título em inglês",
        "texto_en": "Resumo em inglês",
        "titulo_es": "Título em espanhol",
        "texto_es": "Resumo em espanhol"
    }}
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        texto_limpo = response.text.strip()
        if texto_limpo.startswith("
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1
3. Salve as alterações.

---

### 🔄 Passo 3: Limpar o banco e Rodar o teste
1. Vá no arquivo **`banco_noticias.json`** no GitHub, edite, apague tudo e deixe apenas os colchetes vazios `[]`. Salve.
2. Vá na aba **`Actions`** e rode o workflow manualmente de novo.
3. Entre no seu portal pelo celular e atualize a página.

Se a tradução funcionar, as notícias estarão 100% em português brasileiro! Se a tradução falhar, o texto das matérias agora vai mostrar a mensagem técnica exata (exemplo: *Erro detectado pelo sistema: API_KEY_INVALID*), e assim nós saberemos exatamente como consertar. Faça o teste e veja o que aparece!
