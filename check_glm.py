#!/usr/bin/env python3
"""GLM 5.2 check on OpenRouter."""
import urllib.request, json, os, re

with open(os.path.expanduser('~/.vault/env')) as f:
    ct = f.read()
m = re.search(r"OPENROUTER_API_KEY='([^']+)'", ct)
key = m.group(1)

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": f"Bearer {key}"}
)
resp = urllib.request.urlopen(req, timeout=15)
data = json.loads(resp.read())

print("GLM / Zhipu models on OpenRouter:")
for m in data.get('data', []):
    mid = m['id']
    if 'glm' in mid.lower():
        ctx = m.get('context_length', 0)
        p = float(m['pricing']['prompt']) * 1e6
        c = float(m['pricing']['completion']) * 1e6
        print(f"  {mid:50s} ctx={ctx:>6}  ${p:.2f}/1M in  ${c:.2f}/1M out")

print()
# Also check via the Zhipu direct API if we have the key
with open(os.path.expanduser('~/.vault/env')) as f:
    ct2 = f.read()
m2 = re.search(r"ZHIPU|GLM_API|ZAI", ct2, re.I)
if m2:
    # Find the actual key
    for line in ct2.split('\n'):
        if 'ZHIPU' in line.upper() or 'GLM' in line.upper():
            print(f"Direct Zhipu key found: {line.strip()[:50]}...")
else:
    print("No direct Zhipu API key in vault")
    print("GLM 5.2 available via OpenRouter if Zhipu is on the platform")
