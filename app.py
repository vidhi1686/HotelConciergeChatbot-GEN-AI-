import asyncio
import re
import time
from typing import Dict, Any, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

# =========================================================
# Magical Palace - Single-file Hospitality Chatbot Website
# Run: python -m uvicorn app:app --reload --port 8000
# Open: http://localhost:8000
# =========================================================

app = FastAPI(title="Magical Palace Concierge")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ok for local demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# "Compressed" data (Knowledge Cards)
# Keep these short + bullet-based for speed.
# -----------------------------
KNOWLEDGE_CARDS: List[Dict[str, Any]] = [
    {
        "title": "Check-in and Check-out",
        "tags": ["checkin", "checkout", "front desk", "arrival", "departure", "policy"],
        "bullets": [
            "Check-in: 2:00 PM",
            "Check-out: 11:00 AM",
            "Early check-in / late check-out depends on availability (Reception can confirm).",
            "Luggage storage is available at Reception.",
        ],
    },
    {
        "title": "Breakfast",
        "tags": ["breakfast", "food", "dining", "morning", "buffet", "menu"],
        "bullets": [
            "Breakfast is served daily: 7:00 AM – 10:30 AM",
            "Ask for vegetarian options or allergies—staff can help.",
            "If you’re leaving early, ask Reception about a packed breakfast.",
        ],
    },
    {
        "title": "Room Service",
        "tags": ["room service", "in-room dining", "order food", "lunch", "dinner", "snacks", "call", "menu"],
        "bullets": [
            "Hours: 24/7 (limited menu after 11:00 PM).",
            "To order: call Reception or use the in-room phone (Room Service).",
            "Typical delivery time: 25–45 minutes (depends on rush hours).",
            "Mention allergies or dietary preferences when ordering.",
        ],
    },
    {
        "title": "Wi-Fi access",
        "tags": ["wifi", "internet", "password", "network"],
        "bullets": [
            "Connect to: MagicalPalace-Guest",
            "If you need a password: Reception will provide it (may vary by booking).",
            "If it won’t connect: forget the network → reconnect, or restart Wi-Fi on your device.",
        ],
    },
    {
        "title": "Pool and Gym",
        "tags": ["pool", "gym", "fitness", "wellness"],
        "bullets": [
            "Gym: 6:00 AM – 10:00 PM",
            "Pool: 7:00 AM – 8:00 PM",
            "Bring your room key. Towels may be provided poolside.",
        ],
    },
    {
        "title": "Spa",
        "tags": ["spa", "massage", "relax", "wellness"],
        "bullets": [
            "Spa requires booking.",
            "Evenings are busy—book earlier if possible.",
            "Tell us what you want: relaxation, deep tissue, or quick refresh.",
        ],
    },
    {
        "title": "Airport transfer",
        "tags": ["airport", "pickup", "transfer", "taxi", "car"],
        "bullets": [
            "Airport pickup can be arranged via Reception.",
            "Share flight number + arrival time.",
            "Mention large luggage if you have it.",
        ],
    },
    {
        "title": "Nearby attraction: Riverfront Promenade",
        "tags": ["attraction", "nearby", "river", "walk", "sunset", "photos"],
        "bullets": [
            "Best for: sunset views + calm walk",
            "Go early if you want fewer crowds.",
            "Carry water if it’s hot outside.",
        ],
    },
    {
        "title": "Nearby attraction: Old Town Walk",
        "tags": ["attraction", "nearby", "old town", "history", "food", "evening"],
        "bullets": [
            "Best for: evening stroll + street food",
            "Sunset timing feels nicest.",
            "Tell me what you like (history / food / shopping) and I’ll suggest stops.",
        ],
    },
    {
        "title": "Nearby attraction: Local Handicraft Market",
        "tags": ["attraction", "market", "shopping", "souvenirs", "crafts"],
        "bullets": [
            "Best for: gifts and local crafts",
            "Bargaining is common—keep it polite.",
            "Ask the hotel for recommended stalls.",
        ],
    },
]

