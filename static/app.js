const STATUS_LABELS = {
  new: "Новое",
  assigned: "Эксперт назначен",
  inspection: "Осмотр проведён",
  completed: "Протокол оформлен",
};

const listEl = document.getElementById("claims-list");
const emptyEl = document.getElementById("empty-hint");

async function api(path, options = {}) {
  const res = await fetch(path, options);
  const contentType = res.headers.get("content-type") || "";
  const body = contentType.includes("application/json") ? await res.json() : null;
  if (!res.ok) {
    throw new Error(body?.detail || res.statusText || "Ошибка запроса");
  }
  return body;
}

function showMessage(container, message) {
  const el = document.createElement("p");
  el.className = "claim-message";
  el.textContent = message;
  container.appendChild(el);
  setTimeout(() => el.remove(), 4000);
}

function showError(container, message) {
  const el = document.createElement("p");
  el.className = "claim-error";
  el.textContent = message;
  container.appendChild(el);
  setTimeout(() => el.remove(), 4000);
}

async function loadClaims() {
  try {
    const claims = await api("/api/claims");
    renderClaims(claims);
  } catch (e) {
    showError(listEl, e.message);
  }
}

function renderClaims(claims) {
  listEl.innerHTML = "";
  emptyEl.hidden = claims.length > 0;
  claims.forEach((claim) => listEl.appendChild(renderClaim(claim)));
}

function renderClaim(claim) {
  const el = document.createElement("article");
  el.className = "claim";
  el.dataset.id = claim.claim_id;

  el.innerHTML = `
    <div class="claim-head">
      <b>${claim.number}</b>
      <span class="pill ${claim.status}">${STATUS_LABELS[claim.status] || claim.status}</span>
    </div>
    <div class="claim-meta">
      Полис ${claim.policy_number} · ${claim.region} · от ${formatDate(claim.created_at)}
      ${claim.expert_id ? `· эксперт ${shortId(claim.expert_id)}` : ""}
    </div>
    <div class="claim-actions"></div>
  `;

  const actions = el.querySelector(".claim-actions");

  if (claim.status === "new") {
    actions.appendChild(assignBlock(claim));
  }
  if (claim.status === "assigned" || claim.status === "inspection") {
    actions.appendChild(inspectionBlock(claim));
    actions.appendChild(photosBlock(claim));
    actions.appendChild(signatureBlock(claim));
  }
  if (claim.status === "completed") {
    actions.appendChild(protocolBlock(claim));
  }
  return el;
}

function assignBlock(claim) {
  const block = document.createElement("div");
  block.className = "action-block";
  block.innerHTML = `
    <span class="action-title">Назначение эксперта (Strategy)</span>
    <div class="form-row">
      <select>
        <option value="free">free — первый свободный</option>
        <option value="region">region — по региону ДТП</option>
      </select>
      <button>Назначить</button>
    </div>
  `;
  const select = block.querySelector("select");
  block.querySelector("button").addEventListener("click", async () => {
    try {
      await api(`/api/claims/${claim.claim_id}/assign?strategy=${select.value}`, { method: "POST" });
      await loadClaims();
    } catch (e) {
      showError(block, e.message);
    }
  });
  return block;
}

function inspectionBlock(claim) {
  const block = document.createElement("div");
  block.className = "action-block";
  block.innerHTML = `
    <span class="action-title">Результаты осмотра</span>
    <label class="form-row" style="gap:6px;align-items:center">
      <input type="checkbox" style="width:auto">
      <span style="font-size:14px">Зафиксированы повреждения</span>
    </label>
    <input type="text" placeholder="Заключение эксперта">
    <button>Подать акт осмотра</button>
  `;
  const checkbox = block.querySelector('input[type="checkbox"]');
  const notes = block.querySelector('input[type="text"]');
  block.querySelector("button").addEventListener("click", async () => {
    try {
      await api(`/api/claims/${claim.claim_id}/inspection`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ damage_found: checkbox.checked, notes: notes.value }),
      });
      await loadClaims();
    } catch (e) {
      showError(block, e.message);
    }
  });
  return block;
}

function photosBlock(claim) {
  const block = document.createElement("div");
  block.className = "action-block";
  block.innerHTML = `
    <span class="action-title">Фотографии осмотра</span>
    <div class="form-row">
      <input type="file" multiple accept="image/*">
      <button>Загрузить</button>
    </div>
  `;
  const input = block.querySelector('input[type="file"]');
  block.querySelector("button").addEventListener("click", async () => {
    const files = input.files;
    if (files.length === 0) {
      showError(block, "Выберите хотя бы один файл");
      return;
    }
    const formData = new FormData();
    for (const file of files) {
      formData.append("files", file);
    }
    try {
      await api(`/api/claims/${claim.claim_id}/photos`, { method: "POST", body: formData });
      await loadClaims();
      showMessage(block, `Загружено файлов: ${files.length}`);
    } catch (e) {
      showError(block, e.message);
    }
  });
  return block;
}

function signatureBlock(claim) {
  const block = document.createElement("div");
  block.className = "action-block";
  block.innerHTML = `
    <span class="action-title">Подпись клиента на протоколе</span>
    <div class="form-row">
      <input type="text" placeholder="ФИО подписанта" value="Клиент И. О.">
      <button>Подписать</button>
    </div>
  `;
  const input = block.querySelector("input");
  block.querySelector("button").addEventListener("click", async () => {
    try {
      await api(`/api/claims/${claim.claim_id}/signature`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ signed_by: input.value }),
      });
      await loadClaims();
    } catch (e) {
      showError(block, e.message);
    }
  });
  return block;
}

function protocolBlock(claim) {
  const block = document.createElement("div");
  block.className = "action-block";
  const link = document.createElement("a");
  link.href = `/api/claims/${claim.claim_id}/protocol`;
  link.target = "_blank";
  const btn = document.createElement("button");
  btn.textContent = "Скачать PDF-протокол";
  link.appendChild(btn);
  block.appendChild(link);
  return block;
}

function formatDate(iso) {
  return new Date(iso).toLocaleString("ru-RU", {
    day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit",
  });
}

function shortId(uuid) {
  return uuid.slice(0, 8);
}

document.getElementById("claim-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const formError = document.getElementById("form-error");
  formError.hidden = true;
  const payload = {
    policy_number: document.getElementById("policy_number").value.trim(),
    region: document.getElementById("region").value,
    description: document.getElementById("description").value,
  };
  try {
    await api("/api/claims", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    document.getElementById("description").value = "";
    await loadClaims();
  } catch (e) {
    formError.textContent = e.message;
    formError.hidden = false;
  }
});

document.getElementById("reload").addEventListener("click", loadClaims);

loadClaims();
