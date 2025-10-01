const $ = (sel) => document.querySelector(sel);

function showLoading(v) {
  const el = $("#loading");
  if (el) el.classList.toggle("hidden", !v);
}

function showResult(v) {
  const el = $("#resultado");
  if (el) el.classList.toggle("hidden", !v);
}

// Sidebar: abre/fecha
const menuToggle = document.querySelector(".menu-toggle");
const sidebar = document.querySelector(".sidebar");
if (menuToggle && sidebar) {
  menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("open");
  });
}

// Limpar histórico
const clearBtn = document.getElementById("clear-history");
if (clearBtn) {
  clearBtn.addEventListener("click", () => {
    const list = document.getElementById("history-list");
    if (list) list.innerHTML = "";
  });
}

// Limpar textarea e esconder resultado
$("#btn-limpar").addEventListener("click", () => {
  $("#email-text").value = "";
  showResult(false);
});

// Classificar
$("#btn-classificar").addEventListener("click", async () => {
  const txt = $("#email-text").value.trim();
  const fd = new FormData();

  if (txt) fd.append("text", txt);
  else {
    const f = $("#file-input").files[0];
    if (!f) { alert("Cole um email ou envie um .txt/.pdf"); return; }
    fd.append("file", f);
  }

  try {
    showLoading(true);

    const resp = await fetch("/api/classify", { method: "POST", body: fd });
    let data;
    try {
      data = await resp.json();
    } catch {
      throw new Error("Formato inesperado na resposta do servidor");
    }

    if (!resp.ok) {
      throw new Error(data.error || "Erro ao processar");
    }

    const label = data.label || "—";
    $("#titulo-cat").textContent = label === "Produtivo" ? "Email Produtivo" : "Email Improdutivo";
    $("#sub-cat").textContent = label === "Produtivo"
      ? "Este email requer atenção e ação imediata"
      : "Este email não necessita de ação imediata";
    const pct = Math.round((data.confidence || 0) * 100);
    $("#bar-inner").style.width = pct + "%";
    $("#pct").textContent = pct + "%";
    $("#reply").textContent = data.suggested_reply || "";

    showResult(true);
    addToHistory(txt || (fd.get("file") ? "Arquivo enviado" : ""), label, pct);

  } catch (e) {
    alert(e.message || "Erro");
  } finally {
    showLoading(false);
  }
});

function addToHistory(texto, label, confPct) {
  const list = document.getElementById("history-list");
  if (!list) return;

  const item = document.createElement("div");
  item.className = "history-item";

  const title = document.createElement("strong");
  title.textContent = label === "Produtivo" ? "📌 Produtivo" : "❌ Improdutivo";

  const content = document.createElement("p");
  const resumo = (texto || "").toString();
  content.textContent = resumo.length > 140 ? resumo.slice(0, 140) + "..." : resumo;

  const conf = document.createElement("small");
  conf.textContent = `Confiança: ${confPct}%`;

  const del = document.createElement("button");
  del.textContent = "Excluir";
  del.addEventListener("click", () => item.remove());

  item.appendChild(title);
  item.appendChild(content);
  item.appendChild(conf);
  item.appendChild(del);

  list.appendChild(item);
}
