#!/usr/bin/env python3
"""Generate hero image via Higgsfield REST API directly."""
import json, urllib.request, urllib.error, os, sys

# Read token from config
with open(os.path.expanduser('~/.hermes/config.yaml')) as f:
    for line in f:
        if 'Authorization: Bearer hf_' in line:
            token = line.split('hf_')[-1].strip()
            token = 'hf_' + token
            break

print(f"Token: {token[:10]}...{token[-4:]}")

# Try the Higgsfield generation endpoint
payload = json.dumps({
    "model": "recraft-v4-1",
    "prompt": "Hero banner for a tool website — a clean dark-themed collection of floating utility tool widgets and calculator interfaces in a modern tech style. Grid of glowing calculator panels, conversion tools, measurement scales, and code editors floating in dark space. Deep navy background with subtle blue and green accent glows. Professional, minimalist, tech-dashboard aesthetic. No people, no text.",
    "n": 1,
    "aspect_ratio": "16:9",
    "size": "1792x1024"
}).encode()

req = urllib.request.Request(
    "https://api.higgsfield.ai/v1/images/generations",
    data=payload,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    },
    method="POST"
)

try:
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read())
    print(f"\nResponse:")
    print(json.dumps(data, indent=2)[:1000])
except urllib.error.HTTPError as e:
    body = e.read().decode()[:500]
    print(f"HTTP {e.code}: {body}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
