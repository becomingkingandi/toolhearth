import dns from "node:dns/promises";
import net from "node:net";
import tls from "node:tls";

const MAX_BYTES = 1_500_000;
const TIMEOUT_MS = 10_000;
const requests = new Map();

function rateLimited(req) {
  const ip = String(req.headers?.["x-forwarded-for"] || req.socket?.remoteAddress || "unknown").split(",")[0].trim();
  const now = Date.now();
  const current = requests.get(ip);
  if (!current || now - current.started > 60_000) {
    requests.set(ip, { started: now, count: 1 });
    return false;
  }
  current.count += 1;
  return current.count > 20;
}

function isPrivateIp(ip) {
  if (net.isIPv4(ip)) {
    const p = ip.split(".").map(Number);
    return p[0] === 10 || p[0] === 127 || p[0] === 0 ||
      (p[0] === 169 && p[1] === 254) || (p[0] === 172 && p[1] >= 16 && p[1] <= 31) ||
      (p[0] === 192 && p[1] === 168) || (p[0] === 100 && p[1] >= 64 && p[1] <= 127) ||
      p[0] >= 224;
  }
  const value = String(ip).toLowerCase();
  return value === "::1" || value === "::" || value.startsWith("fc") ||
    value.startsWith("fd") || value.startsWith("fe8") || value.startsWith("fe9") ||
    value.startsWith("fea") || value.startsWith("feb");
}

async function safeUrl(raw) {
  let url;
  try {
    url = new URL(String(raw || "").trim());
  } catch {
    throw new Error("Enter a complete URL beginning with http:// or https://.");
  }
  if (!["http:", "https:"].includes(url.protocol) || url.username || url.password) {
    throw new Error("Only public HTTP and HTTPS URLs are supported.");
  }
  if (["localhost", "localhost.localdomain"].includes(url.hostname.toLowerCase())) {
    throw new Error("Private and local addresses are not allowed.");
  }
  const records = await dns.lookup(url.hostname, { all: true });
  if (!records.length || records.some((record) => isPrivateIp(record.address))) {
    throw new Error("Private and local addresses are not allowed.");
  }
  return url;
}

