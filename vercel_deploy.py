#!/usr/bin/env python3
"""Deploy toolhearth.com via Vercel API."""
import json, urllib.request, urllib.error, os, subprocess

# Get Vercel token by sourcing the env file
result = subprocess.run(
    ['bash', '-c', 'source ~/.vault/env 2>/dev/null && echo "$VERCEL_TOKEN"'],
    capture_output=True, text=True
)
token = result.stdout.strip()
if not token:
    print("ERROR: No VERCEL_TOKEN available")
    exit(1)
print(f"Token: {token[:10]}...{token[-4:]}")

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Test user
req = urllib.request.Request("https://api.vercel.com/v2/user", headers=headers)
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    u = data.get('user', {})
    print(f"User: {u.get('name','?')} — {u.get('email','?')}")
except Exception as e:
    print(f"User check failed: {e}")
    exit(1)

# Create project
project_payload = json.dumps({
    "name": "toolhearth",
    "gitRepository": {
        "repo": "becomingkingandi/toolhearth",
        "type": "github"
    },
    "framework": None,
    "buildCommand": None,
    "outputDirectory": None
}).encode()

req2 = urllib.request.Request(
    "https://api.vercel.com/v10/projects",
    data=project_payload, headers=headers, method="POST"
)
try:
    resp2 = urllib.request.urlopen(req2)
    data2 = json.loads(resp2.read())
    print(f"Project: {data2.get('name','?')} (ID: {data2.get('id','?')})")
    # Trigger deploy
    deploy_payload = json.dumps({"projectId": data2['id']}).encode()
    req3 = urllib.request.Request(
        f"https://api.vercel.com/v10/projects/{data2['id']}/deployments",
        data=deploy_payload, headers=headers, method="POST"
    )
    try:
        resp3 = urllib.request.urlopen(req3)
        d3 = json.loads(resp3.read())
        print(f"Deploy URL: https://{d3.get('url','?')}")
        print(f"State: {d3.get('readyState','?')}")
    except urllib.error.HTTPError as e3:
        err3 = e3.read().decode()[:300]
        print(f"Deploy HTTP {e3.code}: {err3}")
except urllib.error.HTTPError as e2:
    err2 = e2.read().decode()[:500]
    print(f"Create project HTTP {e2.code}: {err2}")

# List existing projects
req4 = urllib.request.Request("https://api.vercel.com/v9/projects?limit=5", headers=headers)
try:
    resp4 = urllib.request.urlopen(req4)
    data4 = json.loads(resp4.read())
    projects = data4.get('projects', [])
    if projects:
        print(f"\nExisting projects ({len(projects)}):")
        for p in projects:
            aliases = p.get('alias', [])
            alias_str = aliases[0] if aliases else 'no alias'
            print(f"  {p['name']} — {alias_str}")
except Exception as e4:
    print(f"List projects: {e4}")
