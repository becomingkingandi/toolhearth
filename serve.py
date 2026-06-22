#!/usr/bin/env python3
"""
Tiny HTTP server that renders ~/cheat-sheet/cheat-sheet.md as styled HTML.
GET / → rendered cheat sheet
GET /raw → raw markdown
GET /sync → pull fresh copy from m5 then re-render (calls sync.sh)
"""

import html
import mimetypes
import os
import socketserver
import subprocess
from http.server import BaseHTTPRequestHandler
from pathlib import Path

import markdown

HOST = "0.0.0.0"
PORT = 8888
ROOT = Path(__file__).resolve().parent
MD_PATH = ROOT / "cheat-sheet.md"
PANEL_PATH = ROOT / "panel.md"
LEDGER_PATH = ROOT / "ledger.md"
PLRSHIPPED_PATH = ROOT / "plrshipped.md"
BUILD_PATH = ROOT / "build.md"
TOOLS_PATH = ROOT / "tools.md"
SKILLS_PATH = ROOT / "skills.md"
SYNC_SCRIPT = ROOT / "sync.sh"
TODAY_PATH = ROOT / "today.md"
TODOS_DIR = ROOT / "todos"
TODOS_HTML = TODOS_DIR / "monday.html"
TODOS_PATH = ROOT / "todos"
CLI_DIR = ROOT / "cli-cheat-sheet"
SCREENSHOTS_DIR = Path.home() / "Code" / "screenshots"

CSS = """
body { font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
       max-width: 980px; margin: 2em auto; padding: 0 1em;
       color: #1f2328; line-height: 1.55; background: #ffffff; }
h1, h2, h3 { border-bottom: 1px solid #d1d9e0; padding-bottom: .3em; margin-top: 1.5em; }
h1 { font-size: 2em; }
h2 { font-size: 1.5em; color: #0969da; }
code { background: #f6f8fa; padding: .2em .4em; border-radius: 6px; font-size: 85%;
       font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace; }
pre { background: #f6f8fa; padding: 1em; border-radius: 6px; overflow-x: auto; }
pre code { background: transparent; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #d1d9e0; padding: .5em .8em; text-align: left; }
th { background: #f6f8fa; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
blockquote { border-left: 4px solid #d1d9e0; padding: 0 1em; color: #59636e; margin-left: 0; }
.toolbar { background: #f6f8fa; padding: .5em 1em; border-radius: 6px; margin-bottom: 1em;
           display: flex; gap: 1em; font-size: 90%; }
.toolbar a.active { background: #ddf4ff; padding: .15em .5em; border-radius: 4px; font-weight: 600; }
"""


def split_sections(md):
    """Split markdown into (main_view, commands_view, reference_view).
    'commands_view' is the ## Quick commands section only.
    'reference_view' is the ## Reference section only.
    'main_view' is everything else."""
    parts = md.split("\n## ")
    if len(parts) <= 1:
        return md, "", ""
    preamble = parts[0]
    main_parts = [preamble]
    commands_section = ""
    reference_section = ""
    for p in parts[1:]:
        block = "## " + p
        if p.startswith("Quick commands"):
            commands_section = block
        elif p.startswith("Reference"):
            reference_section = block
        else:
            main_parts.append(block)
    return "\n".join(main_parts), commands_section, reference_section


def toolbar(active):
    def link(path, label, key):
        cls = ' class="active"' if key == active else ""
        return f'<a href="{path}"{cls}>{label}</a>'
    return (
        '<div class="toolbar">'
        + link("/", "📖 Main", "main")
        + link("/panel", "📋 Panel", "panel")
        + link("/todos", "✅ Todos", "todos")
        + link("/today", "⚡ Live", "today")
        + link("/ledger", "📒 Ledger", "ledger")
        + link("/plrshipped", "📕 PLR Shipped", "plrshipped")
        + link("/build", "🏗️ Build", "build")
        + link("/tools", "🔧 Tools", "tools")
        + link("/skills", "🧠 Skills", "skills")
        + link("/commands", "⌨️ Commands", "commands")
        + link("/reference", "📚 Reference", "reference")
        + link("/mem", "🔴 Mem", "mem")
        + link("/preview", "📸 Preview", "preview")
        + link("/cli", "📦 CLI Sheets", "cli")
        + link("/raw", "📄 Raw MD", "raw")
        + link("/sync", "🔄 Sync from m5", "sync")
        + "</div>"
    )


