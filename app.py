
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from chatbot import get_response

app = FastAPI(title="AI Chatbot - Practical 8")


class ChatMessage(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NOIR | AI Assistant</title>

<style>
:root {
    --bg: #15100c;
    --panel: #211711;
    --card: #2b1e16;
    --border: #5b432e;
    --gold: #c6a574;
    --gold-light: #ead8b9;
    --text: #f0e5d3;
    --muted: #b3a08a;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    min-height: 100vh;
    font-family: "Segoe UI", Arial, sans-serif;
    color: var(--text);
    background:
        radial-gradient(ellipse at 80% 0%, #49301f55, transparent 42%),
        radial-gradient(ellipse at 10% 90%, #35221855, transparent 42%),
        linear-gradient(135deg, #120e0b, #1d1510 60%, #120e0b);
}

button, input {
    font: inherit;
}

.app {
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 235px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 28px;
    padding: 28px 16px 18px;
    background: linear-gradient(160deg, #19120e, #251a13 65%, #15100c);
    border-right: 1px solid #493727;
}

.brand {
    display: flex;
    align-items: center;
    gap: 11px;
}

.brand-mark {
    width: 40px;
    height: 40px;
    display: grid;
    place-items: center;
    border-radius: 13px;
    color: #21150d;
    background: linear-gradient(135deg, #ead8b9, #b28a58);
    font-size: 23px;
}

.brand-name {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 3px;
}

.brand-caption {
    margin-top: 3px;
    color: var(--muted);
    font-size: 9px;
    letter-spacing: 1.7px;
}

.new-chat {
    padding: 13px;
    border: 1px solid #d3b88d;
    border-radius: 10px;
    color: #20160e;
    background: linear-gradient(120deg, #dfc69f, #b58b59 60%, #89623e);
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
}

.new-chat:hover, #send-button:hover {
    filter: brightness(1.1);
}

.section-label {
    margin-bottom: 12px;
    color: #a58a6d;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 5px;
    padding: 12px 10px;
    border: 1px solid transparent;
    border-radius: 9px;
    color: #c3b19b;
    font-size: 13px;
}

.nav-item.active {
    color: var(--gold-light);
    background: linear-gradient(115deg, #5b402c66, #38271c55);
    border-color: #84634360;
}

.nav-icon {
    width: 20px;
    color: var(--gold);
    text-align: center;
}

.sidebar-bottom {
    margin-top: auto;
    padding: 14px 11px;
    border: 1px solid #59432f;
    border-radius: 11px;
    background: linear-gradient(135deg, #38271d, #211711);
}

.profile-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    font-weight: 600;
}

.profile-icon {
    width: 32px;
    height: 32px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    color: #21160d;
    background: linear-gradient(135deg, #ead8b9, #a87d4f);
}

.profile-subtitle {
    margin: 5px 0 0 42px;
    color: var(--muted);
    font-size: 11px;
}

/* Main area */
.main {
    display: flex;
    flex: 1;
    flex-direction: column;
    min-width: 0;
}

.topbar {
    min-height: 62px;
    padding: 16px 26px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    background: #19120edb;
    border-bottom: 1px solid #493727;
}

.topbar-title {
    color: #c9ad85;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
}

.status {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 7px 11px;
    border: 1px solid #655139;
    border-radius: 25px;
    color: #e0c7a1;
    background: #30251a;
    font-size: 11px;
    white-space: nowrap;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #c6a574;
}

/* Chat layout */
.chat-area {
    width: 100%;
    max-width: 1000px;
    flex: 1;
    display: flex;
    flex-direction: column;
    margin: 0 auto;
    padding: 26px 28px 15px;
}

.welcome {
    padding: 12px 0 24px;
    text-align: center;
}

.welcome-symbol {
    width: 54px;
    height: 54px;
    display: grid;
    place-items: center;
    margin: 0 auto 15px;
    border: 1px solid #94704b;
    border-radius: 17px;
    color: #21150d;
    background: linear-gradient(140deg, #ead8b9, #c4a070 58%, #88603d);
    font-size: 27px;
}

.eyebrow {
    margin-bottom: 10px;
    color: #ad8a60;
    font-size: 10px;
    letter-spacing: 3px;
}

.welcome h1 {
    margin: 0 0 10px;
    color: #f0e4d1;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(27px, 3vw, 38px);
    font-weight: 500;
}

.welcome h1 span {
    color: #c9a675;
    font-style: italic;
}

.welcome p {
    max-width: 500px;
    margin: 0 auto;
    color: #b7a38c;
    font-size: 13px;
    line-height: 1.8;
}

/* Suggested prompts */
.suggestions {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 22px;
}

.suggestion {
    min-width: 0;
    padding: 15px;
    border: 1px solid #5b4531;
    border-radius: 12px;
    color: var(--text);
    background: linear-gradient(145deg, #38271c, #251a14 75%);
    text-align: left;
    cursor: pointer;
    transition: transform .2s, border-color .2s;
}

.suggestion:hover {
    transform: translateY(-2px);
    border-color: #b08a5c;
}

.suggestion-icon {
    width: 35px;
    height: 35px;
    display: grid;
    place-items: center;
    margin-bottom: 11px;
    border: 1px solid #8c6b4655;
    border-radius: 10px;
    color: #e1c398;
    background: linear-gradient(135deg, #60452d, #38271c);
}

.suggestion strong {
    display: block;
    margin-bottom: 6px;
    color: #e8d7bf;
    font-size: 13px;
}

.suggestion small {
    display: block;
    color: #b4a18b;
    font-size: 11px;
    line-height: 1.7;
}

/* Messages */
#messages {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 5px 0 20px;
}

.message-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    max-width: 88%;
}

.message-row.user-row {
    align-self: flex-end;
    justify-content: flex-end;
}

.avatar {
    width: 32px;
    height: 32px;
    flex-shrink: 0;
    display: grid;
    place-items: center;
    border: 1px solid #94704b;
    border-radius: 10px;
    color: #23170e;
    background: linear-gradient(140deg, #ead8b9, #b38b5b);
}

.message-content {
    min-width: 0;
}

.bubble {
    padding: 12px 15px;
    border-radius: 13px;
    font-size: 13px;
    line-height: 1.8;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.bot-row .bubble {
    border: 1px solid #57402e;
    border-top-left-radius: 4px;
    color: #ebddca;
    background: linear-gradient(135deg, #302219, #241912);
}

.user-row .bubble {
    border: 1px solid #a47c50;
    border-top-right-radius: 4px;
    color: #24170e;
    background: linear-gradient(120deg, #e0c59a, #c09a68 58%, #987047);
}

/* Input: no separate coloured strip */
.composer-wrap {
    margin-top: auto;
    padding-top: 14px;
    background: transparent;
}

.composer {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 7px 6px 17px;
    border: 1px solid #70553a;
    border-radius: 14px;
    background: linear-gradient(120deg, #2b1f17, #211711);
    box-shadow: 0 7px 22px #00000020;
    transition: border-color .2s, box-shadow .2s;
}

.composer:focus-within {
    border-color: #c09a68;
    box-shadow: 0 0 0 3px #c6a57412;
}

#message-input {
    flex: 1;
    min-width: 0;
    padding: 12px 0;
    border: 0;
    outline: 0;
    color: #f1e4d1;
    background: transparent;
    font-size: 13px;
}

#message-input::placeholder {
    color: #a18b73;
}

#send-button {
    width: 42px;
    height: 42px;
    flex-shrink: 0;
    border: 1px solid #d4b488;
    border-radius: 11px;
    color: #24170d;
    background: linear-gradient(135deg, #ead8b9, #c3a071 60%, #9a7148);
    font-size: 19px;
    cursor: pointer;
}

#send-button:disabled {
    opacity: .55;
    cursor: wait;
}

.footer-note {
    margin: 10px 0 0;
    color: #927c65;
    font-size: 10px;
    line-height: 1.6;
    text-align: center;
}

@media (max-width: 760px) {
    .sidebar {
        display: none;
    }

    .topbar {
        padding: 14px 16px;
    }

    .chat-area {
        padding: 20px 14px 14px;
    }

    .suggestions {
        grid-template-columns: 1fr;
        gap: 9px;
    }

    .suggestion {
        display: grid;
        grid-template-columns: 35px 1fr;
        align-items: center;
        column-gap: 11px;
        padding: 12px;
    }

    .suggestion-icon {
        grid-row: span 2;
        margin: 0;
    }

    .suggestion strong {
        margin-bottom: 3px;
    }

    .message-row {
        max-width: 96%;
    }
}
</style>
</head>

<body>
<div class="app">

    <aside class="sidebar">
        <div class="brand">
            <div class="brand-mark">✦</div>
            <div>
                <div class="brand-name">NOIR</div>
                <div class="brand-caption">INTELLIGENT ASSISTANT</div>
            </div>
        </div>

        <button class="new-chat" id="new-chat">＋ &nbsp; New conversation</button>

        <div>
            <div class="section-label">Workspace</div>
            <div class="nav-item active"><span class="nav-icon">✧</span> AI Assistant</div>
            <div class="nav-item"><span class="nav-icon">◇</span> Study support</div>
            <div class="nav-item"><span class="nav-icon">✓</span> Task planning</div>
            <div class="nav-item"><span class="nav-icon">✉</span> Email assistance</div>
        </div>

        <div class="sidebar-bottom">
            <div class="profile-row">
                <div class="profile-icon">✦</div>
                <span>Student Workspace</span>
            </div>
            <div class="profile-subtitle">AI Practical 08</div>
        </div>
    </aside>

    <main class="main">
        <header class="topbar">
            <div class="topbar-title">NLP · PERSONAL ASSISTANT</div>
            <div class="status"><span class="status-dot"></span> Model ready</div>
        </header>

        <section class="chat-area">
            <div class="welcome" id="welcome">
                <div class="welcome-symbol">✦</div>
                <div class="eyebrow">YOUR PERSONAL AI ASSISTANT</div>
                <h1>A little clarity.<br><span>A better way forward.</span></h1>
                <p>
                    Ask for study guidance, organize your tasks,
                    or get help with common email requests.
                </p>
            </div>

            <div class="suggestions" id="suggestions">
                <button class="suggestion"
                    data-message="How should I prepare for exams?">
                    <span class="suggestion-icon">◇</span>
                    <strong>Study support</strong>
                    <small>Practical tips for revision and exam preparation.</small>
                </button>

                <button class="suggestion"
                    data-message="Help me prioritise my work.">
                    <span class="suggestion-icon">✓</span>
                    <strong>Plan my tasks</strong>
                    <small>Organize your work and manage your deadlines.</small>
                </button>

                <button class="suggestion"
                    data-message="Help me write an email to my lecturer.">
                    <span class="suggestion-icon">✉</span>
                    <strong>Email assistance</strong>
                    <small>Get guidance for common email requests.</small>
                </button>
            </div>

            <div id="messages" aria-live="polite"></div>

            <div class="composer-wrap">
                <form class="composer" id="chat-form">
                    <input id="message-input" type="text"
                        placeholder="Write your message..."
                        maxlength="1000" autocomplete="off" required>
                    <button id="send-button" type="submit"
                        aria-label="Send message">➤</button>
                </form>

                <p class="footer-note">
                    AI Practical 08 · Responses use trained intent patterns.
                    This prototype does not access real emails.
                </p>
            </div>
        </section>
    </main>
</div>

<script>
const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const messages = document.getElementById("messages");
const sendButton = document.getElementById("send-button");
const welcome = document.getElementById("welcome");
const suggestions = document.getElementById("suggestions");

let isSending = false;

function addMessage(text, isUser) {
    const row = document.createElement("div");
    row.className = "message-row " + (isUser ? "user-row" : "bot-row");

    if (!isUser) {
        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.textContent = "✦";
        row.appendChild(avatar);
    }

    const content = document.createElement("div");
    content.className = "message-content";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    content.appendChild(bubble);
    row.appendChild(content);
    messages.appendChild(row);

    row.scrollIntoView({behavior: "smooth", block: "nearest"});

    return bubble;
}

async function sendMessage(text) {
    const message = text.trim();

    if (!message || isSending) return;

    isSending = true;
    sendButton.disabled = true;
    welcome.style.display = "none";
    suggestions.style.display = "none";

    addMessage(message, true);
    input.value = "";

    const waiting = addMessage("Preparing a response...", false);

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: message})
        });

        const result = await response.json();

        if (!response.ok) {
            waiting.textContent =
                result.detail || "The request could not be processed.";
        } else {
            // Show the chatbot's response, without the confidence score.
            waiting.textContent = result.response;
        }
    } catch (error) {
        waiting.textContent =
            "Unable to connect to the chatbot. Please try again.";
    } finally {
        isSending = false;
        sendButton.disabled = false;
        input.focus();
    }
}

form.addEventListener("submit", function(event) {
    event.preventDefault();
    sendMessage(input.value);
});

document.querySelectorAll(".suggestion").forEach(function(card) {
    card.addEventListener("click", function() {
        sendMessage(card.dataset.message);
    });
});

document.getElementById("new-chat").addEventListener("click", function() {
    if (isSending) return;

    messages.replaceChildren();
    welcome.style.display = "";
    suggestions.style.display = "";
    input.value = "";
    input.focus();
});
</script>
</body>
</html>
"""


@app.post("/chat")
def chat(message: ChatMessage):
    result = get_response(message.message)

    return {
        "response": result["response"],
        "intent": result["intent"],
        "confidence": result["confidence"]
    }
