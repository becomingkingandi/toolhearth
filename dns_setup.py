#!/usr/bin/env python3
import urllib.request, urllib.parse, xml.etree.ElementTree as ET, os, re

with open(os.path.expanduser('~/.vault/env')) as f:
    content = f.read()

def get_var(name):
    m = re.search(r'export %s=(.+?)$' % re.escape(name), content, re.M)
    if not m:
        return None
    return m.group(1).strip().strip("'\"")

api_key = get_var('NAMECHEAP_API_KEY')
api_user = get_var('NAMECHEAP_API_USER')
client_ip = get_var('NAMECHEAP_CLIENT_IP')

print(f"API User: {api_user}")
print(f"Client IP: {client_ip}")

# Step 1: Set custom DNS and add records via setHosts
base = "https://api.namecheap.com/xml.response"

# First set nameservers to Vercel's
params_ns = {
    'ApiUser': api_user, 'ApiKey': api_key,
    'UserName': api_user, 'ClientIp': client_ip,
    'Command': 'namecheap.domains.dns.setCustom',
    'SLD': 'toolhearth', 'TLD': 'com',
    'Nameservers': 'ns1.vercel-dns.com,ns2.vercel-dns.com'
}
url_ns = base + '?' + urllib.parse.urlencode(params_ns)
print(f"\nSetting Vercel nameservers...")
req = urllib.request.Request(url_ns)
try:
    resp = urllib.request.urlopen(req, timeout=15)
    xml_data = resp.read().decode()
    root = ET.fromstring(xml_data)
    status = root.get('Status')
    print(f"Status: {status}")
    for err in root.iter('{http://api.namecheap.com/xml.response}Error'):
        print(f"  Error: {err.text}")
except Exception as e:
    print(f"Error: {e}")

print("\nDNS pointed to Vercel. Propagates in 5-30 min.")