# -----------------------------
# Super fast retrieval + caching
# -----------------------------
TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(s: str) -> List[str]:
    return TOKEN_RE.findall(s.lower())


CACHE: Dict[str, Dict[str, Any]] = {}
CACHE_TTL = 10 * 60  # 10 minutes


def cache_get(q: str) -> str | None:
    obj = CACHE.get(q)
    if not obj:
        return None
    if time.time() - obj["ts"] > CACHE_TTL:
        CACHE.pop(q, None)
        return None
    return obj["answer"]


def cache_set(q: str, ans: str):
    CACHE[q] = {"ts": time.time(), "answer": ans}


def retrieve_cards(query: str, k: int = 2) -> List[Dict[str, Any]]:
    """Return up to `k` matching knowledge cards (default 2)."""
    q_tokens = tokenize(query)
    if not q_tokens:
        return []

    scored = []
    for card in KNOWLEDGE_CARDS:
        text = " ".join([card["title"]] + card["tags"] + card["bullets"])
        tset = set(tokenize(text))
        overlap = sum(1 for t in q_tokens if t in tset)
        if overlap > 0:
            scored.append((overlap, card))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:k]]


def build_breakfast_menu() -> str:
    return (
        "Breakfast (7:00 AM – 10:30 AM)\n"
        "- Served daily in the restaurant.\n"
        "- Vegetarian options available. Please mention allergies.\n\n"
        "Breakfast Menu (Sample)\n"
        "• Hot Dishes\n"
        "  - Masala omelette / Plain omelette\n"
        "  - Pancakes with honey or maple syrup\n"
        "  - Idli & sambar\n"
        "  - Poha (light & savory)\n\n"
        "• Fresh Bakery\n"
        "  - Croissants, muffins, toast\n"
        "  - Butter, jam, peanut butter\n\n"
        "• Healthy Corner\n"
        "  - Seasonal fruit bowl\n"
        "  - Yogurt + granola\n"
        "  - Oats porridge (milk / water)\n\n"
        "• Beverages\n"
        "  - Tea (assam / green), coffee\n"
        "  - Fresh juice (seasonal)\n\n"
        "If you’re leaving early, Reception can arrange a packed breakfast on request."
    )


def build_room_service_menu() -> str:
    return (
        "Room Service (In-room Dining)\n"
        "- Hours: 24/7 (limited menu after 11:00 PM)\n"
        "- To order: call Reception or use the in-room phone (Room Service)\n"
        "- Typical delivery time: 25–45 minutes\n"
        "- Please mention allergies or dietary preferences\n\n"
        "Room Service Menu (Popular picks)\n"
        "• Snacks\n"
        "  - French fries\n"
        "  - Veg sandwich / Chicken sandwich\n"
        "  - Soup of the day\n\n"
        "• Mains\n"
        "  - Butter paneer + naan\n"
        "  - Veg biryani / Chicken biryani\n"
        "  - Pasta (white sauce / red sauce)\n\n"
        "• Drinks\n"
        "  - Tea / Coffee\n"
        "  - Soft drinks / Fresh juice\n\n"
        "Tell me what you want (veg/non-veg, spicy/mild) and I’ll suggest a few options."
    )


