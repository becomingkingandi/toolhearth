#!/usr/bin/env python3
"""Build toolhearth.com — inject template into all pages, generate homepage."""

import os, re, json
from collections import OrderedDict

ROOT = os.path.dirname(os.path.abspath(__file__))

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


# ── Template parts ────────────────────────────────────────────────────

def make_header():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- toolhearth.com -->
<link rel="stylesheet" href="/style.css">
'''

def make_header_close():
    return '''
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="/" class="logo">tool<span>hearth</span></a>
    <nav class="header-nav">
      <a href="/">Home</a>
      <a href="/#calculators">Calculators</a>
      <a href="/#converters">Converters</a>
      <a href="/#dev-tools">Dev Tools</a>
    </nav>
  </div>
</header>
<div class="container">
'''

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
    return '\n'.join(lines)

FOOTER = f'''</div><!-- /container -->
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-grid">
{make_footer_links()}
    </div>
    <div class="footer-bottom">
      &copy; 2026 <a href="https://toolhearth.com">toolhearth.com</a> &mdash; Free online tools, calculators, and utilities.
    </div>
  </div>
</footer>
</body>
</html>'''


# ── Homepage ───────────────────────────────────────────────────────────

def build_homepage():
    out = make_header()
    out += '''<title>toolhearth.com — Free Online Tools, Calculators & Utilities</title>
<meta name="description" content="Free online tools, calculators, converters, and utilities. BMI calculator, currency converter, password generator, and 100+ more tools.">
<link rel="canonical" href="https://toolhearth.com/">
'''
    out += make_header_close()
    out += '''
<section class="hero">
  <h1>Free Online Tools</h1>
  <p>Calculators, converters, generators, and utilities — all free, no sign-up required.</p>
  <div class="hero-search">
    <input type="text" id="toolSearch" placeholder="Search tools..." oninput="filterTools(this.value)">
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
        html = f.read()

    # Extract title and metadata
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = title_match.group(1).strip() if title_match else ""

    desc_match = re.search(r'<meta name="description" content="(.*?)"', html)
    desc = desc_match.group(1).strip() if desc_match else ""

    # Extract primary content - everything between <body>...</body>
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if not body_match:
        body_match = re.search(r'<body[^>]*>(.*)', html, re.DOTALL)
    body_content = body_match.group(1).strip() if body_match else html

    # If this page has already been injected, unwrap the previous site shell so
    # repeated builds stay idempotent instead of nesting headers and footers.
    tool_marker = '<div class="tool-content">'
    if tool_marker in body_content:
        body_content = body_content.split(tool_marker)[-1]
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

    # Clean up body content - remove inline styles, scripts that were in head
    # Remove the massive <style> block
    body_content = re.sub(r'<style>.*?</style>', '', body_content, flags=re.DOTALL)

    # Get file slug for breadcrumbs
    basename = os.path.basename(filepath)
    slug = basename.replace(".html", "")
    cat = get_category(slug)

    # Build output
    out = make_header()
    out += f'<title>{title}</title>\n'
    if desc:
        out += f'<meta name="description" content="{desc}">\n'
    out += f'<link rel="canonical" href="https://toolhearth.com/{basename}">\n'
    out += make_header_close()
    out += make_breadcrumbs(slug, cat)
    out += '<div class="tool-content">\n'
    out += body_content
    out += '\n</div>\n'
    out += FOOTER

    return out


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

    print(f"[OK] {injected} pages injected with template")
    print(f"[OK] Total files: {len([f for f in os.listdir(ROOT) if f.endswith('.html')])} HTML files")

if __name__ == "__main__":
    main()
