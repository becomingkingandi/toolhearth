#!/usr/bin/env python3
"""Build toolhearth.com — inject template into all pages, generate homepage."""

import os, re, json, html as html_lib
from datetime import date
from xml.etree import ElementTree as ET
from collections import OrderedDict

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://toolhearth.com"
SITE_NAME = "toolhearth.com"
SITE_DESCRIPTION = "Free online tools, calculators, converters, and utilities."
SOCIAL_IMAGE = f"{SITE_URL}/social-preview.svg"

LEGACY_LINK_ALIASES = {
    "/online-timer.html": "/timer.html",
    "/color-palette-generator.html": "/color-palette.html",
    "/html-entity-encoder.html": "/html-entities.html",
    "/password-strength-checker.html": "/password-strength.html",
    "/qr-code-generator.html": "/qr-generator.html",
    "/random-quote-generator.html": "/random-quote.html",
}

GENERIC_DESCRIPTIONS = {
    "compound-interest-calculator": "Calculate compound interest, future value, and growth over time with a free compound interest calculator.",
    "debt-payoff-calculator": "Plan debt payoff scenarios, compare extra payment strategies, and estimate your payoff date with a free calculator.",
    "investment-returns-calculator": "Estimate investment growth, annual returns, and future portfolio value with a free investment returns calculator.",
    "retirement-calculator": "Estimate how much you may need for retirement and project savings growth with a free retirement calculator.",
    "pdf-compress": "Compress PDF files online to reduce file size while keeping documents easy to share and download.",
    "pdf-to-word": "Convert PDF files to editable Word documents online with a fast, free PDF to Word converter.",
    "pdf-to-jpeg": "Convert PDF pages to JPEG images online with a free PDF to JPEG converter for quick image extraction.",
    "bitcoin-flow": "Explore a visual breakdown of how bitcoin laundering and transaction flows are often discussed online.",
}

FORCE_DESCRIPTION_OVERRIDES = {
    "privacy": "Read the ToolHearth privacy policy to learn what information we collect, how it is used, and how browser-based tools protect your data.",
    "bmi-calculator-health-guide": "Calculate and interpret BMI, understand its limitations, and learn which additional health measurements can provide a more complete picture.",
    "character-counter-seo-tips": "Use precise character counts to improve SEO titles and descriptions, avoid truncation, and write clearer snippets that earn more search clicks.",
    "how-to-convert-inches-to-feet": "Convert inches to feet and feet to inches with simple formulas, a reference table, and practical examples for construction, DIY, and daily measurements.",
    "index": "Browse practical ToolHearth guides for calculators, converters, design tools, developer utilities, personal finance, health, and everyday productivity.",
    "json-formatter-developer-tips": "Format and validate JSON with practical techniques for debugging APIs, editing configuration files, cleaning data, and finding common syntax errors.",
    "affiliate-best-web-hosting": "Compare top web hosting providers for small businesses with pricing, features, and expert notes.",
    "affiliate-best-email-tools": "Compare email marketing tools for small businesses with pricing, deliverability, and key features.",
    "affiliate-best-crm-software": "Compare CRM software for small businesses with pricing, pipelines, automations, and integrations.",
    "affiliate-best-ai-writing": "Compare AI writing assistants with pricing, use cases, and feature breakdowns.",
    "affiliate-best-ai-marketing-tools": "Compare AI marketing tools for small businesses with pricing, features, and workflows.",
    "affiliate-best-online-course": "Compare online course platforms with pricing, creator tools, and feature breakdowns.",
    "affiliate-best-vpn-services": "Compare VPN services with privacy features, speed, and pricing for secure browsing.",
    "affiliate-best-stock-trading": "Compare stock trading apps with fees, platform features, and beginner-friendly tools.",
}