def build_answer(query: str) -> str:
    q_lower = query.lower()
    q_tokens = set(tokenize(query))

    # Check-in / Check-out quick path
    if any(x in q_lower for x in ("check-in", "checkin", "check in", "checkout", "check-out", "check out")):
        return (
            "Check-in and Check-out\n"
            "- Check-in time: 2:00 PM\n"
            "- Check-out time: 11:00 AM\n"
            "- Early check-in or late check-out is subject to availability.\n"
            "- Luggage storage is available at Reception."
        )

    # Breakfast quick path (with menu)
    if "breakfast" in q_lower:
        return build_breakfast_menu()

    # Room service quick path (with menu)
    if any(x in q_lower for x in ("room service", "in-room", "in room", "order food", "dinner", "lunch")):
        return build_room_service_menu()

    # Nearby attractions quick path
    if any(x in q_lower for x in ("attraction", "attractions", "nearby", "near")):
        return (
            "Nearby Attractions\n"
            "• Old Town Walk\n"
            "  - Best for: evening strolls and street food\n"
            "  - Ideal around sunset for the best atmosphere\n\n"
            "• Riverfront Promenade\n"
            "  - Best for: calm walks and sunset views\n"
            "  - Less crowded earlier in the evening\n\n"
            "• Local Handicraft Market\n"
            "  - Best for: gifts and local crafts"
        )

    # Airport transfer quick path
    if any(x in q_lower for x in ("airport", "transfer", "pickup", "pick-up")):
        return (
            "Airport Transfer\n"
            "- Airport pickup and drop-off can be arranged through Reception.\n"
            "- Please share your flight number and arrival or departure time.\n"
            "- If you have large luggage, let Reception know in advance."
        )

    # Wi-Fi quick path
    if any(t in q_tokens for t in ("wifi", "wi-fi")):
        return (
            "Wi-Fi Access\n"
            "- Connect to the network: MagicalPalace-Guest\n"
            "- If a password is required, Reception will provide it (this may vary by booking).\n"
            "- If your device doesn’t connect, try forgetting the network and reconnecting."
        )

    # fallback behavior: up to 2 cards, concise formatting
    cards = retrieve_cards(query, k=2)

    if not cards:
        return (
            "Sorry, I couldn't find that in the Magical Palace guide.\n\n"
            "Try: 'breakfast menu', 'room service', 'wifi', 'check-out', 'spa booking', or 'nearby attractions'."
        )

    if len(cards) == 1:
        c = cards[0]
        bullets = [b.replace("\n", " ").strip() for b in c["bullets"]][:3]
        lines = [f"{c['title']}"]
        for b in bullets:
            lines.append(f"- {b}")
        return "\n".join(lines)

    lines = ["Here are some helpful items:"]
    for c in cards:
        first = c["bullets"][0].replace("\n", " ").strip()
        lines.append(f"- {c['title']}: {first}")

    return "\n".join(lines)


