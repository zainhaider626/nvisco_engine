import os
import json
import uuid
import smtplib
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ================= CONFIGURATION =================
DOMAIN = "www.nvisco.com"
SITE_URL = f"https://{DOMAIN}"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GMAIL_USER = "nvisco.pak@gmail.com"
GMAIL_APP_PASS = os.getenv("GMAIL_APP_PASS")
RECIPIENT_EMAIL = "nvisco.pak@gmail.com"

INDEXNOW_KEY = os.getenv("INDEXNOW_KEY", str(uuid.uuid4()).replace("-", ""))

# ================= GMAIL NOTIFICATION ENGINE =================
def send_email_alert(subject, body, link=""):
    """Dispatches lead alerts straight to nvisco.pak@gmail.com."""
    if not GMAIL_APP_PASS:
        print("[!] GMAIL_APP_PASS secret is missing. Email skipped.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = f"Nvisco Bot <{GMAIL_USER}>"
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"🚀 NVISCO Lead Alert: {subject}"

        formatted_content = f"""Hello NVISCO Team,

A prospective hardware client inquiry has been detected!

TOPIC / REQUEST:
{subject}

DETAILS:
{body}

DIRECT POST LINK:
{link}

---------------------------------------------------
This email was generated 24/7 by the NVISCO Autonomous Engine.
"""
        msg.attach(MIMEText(formatted_content, 'plain'))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASS)
            server.send_message(msg)
        print(f"[+] Alert successfully emailed to {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"[!] Email send error: {e}")

# ================= SITE AUDIT & AUTO-FIXER =================
def audit_and_autofix():
    print("[*] Running Site Audit & Auto-Fixer...")
    if not os.path.exists("robots.txt"):
        with open("robots.txt", "w") as f:
            f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
        print("[+] Created robots.txt")

    audit_results = []
    html_files = [f for f in os.listdir(".") if f.endswith(".html")]

    for page in html_files:
        with open(page, "r", encoding="utf-8") as f:
            content = f.read()

        issues = []
        if "<title>" not in content.lower():
            issues.append("Missing <title>")
        if 'name="description"' not in content.lower():
            issues.append("Missing meta description")
        if "application/ld+json" not in content.lower():
            issues.append("Missing Schema JSON-LD")

        audit_results.append({
            "file": page,
            "issues": issues,
            "score": max(20, 100 - (len(issues) * 25))
        })
    return audit_results

# ================= INSTANT INDEXNOW SUBMISSION =================
def ping_indexnow(urls):
    if not urls:
        return
    print(f"[*] Submitting {len(urls)} URLs to IndexNow (Bing/Yandex)...")
    key_file = f"{INDEXNOW_KEY}.txt"
    if not os.path.exists(key_file):
        with open(key_file, "w") as f:
            f.write(INDEXNOW_KEY)

    payload = {
        "host": DOMAIN,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{SITE_URL}/{key_file}",
        "urlList": urls
    }
    try:
        r = requests.post("https://api.indexnow.org/indexnow", json=payload, timeout=10)
        print(f"[+] IndexNow ping response: {r.status_code}")
    except Exception as e:
        print(f"[!] IndexNow error: {e}")

# ================= CONTENT ENGINE (16-LAYER PCB & ROBOTICS) =================
HIGH_INTENT_TOPICS = [
    {
        "title": "16-Layer High-Speed PCB Stackup & HDI Engineering Guide",
        "slug": "16-layer-pcb-design-stackup-guide",
        "desc": "Technical breakdown of 16-layer PCB stackups, differential pairs, microvias, and impedance control."
    },
    {
        "title": "Turnkey Hardware Development: Idea to Market Launch",
        "slug": "idea-to-product-hardware-development",
        "desc": "How NVISCO bridges 3D CAD design, custom multi-layer circuit boards, and firmware for production-ready robotics."
    },
    {
        "title": "Custom Embedded Firmware Architecture for Autonomous Robotics",
        "slug": "custom-robotics-firmware-architecture",
        "desc": "Designing deterministic real-time firmware for STM32, ESP32, and robotic motor control systems."
    }
]

def generate_targeted_content():
    if not GEMINI_API_KEY:
        return None

    topic = HIGH_INTENT_TOPICS[datetime.now().timetuple().tm_yday % len(HIGH_INTENT_TOPICS)]
    filename = f"{topic['slug']}.html"

    if os.path.exists(filename):
        return None

    print(f"[*] Drafting technical authority page: {topic['title']}")
    prompt = f"""
    Write an exhaustive 1,200-word engineering article titled '{topic['title']}' for NVISCO (www.nvisco.com).
    Topics: 16-layer PCB designs, HDI microvias, signal integrity, 3D CAD enclosures, firmware architecture.
    Format: Return semantic HTML body ONLY (<h2>, <h3>, <p>, <ul>, <li>, <code>, <table>). No markdown backticks.
    Tone: Professional hardware systems engineering team.
    """

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        res = requests.post(endpoint, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
        body = res.json()["candidates"][0]["content"]["parts"][0]["text"].replace("```html", "").replace("```", "").strip()

        schema = {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": topic["title"],
            "description": topic["desc"],
            "publisher": {"@type": "Organization", "name": "NVISCO", "url": SITE_URL}
        }

        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic['title']} | NVISCO</title>
    <meta name="description" content="{topic['desc']}">
    <link rel="canonical" href="{SITE_URL}/{filename}" />
    <script type="application/ld+json">{json.dumps(schema)}</script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.8; color: #1e293b; max-width: 840px; margin: 40px auto; padding: 0 20px; }}
        h1, h2, h3 {{ color: #0f172a; }}
        code {{ background: #f1f5f9; padding: 2px 5px; border-radius: 4px; }}
        .cta {{ background: #0f172a; color: #fff; padding: 25px; border-radius: 8px; margin-top: 40px; }}
        .cta a {{ color: #38bdf8; font-weight: bold; text-decoration: none; }}
    </style>
</head>
<body>
    <p><a href="{SITE_URL}">&larr; Return to NVISCO Official Home</a></p>
    <h1>{topic['title']}</h1>
    <p><em>Authored by NVISCO Intelligent Systems & Robotics Engineering</em></p>
    {body}
    <div class="cta">
        <h3>Need 16-Layer PCB Layout or Turnkey Robotics Development?</h3>
        <p>From initial concept sketches to certified, production-ready hardware, NVISCO handles the full engineering lifecycle.</p>
        <p><a href="{SITE_URL}">Start your hardware project with NVISCO &rarr;</a></p>
    </div>
</body>
</html>"""

        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_html)

        update_sitemap(filename)
        return f"{SITE_URL}/{filename}"
    except Exception as e:
        print(f"[!] Content error: {e}")
        return None

def update_sitemap(new_file):
    sitemap_path = "sitemap.xml"
    today = datetime.now().strftime("%Y-%m-%d")
    new_url = f"{SITE_URL}/{new_file}"

    if not os.path.exists(sitemap_path):
        root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    else:
        root = ET.parse(sitemap_path).getroot()

    for url in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc is not None and loc.text == new_url:
            return

    url_el = ET.SubElement(root, "url")
    ET.SubElement(url_el, "loc").text = new_url
    ET.SubElement(url_el, "lastmod").text = today
    ET.SubElement(url_el, "priority").text = "0.8"

    ET.ElementTree(root).write(sitemap_path, encoding="utf-8", xml_declaration=True)

# ================= HARDWARE LEAD FINDER (HACKER NEWS + REDDIT) =================
def find_leads_and_alert():
    print("[*] Searching public forums for hardware & PCB design clients...")
    
    # 1. Check Hacker News
    try:
        res = requests.get("https://hn.algolia.com/api/v1/search_by_date?query=pcb%20OR%20firmware&tags=comment,story", timeout=10).json()
        for hit in res.get("hits", [])[:5]:
            text = (hit.get("comment_text") or hit.get("title") or "").lower()
            if any(k in text for k in ["looking for", "hire", "need someone", "contractor", "freelance"]):
                story_id = hit.get("story_id") or hit.get("objectID")
                link = f"https://news.ycombinator.com/item?id={story_id}"
                send_email_alert(
                    subject="Hacker News Hardware Contractor Request",
                    body=f"Post: {hit.get('title') or 'Contracting Inquiry'}\nExcerpt: {text[:200]}...",
                    link=link
                )
                return
    except Exception as e:
        print(f"[!] HN scan error: {e}")

    # 2. Check Reddit
    subs = ["PrintedCircuitBoard", "embedded", "hardwarestartups"]
    headers = {"User-Agent": "NviscoLeadBot/1.0"}
    for s in subs:
        try:
            r = requests.get(f"https://www.reddit.com/r/{s}/new.json?limit=10", headers=headers, timeout=10)
            if r.status_code == 200:
                for post in r.json().get("data", {}).get("children", []):
                    p = post["data"]
                    text = (p.get("title", "") + " " + p.get("selftext", "")).lower()
                    if any(k in text for k in ["need pcb", "hire", "looking for an engineer", "firmware help"]):
                        send_email_alert(
                            subject=f"Reddit Inquiry on r/{s}: {p.get('title')}",
                            body=p.get('selftext', '')[:300] + "...",
                            link=f"https://reddit.com{p.get('permalink')}"
                        )
                        return
        except Exception as e:
            print(f"[!] Reddit scan error for r/{s}: {e}")

# ================= LIVE DASHBOARD =================
def build_dashboard(audit_data):
    total = len(audit_data)
    avg_score = int(sum(p["score"] for p in audit_data) / max(total, 1))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NVISCO Engine Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 24px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .metric-box {{ display: flex; gap: 20px; margin: 25px 0; }}
        .card {{ background: #1e293b; padding: 20px; border-radius: 8px; flex: 1; border: 1px solid #334155; }}
        .num {{ font-size: 2.2rem; font-weight: bold; color: #38bdf8; }}
        table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 8px; overflow: hidden; }}
        th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ background: #020617; color: #94a3b8; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>NVISCO 24/7 Engine Dashboard</h2>
        <p style="color: #94a3b8;">Alerts connected to: <strong>{GMAIL_USER}</strong></p>
        <div class="metric-box">
            <div class="card"><div>Site Health</div><div class="num">{avg_score}%</div></div>
            <div class="card"><div>Published Pages</div><div class="num">{total}</div></div>
        </div>
        <h3>Page Audits</h3>
        <table>
            <thead><tr><th>Page</th><th>Health</th><th>Notes</th></tr></thead>
            <tbody>
                {''.join(f"<tr><td><code>{p['file']}</code></td><td>{p['score']}%</td><td>{', '.join(p['issues']) if p['issues'] else 'Valid'}</td></tr>" for p in audit_data)}
            </tbody>
        </table>
    </div>
</body>
</html>"""
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    audit_data = audit_and_autofix()
    new_page = generate_targeted_content()
    urls = [f"{SITE_URL}/", f"{SITE_URL}/dashboard.html"]
    if new_page:
        urls.append(new_page)
    ping_indexnow(urls)
    find_leads_and_alert()
    build_dashboard(audit_data)