# ── Category definitions ──────────────────────────────────────────────
CATEGORIES = OrderedDict([
    ("Calculators", [
        "bmi-calculator", "body-fat-calculator", "bmr-calculator", "calorie-calculator",
        "macro-calculator", "ideal-weight-calculator", "water-intake-calculator",
        "sleep-calculator", "blood-alcohol-calculator", "running-pace-calculator",
        "due-date-calculator", "ovulation-calculator", "pregnancy-week-calculator",
        "mortgage-calculator", "compound-interest-calculator", "investment-calculator",
        "investment-returns-calculator", "retirement-calculator", "salary-calculator",
        "budget-calculator", "savings-goal-calculator", "debt-payoff-calculator",
        "tip-calculator", "discount-calculator", "fuel-cost-calculator",
        "gpa-calculator", "grade-calculator", "birthday-countdown",
        "event-countdown", "christmas-planning",
    ]),
    ("Converters", [
        "unit-converter", "currency-converter", "inches-to-feet", "km-to-miles",
        "mm-to-inches", "temperature-converter", "timezone-converter",
        "text-case-converter", "binary-translator", "morse-code",
        "roman-numeral", "base64", "url-encoder",
        "color-converter", "html-entities", "yaml-json-converter",
        "json-formatter", "sql-formatter", "markdown-preview",
        "cron-expression-generator",
    ]),
    ("Developer Tools", [
        "ascii-table", "regex-tester", "uuid-generator", "jwt-decoder",
        "html-preview", "diff-checker", "csv-viewer", "mime-types",
        "seo-meta-generator", "password-strength", "color-picker",
        "color-palette", "gradient-builder", "box-shadow",
        "typography-tester", "grid-layout", "emoji-picker",
        "lorem-ipsum", "browser-info", "what-is-my-ip",
        "word-counter", "character-counter", "anagram-solver",
        "word-unscrambler", "wordle-solver", "random-word-generator",
    ]),
    ("Generators", [
        "qr-generator", "random-number", "random-quote", "random-fact",
        "random-name-generator", "password-generator", "list-randomizer",
        "decision-maker", "dice-roller", "joke-generator",
        "programming-jokes", "cat-facts", "dog-pics",
        "anime-quotes", "trivia", "cocktail-recipes",
        "bible-verse", "nasa-apod", "hacker-news",
        "weather", "country-lookup",
    ]),
    ("Timers & Clocks", [
        "pomodoro-timer", "timer", "stopwatch", "metronome",
        "world-clock", "countdown-timer",
    ]),
    ("Health & Fitness", [
        "bmi-calculator", "calorie-calculator", "body-fat-calculator",
        "bmr-calculator", "ideal-weight-calculator", "macro-calculator",
        "water-intake-calculator", "sleep-calculator", "blood-alcohol-calculator",
        "running-pace-calculator", "food-nutrition",
    ]),
])

# Flat category mapping for breadcrumbs (first match wins)
def get_category(tool_name):
    for cat, tools in CATEGORIES.items():
        if tool_name in tools:
            return cat
    return None

# Name display map
NAME_OVERRIDES = {
    "bmi-calculator": "BMI Calculator",
    "bmr-calculator": "BMR Calculator",
    "body-fat-calculator": "Body Fat Calculator",
    "blood-alcohol-calculator": "Blood Alcohol Calculator",
    "compound-interest-calculator": "Compound Interest Calculator",
    "debt-payoff-calculator": "Debt Payoff Calculator",
    "investment-returns-calculator": "Investment Returns Calculator",
    "pregnancy-week-calculator": "Pregnancy Week Calculator",
    "running-pace-calculator": "Running Pace Calculator",
    "savings-goal-calculator": "Savings Goal Calculator",
    "water-intake-calculator": "Water Intake Calculator",
    "ideal-weight-calculator": "Ideal Weight Calculator",
    "due-date-calculator": "Due Date Calculator",
    "fuel-cost-calculator": "Fuel Cost Calculator",
    "retirement-calculator": "Retirement Calculator",
    "birthday-countdown": "Birthday Countdown",
    "event-countdown": "Event Countdown",
    "christmas-planning": "Christmas Planning",
    "inches-to-feet": "Inches to Feet",
    "km-to-miles": "KM to Miles",
    "mm-to-inches": "MM to Inches",
    "text-case-converter": "Text Case Converter",
    "binary-translator": "Binary Translator",
    "morse-code": "Morse Code",
    "roman-numeral": "Roman Numeral Converter",
    "url-encoder": "URL Encoder / Decoder",
    "color-converter": "Color Converter",
    "html-entities": "HTML Entities",
    "yaml-json-converter": "YAML to JSON Converter",
    "json-formatter": "JSON Formatter",
    "sql-formatter": "SQL Formatter",
    "markdown-preview": "Markdown Preview",
    "cron-expression-generator": "Cron Expression Generator",
    "ascii-table": "ASCII Table",
    "regex-tester": "Regex Tester",
    "uuid-generator": "UUID Generator",
    "jwt-decoder": "JWT Decoder",
    "html-preview": "HTML Preview",
    "diff-checker": "Diff Checker",
    "csv-viewer": "CSV Viewer",
    "mime-types": "MIME Types Reference",
    "seo-meta-generator": "SEO Meta Tag Generator",
    "password-strength": "Password Strength Checker",
    "color-picker": "Color Picker",
    "color-palette": "Color Palette Generator",
    "gradient-builder": "Gradient Builder",
    "box-shadow": "Box Shadow Generator",
    "typography-tester": "Typography Tester",
    "grid-layout": "Grid Layout Generator",
    "emoji-picker": "Emoji Picker",
    "lorem-ipsum": "Lorem Ipsum Generator",
    "browser-info": "Browser Info",
    "what-is-my-ip": "What Is My IP",
    "word-counter": "Word Counter",
    "qr-generator": "QR Code Generator",
    "random-number": "Random Number Generator",
    "random-quote": "Random Quote Generator",
    "random-fact": "Random Fact Generator",
    "random-name-generator": "Random Name Generator",
    "list-randomizer": "List Randomizer",
    "decision-maker": "Decision Maker",
    "dice-roller": "Dice Roller",
    "joke-generator": "Joke Generator",
    "programming-jokes": "Programming Jokes",
    "cat-facts": "Cat Facts",
    "dog-pics": "Dog Pics",
    "anime-quotes": "Anime Quotes",
    "cocktail-recipes": "Cocktail Recipes",
    "bible-verse": "Bible Verse Generator",
    "nasa-apod": "NASA Astronomy Picture",
    "hacker-news": "Hacker News Reader",
    "weather": "Weather Lookup",
    "country-lookup": "Country Lookup",
    "pomodoro-timer": "Pomodoro Timer",
    "stopwatch": "Stopwatch",
    "metronome": "Metronome",
    "world-clock": "World Clock",
    "food-nutrition": "Food Nutrition Lookup",
    "typography-tester": "Typography Tester",
    "password-generator": "Password Generator",
    "dictionary": "Dictionary Lookup",
    "anagram-solver": "Anagram Solver",
    "word-unscrambler": "Word Unscrambler",
    "wordle-solver": "Wordle Solver",
    "random-word-generator": "Random Word Generator",
}

