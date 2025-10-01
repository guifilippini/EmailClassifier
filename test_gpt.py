# test_gpt.py
from backend.gpt_client import ask_gpt

email_exemplo = """
Olá, equipe. Poderiam me confirmar o status do pedido #4521? Preciso confirmar prazo para pagamento.
Obrigado.
"""

res = ask_gpt(email_exemplo)
print("=== RESPOSTA ===")
print(res)