def render(view="main"):
    md = MD_PATH.read_text() if MD_PATH.exists() else "# Cheat sheet not found"
    main, commands, reference = split_sections(md)
    if view == "commands" and commands:
        content = commands
    elif view == "reference" and reference:
        content = reference
    else:
        content = main
    body = markdown.markdown(content, extensions=["fenced_code", "tables", "toc"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>m2 cheat sheet</title><style>{CSS}</style></head><body>{toolbar(view)}{body}</body></html>"""


def render_panel():
    md = PANEL_PATH.read_text() if PANEL_PATH.exists() else "# Panel not found"
    body = markdown.markdown(md, extensions=["fenced_code", "tables", "toc"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>What Claude needs from you</title><style>{CSS}</style></head><body>{toolbar("panel")}{body}</body></html>"""


def render_ledger():
    md = LEDGER_PATH.read_text() if LEDGER_PATH.exists() else "# Ledger not found"
    body = markdown.markdown(md, extensions=["fenced_code", "tables", "toc"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>The Ledger</title><style>{CSS}</style></head><body>{toolbar("ledger")}{body}</body></html>"""


def render_plrshipped():
    md = PLRSHIPPED_PATH.read_text() if PLRSHIPPED_PATH.exists() else "# PLR Shipped status not found"
    body = markdown.markdown(md, extensions=["fenced_code", "tables", "toc"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>PLR Shipped — launch status</title><style>{CSS}</style></head><body>{toolbar("plrshipped")}{body}</body></html>"""


def render_build():
    md = BUILD_PATH.read_text() if BUILD_PATH.exists() else "# Build workflow not found"
    body = markdown.markdown(md, extensions=["fenced_code", "tables", "toc"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Build Workflow</title><style>{CSS}</style></head><body>{toolbar("build")}{body}</body></html>"""


def render_tools():
    md = TOOLS_PATH.read_text() if TOOLS_PATH.exists() else "# Tools not found"
    body = markdown.markdown(md, extensions=["fenced_code", "tables", "toc"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>m2 Tools</title><style>{CSS}</style></head><body>{toolbar("tools")}{body}</body></html>"""


def render_skills():
    md = SKILLS_PATH.read_text() if SKILLS_PATH.exists() else "# Skills not found"
    body = markdown.markdown(md, extensions=["fenced_code", "tables", "toc"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Claude Skills</title><style>{CSS}</style></head><body>{toolbar("skills")}{body}</body></html>"""


def render_preview():
    desktop = SCREENSHOTS_DIR / "latest-desktop.png"
    mobile  = SCREENSHOTS_DIR / "latest-mobile.png"
    has_desktop = desktop.exists()
    has_mobile  = mobile.exists()
    if not has_desktop and not has_mobile:
        body = "<h1>📸 Preview</h1>\n<p>No screenshots yet. Run <code>webshot</code> on m2 after starting your dev server.</p><pre>webshot                      # default http://localhost:3000\\nwebshot http://localhost:5173</pre>"
    else:
        imgs = ""
        if has_desktop:
            mtime = desktop.stat().st_mtime
            import time
            age = int(time.time() - mtime)
            imgs += f'<h2>Desktop (1440px) — {age}s ago</h2><img src="/screenshots/latest-desktop.png" style="max-width:100%;border:1px solid #d1d9e0;border-radius:6px">'
        if has_mobile:
            imgs += f'<h2>Mobile (390px)</h2><img src="/screenshots/latest-mobile.png" style="max-width:390px;border:1px solid #d1d9e0;border-radius:6px">'
        body = f'<h1>📸 Preview</h1><p>Auto-refreshes every 8s. Run <code>webshot</code> after each change.</p>{imgs}'
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Preview</title><meta http-equiv="refresh" content="8"><style>{CSS}</style></head><body>{toolbar("preview")}{body}</body></html>"""


def render_mem():
    import json, time as _time
    STATUS = Path("/tmp/mem-status.json")
    ALERTS = Path("/tmp/mem-alerts.log")
    LOG    = Path("/tmp/mem-monitor.log")

    try:
        s = json.loads(STATUS.read_text())
    except Exception:
        s = None

    level_color = {"ok": "#16a34a", "warning": "#d97706", "alert": "#ea580c", "critical": "#dc2626"}
    level = s.get("level", "unknown") if s else "unknown"
    color = level_color.get(level, "#888")

    badge_css = f"display:inline-block;background:{color};color:#fff;border-radius:6px;padding:.3em .9em;font-weight:700;font-size:1.1em;margin:.3em 0"

    if s:
        ts_str = s.get("ts", "?")[:19].replace("T", " ")
        usable = s.get("usable_gb", 0)
        free   = s.get("free_gb", 0)
        inact  = s.get("inactive_gb", 0)
        wired  = s.get("wired_gb", 0)
        comp   = s.get("compressed_gb", 0)
        action = s.get("action") or ""
        top    = s.get("top_procs", [])

        bar_pct  = max(0, min(100, int(usable / 64 * 100)))
        bar_color = color
        bar_html = f'<div style="background:#e5e7eb;border-radius:6px;height:18px;width:100%;margin:.5em 0"><div style="background:{bar_color};height:18px;border-radius:6px;width:{bar_pct}%"></div></div>'

        top_rows = "".join(
            f"<tr><td>{p['name']}</td><td style='text-align:right'>{p['mb']:.0f} MB</td></tr>"
            for p in top
        )

        action_html = f'<p style="color:{color};font-weight:700">⚡ Action taken: {html.escape(action)}</p>' if action else ""

        body = f"""
<h1>🔴 m2 Memory Monitor</h1>
<p style="color:#888;font-size:.9em">Last check: {ts_str} &nbsp;|&nbsp; Auto-refreshes every 15s</p>
<p><span style="{badge_css}">{level.upper()}</span></p>
{action_html}
<h2>Current state</h2>
<table>
<tr><th>Metric</th><th>GB</th></tr>
<tr><td><strong>Usable (free + inactive)</strong></td><td><strong>{usable:.2f}</strong></td></tr>
<tr><td>Free pages</td><td>{free:.2f}</td></tr>
<tr><td>Inactive (reclaimable)</td><td>{inact:.2f}</td></tr>
<tr><td>Wired (pinned)</td><td>{wired:.2f}</td></tr>
<tr><td>Compressed pool</td><td>{comp:.2f}</td></tr>
</table>
{bar_html}
<p style="font-size:.8em;color:#888">Bar = usable / 64 GB total</p>
<h2>Top processes by RSS</h2>
<table><tr><th>Process</th><th>RSS</th></tr>{top_rows}</table>
<h2>Thresholds</h2>
<table>
<tr><th>Level</th><th>Trigger</th><th>Action</th></tr>
<tr style="color:#d97706"><td>warning</td><td>&lt; 4 GB usable</td><td>log only</td></tr>
<tr style="color:#ea580c"><td>alert</td><td>&lt; 2 GB usable</td><td>log + macOS notification</td></tr>
<tr style="color:#dc2626"><td>critical</td><td>&lt; 0.8 GB usable</td><td>SIGTERM ComfyUI + notify</td></tr>
</table>
"""
    else:
        body = "<h1>🔴 m2 Memory Monitor</h1><p>Status file not found — is mem-monitor running?</p><pre>launchctl load ~/Library/LaunchAgents/com.shemika.mem-monitor.plist</pre>"

    # Recent alerts
    if ALERTS.exists():
        lines = ALERTS.read_text().strip().splitlines()[-20:]
        if lines:
            body += "<h2>Recent alerts</h2><pre>" + html.escape("\n".join(lines)) + "</pre>"

    return f"""<!doctype html><html><head><meta charset="utf-8"><title>m2 Memory</title>
<meta http-equiv="refresh" content="15">
<style>{CSS}</style></head><body>{toolbar("mem")}{body}</body></html>"""


def render_cli_index():
    """Index page for the cloned milanaryal/cli-cheat-sheet repo."""
    md_files = sorted(p.name for p in CLI_DIR.glob("*.md")) if CLI_DIR.exists() else []
    pdf_files = sorted(p.name for p in CLI_DIR.glob("*.pdf")) if CLI_DIR.exists() else []
    if not md_files and not pdf_files:
        content = (
            "# CLI Cheat Sheet\n\nRepo not cloned yet. Run:\n\n```\n"
            f"git clone https://github.com/milanaryal/cli-cheat-sheet {CLI_DIR}\n```"
        )
    else:
        pages = "\n".join(f"- [{n}](/cli/{n})" for n in md_files)
        pdfs = "\n".join(f"- [{n}](/cli/{n})" for n in pdf_files)
        content = (
            "# CLI Cheat Sheet\n\n"
            "Full clone of [milanaryal/cli-cheat-sheet]"
            "(https://github.com/milanaryal/cli-cheat-sheet) — every page, served from m2.  \n"
            f"Refresh anytime: `cd {CLI_DIR} && git pull`.\n\n"
            "## Pages\n\n" + pages + "\n\n## PDF references\n\n" + pdfs + "\n"
        )
    body = markdown.markdown(content, extensions=["fenced_code", "tables", "toc"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>CLI Cheat Sheet</title><style>{CSS}</style></head><body>{toolbar("cli")}{body}</body></html>"""


def render_today():
    """Live status page — what's been done, what's in progress, what's next."""
    md = TODAY_PATH.read_text() if TODAY_PATH.exists() else "# Live Status\n\n*Nothing logged yet.*"
    body = markdown.markdown(md, extensions=["fenced_code", "tables", "toc"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>⚡ Live Status</title>
<meta http-equiv="refresh" content="30">
<style>{CSS}</style></head><body>{toolbar("today")}{body}</body></html>"""


def render_todos():
    """Serve monday.html wrapped in cheat-sheet chrome."""
    md_path = TODOS_HTML
    if not md_path.exists():
        return "<h1>Todos</h1><p>monday.html not found — run `scp` to push it from staging.</p>"
    html = md_path.read_text()
    # Inject into a clean page with toolbar
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Todos</title>
<style>{CSS}
body {{ max-width: 820px; }}
.block {{ border-radius: 8px; padding: 14px 16px; }}
</style></head><body>{toolbar("todos")}{html}</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self._send(200, "text/html; charset=utf-8", render("main"))
        elif self.path == "/panel" or self.path.startswith("/panel?"):
            self._send(200, "text/html; charset=utf-8", render_panel())
        elif self.path == "/todos" or self.path.startswith("/todos?"):
            self._send(200, "text/html; charset=utf-8", render_todos())
        elif self.path == "/today" or self.path.startswith("/today?"):
            self._send(200, "text/html; charset=utf-8", render_today())
        elif self.path == "/ledger" or self.path.startswith("/ledger?"):
            self._send(200, "text/html; charset=utf-8", render_ledger())
        elif self.path == "/plrshipped" or self.path.startswith("/plrshipped?"):
            self._send(200, "text/html; charset=utf-8", render_plrshipped())
        elif self.path == "/build" or self.path.startswith("/build?"):
            self._send(200, "text/html; charset=utf-8", render_build())
        elif self.path == "/tools" or self.path.startswith("/tools?"):
            self._send(200, "text/html; charset=utf-8", render_tools())
        elif self.path == "/skills" or self.path.startswith("/skills?"):
            self._send(200, "text/html; charset=utf-8", render_skills())
        elif self.path == "/mem" or self.path.startswith("/mem?"):
            self._send(200, "text/html; charset=utf-8", render_mem())
        elif self.path == "/commands" or self.path.startswith("/commands?"):
            self._send(200, "text/html; charset=utf-8", render("commands"))
        elif self.path == "/reference" or self.path.startswith("/reference?"):
            self._send(200, "text/html; charset=utf-8", render("reference"))
        elif self.path == "/preview" or self.path.startswith("/preview?"):
            self._send(200, "text/html; charset=utf-8", render_preview())
        elif self.path.startswith("/screenshots/"):
            self._serve_screenshot()
        elif self.path == "/cli" or self.path.startswith("/cli?"):
            self._send(200, "text/html; charset=utf-8", render_cli_index())
        elif self.path.startswith("/cli/"):
            self._serve_cli_file()
        elif self.path == "/raw":
            self._send(200, "text/plain; charset=utf-8", MD_PATH.read_text() if MD_PATH.exists() else "")
        elif self.path in ("/meme-temp", "/meme-temp.html"):
            try:
                result = subprocess.run(["python3", os.path.expanduser("~/bin/meme-temp"), "--html"],
                                        capture_output=True, text=True, timeout=20)
                if result.returncode == 0:
                    self._send(200, "text/html; charset=utf-8", result.stdout)
                else:
                    self._send(500, "text/plain", f"meme-temp failed: {result.stderr[:200]}")
            except Exception as e:
                self._send(500, "text/plain", f"meme-temp error: {e}")
        elif self.path in ("/bloomberg-term", "/bloomberg-term.html", "/bb"):
            try:
                result = subprocess.run(["python3", os.path.expanduser("~/bin/bloomberg-term"), "--html"],
                                        capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    self._send(200, "text/html; charset=utf-8", result.stdout)
                else:
                    self._send(500, "text/plain", f"bloomberg-term failed: {result.stderr[:200]}")
            except Exception as e:
                self._send(500, "text/plain", f"bloomberg-term error: {e}")
        elif self.path == "/sync":
            try:
                result = subprocess.run(["bash", str(SYNC_SCRIPT)], capture_output=True, text=True, timeout=15)
                msg = f"$ {SYNC_SCRIPT}\n\nstdout:\n{result.stdout}\n\nstderr:\n{result.stderr}\n\nexit={result.returncode}"
                self._send(200, "text/plain; charset=utf-8", msg)
            except Exception as e:
                self._send(500, "text/plain; charset=utf-8", f"sync failed: {e}")
        elif self.path in ("/boring-portfolio", "/boring-portfolio.html"):
            self._serve_static_html("boring-portfolio.html")
        elif self.path in ("/boring-calculators", "/boring-calculators.html"):
            self._serve_static_html("boring-calculators.html")
        elif self.path.startswith("/yt2site-"):
            fname = self.path.lstrip("/").split("?")[0]
            self._serve_static_html(fname)
        elif self.path.startswith("/affiliate-"):
            fname = self.path.lstrip("/").split("?")[0]
            self._serve_static_html(fname)
        elif self.path.startswith("/boring-"):
            fname = self.path.lstrip("/").split("?")[0]
            self._serve_static_html(fname)
        elif self.path.startswith("/unit-converter"):
            fname = "unit-converter.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/niche-directory"):
            fname = "niche-directory.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/template-marketplace"):
            fname = "template-marketplace.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/remote-ai-jobs-board"):
            fname = "remote-ai-jobs-board.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/seo-meta-generator"):
            fname = "seo-meta-generator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/what-is-my-ip"):
            fname = "what-is-my-ip.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/white-screen"):
            fname = "white-screen.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/currency-converter"):
            fname = "currency-converter.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/inches-to-feet"):
            fname = "inches-to-feet.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/km-to-miles"):
            fname = "km-to-miles.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/mm-to-inches"):
            fname = "mm-to-inches.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/pdf-compress"):
            fname = "pdf-compress.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/pdf-to-word"):
            fname = "pdf-to-word.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/pdf-to-jpeg"):
            fname = "pdf-to-jpeg.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/ai-content-repurposing"):
            fname = "ai-content-repurposing.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/ai-voice-agent"):
            fname = "ai-voice-agent.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/ai-lead-gen"):
            fname = "ai-lead-gen.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/ai-consulting"):
            fname = "ai-consulting.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/virtual-assistant-agency"):
            fname = "virtual-assistant-agency.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/christmas-planning"):
            fname = "christmas-planning.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/typing-test"):
            fname = "typing-test.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/budget-calculator"):
            fname = "budget-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/mortgage-calculator"):
            fname = "mortgage-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/sleep-calculator"):
            fname = "sleep-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/jwt-decoder"):
            fname = "jwt-decoder.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/diff-checker"):
            fname = "diff-checker.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/color-converter"):
            fname = "color-converter.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/url-encoder"):
            fname = "url-encoder.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/yaml-json-converter"):
            fname = "yaml-json-converter.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/qr-generator"):
            fname = "qr-generator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/json-formatter"):
            fname = "json-formatter.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/base64-encoder"):
            fname = "base64-encoder.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/uuid-generator"):
            fname = "uuid-generator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/lorem-ipsum"):
            fname = "lorem-ipsum.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/text-case-converter"):
            fname = "text-case-converter.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/word-counter"):
            fname = "word-counter.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/list-randomizer"):
            fname = "list-randomizer.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/regex-tester"):
            fname = "regex-tester.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/html-entities"):
            fname = "html-entities.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/color-palette"):
            fname = "color-palette.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/gradient-builder"):
            fname = "gradient-builder.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/typography-tester"):
            fname = "typography-tester.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/box-shadow"):
            fname = "box-shadow.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/grid-layout"):
            fname = "grid-layout.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/joke-generator"):
            fname = "joke-generator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/random-quote"):
            fname = "random-quote.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/weather"):
            fname = "weather.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/bitcoin-price"):
            fname = "bitcoin-price.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/random-fact"):
            fname = "random-fact.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/dictionary"):
            fname = "dictionary.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/github-profile"):
            fname = "github-profile.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/hacker-news"):
            fname = "hacker-news.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/dog-pics"):
            fname = "dog-pics.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/cat-facts"):
            fname = "cat-facts.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/world-clock"):
            fname = "world-clock.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/country-lookup"):
            fname = "country-lookup.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/timezone-converter"):
            fname = "timezone-converter.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/mime-types"):
            fname = "mime-types.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/browser-info"):
            fname = "browser-info.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/compound-interest-calculator"):
            fname = "compound-interest-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/investment-returns-calculator"):
            fname = "investment-returns-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/debt-payoff-calculator"):
            fname = "debt-payoff-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/retirement-calculator"):
            fname = "retirement-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/anime-quotes"):
            fname = "anime-quotes.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/ascii-table"):
            fname = "ascii-table.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/base64"):
            fname = "base64.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/bible-verse"):
            fname = "bible-verse.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/binary-translator"):
            fname = "binary-translator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/birthday-countdown"):
            fname = "birthday-countdown.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/blood-alcohol-calculator"):
            fname = "blood-alcohol-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/bmr-calculator"):
            fname = "bmr-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/body-fat-calculator"):
            fname = "body-fat-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/calorie-calculator"):
            fname = "calorie-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/cocktail-recipes"):
            fname = "cocktail-recipes.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/color-picker"):
            fname = "color-picker.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/cron-expression-generator"):
            fname = "cron-expression-generator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/csv-viewer"):
            fname = "csv-viewer.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/decision-maker"):
            fname = "decision-maker.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/dice-roller"):
            fname = "dice-roller.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/discount-calculator"):
            fname = "discount-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/due-date-calculator"):
            fname = "due-date-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/emoji-picker"):
            fname = "emoji-picker.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/event-countdown"):
            fname = "event-countdown.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/food-nutrition"):
            fname = "food-nutrition.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/fuel-cost-calculator"):
            fname = "fuel-cost-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/gpa-calculator"):
            fname = "gpa-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/grade-calculator"):
            fname = "grade-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/html-entity-reference"):
            fname = "html-entity-reference.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/html-preview"):
            fname = "html-preview.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/ideal-weight-calculator"):
            fname = "ideal-weight-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/investment-calculator"):
            fname = "investment-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/json-formatter-v2"):
            fname = "json-formatter-v2.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/leap-year-checker"):
            fname = "leap-year-checker.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/macro-calculator"):
            fname = "macro-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/markdown-preview"):
            fname = "markdown-preview.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/metronome"):
            fname = "metronome.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/morse-code"):
            fname = "morse-code.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/nasa-apod"):
            fname = "nasa-apod.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/ovulation-calculator"):
            fname = "ovulation-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/password-strength"):
            fname = "password-strength.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/pomodoro-timer"):
            fname = "pomodoro-timer.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/pregnancy-week-calculator"):
            fname = "pregnancy-week-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/programming-jokes"):
            fname = "programming-jokes.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/random-name-generator"):
            fname = "random-name-generator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/random-number"):
            fname = "random-number.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/regex-tester-v2"):
            fname = "regex-tester-v2.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/roman-numeral"):
            fname = "roman-numeral.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/running-pace-calculator"):
            fname = "running-pace-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/salary-calculator"):
            fname = "salary-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/savings-goal-calculator"):
            fname = "savings-goal-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/sql-formatter"):
            fname = "sql-formatter.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/stopwatch"):
            fname = "stopwatch.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/timer"):
            fname = "timer.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/tip-calculator"):
            fname = "tip-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/trivia"):
            fname = "trivia.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/water-intake-calculator"):
            fname = "water-intake-calculator.html"
            self._serve_static_html(fname)
        elif self.path.startswith("/travel-reading"):
            fname = "travel-reading.html"
            self._serve_static_html(fname)
        elif self.path == "/sitemap.xml":
            self._send(200, "application/xml", (ROOT / "sitemap.xml").read_bytes())
        elif self.path == "/robots.txt":
            self._send(200, "text/plain", (ROOT / "robots.txt").read_text())
        else:
            self._send(404, "text/plain", f"not found: {self.path}")

    def _serve_screenshot(self):
        fname = self.path[len("/screenshots/"):].split("?")[0]
        target = (SCREENSHOTS_DIR / fname).resolve()
        if SCREENSHOTS_DIR.resolve() not in target.parents and target != SCREENSHOTS_DIR.resolve():
            self._send(404, "text/plain", "not found")
            return
        if not target.is_file():
            self._send(404, "text/plain", "not found")
            return
        self._send(200, "image/png", target.read_bytes())

    def _serve_cli_file(self):
        """Serve one file from the cloned cli-cheat-sheet repo.
        .md files are rendered to HTML; pdf/image files are sent raw."""
        rel = self.path[len("/cli/"):].split("?")[0]
        cli_root = CLI_DIR.resolve()
        target = (CLI_DIR / rel).resolve()
        # path-traversal guard: target must live inside CLI_DIR
        if target != cli_root and cli_root not in target.parents:
            self._send(404, "text/plain", f"not found: {self.path}")
            return
        if not target.is_file():
            self._send(404, "text/plain", f"not found: {self.path}")
            return
        if target.suffix == ".md":
            md = target.read_text()
            body = markdown.markdown(md, extensions=["fenced_code", "tables", "toc"])
            page = f"""<!doctype html><html><head><meta charset="utf-8"><title>{target.name}</title><style>{CSS}</style></head><body>{toolbar("cli")}{body}</body></html>"""
            self._send(200, "text/html; charset=utf-8", page)
        else:
            ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
            self._send(200, ctype, target.read_bytes())

    def _serve_static_html(self, fname):
        """Serve a static HTML file from the cheat-sheet root directory."""
        ROOT = Path(__file__).resolve().parent
        target = ROOT / fname
        safe = target.resolve()
        if ROOT.resolve() not in safe.parents and safe != ROOT.resolve():
            self._send(404, "text/plain", "not found")
            return
        if not safe.is_file():
            self._send(404, "text/plain", f"not found: {fname}")
            return
        self._send(200, "text/html; charset=utf-8", safe.read_text())

    def _send(self, code, content_type, body):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # quiet (drops default request logging)
        pass


class ReusableServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    with ReusableServer((HOST, PORT), Handler) as srv:
        print(f"cheat-sheet server listening on http://{HOST}:{PORT}/  (md={MD_PATH})", flush=True)
        srv.serve_forever()