def display_name(slug):
    slug = slug.replace(".html", "")
    if slug in NAME_OVERRIDES:
        return NAME_OVERRIDES[slug]
    return slug.replace("-", " ").title()


def html_escape(value):
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def normalize_text(value):
    previous = None
    current = value
    while current != previous:
        previous = current
        current = html_lib.unescape(current)
    return current


def make_seo_tags(*, title, description, canonical, og_type="website", json_ld=None):
    tags = [
        f"<title>{html_escape(title)}</title>",
        f'<meta name="description" content="{html_escape(description)}">',
        '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">',
        f'<link rel="canonical" href="{canonical}">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:title" content="{html_escape(title)}">',
        f'<meta property="og:description" content="{html_escape(description)}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:url" content="{canonical}">',
        f'<meta property="og:image" content="{SOCIAL_IMAGE}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="toolhearth.com — free online tools and calculators">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{html_escape(title)}">',
        f'<meta name="twitter:description" content="{html_escape(description)}">',
        f'<meta name="twitter:image" content="{SOCIAL_IMAGE}">',
    ]
    if json_ld is not None:
        tags.append(
            '<script type="application/ld+json">'
            + json.dumps(json_ld, separators=(",", ":"))
            + "</script>"
        )
    return "\n".join(tags) + "\n"


def make_shared_page_script():
    return '''<script>
const emailForm = document.getElementById("email-form");
if (emailForm) {
  emailForm.addEventListener("submit", async function(e) {
    e.preventDefault();
    var btn = this.querySelector("button");
    btn.disabled = true;
    btn.textContent = "Subscribing...";
    try {
      var r = await fetch("/api/subscribe", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({email: this.email.value, source: "toolhearth"})
      });
      if (r.ok) {
        btn.textContent = "Check your email!";
        this.email.value = "";
        setTimeout(function() { btn.disabled = false; btn.textContent = "Subscribe"; }, 3000);
      } else {
        btn.textContent = "Try again";
        btn.disabled = false;
      }
    } catch (e) {
      btn.textContent = "Try again";
      btn.disabled = false;
    }
  });
}

const contactForm = document.getElementById("contact-form");
if (contactForm) {
  contactForm.addEventListener("submit", async function(e) {
    e.preventDefault();
    var btn = this.querySelector("button");
    var status = document.getElementById("form-status");
    btn.disabled = true;
    btn.textContent = "Sending...";
    if (status) status.textContent = "";

    try {
      var r = await fetch("/api/contact", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
          name: this.name.value,
          email: this.email.value,
          subject: this.subject.value,
          message: this.message.value
        })
      });

      if (r.ok) {
        if (status) status.textContent = "Message sent! We'll reply within 24 hours.";
        this.reset();
        btn.textContent = "Send Message";
        btn.disabled = false;
      } else {
        if (status) status.textContent = "Error sending. Try emailing: support@toolhearth.com";
        btn.textContent = "Send Message";
        btn.disabled = false;
      }
    } catch (e) {
      if (status) status.textContent = "Error sending. Try emailing: support@toolhearth.com";
      btn.textContent = "Send Message";
      btn.disabled = false;
    }
  });
}

const cookieConsent = document.getElementById("cookie-consent");
const cookieAccept = document.getElementById("cookie-accept");
if (cookieConsent && cookieAccept && !document.cookie.includes("consent=yes")) {
  cookieConsent.style.display = "flex";
  cookieAccept.onclick = function() {
    document.cookie = "consent=yes; path=/; max-age=31536000";
    cookieConsent.style.display = "none";
  };
}
</script>
'''


# ── Template parts ────────────────────────────────────────────────────

