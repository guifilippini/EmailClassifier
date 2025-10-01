import os
import json
import re
from typing import Optional, Dict, Any
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

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
    if not API_KEY:
        print("❌ Nenhuma chave GROQ_API_KEY configurada.")
        return None

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"Email:\n{email_text}"}
            ],
            "max_tokens": 400,
            "temperature": 0.25,
        }

        r = requests.post(API_URL, headers=headers, json=payload)
        r.raise_for_status()
        resp_json = r.json()

        content = resp_json["choices"][0]["message"]["content"]

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, flags=re.DOTALL)
            if match:
                return json.loads(match.group())
            return {"categoria": "Desconhecido", "resposta": content, "confianca": 0.5}

    except Exception as e:
        print("Erro ao chamar a API do Groq:", str(e))
        return None
