from flask import Flask, render_template_string

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Python CI/CD with Jenkins, Docker & Kubernetes</title>
    <style>
        :root {
            --bg1: #0f172a;
            --bg2: #020617;
            --accent: #22c55e;
            --accent2: #38bdf8;
            --text: #e5e7eb;
            --muted: #9ca3af;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        body {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: radial-gradient(circle at top, #1e293b 0, var(--bg2) 45%, black 100%);
            color: var(--text);
            overflow: hidden;
        }

        .glow-orb {
            position: fixed;
            width: 420px;
            height: 420px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(56,189,248,0.18), transparent 60%);
            filter: blur(6px);
            animation: float 12s ease-in-out infinite alternate;
            top: -80px;
            right: -60px;
            pointer-events: none;
        }

        .container {
            position: relative;
            width: min(960px, 100%);
            padding: 32px;
            border-radius: 24px;
            border: 1px solid rgba(148,163,184,0.3);
            background: radial-gradient(circle at top left, rgba(34,197,94,0.12), rgba(15,23,42,0.96));
            box-shadow:
                0 18px 40px rgba(15,23,42,0.85),
                0 0 0 1px rgba(15,23,42,0.9);
            overflow: hidden;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }

        .title-block h1 {
            font-size: 1.9rem;
            letter-spacing: 0.04em;
        }

        .title-block p {
            color: var(--muted);
            margin-top: 6px;
            font-size: 0.95rem;
        }

        .status-pill {
            padding: 8px 14px;
            border-radius: 999px;
            border: 1px solid rgba(74,222,128,0.4);
            background: linear-gradient(to right, rgba(22,163,74,0.2), rgba(34,197,94,0.1));
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            color: #bbf7d0;
            box-shadow: 0 0 32px rgba(22,163,74,0.35);
        }

        .dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: #22c55e;
            box-shadow: 0 0 12px rgba(74,222,128,0.9);
            animation: pulse 1.4s infinite;
        }

        .content {
            display: grid;
            grid-template-columns: 2.1fr 1.3fr;
            gap: 18px;
        }

        .card {
            border-radius: 18px;
            padding: 16px 18px;
            background: rgba(15,23,42,0.92);
            border: 1px solid rgba(51,65,85,0.9);
            backdrop-filter: blur(18px);
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at top left, rgba(34,197,94,0.26), transparent 55%);
            opacity: 0;
            transition: opacity 0.5s ease;
            pointer-events: none;
        }

        .card:hover::before {
            opacity: 1;
        }

        .card h2 {
            font-size: 1rem;
            margin-bottom: 8px;
        }

        .subtitle {
            font-size: 0.82rem;
            color: var(--muted);
            margin-bottom: 10px;
        }

        /* Animated pipeline */
        .pipeline {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 6px;
            flex-wrap: wrap;
        }

        .step {
            position: relative;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(148,163,184,0.5);
            font-size: 0.78rem;
            display: flex;
            align-items: center;
            gap: 6px;
            overflow: hidden;
        }

        .step span.icon {
            font-size: 0.9rem;
        }

        .step::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, transparent, rgba(248,250,252,0.18), transparent);
            transform: translateX(-120%);
            animation: shimmer 4s infinite;
        }

        .arrow {
            font-size: 1.1rem;
            color: var(--muted);
        }

        /* Code block */
        .code-block {
            font-family: "Fira Code", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 0.8rem;
            line-height: 1.55;
            padding: 12px 14px;
            border-radius: 14px;
            background: radial-gradient(circle at top left, rgba(15,118,110,0.28), rgba(15,23,42,1));
            color: #e5e7eb;
            position: relative;
            overflow: hidden;
        }

        .code-block::before {
            content: "app.py";
            position: absolute;
            top: 6px;
            right: 10px;
            font-size: 0.7rem;
            color: rgba(148,163,184,0.85);
        }

        .code-line {
            opacity: 0;
            transform: translateX(-8px);
            animation: typeIn 0.45s forwards;
        }

        .code-line:nth-child(1)  { animation-delay: 0.05s; }
        .code-line:nth-child(2)  { animation-delay: 0.18s; }
        .code-line:nth-child(3)  { animation-delay: 0.31s; }
        .code-line:nth-child(4)  { animation-delay: 0.44s; }
        .code-line:nth-child(5)  { animation-delay: 0.57s; }
        .code-line:nth-child(6)  { animation-delay: 0.70s; }
        .code-line:nth-child(7)  { animation-delay: 0.83s; }
        .code-line:nth-child(8)  { animation-delay: 0.96s; }
        .code-line:nth-child(9)  { animation-delay: 1.09s; }

        .kw { color: #38bdf8; }
        .fn { color: #22c55e; }
        .str { color: #fbbf24; }

        /* Right column items */
        .badge-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 6px;
            font-size: 0.8rem;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(148,163,184,0.5);
            color: var(--muted);
        }

        .pill-dot {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: var(--accent2);
            box-shadow: 0 0 10px rgba(56,189,248,0.9);
        }

        .footer {
            margin-top: 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.78rem;
            color: var(--muted);
        }

        .tag {
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px dashed rgba(148,163,184,0.6);
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.25); opacity: 0.5; }
        }

        @keyframes float {
            0% { transform: translate3d(0, 0, 0); }
            100% { transform: translate3d(-40px, 30px, 0); }
        }

        @keyframes shimmer {
            0% { transform: translateX(-130%); }
            100% { transform: translateX(130%); }
        }

        @keyframes typeIn {
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @media (max-width: 780px) {
            body {
                padding: 16px;
            }
            .container {
                padding: 18px;
            }
            .content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="glow-orb"></div>

    <div class="container">
        <div class="header">
            <div class="title-block">
                <h1>Python CI/CD Project</h1>
                <p>Flask · Jenkins · Docker · Kubernetes — with a live animated UI.</p>
            </div>
            <div class="status-pill">
                <div class="dot"></div>
                <span>Pipeline: <strong>Healthy &amp; Deployed</strong></span>
            </div>
        </div>

        <div class="content">
            <!-- LEFT: code + pipeline -->
            <div class="card">
                <h2>app.py – Flask entrypoint</h2>
                <p class="subtitle">
                    This is the Python application you package into a Docker image and deploy with Jenkins.
                </p>

                <div class="code-block">
                    <div class="code-line"><span class="kw">from</span> flask <span class="kw">import</span> Flask</div>
                    <div class="code-line">&nbsp;</div>
                    <div class="code-line">app = Flask(<span class="str">__name__</span>)</div>
                    <div class="code-line">&nbsp;</div>
                    <div class="code-line">@app.route(<span class="str">"/"</span>)</div>
                    <div class="code-line"><span class="kw">def</span> <span class="fn">home</span>():</div>
                    <div class="code-line">&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">return</span> <span class="str">"Hello from Python CI/CD Project deployed using Jenkins + Docker + Kubernetes!"</span></div>
                    <div class="code-line">&nbsp;</div>
                    <div class="code-line"><span class="kw">if</span> <span class="str">"__name__"</span> == <span class="str">"__main__"</span>:</div>
                    <div class="code-line">&nbsp;&nbsp;&nbsp;&nbsp;app.run(host=<span class="str">"0.0.0.0"</span>, port=5000)</div>
                </div>

                <div class="pipeline">
                    <div class="step">
                        <span class="icon">💻</span> Code Commit
                    </div>
                    <div class="arrow">➜</div>
                    <div class="step">
                        <span class="icon">⚙️</span> Jenkins CI
                    </div>
                    <div class="arrow">➜</div>
                    <div class="step">
                        <span class="icon">🐳</span> Docker Image
                    </div>
                    <div class="arrow">➜</div>
                    <div class="step">
                        <span class="icon">☸️</span> K8s Deployment
                    </div>
                </div>
            </div>

            <!-- RIGHT: quick info -->
            <div class="card">
                <h2>Deployment Snapshot</h2>
                <p class="subtitle">
                    Quick view of your live stack for demos and portfolios.
                </p>

                <div class="badge-list">
                    <div class="badge">
                        <span class="pill-dot"></span>
                        <span><strong>Flask</strong> web app listening on port 5000</span>
                    </div>
                    <div class="badge">
                        <span class="pill-dot"></span>
                        <span><strong>Docker</strong> image built from <code>Dockerfile</code></span>
                    </div>
                    <div class="badge">
                        <span class="pill-dot"></span>
                        <span><strong>Jenkins</strong> pipeline: build → test → push → deploy</span>
                    </div>
                    <div class="badge">
                        <span class="pill-dot"></span>
                        <span><strong>Kubernetes</strong> Deployment + NodePort Service</span>
                    </div>
                </div>

                <div class="footer">
                    <span>Message: <strong>"Hello from Python CI/CD Project"</strong></span>
                    <span class="tag">Perfect for DevOps portfolio 🚀</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    # Returns animated HTML UI
    return render_template_string(TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