def make_header():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#8a4b2c">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<!-- toolhearth.com -->
<link rel="stylesheet" href="/style.css">
<link rel="stylesheet" href="/hc-design.css">
'''

def make_header_close():
    return '''
</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header">
  <div class="site-announcement">Free tools. No accounts. Browser-first processing.</div>
  <div class="header-inner">
    <a href="/" class="logo" aria-label="ToolHearth home">Tool<span>Hearth</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-navigation" aria-label="Open navigation">☰</button>
    <nav class="header-nav" id="primary-navigation" aria-label="Primary navigation">
      <a href="/">Home</a>
      <a href="/#calculators">Calculators</a>
      <a href="/#converters">Converters</a>
      <a href="/#developer-tools">Dev Tools</a>
      <a href="/blog/">Blog</a>
      <a href="/contact.html">Contact</a>
    </nav>
  </div>
</header>
<div class="container" id="main-content">
'''


MONEY_PAGES = [
    ("affiliate-best-web-hosting", "Best Web Hosting"),
    ("affiliate-best-email-tools", "Best Email Tools"),
    ("affiliate-best-crm-software", "Best CRM Software"),
    ("affiliate-best-ai-writing", "Best AI Writing"),
    ("affiliate-best-ai-marketing-tools", "Best AI Marketing Tools"),
    ("virtual-assistant-agency", "Virtual Assistant Agency"),
    ("template-marketplace", "Template Marketplace"),
    ("pdf-compress", "PDF Compress"),
    ("pdf-to-word", "PDF to Word"),
    ("pdf-to-jpeg", "PDF to JPEG"),
    ("compound-interest-calculator", "Compound Interest"),
    ("investment-returns-calculator", "Investment Returns"),
    ("retirement-calculator", "Retirement Calculator"),
    ("debt-payoff-calculator", "Debt Payoff"),
    ("remote-ai-jobs-board", "Remote AI Jobs Board"),
]

MONEY_FOOTER_PAGES = [
    ("affiliate-best-web-hosting", "Best Web Hosting"),
    ("affiliate-best-email-tools", "Best Email Tools"),
    ("affiliate-best-crm-software", "Best CRM Software"),
    ("template-marketplace", "Template Marketplace"),
    ("pdf-compress", "PDF Compress"),
    ("pdf-to-word", "PDF to Word"),
    ("pdf-to-jpeg", "PDF to JPEG"),
    ("retirement-calculator", "Retirement Calculator"),
]

FINANCE_CLUSTER = [
    "compound-interest-calculator",
    "investment-calculator",
    "investment-returns-calculator",
    "retirement-calculator",
    "budget-calculator",
    "savings-goal-calculator",
    "debt-payoff-calculator",
    "mortgage-calculator",
    "salary-calculator",
    "tip-calculator",
    "discount-calculator",
    "fuel-cost-calculator",
]

HEALTH_CLUSTER = [
    "bmi-calculator",
    "body-fat-calculator",
    "bmr-calculator",
    "calorie-calculator",
    "macro-calculator",
    "ideal-weight-calculator",
    "water-intake-calculator",
    "sleep-calculator",
    "blood-alcohol-calculator",
    "running-pace-calculator",
    "food-nutrition",
]

DEV_CLUSTER = [
    "seo-meta-generator",
    "json-formatter",
    "yaml-json-converter",
    "sql-formatter",
    "markdown-preview",
    "regex-tester",
    "base64",
    "jwt-decoder",
    "uuid-generator",
    "html-preview",
    "diff-checker",
    "csv-viewer",
    "word-counter",
    "character-counter",
    "browser-info",
    "what-is-my-ip",
]

MONEY_CLUSTER = [
    "affiliate-best-web-hosting",
    "affiliate-best-email-tools",
    "affiliate-best-crm-software",
    "affiliate-best-ai-writing",
    "affiliate-best-ai-marketing-tools",
    "template-marketplace",
    "virtual-assistant-agency",
    "pdf-compress",
    "pdf-to-word",
    "pdf-to-jpeg",
    "retirement-calculator",
]

def smart_description(slug, title, desc):
    if slug in FORCE_DESCRIPTION_OVERRIDES:
        return FORCE_DESCRIPTION_OVERRIDES[slug]
    desc = (desc or "").strip()
    if not desc or desc == SITE_DESCRIPTION:
        if slug in GENERIC_DESCRIPTIONS:
            return GENERIC_DESCRIPTIONS[slug]
        if "calculator" in slug:
            return f"Use {title} to get quick, accurate results with a free online calculator."
        if "converter" in slug or "to-" in slug:
            return f"Use {title} to convert values quickly with a free online tool."
        if "generator" in slug or "picker" in slug:
            return f"Use {title} to create results instantly with a free online generator."
        if slug.endswith("-tool"):
            return f"Use {title} online with a fast, free utility."
        return f"Use {title} online with a fast, free tool."
    return desc

def make_related_links(items, exclude_slug=None):
    links = []
    for tool in items:
        if tool == exclude_slug:
            continue
        links.append(f'    <a href="/{tool}.html" class="cat-link" data-tool="{tool}">{display_name(tool)}</a>')
        if len(links) >= 6:
            break
    return links

def get_related_cluster(slug, category):
    if slug in FINANCE_CLUSTER:
        return FINANCE_CLUSTER
    if slug in HEALTH_CLUSTER:
        return HEALTH_CLUSTER
    if slug in DEV_CLUSTER:
        return DEV_CLUSTER
    if slug in MONEY_CLUSTER or slug.startswith("pdf-") or slug.startswith("affiliate-best-") or slug in {"template-marketplace", "virtual-assistant-agency"}:
        return MONEY_CLUSTER
    if category and category in CATEGORIES:
        return CATEGORIES[category]
    return []

def make_breadcrumbs(tool_name, category):
    cat_slug = category.lower().replace(" & ", "-").replace(" ", "-") if category else ""
    out = '<div class="breadcrumbs">\n'
    out += f'  <a href="/">Home</a><span class="sep">/</span>\n'
    if category:
        out += f'  <a href="/#{cat_slug}">{category}</a><span class="sep">/</span>\n'
    out += f'  <span class="current">{display_name(tool_name)}</span>\n'
    out += '</div>\n'
    return out

def make_footer_links():
    lines = []
    for cat, tools in CATEGORIES.items():
        cat_slug = cat.lower().replace(" & ", "-").replace(" ", "-")
        lines.append(f'  <div class="footer-col">')
        lines.append(f'    <h4>{cat}</h4>')
        for t in tools[:8]:
            fname = t if t.endswith(".html") else t + ".html"
            lines.append(f'    <a href="/{fname}">{display_name(t)}</a>')
        lines.append(f'  </div>')
    lines.append('  <div class="footer-col">')
    lines.append('    <h4>Money Pages</h4>')
    for slug, label in MONEY_FOOTER_PAGES:
        lines.append(f'    <a href="/{slug}.html">{label}</a>')
    lines.append('  </div>')
    return '\n'.join(lines)

def make_trust_links():
    return '''
      <nav class="footer-trust" aria-label="Company and legal">
        <a href="/about.html">About</a>
        <a href="/contact.html">Contact</a>
        <a href="/privacy.html">Privacy</a>
        <a href="/terms.html">Terms</a>
      </nav>'''

def make_related_block(slug, category):
    items = get_related_cluster(slug, category)
    if not items:
        return ""

    links = make_related_links(items, exclude_slug=slug)
    if not links:
        return ""

    return f'''
