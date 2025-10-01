
def classify_local(text: str):
    if any(w in text.lower() for w in ["obrigado","feliz","parabéns",
        "grátis","urgente","agora","oportunidade","seu email ganhou","você é um vencedor",
        "ganhe dinheiro","renda extra","dinheiro rápido","oferta limitada","últimas vagas disponíveis para este treinamento"]):
        return "Improdutivo", 0.9, None
    return "Produtivo", 0.9, None