async function fetchPage(raw, method = "GET") {
  const started = Date.now();
  let url = await safeUrl(raw);
  let response;
  for (let redirects = 0; redirects <= 5; redirects += 1) {
    response = await fetch(url, {
      method,
      redirect: "manual",
      signal: AbortSignal.timeout(TIMEOUT_MS),
      headers: { "user-agent": "ToolHearth Site Tools/1.0 (+https://toolhearth.com)" },
    });
    if (![301, 302, 303, 307, 308].includes(response.status)) break;
    const location = response.headers.get("location");
    if (!location) break;
    url = await safeUrl(new URL(location, url).href);
    if (redirects === 5) throw new Error("The URL exceeded the redirect limit.");
  }
  if (method === "HEAD" && response.status === 405) {
    response = await fetch(url, {
      method: "GET",
      redirect: "manual",
      signal: AbortSignal.timeout(TIMEOUT_MS),
      headers: { "user-agent": "ToolHearth Site Tools/1.0 (+https://toolhearth.com)", range: "bytes=0-0" },
    });
  }
  const elapsedMs = Date.now() - started;
  const headers = Object.fromEntries(response.headers.entries());
  if (method === "HEAD") {
    response.body?.cancel();
    return { url: response.url, status: response.status, headers, elapsedMs, html: "", bytes: 0 };
  }
  const reader = response.body?.getReader();
  const chunks = [];
  let bytes = 0;
  while (reader) {
    const { done, value } = await reader.read();
    if (done) break;
    bytes += value.byteLength;
    if (bytes > MAX_BYTES) {
      await reader.cancel();
      throw new Error("The page is larger than the 1.5 MB inspection limit.");
    }
    chunks.push(value);
  }
  const combined = new Uint8Array(bytes);
  let offset = 0;
  for (const chunk of chunks) {
    combined.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return {
    url: response.url,
    status: response.status,
    headers,
    elapsedMs,
    bytes,
    html: new TextDecoder().decode(combined),
  };
}

function parsePage(page) {
  const html = page.html;
  const title = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1]?.replace(/<[^>]+>/g, "").trim() || "";
  const description = html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)/i)?.[1] ||
    html.match(/<meta[^>]+content=["']([^"']*)["'][^>]+name=["']description["']/i)?.[1] || "";
  const headings = [...html.matchAll(/<(h[1-6])\b[^>]*>([\s\S]*?)<\/\1>/gi)].map((m) => ({
    level: Number(m[1].slice(1)),
    text: m[2].replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim(),
  }));
  const images = [...html.matchAll(/<img\b([^>]*)>/gi)].map((m) => ({
    src: m[1].match(/\bsrc=["']([^"']+)/i)?.[1] || "",
    alt: m[1].match(/\balt=["']([^"']*)/i)?.[1] ?? null,
  }));
  const links = [...html.matchAll(/<a\b[^>]*href=["']([^"'#]+)[^"']*["']/gi)]
    .map((m) => {
      try {
        const url = new URL(m[1], page.url);
        return ["http:", "https:"].includes(url.protocol) ? url.href : "";
      } catch { return ""; }
    }).filter(Boolean);
  const icons = [...html.matchAll(/<link\b([^>]*rel=["'][^"']*icon[^"']*["'][^>]*)>/gi)]
    .map((m) => m[1].match(/\bhref=["']([^"']+)/i)?.[1] || "")
    .filter(Boolean).map((href) => {
      try {
        const url = new URL(href, page.url);
        return ["http:", "https:"].includes(url.protocol) ? url.href : "";
      } catch { return ""; }
    }).filter(Boolean);
  return {
    ...page,
    title,
    description,
    headings,
    images,
    links: [...new Set(links)].slice(0, 100),
    icons: [...new Set(icons)],
    html: html.slice(0, MAX_BYTES),
  };
}

async function checkLinks(url) {
  const page = parsePage(await fetchPage(url));
  const candidates = page.links.slice(0, 25);
  const results = await Promise.all(candidates.map(async (link) => {
    try {
      const item = await fetchPage(link, "HEAD");
      return { url: link, status: item.status, ok: item.status < 400, elapsedMs: item.elapsedMs };
    } catch (error) {
      return { url: link, status: 0, ok: false, error: error.message };
    }
  }));
  return { source: page.url, checked: results.length, results };
}

async function domainInfo(raw) {
  const url = await safeUrl(raw.includes("://") ? raw : `https://${raw}`);
  const hostname = url.hostname;
  const [a, aaaa, mx, ns, txt] = await Promise.all([
    dns.resolve4(hostname).catch(() => []),
    dns.resolve6(hostname).catch(() => []),
    dns.resolveMx(hostname).catch(() => []),
    dns.resolveNs(hostname).catch(() => []),
    dns.resolveTxt(hostname).catch(() => []),
  ]);
  const certificate = await new Promise((resolve) => {
    const socket = tls.connect(443, hostname, { servername: hostname, timeout: 7000 }, () => {
      const cert = socket.getPeerCertificate();
      socket.end();
      resolve(cert?.valid_to ? {
        subject: cert.subject?.CN || hostname,
        issuer: cert.issuer?.O || cert.issuer?.CN || "",
        validFrom: cert.valid_from,
        validTo: cert.valid_to,
        daysRemaining: Math.ceil((new Date(cert.valid_to) - Date.now()) / 86400000),
      } : null);
    });
    socket.on("error", () => resolve(null));
    socket.on("timeout", () => { socket.destroy(); resolve(null); });
  });
  return { hostname, dns: { a, aaaa, mx, ns, txt }, certificate };
}

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });
  if (rateLimited(req)) return res.status(429).json({ error: "Too many checks. Please wait one minute and try again." });
  const { action, url } = req.body || {};
  try {
    if (action === "page") return res.status(200).json(parsePage(await fetchPage(url)));
    if (action === "status") return res.status(200).json(await fetchPage(url, "HEAD"));
    if (action === "links") return res.status(200).json(await checkLinks(url));
    if (action === "domain") return res.status(200).json(await domainInfo(String(url || "")));
    return res.status(400).json({ error: "Unknown action" });
  } catch (error) {
    return res.status(400).json({ error: error?.message || "Inspection failed" });
  }
}