<section class="card related-box" aria-labelledby="related-tools">
  <h2 id="related-tools">Related Tools</h2>
  <p class="text-muted">More tools in the same category that people often use next.</p>
  <div class="cat-grid">
{chr(10).join(links)}
  </div>
</section>
'''

def make_affiliate_disclosure(slug):
    if not slug.startswith("affiliate-best-"):
        return ""
    return '''
<aside class="affiliate-disclosure" aria-label="Affiliate disclosure">
  <strong>Affiliate disclosure</strong>
  <span>ToolHearth may earn a commission if you purchase through links on this page, at no extra cost to you. Rankings and editorial opinions are our own.</span>
</aside>
'''

def commercial_destination(slug, category):
    if slug.startswith("affiliate-best-") or slug in {"template-marketplace", "virtual-assistant-agency"}:
        return None
    if slug in FINANCE_CLUSTER:
        return ("template-marketplace", "Put your result into a plan", "Explore practical finance and planning templates.")
    if slug in DEV_CLUSTER or category in {"Developer Tools", "Writing & Text"}:
        return ("affiliate-best-ai-marketing-tools", "Build on your result", "Compare tools for publishing, marketing, and growing your work.")
    if slug in {"password-generator", "what-is-my-ip", "browser-info", "jwt-decoder"}:
        return ("affiliate-best-vpn-services", "Improve your privacy setup", "Compare privacy tools and services before choosing one.")
    if category in {"Business", "Productivity"}:
        return ("affiliate-best-crm-software", "Choose your next business tool", "See our comparison of software for organizing customers and work.")
    return None

def make_commercial_funnel(slug, category):
    destination = commercial_destination(slug, category)
    if not destination:
        return ""
    target, heading, copy = destination
    return f'''
<aside class="commercial-funnel" aria-label="Recommended next step">
  <div>
    <span class="commercial-eyebrow">Recommended next step</span>
    <h2>{html_escape(heading)}</h2>
    <p>{html_escape(copy)}</p>
  </div>
  <a class="commercial-cta" href="/{html_escape(target)}.html" data-commercial-cta="{html_escape(target)}">Explore the guide</a>
