#!/usr/bin/env python3
"""Fail the build when core crawlability and on-page SEO contracts regress."""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://toolhearth.com"
errors = []
warnings = []


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def local_path(url):
    path = urlparse(url).path
    if path in ("", "/"):
        return os.path.join(ROOT, "index.html")
    if path.endswith("/"):
        return os.path.join(ROOT, path.lstrip("/"), "index.html")
    return os.path.join(ROOT, path.lstrip("/"))


html_files = []
for directory, _, filenames in os.walk(ROOT):
    if ".git" in directory or "graphify-out" in directory:
        continue
    html_files.extend(os.path.join(directory, f) for f in filenames if f.endswith(".html"))

for path in sorted(html_files):
    rel = os.path.relpath(path, ROOT)
    source = read(path)
    static_source = re.sub(r"<script\b[^>]*>.*?</script>", "", source, flags=re.I | re.S)
    static_source = re.sub(r"<style\b[^>]*>.*?</style>", "", static_source, flags=re.I | re.S)
    titles = re.findall(r"<title>(.*?)</title>", static_source, re.I | re.S)
    descriptions = re.findall(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)', static_source, re.I)
    canonicals = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', static_source, re.I)
    h1s = re.findall(r"<h1\b", static_source, re.I)
    if len(titles) != 1 or not titles[0].strip():
        errors.append(f"{rel}: expected one non-empty title")
    if len(descriptions) != 1 or not descriptions[0].strip():
        errors.append(f"{rel}: expected one non-empty meta description")
    if len(canonicals) != 1:
        errors.append(f"{rel}: expected one canonical URL")
    elif not os.path.isfile(local_path(canonicals[0])):
        errors.append(f"{rel}: canonical points to missing file: {canonicals[0]}")
    if len(h1s) != 1:
        warnings.append(f"{rel}: expected one H1, found {len(h1s)}")
    for raw in re.findall(r'href=["\']([^"\'#?]+)', static_source, re.I):
        if raw.startswith(("mailto:", "tel:", "javascript:", "http://", "https://")):
            continue
        target = local_path(SITE + (raw if raw.startswith("/") else "/" + raw))
        if not os.path.exists(target):
            errors.append(f"{rel}: broken internal link: {raw}")

sitemap_path = os.path.join(ROOT, "sitemap.xml")
try:
    tree = ET.parse(sitemap_path)
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = [node.text for node in tree.findall("sm:url/sm:loc", namespace)]
    if not sitemap_urls:
        errors.append("sitemap.xml: no URLs found")
    for url in sitemap_urls:
        if not url or not url.startswith(SITE) or not os.path.isfile(local_path(url)):
            errors.append(f"sitemap.xml: URL has no built file: {url}")
except (ET.ParseError, OSError) as exc:
    errors.append(f"sitemap.xml: {exc}")

for path in html_files:
    source = read(path)
    for script in re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', source, re.I | re.S):
        try:
            json.loads(script)
        except json.JSONDecodeError as exc:
            errors.append(f"{os.path.relpath(path, ROOT)}: invalid JSON-LD: {exc}")

print(f"SEO audit: {len(html_files)} HTML files · {len(errors)} errors · {len(warnings)} warnings")
for warning in warnings[:20]:
    print(f"WARN: {warning}")
for error in errors[:100]:
    print(f"ERROR: {error}")
sys.exit(1 if errors else 0)
