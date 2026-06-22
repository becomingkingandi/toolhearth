#!/usr/bin/env python3
"""Inject SEO meta tags, SoftwareApplication schema, and related tools into all tool HTML files."""

import json, re, os
from pathlib import Path

CHEAT = Path(os.path.expanduser("~/cheat-sheet"))
META_FILE = CHEAT / ".seo-meta.json"

meta = json.loads(META_FILE.read_text())

# Category groups for cross-linking
CATEGORIES = {
    "health": ["calorie-calculator", "bmr-calculator", "body-fat-calculator", "water-intake-calculator",
                "due-date-calculator", "pregnancy-week-calculator", "ovulation-calculator",
                "ideal-weight-calculator", "blood-alcohol-calculator", "macro-calculator", "sleep-calculator"],
    "finance": ["salary-calculator", "gpa-calculator", "grade-calculator", "investment-calculator",
                "savings-goal-calculator", "mortgage-calculator", "budget-calculator", "tip-calculator",
                "discount-calculator", "fuel-cost-calculator", "tax-calculator"],
    "dev": ["json-formatter", "base64", "uuid-generator", "lorem-ipsum", "regex-tester", "jwt-decoder",
            "diff-checker", "url-encoder", "yaml-json-converter", "markdown-preview", "html-preview",
            "sql-formatter", "cron-expression-generator", "html-entity-reference", "ascii-table",
            "csv-viewer", "number-base-converter"],
    "utility": ["what-is-my-ip", "white-screen", "qr-generator", "timer", "stopwatch", "pomodoro-timer",
                "event-countdown", "random-name-generator", "password-strength", "list-randomizer",
                "text-case-converter", "word-counter", "html-entities", "dice-roller", "decision-maker",
                "color-picker", "random-number", "emoji-picker", "birthday-countdown", "typing-test"],
    "api": ["weather", "bitcoin-price", "joke-generator", "random-quote", "random-fact", "dictionary",
            "github-profile", "hacker-news", "dog-pics", "cat-facts", "trivia", "cocktail-recipes",
            "nasa-apod", "bible-verse", "programming-jokes", "anime-quotes", "food-nutrition"],
    "design": ["color-converter", "color-palette", "gradient-builder", "typography-tester", "box-shadow", "grid-layout"],
    "converter": ["unit-converter", "currency-converter", "inches-to-feet", "km-to-miles", "mm-to-inches",
                  "timezone-converter", "binary-translator", "morse-code", "roman-numeral", "leap-year-checker"],
    "reference": ["mime-types", "country-lookup", "world-clock", "http-status-codes", "html-entity-reference",
                  "seo-meta-generator", "browser-info"],
    "fitness": ["running-pace-calculator", "metronome"],
}

# Build slug-to-category mapping
slug_cat = {}
for cat, slugs in CATEGORIES.items():
    for s in slugs:
        slug_cat[s] = cat

def inject_file(slug, info):
    path = CHEAT / f"{slug}.html"
    if not path.exists():
        return f"MISSING {slug}.html"

    html = path.read_text()
    title = info["title"]
    desc = info["desc"]
    cat = info.get("cat", "utility")

    # Replaced 5 times
    changes = 0

    # 1. Replace <title>
    new_html = re.sub(
        r'<title>.*?</title>',
        f'<title>{title}</title>',
        html, count=1
    )
    if new_html != html:
        changes += 1

    # 2. Replace or add meta description
    if re.search(r'<meta\s+name="description"\s+content="[^"]*"', new_html, re.I):
        new_html = re.sub(
            r'<meta\s+name="description"\s+content="[^"]*"',
            f'<meta name="description" content="{desc}">',
            new_html, count=1, flags=re.I
        )
        changes += 1
    elif re.search(r'<meta\s+name="description"\s+content=\'[^\']*\'', new_html, re.I):
        new_html = re.sub(
            r"<meta\s+name='description'\s+content='[^']*'",
            f"<meta name='description' content='{desc}'>",
            new_html, count=1, flags=re.I
        )
        changes += 1
    else:
        # Add after <title>
        new_html = new_html.replace(
            f'<title>{title}</title>',
            f'<title>{title}</title>\n<meta name="description" content="{desc}">'
        )
        changes += 1

    # 3. Add SoftwareApplication schema
    schema = f'''<script type="application/ld+json">
{json.dumps({
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": title,
    "description": desc,
    "applicationCategory": "UtilitiesApplication",
    "operatingSystem": "Web",
    "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
    }
}, indent=2)}
</script>'''

    if '</head>' in new_html:
        # Remove any existing schema
        new_html = re.sub(
            r'<script type="application/ld\+json">.*?</script>\s*',
            '', new_html, count=1, flags=re.DOTALL
        )
        new_html = new_html.replace('</head>', f'{schema}\n</head>')
        changes += 1

    # 4. Related tools
    if cat in CATEGORIES and slug in CATEGORIES[cat]:
        related = [s for s in CATEGORIES[cat] if s != slug and (CHEAT / f"{s}.html").exists()]
        if related:
            related_html = '\n'.join(
                f'      <a href="/{r}" style="display:inline-block;background:#161b22;border:1px solid #30363d;border-radius:6px;padding:.4rem .8rem;margin:.25rem;color:#58a6ff;text-decoration:none;font-size:.85rem;">{meta.get(r,{}).get("title", r.replace("-"," ").title())}</a>'
                for r in related[:6]
            )

            related_section = f'''
  <div style="max-width:720px;margin:0 auto;padding:0 1rem 2rem;">
    <h3 style="color:#8b949e;font-size:.9rem;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5rem;">Related Tools</h3>
    <div style="display:flex;flex-wrap:wrap;gap:.25rem;">
{related_html}
    </div>
  </div>
'''

            # Insert before footer
            if '</body>' in new_html:
                new_html = new_html.replace('</body>', f'{related_section}\n</body>')
                changes += 1

    # Write if changed
    if changes > 0:
        path.write_text(new_html)
        return f"✅ {slug} ({changes} changes)"
    return f"  {slug} — no changes needed"

# Process all files
count = 0
errors = []
for slug, info in sorted(meta.items()):
    result = inject_file(slug, info)
    if result.startswith("✅"):
        count += 1
        print(result)
    elif result.startswith("MISSING"):
        pass  # Skip missing files silently

print(f"\n{'='*50}")
print(f"Injected SEO into {count}/{len(meta)} files")
print(f"{'='*50}")
