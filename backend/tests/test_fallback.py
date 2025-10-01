
from backend.fallback import classify_local

def test_classify_local_produtivo():
    label, conf, _ = classify_local("Preciso de suporte técnico")
    assert label == "Produtivo"

def test_classify_local_improdutivo():
    label, conf, _ = classify_local("Parabéns pelo seu prêmio!")
    assert label == "Improdutivo"
