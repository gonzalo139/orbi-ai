(function () {
  const ORBI_API = "https://orbi-ai-r41a.onrender.com";
  const BUSINESS_ID = window.ORBI_BUSINESS_ID || "demo";
  let history = [];

  const styles = `
    #orbi-btn {
      position: fixed; bottom: 24px; right: 24px;
      width: 56px; height: 56px; border-radius: 50%;
      background: #6C63FF; color: white; font-size: 26px;
      border: none; cursor: pointer; box-shadow: 0 4px 16px rgba(108,99,255,0.4);
      z-index: 9999; transition: transform 0.2s;
    }
    #orbi-btn:hover { transform: scale(1.1); }
    #orbi-box {
      display: none; position: fixed; bottom: 90px; right: 24px;
      width: 340px; height: 480px; background: white;
      border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.15);
      z-index: 9999; flex-direction: column; overflow: hidden;
    }
    #orbi-box.open { display: flex; }
    #orbi-header {
      background: #6C63FF; color: white; padding: 16px;
      font-family: sans-serif; font-weight: bold; font-size: 15px;
    }
    #orbi-messages {
      flex: 1; overflow-y: auto; padding: 16px;
      font-family: sans-serif; font-size: 14px; display: flex;
      flex-direction: column; gap: 10px;
    }
    .orbi-msg { max-width: 80%; padding: 10px 14px; border-radius: 12px; line-height: 1.4; }
    .orbi-msg.bot { background: #f0eeff; color: #333; align-self: flex-start; }
    .orbi-msg.user { background: #6C63FF; color: white; align-self: flex-end; }
    #orbi-input-area {
      display: flex; padding: 12px; border-top: 1px solid #eee; gap: 8px;
    }
    #orbi-input {
      flex: 1; border: 1px solid #ddd; border-radius: 8px;
      padding: 8px 12px; font-size: 14px; outline: none; font-family: sans-serif;
    }
    #orbi-send {
      background: #6C63FF; color: white; border: none;
      border-radius: 8px; padding: 8px 14px; cursor: pointer; font-size: 18px;
    }
  `;

  const html = `
    <style>${styles}</style>
    <button id="orbi-btn">💬</button>
    <div id="orbi-box">
      <div id="orbi-header">🤖 Orbi — Asistente virtual</div>
      <div id="orbi-messages">
        <div class="orbi-msg bot">¡Hola! ¿En qué puedo ayudarte hoy?</div>
      </div>
      <div id="orbi-input-area">
        <input id="orbi-input" type="text" placeholder="Escribí tu consulta..." />
        <button id="orbi-send">➤</button>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML("beforeend", html);

  const btn = document.getElementById("orbi-btn");
  const box = document.getElementById("orbi-box");
  const input = document.getElementById("orbi-input");
  const send = document.getElementById("orbi-send");
  const messages = document.getElementById("orbi-messages");

  btn.addEventListener("click", () => box.classList.toggle("open"));

  function addMessage(text, type) {
    const div = document.createElement("div");
    div.className = `orbi-msg ${type}`;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;
    addMessage(text, "user");
    input.value = "";
    addMessage("...", "bot");

    try {
      const res = await fetch(`${ORBI_API}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          business_id: BUSINESS_ID,
          history: history
        })
      });
      const data = await res.json();
      const botReply = data.response;
      messages.lastChild.textContent = botReply;

      history.push({ role: "user", content: text });
      history.push({ role: "assistant", content: botReply });

    } catch {
      messages.lastChild.textContent = "Error al conectar con Orbi.";
    }
  }

  send.addEventListener("click", sendMessage);
  input.addEventListener("keydown", e => { if (e.key === "Enter") sendMessage(); });
})();