# HotelConciergeChatbot-GEN-AI-

# Add this at the top of your HTML_PAGE string in app.py
# I've added a 'View Logic' button and a Mermaid.js modal.

HTML_PAGE = r"""
<!doctype html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({ startOnLoad: true, theme: 'dark' });</script>
  <style>
    /* New Styles for Flowcharts */
    .modal { display:none; position:fixed; z-index:100; left:0; top:0; width:100%; height:100%; background:rgba(0,0,0,0.8); backdrop-filter:blur(5px); overflow:auto; }
    .modal-content { background:var(--bg1); margin:5% auto; padding:20px; border:1px solid var(--border); width:90%; max-width:900px; border-radius:22px; }
    .close { color:var(--text); float:right; font-size:28px; cursor:pointer; }
    .mermaid { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top">
       <button onclick="document.getElementById('flowModal').style.display='block'" class="pill" style="cursor:pointer">view Architecture 🧠</button>
    </div>

    <div id="flowModal" class="modal">
      <div class="modal-content">
        <span class="close" onclick="document.getElementById('flowModal').style.display='none'">&times;</span>
        <h2 style="margin-top:0">System Architecture</h2>
        <div class="mermaid">
            flowchart TD
                A[Guest] --> B[FastAPI Backend]
                B --> C{Cached?}
                C -- Yes --> D[Instant Return]
                C -- No --> E[Intent Scraper]
                E --> F[Knowledge Cards]
                F --> G[JSON/SSE Response]
        </div>
      </div>
    </div>
  </div>
  </body>
</html>
"""


🏨 Magical Palace Concierge
A High-Performance, Lightweight Hospitality Chatbot built with FastAPI.

Magical Palace Concierge is a production-ready, single-file hospitality assistant. It leverages an intent-based retrieval system to provide guests with instant information regarding hotel services, menus, and local attractions without the latency or cost of external LLM APIs.

🚀 Key Features
⚡ Sub-10ms Latency: Uses an in-memory TTL cache and keyword token overlap scoring for near-instant responses.

💎 Modern UI: A sleek, "glassmorphism" interface built with Vanilla JS and CSS—no heavy frontend frameworks required.

📡 Hybrid Communication: Supports both standard JSON POST requests and Server-Sent Events (SSE) for streaming responses.

📦 Zero-Dependency AI: Pre-configured "Knowledge Cards" allow for intelligent matching without expensive GPU or API requirements.

🛠️ Deploy-Ready: Single app.py structure makes it ideal for Docker, Heroku, or AWS Lambda deployments.

🏗️ System Architecture
High-Level Interaction
The system follows a reactive pattern where user queries are tokenized and matched against a local knowledge base.


flowchart LR
    User((Guest)) -->|HTTPS| API[FastAPI Gateway]
    API --> Cache{TTL Cache}
    Cache -->|Miss| Engine[Intent Engine]
    Engine --> Cards[(Knowledge Cards)]
    Cards --> UI[Glass UI]

    Layer,Technology
Backend,"Python 3.9+, FastAPI"
Frontend,"HTML5, CSS3 (Flex/Grid), Vanilla JavaScript"
Streaming,SSE (Server-Sent Events) via sse-starlette
Caching,In-memory Dictionary with TTL (Time-To-Live)

