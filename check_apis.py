#!/usr/bin/env python3
"""Check AI API tiers and access levels."""
import urllib.request, urllib.error, json, os, re

with open(os.path.expanduser('~/.vault/env')) as f:
    content = f.read()

def get_var(name):
    m = re.search(r'export %s=(.+?)$' % re.escape(name), content, re.M)
    if not m:
        return None
    return m.group(1).strip().strip("'\"")

def api_get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code, "_body": e.read().decode()[:200]}
    except Exception as e:
        return {"_error": str(e)}

print("=" * 50)
print("TOGETHER AI")
print("=" * 50)
together_key = get_var('TOGETHER_API_KEY')
if together_key:
    data = api_get("https://api.together.xyz/v1/models",
                   {"Authorization": f"Bearer {together_key}"})
    if isinstance(data, list):
        print(f"Models accessible: {len(data)}")
        # Check tier/status
        status = api_get("https://api.together.xyz/v1/account",
                        {"Authorization": f"Bearer {together_key}"})
        if isinstance(status, dict) and 'rate_limit' in status:
            print(f"Account: {status}")
        else:
            print(f"Status response: {json.dumps(status)[:300]}")
    else:
        print(f"Response: {json.dumps(data)[:300]}")

print()
print("=" * 50)
print("NVIDIA NIM")
print("=" * 50)
nvidia_key = get_var('NVIDIA_API_KEY')
if nvidia_key:
    # Check Nim catalog access
    data = api_get("https://api.nvcf.nvidia.com/v2/nvcf/models",
                   {"Authorization": f"Bearer {nvidia_key}"})
    print(f"NIM models: {json.dumps(data)[:500]}")

print()
print("=" * 50)
print("GROQ")
print("=" * 50)
groq_key = get_var('GROQ_API_KEY')
if groq_key:
    data = api_get("https://api.groq.com/openai/v1/models",
                   {"Authorization": f"Bearer {groq_key}"})
    if 'data' in data:
        print(f"Models: {len(data['data'])}")
        for m in data['data'][:10]:
            print(f"  {m['id']}")
    else:
        print(f"Response: {json.dumps(data)[:200]}")

print()
print("=" * 50)
print("SUMMARY")
print("=" * 50)
for name, key in [("Together AI", together_key), ("NVIDIA NIM", nvidia_key),
                   ("Groq", groq_key), ("OpenRouter", get_var('OPENROUTER_API_KEY')),
                   ("OpenAI", get_var('OPENAI_API_KEY')), ("DeepSeek", get_var('DEEPSEEK_API_KEY'))]:
    if key:
        print(f"  {name}: KEY EXISTS ({key[:8]}...{key[-4:]})")
    else:
        print(f"  {name}: NO KEY")
