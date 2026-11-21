const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("input");
const language = document.getElementById("language");
const sendBtn = form.querySelector("button");

const sessionId = localStorage.getItem("sid") || crypto.randomUUID();
localStorage.setItem("sid", sessionId);

const escapeHtml = (s) =>
  s.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

function render(text) {
  // Close an unfinished code fence so partial streams render cleanly
  if ((text.match(/```/g) || []).length % 2) text += "\n```";
  return escapeHtml(text)
    .replace(/```\w*\n([\s\S]*?)```/g, "<pre><code>$1</code></pre>")
    .replace(/`([^`\n]+)`/g, "<code>$1</code>");
}

function addMessage(html, role) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.innerHTML = html;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question) return;

  addMessage(escapeHtml(question), "user");
  input.value = "";
  sendBtn.disabled = true;
  const bot = addMessage("Thinking...", "bot");

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        session_id: sessionId,
        language: language.value,
      }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Something went wrong.");
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let text = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      text += decoder.decode(value, { stream: true });
      bot.innerHTML = render(text);
      chat.scrollTop = chat.scrollHeight;
    }
  } catch (err) {
    bot.innerHTML = `⚠️ ${escapeHtml(err.message)}`;
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
});

document.getElementById("clear").addEventListener("click", async () => {
  await fetch("/api/clear", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId }),
  });
  chat.innerHTML = '<div class="msg bot">Chat cleared. Ask me anything about code.</div>';
});