</aside>
<div class="ad-slot" data-ad-slot="tool-after-content" hidden aria-hidden="true"></div>
'''

FOOTER = f'''</div><!-- /container -->
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-grid">
{make_footer_links()}
    </div>
    <div class="footer-bottom">
      &copy; 2026 <a href="https://toolhearth.com">toolhearth.com</a> &mdash; Free online tools, calculators, and utilities.
{make_trust_links()}
    </div>
  </div>
</footer>
<nav class="mobile-dock" aria-label="Mobile navigation">
  <a href="/">Tools</a>
  <a href="/#calculators">Calc</a>
  <a href="/#generators">Generate</a>
  <a href="/blog/">Learn</a>
</nav>
<script src="/analytics.js" defer></script>
<script>
(() => {{
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".menu-toggle");
  if (!header || !toggle) return;
  toggle.addEventListener("click", () => {{
    const open = header.dataset.menuOpen !== "true";
    header.dataset.menuOpen = String(open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
  }});
  header.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {{
    header.dataset.menuOpen = "false";
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open navigation");
  }}));
}})();
</script>
</body>
</html>'''


# ── Homepage ───────────────────────────────────────────────────────────

def build_homepage():
    homepage_description = "Free online tools, calculators, converters, and utilities. BMI calculator, currency converter, password generator, and 100+ more tools."
    out = make_header()
    out += make_seo_tags(
        title="toolhearth.com — Free Online Tools, Calculators & Utilities",
        description=homepage_description,
        canonical=f"{SITE_URL}/",
        json_ld={
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE_NAME,
            "url": f"{SITE_URL}/",
            "description": homepage_description,
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{SITE_URL}/?q={{search_term_string}}",
                "query-input": "required name=search_term_string",
            },
        },
    )
    out += make_header_close()
    out += '''
<section class="hero">
  <h1>Free Online Tools</h1>
  <p>Calculators, converters, generators, and utilities — all free, no sign-up required.</p>
  <div class="hero-search">
    <input type="text" id="toolSearch" placeholder="Search tools..." oninput="filterTools(this.value)">
  </div>
</section>

<section style="margin: 48px 0; padding: 32px; background: var(--color-cream-200); border-radius: 8px; text-align: center;">
  <h2 style="margin-top: 0;">Popular Right Now</h2>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px; margin-top: 24px;">
    <a href="/bmi-calculator.html" class="cat-link" style="padding: 16px; background: white; border-radius: 6px; text-decoration: none; color: inherit;">BMI Calculator</a>
    <a href="/currency-converter.html" class="cat-link" style="padding: 16px; background: white; border-radius: 6px; text-decoration: none; color: inherit;">Currency Converter</a>
    <a href="/password-generator.html" class="cat-link" style="padding: 16px; background: white; border-radius: 6px; text-decoration: none; color: inherit;">Password Generator</a>
    <a href="/qr-generator.html" class="cat-link" style="padding: 16px; background: white; border-radius: 6px; text-decoration: none; color: inherit;">QR Code Generator</a>
  </div>
</section>

<div id="toolContainer">
'''
    for cat, tools in CATEGORIES.items():
        cat_slug = cat.lower().replace(" & ", "-").replace(" ", "-")
        out += f'<section class="cat-section" data-category="{cat_slug}">\n'
        out += f'  <h2 id="{cat_slug}">{cat}</h2>\n'
        out += '  <div class="cat-grid">\n'
        for t in tools:
            fname = t if t.endswith(".html") else t + ".html"
            out += f'    <a href="/{fname}" class="cat-link" data-tool="{t}">{display_name(t)}</a>\n'
        out += '  </div>\n'
        out += '</section>\n'

    out += '''
</div>

<section class="homepage-about" aria-labelledby="why-toolhearth">
  <h2 id="why-toolhearth">Useful answers without the friction</h2>
  <p>toolhearth brings practical calculators, converters, generators, and browser-based utilities into one fast, free collection. Tools run directly in your browser and do not require an account.</p>
  <p>Use the categories above to find everyday health, finance, developer, writing, and time tools. Important decisions should always be checked against qualified professional advice and authoritative sources.</p>
</section>

<section class="cat-section" data-category="money-pages">
  <h2 id="money-pages">High-Intent Money Pages</h2>
  <div class="cat-grid">
'''
    for slug, label in MONEY_PAGES:
        out += f'    <a href="/{slug}.html" class="cat-link" data-tool="{slug}">{label}</a>\n'
    out += '''
  </div>
</section>

