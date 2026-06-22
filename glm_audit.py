#!/usr/bin/env python3
import urllib.request, json, os, re

with open(os.path.expanduser('~/.vault/env')) as f:
    ct = f.read()
# Proper regex: capture value between single quotes after OPENROUTER_API_KEY=
m = re.search(r"OPENROUTER_API_KEY='([^']+)'", ct)
if not m:
    print("ERROR: Could not find OpenRouter key")
    exit(1)
key = m.group(1)

# Count tool pages
tool_path = os.path.expanduser('~/toolhearth.com')
files = [f for f in os.listdir(tool_path) if f.endswith('.html') and f != 'index.html']

prompt = f"""Analyze toolhearth.com — a free online tools website mimicking calculator.net.

STRUCTURE:
- 1 homepage with search, category cards, animated hero (dark GitHub theme)
- {len(files)} individual tool pages with shared template
- Shared CSS, breadcrumbs, canonical URLs, schema.org markup
- Custom domain on Vercel
- Zero analytics, zero ads, zero social tags
- Pages have meta titles + descriptions

GIVE ME:
1. SEO gaps — top 5 things missing that hurt ranking
2. Ad placement — exactly where AdSense units go in the template
3. Priority order — week 1 / week 2 / week 3
4. Quick wins — stuff fixable in 30 minutes

Use numbered items only. Be specific."""

payload = json.dumps({
    "model": "z-ai/glm-5.2",
    "messages": [
        {"role": "system", "content": "Senior SEO + monetization consultant. Give numbered action items only. No fluff."},
        {"role": "user", "content": prompt}
    ],
    "max_tokens": 1500
}).encode()

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=payload,
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://toolhearth.com",
        "X-Title": "toolhearth"
    }
)

resp = urllib.request.urlopen(req, timeout=120)
data = json.loads(resp.read())
print(data['choices'][0]['message']['content'])
print("\n---")
print(f"Model: {data['model']}")
print(f"Tokens: {data['usage']}")