# -----------------------------
# Website UI (HTML + CSS + JS)
# Eye-catchy, modern glassy look
# -----------------------------
HTML_PAGE = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Magical Palace Concierge</title>
  <style>
    :root{
      --bg1:#0b1020;
      --bg2:#0b3a3f;
      --card: rgba(255,255,255,0.09);
      --card2: rgba(255,255,255,0.13);
      --text:#eef2ff;
      --muted: rgba(238,242,255,0.72);
      --border: rgba(255,255,255,0.14);

      --brand:#22c55e;     /* emerald */
      --brand2:#06b6d4;    /* cyan */
      --accent:#f59e0b;    /* gold */
      --danger:#fb7185;
    }

    *{box-sizing:border-box}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
      color:var(--text);
      background:
        radial-gradient(1200px 800px at 15% 10%, rgba(34,197,94,0.35), transparent 55%),
        radial-gradient(900px 700px at 90% 20%, rgba(6,182,212,0.35), transparent 55%),
        radial-gradient(1100px 900px at 60% 95%, rgba(245,158,11,0.20), transparent 55%),
        linear-gradient(180deg, var(--bg1), var(--bg2));
      min-height:100vh;
    }

    .wrap{
      max-width:1150px;
      margin:0 auto;
      padding:22px;
    }

    .top{
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:16px;
      margin-bottom:14px;
    }

    .brandline{
      display:flex;
      align-items:flex-start;
      gap:12px;
    }

    .logo{
      width:44px; height:44px;
      border-radius:14px;
      background: linear-gradient(135deg, rgba(34,197,94,0.95), rgba(6,182,212,0.95));
      box-shadow: 0 14px 30px rgba(0,0,0,0.35);
      display:flex; align-items:center; justify-content:center;
      font-weight:900;
      letter-spacing:-0.02em;
    }

    .title{
      font-size:24px;
      font-weight:800;
      letter-spacing:-0.02em;
      line-height:1.05;
    }

    .subtitle{
      margin-top:6px;
      color:var(--muted);
      font-size:13px;
      max-width:580px;
    }

    .badge{
      display:flex;
      align-items:center;
      gap:8px;
      background: rgba(34,197,94,0.18);
      color: var(--text);
      border:1px solid rgba(34,197,94,0.26);
      border-radius:999px;
      padding:8px 12px;
      font-size:12px;
      font-weight:700;
    }

    .dot{
      width:8px; height:8px; border-radius:999px;
      background: var(--brand);
      box-shadow: 0 0 0 4px rgba(34,197,94,0.18);
    }

    .grid{
      display:grid;
      grid-template-columns: 320px 1fr;
      gap:14px;
    }

    @media (max-width: 950px){
      .grid{grid-template-columns:1fr}
    }

    .panel{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius:22px;
      padding:14px;
      box-shadow: 0 18px 55px rgba(0,0,0,0.35);
      backdrop-filter: blur(12px);
    }

    .panel h3{
      margin:0 0 10px 0;
      font-size:12px;
      font-weight:900;
      letter-spacing:0.08em;
      text-transform:uppercase;
      color: rgba(238,242,255,0.88);
    }

    .quick{
      display:grid;
      grid-template-columns: 1fr;
      gap:9px;
    }

    .quick button{
      width:100%;
      text-align:left;
      border: 1px solid rgba(255,255,255,0.14);
      background: rgba(255,255,255,0.08);
      color: var(--text);
      border-radius:16px;
      padding:12px 12px;
      cursor:pointer;
      font-size:13px;
      font-weight:700;
      transition: transform .05s ease, background .15s ease, border-color .15s ease;
    }

    .quick button:hover{
      background: rgba(255,255,255,0.12);
      border-color: rgba(255,255,255,0.22);
    }

    .quick button:active{ transform: translateY(1px); }

    .tip{
      margin-top:12px;
      border-radius:18px;
      padding:12px;
      background: rgba(6,182,212,0.10);
      border: 1px solid rgba(6,182,212,0.18);
      font-size:13px;
      color: rgba(238,242,255,0.9);
    }

    .tip b{
      display:block;
      margin-bottom:6px;
      color: rgba(238,242,255,0.95);
    }

    .chiprow{
      display:flex;
      flex-wrap:wrap;
      gap:8px;
      margin-top:10px;
    }

    .chip{
      padding:8px 10px;
      border-radius:999px;
      border:1px solid rgba(255,255,255,0.16);
      background: rgba(255,255,255,0.07);
      color: rgba(238,242,255,0.9);
      font-size:12px;
      cursor:pointer;
      font-weight:700;
    }

    .chip:hover{ background: rgba(255,255,255,0.11); }

    .chat{
      display:flex;
      flex-direction:column;
      height:74vh;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius:22px;
      box-shadow: 0 18px 55px rgba(0,0,0,0.35);
      overflow:hidden;
      backdrop-filter: blur(12px);
    }

    .chathead{
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding:14px 14px 10px 14px;
      border-bottom:1px solid rgba(255,255,255,0.10);
      background: rgba(255,255,255,0.06);
    }

    .chathead .left{
      display:flex;
      align-items:center;
      gap:10px;
    }

    .avatar{
      width:34px; height:34px; border-radius:14px;
      background: linear-gradient(135deg, rgba(245,158,11,0.95), rgba(34,197,94,0.75));
      display:flex; align-items:center; justify-content:center;
      font-weight:900;
    }

    .chathead .name{
      font-size:13px;
      font-weight:900;
      letter-spacing:-0.01em;
    }

    .chathead .desc{
      margin-top:3px;
      font-size:12px;
      color: var(--muted);
      font-weight:600;
    }

    .pill{
      display:flex; align-items:center; gap:8px;
      padding:8px 12px;
      border-radius:999px;
      border:1px solid rgba(255,255,255,0.14);
      background: rgba(255,255,255,0.07);
      font-size:12px;
      font-weight:800;
      color: rgba(238,242,255,0.9);
    }

    .messages{
      padding:14px;
      flex:1;
      overflow:auto;
    }

    .row{display:flex; margin-bottom:12px}
    .row.user{justify-content:flex-end}

    .bubble{
      max-width: 86%;
      padding: 12px 14px;
      border-radius: 18px;
      font-size: 14px;
      line-height: 1.38;
      white-space: pre-wrap;
      border: 1px solid rgba(255,255,255,0.12);
    }

    .bubble.user{
      background: linear-gradient(135deg, rgba(34,197,94,0.92), rgba(6,182,212,0.78));
      color: #071018;
      border-top-right-radius: 8px;
      font-weight:800;
    }

    .bubble.bot{
      background: rgba(255,255,255,0.08);
      color: rgba(238,242,255,0.95);
      border-top-left-radius: 8px;
    }

    .composer{
      border-top:1px solid rgba(255,255,255,0.10);
      padding:12px;
      display:flex;
      gap:10px;
      background: rgba(255,255,255,0.06);
      align-items:center;
    }

    input{
      flex:1;
      padding:12px 12px;
      border-radius:16px;
      border:1px solid rgba(255,255,255,0.14);
      background: rgba(11,16,32,0.35);
      color: rgba(238,242,255,0.95);
      font-size:14px;
      outline:none;
    }

    input::placeholder{ color: rgba(238,242,255,0.55); }

    input:focus{
      box-shadow: 0 0 0 3px rgba(6,182,212,0.25);
      border-color: rgba(6,182,212,0.35);
    }

    .send{
      background: linear-gradient(135deg, rgba(245,158,11,0.95), rgba(251,191,36,0.85));
      color: #1b1200;
      border:none;
      border-radius:16px;
      padding:12px 14px;
      font-weight:900;
      cursor:pointer;
      font-size:14px;
      box-shadow: 0 10px 24px rgba(0,0,0,0.25);
      transition: transform .05s ease, filter .15s ease;
    }

    .send:hover{ filter: brightness(1.03); }
    .send:active{ transform: translateY(1px); }
    .send:disabled{ opacity:0.6; cursor:not-allowed; }

    .small{
      padding:0 14px 12px 14px;
      color: rgba(238,242,255,0.70);
      font-size:12px;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <div class="brandline">
        <div class="logo">MP</div>
        <div>
          <div class="title">Magical Palace Concierge ✨</div>
          <div class="subtitle">Fast, friendly help for hotel services, room service, and nearby attractions — powered by the hotel’s quick guide.</div>
        </div>
      </div>
      <div class="badge"><span class="dot"></span> Online</div>
    </div>

    <div class="grid">
      <div class="panel">
        <h3>Quick help</h3>

        <div class="quick">
          <button onclick="quickAsk('What time is check-in and check-out?')">🕑 Check-in / Check-out</button>
          <button onclick="quickAsk('Show breakfast menu')">🍳 Breakfast menu</button>
          <button onclick="quickAsk('How do I get Wi-Fi?')">📶 Wi-Fi help</button>
          <button onclick="quickAsk('Show room service menu')">🛎️ Room service</button>
          <button onclick="quickAsk('Suggest nearby attractions')">🗺️ Nearby attractions</button>
          <button onclick="quickAsk('How do I book an airport transfer?')">🚕 Airport transfer</button>
        </div>

        <div class="tip">
          <b>Tip</b>
          Try: “breakfast menu”, “room service menu”, “late checkout”, “spa booking”, “nearby attractions”.
          <div class="chiprow">
            <div class="chip" onclick="quickAsk('Breakfast menu')">Breakfast</div>
            <div class="chip" onclick="quickAsk('Room service menu')">Room service</div>
            <div class="chip" onclick="quickAsk('Wi-Fi help')">Wi-Fi</div>
            <div class="chip" onclick="quickAsk('Nearby attractions')">Attractions</div>
          </div>
        </div>
      </div>

      <div class="chat">
        <div class="chathead">
          <div class="left">
            <div class="avatar">✨</div>
            <div>
              <div class="name">Concierge Assistant</div>
              <div class="desc">Ask for menus, timings, and guest help</div>
            </div>
          </div>
          <div class="pill">Magical Palace</div>
        </div>

        <div id="messages" class="messages"></div>

        <div class="composer">
          <input id="input" placeholder="Ask: breakfast menu, room service, Wi-Fi, airport transfer…" />
          <button id="send" class="send" onclick="send()">Send</button>
        </div>

        <div class="small">Magical Palace • Responses use the hotel’s compressed guide data</div>
      </div>
    </div>
  </div>

  <script>
    const messagesEl = document.getElementById("messages");
    const inputEl = document.getElementById("input");
    const sendBtn = document.getElementById("send");

    function addBubble(text, who){
      const row = document.createElement("div");
      row.className = "row " + (who === "user" ? "user" : "bot");
      const bubble = document.createElement("div");
      bubble.className = "bubble " + (who === "user" ? "user" : "bot");
      bubble.textContent = text;
      row.appendChild(bubble);
      messagesEl.appendChild(row);
      messagesEl.scrollTop = messagesEl.scrollHeight;
      return bubble;
    }

    addBubble("Welcome to Magical Palace ✨\n\nAsk me about hotel services, policies, room service, or nearby attractions.", "bot");

    inputEl.addEventListener("keydown", (e) => {
      if(e.key === "Enter") send();
    });

    function quickAsk(q){
      inputEl.value = q;
      send();
    }

    async function send(){
      const q = (inputEl.value || "").trim();
      if(!q) return;

      inputEl.value = "";
      addBubble(q, "user");

      sendBtn.disabled = true;

      const botBubble = addBubble("Typing…", "bot");

      try{
        // Use JSON endpoint for reliability (still keeps /chat/stream available)
        const resp = await fetch("/chat", {
          method: "POST",
          headers: {"Content-Type":"application/json"},
          body: JSON.stringify({message:q})
        });

        const json = await resp.json();
        botBubble.textContent = (json.answer || "No answer.");
      }catch(e){
        botBubble.textContent = "Server error. Make sure the app is running.";
      }

      sendBtn.disabled = false;
    }
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE


@app.post("/chat/stream")
async def chat_stream(payload: Dict[str, Any]):
    msg = (payload.get("message") or "").strip()
    if not msg:
        async def empty_gen():
            yield "data: Please type a question.\n\n"
            yield "data: [DONE]\n\n"
        return EventSourceResponse(empty_gen())

    key = msg.lower()
    cached = cache_get(key)
    if cached is not None:
        async def cached_gen():
            yield f"data: {cached}\n\n"
            yield "data: [DONE]\n\n"
        return EventSourceResponse(cached_gen())

    answer = build_answer(msg)
    cache_set(key, answer)

    async def gen():
        chunk = 80
        for i in range(0, len(answer), chunk):
            piece = answer[i:i+chunk]
            piece = piece.replace("\r", "")
            piece = piece.replace("\n", "\n" + "data: ")
            yield f"data: {piece}\n\n"
            await asyncio.sleep(0.02)
        yield "data: [DONE]\n\n"

    return EventSourceResponse(gen())


@app.post("/chat")
async def chat(payload: Dict[str, Any]):
    msg = (payload.get("message") or "").strip()
    return {"answer": build_answer(msg)}
