#!/usr/bin/env python3
"""Check OpenRouter account and accessible models."""
import urllib.request, urllib.error, json, os, re

with open(os.path.expanduser('~/.vault/env')) as f:
    content = f.read()

def get_var(name):
    m = re.search(r'export %s=(.+?)$' % re.escape(name), content, re.M)
    if not m:
        return None
    return m.group(1).strip().strip("'\"")

key = get_var('OPENROUTER_API_KEY')
if not key:
    print("No OpenRouter key found")
    exit(1)

print(f"Key: {key[:10]}...{key[-4:]}")

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

# Check account/credits
req = urllib.request.Request("https://openrouter.ai/api/v1/auth/key", headers=headers)
try:
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    print(f"\nAccount:")
    print(f"  Credits: {data.get('credits', '?')}")
    print(f"  Usage: {data.get('usage', '?')}")
    print(f"  Limit: {json.dumps(data)[:400]}")
except urllib.error.HTTPError as e:
    print(f"Auth check HTTP {e.code}: {e.read().decode()[:200]}")

# Check available models
req2 = urllib.request.Request("https://openrouter.ai/api/v1/models", headers=headers)
try:
    resp2 = urllib.request.urlopen(req2, timeout=15)
    data2 = json.loads(resp2.read())
    models = data2.get('data', [])
    print(f"\nModels available: {len(models)}")

    # Show key ones - Claude, GPT, Gemini, Llama, DeepSeek
    for m in models:
        mid = m.get('id', '')
        pricing = m.get('pricing', {})
        context = m.get('context_length', 0)
        if any(x in mid.lower() for x in ['claude', 'gpt-4', 'gemini', 'llama', 'deepseek', 'mistral']):
            prompt = pricing.get('prompt', 0)
            completion = pricing.get('completion', 0)
            print(f"  {mid:45s} ctx={context:>6}  ${float(prompt)*1e6:.2f}/1M in  ${float(completion)*1e6:.2f}/1M out")
except urllib.error.HTTPError as e2:
    print(f"Models HTTP {e2.code}: {e2.read().decode()[:200]}")
