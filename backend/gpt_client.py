import os
import json
import re
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Carrega .env
load_dotenv()


try:
    from groq import Groq
except Exception:
    Groq = None  

SYSTEM = """
Você é um assistente de suporte de uma empresa financeira.
Dado o texto de um email, classifique em "Produtivo" (requer ação/resposta)
ou "Improdutivo" (sem ação imediata) e sugira UMA resposta automática curta.
A resposta deve ser educada, objetiva e ter entre 2 a 4 linhas, em português do Brasil.

IMPORTANTE: Responda SOMENTE em JSON válido, no formato:
{
  "categoria": "Produtivo ou Improdutivo",
  "resposta": "texto sugerido",
  "confianca": 0.9
}
"""

def ask_gpt(email_text: str) -> Optional[Dict[str, Any]]:
    """
    Chama a Groq API para classificar o email e gerar resposta.
    Retorna dicionário com keys: categoria, resposta, confianca
    Em caso de falha, retorna None (o main fará fallback local).
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Nenhuma chave GROQ_API_KEY configurada no ambiente.")
        return None

    if Groq is None:
        print("Cliente Groq não disponível (pacote não instalado).")
        return None

    try:
        client = Groq(api_key=api_key)

       
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"Email:\n{email_text}"}
            ],
            max_tokens=400,
            temperature=0.25,
        )

     
        content = ""
        try:
            content = resp.choices[0].message.content or ""
        except Exception:
           
            content = str(resp)

       
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # extrai primeiro bloco JSON {...} no texto
            m = re.search(r"\{.*\}", content, flags=re.DOTALL)
            if m:
                try:
                    return json.loads(m.group())
                except Exception:
                    pass
           
            return {"categoria": "Desconhecido", "resposta": content, "confianca": 0.5}

    except Exception as e:
        print("Erro ao chamar a API do Groq:", str(e))
        return None
