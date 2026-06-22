#!/usr/bin/env python3
"""Check Cloudflare API access + create Pages project."""
import json, urllib.request, os, sys

# Read token from runtime.env
token = None
with open(os.path.expanduser('~/.vault/runtime.env')) as f:
    for line in f:
        if 'CLOUDFLARE_API_TOKEN' in line and "=" in line:
            token = line.split("=", 1)[1].strip().strip("'").strip('"')
            break

if not token or token == '***':
    print("ERROR: No valid Cloudflare API token found")
    sys.exit(1)

print(f"Token found: {token[:8]}...{token[-4:]}")

# Get accounts
req = urllib.request.Request(
    "https://api.cloudflare.com/client/v4/accounts",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
)
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    if data.get('success') and data['result']:
        for a in data['result']:
            print(f"ACCOUNT: {a['id']} — {a['name']}")
        account_id = data['result'][0]['id']
    else:
        # Try X-Auth-Key format
        print(f"Bearer failed: {data.get('errors', 'no errors')}")
        # Maybe it's an API key, not a token
        sys.exit(1)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()[:200]}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# Create Pages project
pages_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects"
pages_body = json.dumps({
    "name": "toolhearth",
    "production_branch": "main",
    "build_config": {
        "build_command": "",
        "destination_dir": "/"
    },
    "deployment_configs": {
        "preview": {},
        "production": {}
    }
}).encode()

req2 = urllib.request.Request(
    pages_url, data=pages_body,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST"
)
try:
    resp2 = urllib.request.urlopen(req2)
    data2 = json.loads(resp2.read())
    if data2.get('success'):
        p = data2['result']
        print(f"\nPAGES PROJECT CREATED: {p['name']}")
        print(f"URL: {p.get('subdomain', 'pending')}")
        print(f"ID: {p['id']}")
    else:
        # Might already exist
        errors = data2.get('errors', [])
        for e in errors:
            print(f"Pages error: {e.get('message','?')}")
        # Check if it exists already
        print("\nChecking if project already exists...")
        req3 = urllib.request.Request(pages_url, headers={"Authorization": f"Bearer {token}"})
        resp3 = urllib.request.urlopen(req3)
        existing = json.loads(resp3.read())
        for p in existing.get('result', []):
            print(f"  Existing: {p['name']} — {p.get('subdomain','?')}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()[:300]}")
except Exception as e:
    print(f"Error creating pages: {e}")