<script>
function filterTools(q) {
  q = q.toLowerCase();
  document.querySelectorAll('.cat-link').forEach(el => {
    el.style.display = el.textContent.toLowerCase().includes(q) ? 'block' : 'none';
  });
  document.querySelectorAll('.cat-section').forEach(section => {
    const visible = [...section.querySelectorAll('.cat-link')].some(el => el.style.display !== 'none');
    section.style.display = visible ? 'block' : 'none';
  });
}
</script>
'''
    out += FOOTER
    return out


# ── Inject template into existing tool pages ───────────────────────────

def inject_tool_page(filepath):
    """Read an existing HTML tool page, extract content between <body> tags,
    inject into template with breadcrumbs."""
    with open(filepath, 'r', encoding='utf-8') as f:
        source_html = f.read()

    # Extract title and metadata
    title_match = re.search(r'<title>(.*?)</title>', source_html, re.DOTALL)
    title = normalize_text(title_match.group(1).strip()) if title_match else ""

    desc_match = re.search(r'<meta name="description" content="(.*?)"', source_html)
    desc = normalize_text(desc_match.group(1).strip()) if desc_match else ""

    # Extract primary content - everything between <body>...</body>
    body_match = re.search(r'<body[^>]*>(.*?)</body>', source_html, re.DOTALL)
    if not body_match:
        body_match = re.search(r'<body[^>]*>(.*)', source_html, re.DOTALL)
    body_content = body_match.group(1).strip() if body_match else source_html

    # If this page has already been injected, unwrap the previous site shell so
    # repeated builds stay idempotent instead of nesting headers and footers.
    tool_marker_pattern = r'<div class="tool-content[^"]*"[^>]*>'
    if re.search(tool_marker_pattern, body_content):
        body_content = re.split(tool_marker_pattern, body_content)[-1]
        body_content = re.sub(
            r'\s*</div>\s*</div><!-- /container -->\s*<footer class="site-footer">.*$',
            '',
            body_content,
            flags=re.DOTALL,
        ).strip()
        body_content = re.sub(
            r'\s*</div>\s*</div>\s*(<script\b)',
            r'\n\1',
            body_content,
            count=1,
            flags=re.DOTALL,
        ).strip()
        body_content = re.sub(
            r'\s*<footer class="site-footer">\s*<div class="footer-inner">.*?</footer>',
            '',
            body_content,
            flags=re.DOTALL,
        ).strip()
    body_content = re.sub(
        r'\s*<section class="card related-box" aria-labelledby="related-tools">.*?</section>\s*',
        '\n',
        body_content,
        flags=re.DOTALL,
    )
    body_content = re.sub(
        r'\s*<div class="workbench-kicker">.*?</div>\s*',
        '\n',
        body_content,
        flags=re.DOTALL,
    )
    body_content = re.sub(
        r'\s*<aside class="affiliate-disclosure".*?</aside>\s*',
        '\n',
        body_content,
        flags=re.DOTALL,
    )
    body_content = re.sub(
        r'\s*<aside class="commercial-funnel".*?</aside>\s*(?:<div class="ad-slot".*?</div>\s*)?',
        '\n',
        body_content,
        flags=re.DOTALL,
    )
    body_content = re.sub(
        r'\s*<div style="max-width:720px;margin:0 auto;padding:0 1rem 2rem;">.*?<div style="display:flex;flex-wrap:wrap;gap:\.25rem;">.*?</div>\s*</div>\s*',
        '\n',
        body_content,
        flags=re.DOTALL,
    )
    for old_url, current_url in LEGACY_LINK_ALIASES.items():
        body_content = body_content.replace(old_url, current_url)

    # Clean up body content - remove inline styles, scripts that were in head
    # Remove the massive <style> block
    body_content = re.sub(r'<style>.*?</style>', '', body_content, flags=re.DOTALL)
    body_content = re.sub(r'(?:</body>\s*</html>\s*)+$', '', body_content, flags=re.IGNORECASE | re.DOTALL).strip()
    body_without_scripts = re.sub(r'<script\b.*?</script>', '', body_content, flags=re.IGNORECASE | re.DOTALL)
    if not is_blog_path(filepath) and not re.search(r'<h1\b', body_without_scripts, flags=re.IGNORECASE):
        body_content = f'<h1 class="sr-only">{html_escape(title or display_name(os.path.basename(filepath)))}</h1>\n' + body_content
    if "email-form" in body_content or "contact-form" in body_content or "cookie-consent" in body_content:
        body_content = re.sub(
            r'<script>.*?document\.getElementById\("(?:contact-form|email-form)"\).*?</script>',
            make_shared_page_script(),
            body_content,
            count=1,
            flags=re.DOTALL,
        )

    # Get file slug for breadcrumbs
    basename = os.path.basename(filepath)
    slug = basename.replace(".html", "")
    cat = get_category(slug)
    is_blog = os.path.basename(os.path.dirname(filepath)) == "blog"
    page_path = f"/blog/{slug}" if is_blog else f"/{slug}"
    if is_blog and slug == "index":
        page_path = "/blog/"
    canonical = f"{SITE_URL}{page_path}"
    desc = smart_description(slug, title, desc)

    if is_blog and slug == "index":
        json_ld = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": title,
            "description": desc,
            "mainEntityOfPage": canonical,
            "url": canonical,
            "publisher": {
                "@type": "Organization",
                "name": SITE_NAME,
                "url": f"{SITE_URL}/",
            },
        }
    elif is_blog:
        json_ld = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "description": desc,
            "mainEntityOfPage": canonical,
            "url": canonical,
            "publisher": {
                "@type": "Organization",
                "name": SITE_NAME,
                "url": f"{SITE_URL}/",
            },
        }
    else:
        json_ld = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "description": desc,
            "url": canonical,
            "breadcrumb": {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{SITE_URL}/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": display_name(slug),
                        "item": canonical,
                    },
                ],
            },
        }

    # Build output
    out = make_header()
    out += make_seo_tags(
        title=title,
        description=desc,
        canonical=canonical,
        og_type="website" if is_blog and slug == "index" else ("article" if is_blog else "website"),
        json_ld=json_ld,
    )
    out += make_header_close()
    out += make_breadcrumbs(slug, cat)
    category_key = (
        cat.lower().replace(" & ", "-").replace(" ", "-")
        if cat else ("article" if is_blog else "utility")
    )
    out += (
        f'<div class="tool-content tool-workbench" '
        f'data-tool="{html_escape(slug)}" data-category="{html_escape(category_key)}">\n'
    )
    if not is_blog and slug != "seo-meta-generator":
        out += (
            f'<div class="workbench-kicker">'
            f'<span>{html_escape(cat or "ToolHearth Utility")}</span>'
            f'<span>Module / {html_escape(slug.upper())}</span>'
            f'</div>\n'
        )
    out += make_affiliate_disclosure(slug)
    out += body_content
    if not is_blog:
        out += '\n' + make_commercial_funnel(slug, cat)
    related_block = make_related_block(slug, cat) if not is_blog else ""
    if related_block and "related-box" not in body_content and "Related Tools" not in body_content:
        out += '\n' + related_block
    out += '\n</div>\n'
    if ("email-form" in body_content or "contact-form" in body_content or "cookie-consent" in body_content) and "<script>" not in body_content:
        out += make_shared_page_script()
    out += FOOTER

    return out


def is_blog_path(filepath):
    return os.path.basename(os.path.dirname(filepath)) == "blog"


def generate_sitemap():
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    urlset = ET.Element(f"{{{namespace}}}urlset")
    today = date.today().isoformat()

    paths = [("index.html", "/")]
    paths.extend(
        (fname, f"/{fname[:-5]}")
        for fname in sorted(os.listdir(ROOT))
        if fname.endswith(".html") and fname != "index.html"
    )
    blog_dir = os.path.join(ROOT, "blog")
    if os.path.isdir(blog_dir):
        paths.extend(
            (
                f"blog/{fname}",
                "/blog/" if fname == "index.html" else f"/blog/{fname[:-5]}",
            )
            for fname in sorted(os.listdir(blog_dir))
            if fname.endswith(".html")
        )

    for source, route in paths:
        url = ET.SubElement(urlset, f"{{{namespace}}}url")
        ET.SubElement(url, f"{{{namespace}}}loc").text = f"{SITE_URL}{route}"
        ET.SubElement(url, f"{{{namespace}}}lastmod").text = today
        ET.SubElement(url, f"{{{namespace}}}changefreq").text = "weekly" if route in {"/", "/blog/"} else "monthly"
        priority = "1.0" if route == "/" else ("0.8" if route == "/blog/" else "0.7")
        ET.SubElement(url, f"{{{namespace}}}priority").text = priority

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    tree.write(os.path.join(ROOT, "sitemap.xml"), encoding="UTF-8", xml_declaration=True)


# ── Main ───────────────────────────────────────────────────────────────

def main():
    # Build homepage
    homepage = build_homepage()
    with open(os.path.join(ROOT, "index.html"), 'w', encoding='utf-8') as f:
        f.write(homepage)
    print("[OK] index.html — homepage built")

    # Inject template into all HTML files (except index.html and blog/ pages for now)
    html_files = [f for f in os.listdir(ROOT) if f.endswith(".html") and f != "index.html"]
    # Exclude blog/ subdirectory
    injected = 0
    for fname in html_files:
        path = os.path.join(ROOT, fname)
        try:
            result = inject_tool_page(path)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(result)
            injected += 1
        except Exception as e:
            print(f"[FAIL] {fname}: {e}")

    # Also do blog pages
    blog_dir = os.path.join(ROOT, "blog")
    if os.path.isdir(blog_dir):
        for fname in os.listdir(blog_dir):
            if not fname.endswith(".html"):
                continue
            path = os.path.join(blog_dir, fname)
            try:
                result = inject_tool_page(path)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(result)
                injected += 1
            except Exception as e:
                print(f"[FAIL] blog/{fname}: {e}")

    generate_sitemap()
    print("[OK] sitemap.xml — complete route inventory generated")
    print(f"[OK] {injected} pages injected with template")
    print(f"[OK] Total files: {len([f for f in os.listdir(ROOT) if f.endswith('.html')])} HTML files")

if __name__ == "__main__":
    main()
