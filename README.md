# Nvisco Engine

An automation script that supports the Nvisco website. It audits site pages, drafts search optimized articles, submits updated URLs to search engines and alerts the team to public requests for hardware help. It runs on a schedule through GitHub Actions.

## Functions

| Function | Description |
|---|---|
| Site audit | Checks each HTML page for a title, meta description and structured data, then scores page health |
| Content drafting | Uses the Gemini API to write articles on PCB design, hardware development and robotics firmware, and adds them to `sitemap.xml` |
| Search submission | Sends new and updated URLs to search engines through IndexNow |
| Lead alerts | Scans Hacker News and selected Reddit communities for people seeking hardware contractors and emails an alert |
| Dashboard | Generates `dashboard.html` with site health and page audit results |

## Configuration

Set these as GitHub repository secrets:

| Secret | Purpose |
|---|---|
| `GEMINI_API_KEY` | Content drafting |
| `GMAIL_ADDRESS` | Account that receives lead alerts |
| `GMAIL_APP_PASSWORD` | Gmail App Password for sending alerts |
| `INDEXNOW_KEY` | Key for IndexNow submissions |

Features that need a missing secret are skipped.

## Running

The workflow in `.github/workflows/nvisco_runner.yml` runs twice a day and can also be started manually from the Actions tab. To run it locally:

```bash
pip install requests
python nvisco_engine.py
```

## Author

Zain Haider, Founder of [Nvisco](https://nvisco.com).
