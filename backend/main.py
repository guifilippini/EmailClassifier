from __future__ import annotations
import io, time, pathlib
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pdfminer.high_level import extract_text as pdf_extract_text

from backend.fallback import classify_local
from backend.gpt_client import ask_gpt

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
ASSETS_DIR = SRC_DIR / "assets"

app = FastAPI(title="AutoU Email Classifier", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")


def read_uploaded(file: UploadFile) -> str:
    content = file.file.read()
    if not content:
        return ""
    name = (file.filename or "").lower()
    ctype = (file.content_type or "").lower()

    if name.endswith(".txt") or "text/plain" in ctype:
        try:
            return content.decode("utf-8", errors="ignore")
        except Exception:
            return content.decode("latin-1", errors="ignore")

    if name.endswith(".pdf") or "pdf" in ctype:
        try:
            text = pdf_extract_text(io.BytesIO(content))
            return text.strip()
        except Exception:
            return ""

    try:
        return content.decode("utf-8", errors="ignore")
    except Exception:
        return ""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse((SRC_DIR / "index.html").read_text(encoding="utf-8"))


@app.post("/api/classify")
async def classify(text: str = Form(None), file: UploadFile = File(None)):
    t0 = time.time()
    raw = (text or "").strip()
    if file is not None and not raw:
        raw = read_uploaded(file)
    if not raw:
        return JSONResponse(
            {"error": "Não foi possível extrair texto do arquivo. Envie um .txt ou um .pdf com texto digital."},
            status_code=400
        )

    gpt = ask_gpt(raw)
    if gpt:
        label = gpt.get("categoria", "Produtivo")
        reply = gpt.get("resposta", "")
        conf = float(gpt.get("confianca", 0.85))
    else:
        label, conf, _ = classify_local(raw)
        reply = "Agradecemos a mensagem!" if label == "Improdutivo" else "Obrigado pelo contato. Retornaremos em breve."

    return {
        "label": label,
        "confidence": round(conf, 4),
        "suggested_reply": reply,
        "length_chars": len(raw)
    }


@app.get("/health")
def health():
    return {"status": "ok"}
