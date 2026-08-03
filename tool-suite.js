(function () {
  "use strict";

  const root = document.querySelector(".direct-tool[data-app]");
  if (!root) return;
  const app = root.dataset.app;
  const approvedPageIntro = root.innerHTML;
  const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[char]));
  const formatBytes = (bytes) => bytes < 1024 ? `${bytes} B` :
    bytes < 1048576 ? `${(bytes / 1024).toFixed(1)} KB` : `${(bytes / 1048576).toFixed(2)} MB`;
  const setStatus = (message, error) => {
    const node = root.querySelector(".status");
    if (!node) return;
    node.textContent = message;
    node.classList.toggle("error", Boolean(error));
  };
  const setBusy = (busy) => {
    root.querySelectorAll("button").forEach((button) => { button.disabled = busy; });
  };
  async function request(action, url) {
    const response = await fetch("/api/site-tools", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ action, url }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "The check could not be completed.");
    return data;
  }
  function download(name, content, type) {
    const link = document.createElement("a");
    link.href = URL.createObjectURL(new Blob([content], { type }));
    link.download = name;
    link.click();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  }
  function panel(form, result = "") {
    root.innerHTML = `${approvedPageIntro}<section class="tool-panel">${form}<p class="status" role="status" aria-live="polite"></p></section>
      <section class="result-panel" ${result ? "" : "hidden"}>${result}</section>`;
  }
  function urlForm(label, button, placeholder = "https://example.com") {
    return `<form class="url-form"><label for="target-url">${label}</label>
      <div class="control-grid"><input id="target-url" type="url" required placeholder="${placeholder}" autocomplete="url">
      <button type="submit">${button}</button></div></form>`;
  }
  function bindUrl(action, render) {
    root.querySelector(".url-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const url = root.querySelector("#target-url").value;
      setBusy(true); setStatus("Working…");
      try {
        const data = await request(action, url);
        render(data);
        root.querySelector(".result-panel").hidden = false;
        setStatus("Complete.");
      } catch (error) { setStatus(error.message, true); }
      finally { setBusy(false); }
    });
  }
  function metrics(items) {
    return `<div class="metric-grid">${items.map(([value, label]) =>
      `<div class="metric"><strong>${escapeHtml(value)}</strong><span>${escapeHtml(label)}</span></div>`).join("")}</div>`;
  }

  const apps = {
    "accessibility-checker": function () {
      panel(urlForm("Public page URL", "Check accessibility"));
      bindUrl("page", (data) => {
        const issues = [];
        const h1s = data.headings.filter((h) => h.level === 1);
        const missingAlt = data.images.filter((image) => image.alt === null);
        if (!data.html.match(/<html[^>]+lang=/i)) issues.push("The HTML element has no language attribute.");
        if (!data.title) issues.push("The page has no document title.");
        if (h1s.length !== 1) issues.push(`Expected one H1 heading; found ${h1s.length}.`);
        if (missingAlt.length) issues.push(`${missingAlt.length} image(s) have no alt attribute.`);
        if (!data.html.match(/<main\b/i)) issues.push("No main landmark was detected.");
        if (!data.html.match(/(?:skip|jump)[^<]{0,25}(?:content|main)/i)) issues.push("No obvious skip-to-content link was detected.");
        root.querySelector(".result-panel").innerHTML = `<h2>Accessibility review</h2>${metrics([
          [issues.length, "Potential issues"], [data.images.length, "Images"], [data.headings.length, "Headings"], [data.status, "HTTP status"]
        ])}<ul class="result-list">${(issues.length ? issues : ["No issues were detected by these automated checks."]).map((issue) =>
          `<li class="${issues.length ? "fail" : ""}">${escapeHtml(issue)}</li>`).join("")}</ul>
          <p class="text-muted">Automated checks cannot prove WCAG conformance. Complete keyboard and assistive-technology testing is still required.</p>`;
      });
    },
    "website-performance-analyzer": function () {
      panel(urlForm("Public page URL", "Analyze performance"));
      bindUrl("page", (data) => {
        const scripts = (data.html.match(/<script\b/gi) || []).length;
        const styles = (data.html.match(/<link[^>]+stylesheet/gi) || []).length;
        const score = Math.max(0, Math.min(100, 100 - Math.round(data.elapsedMs / 50) -
          Math.round(data.bytes / 100000) - scripts - styles));
        root.querySelector(".result-panel").innerHTML = `<h2>Response analysis</h2>${metrics([
          [score, "Diagnostic score"], [`${data.elapsedMs} ms`, "Server response"], [formatBytes(data.bytes), "HTML transfer"], [data.status, "HTTP status"]
        ])}<ul class="result-list">
          <li>${scripts} script element(s) and ${styles} stylesheet request(s) detected.</li>
          <li>${data.images.length} image element(s) detected in the initial HTML.</li>
          <li>This is a first-response diagnostic, not a synthetic Lighthouse lab test.</li>
        </ul>`;
      });
    },
    "broken-link-checker": function () {
      panel(urlForm("Public page URL", "Check links"));
      bindUrl("links", (data) => {
        const broken = data.results.filter((item) => !item.ok);
        root.querySelector(".result-panel").innerHTML = `<h2>Link report</h2>${metrics([
          [data.checked, "Links checked"], [broken.length, "Potentially broken"], [data.checked - broken.length, "Healthy"], ["25", "Check limit"]
        ])}<ul class="result-list">${data.results.map((item) =>
          `<li class="${item.ok ? "" : "fail"}"><strong>${item.status || "Error"}</strong> ${escapeHtml(item.url)}</li>`).join("")}</ul>`;
      });
    },
    "domain-inspector": function () {
      panel(urlForm("Domain or website URL", "Inspect domain", "example.com"));
      bindUrl("domain", (data) => {
        const dnsRows = Object.entries(data.dns).flatMap(([type, values]) =>
          values.map((value) => `<tr><th>${type.toUpperCase()}</th><td>${escapeHtml(typeof value === "string" ? value : JSON.stringify(value))}</td></tr>`)).join("");
        const cert = data.certificate;
        root.querySelector(".result-panel").innerHTML = `<h2>${escapeHtml(data.hostname)}</h2>${metrics([
          [data.dns.a.length + data.dns.aaaa.length, "IP addresses"], [data.dns.mx.length, "Mail servers"],
          [data.dns.ns.length, "Name servers"], [cert ? cert.daysRemaining : "—", "TLS days remaining"]
        ])}<table><tbody>${dnsRows || "<tr><td>No DNS records returned.</td></tr>"}</tbody></table>
          ${cert ? `<h3>TLS certificate</h3><p>Subject: ${escapeHtml(cert.subject)}<br>Issuer: ${escapeHtml(cert.issuer)}<br>Expires: ${escapeHtml(cert.validTo)}</p>` : ""}`;
      });
    },
    "sitemap-generator": function () {
      panel(urlForm("Public page URL", "Generate sitemap"));
      bindUrl("page", (data) => {
        const origin = new URL(data.url).origin;
        const urls = [data.url, ...data.links.filter((link) => {
          try { return new URL(link).origin === origin; } catch (_) { return false; }
        })];
        const unique = [...new Set(urls)].slice(0, 100);
        const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${unique.map((url) =>
          `  <url><loc>${escapeHtml(url)}</loc></url>`).join("\n")}\n</urlset>`;
        root.querySelector(".result-panel").innerHTML = `<h2>Sitemap preview</h2>${metrics([[unique.length, "URLs found"], [origin, "Site origin"]])}
          <button type="button" class="xml-download">Download sitemap.xml</button><pre><code>${escapeHtml(xml)}</code></pre>`;
        root.querySelector(".xml-download").addEventListener("click", () => download("sitemap.xml", xml, "application/xml"));
      });
    },
    "http-status-checker": function () {
      panel(urlForm("Public URL", "Check status"));
      bindUrl("status", (data) => {
        root.querySelector(".result-panel").innerHTML = `<h2>HTTP response</h2>${metrics([
          [data.status, "Status code"], [`${data.elapsedMs} ms`, "Response time"], [new URL(data.url).protocol.replace(":", "").toUpperCase(), "Protocol"], [Object.keys(data.headers).length, "Headers"]
        ])}<table><tbody>${Object.entries(data.headers).map(([name, value]) =>
          `<tr><th>${escapeHtml(name)}</th><td>${escapeHtml(value)}</td></tr>`).join("")}</tbody></table>`;
      });
    },
    "responsive-website-checker": function () {
      root.innerHTML = `${approvedPageIntro}<section class="tool-panel"><form class="preview-form"><label for="preview-url">Public page URL</label>
        <div class="control-grid"><input id="preview-url" type="url" required placeholder="https://example.com"><button>Open preview</button></div></form>
        <div class="control-grid" role="group" aria-label="Preview width"><button type="button" data-width="375">Mobile</button><button type="button" data-width="768">Tablet</button><button type="button" data-width="100%">Desktop</button></div>
        <p class="status">Some websites block embedding with security headers; open those sites directly and resize your browser.</p></section>
        <section class="result-panel"><div class="device-frame" style="width:375px;max-width:100%"><iframe title="Responsive website preview"></iframe></div></section>`;
      const frame = root.querySelector("iframe");
      root.querySelector(".preview-form").addEventListener("submit", (event) => {
        event.preventDefault();
        frame.src = root.querySelector("#preview-url").value;
      });
      root.querySelectorAll("[data-width]").forEach((button) => button.addEventListener("click", () => {
        root.querySelector(".device-frame").style.width = button.dataset.width === "100%" ? "100%" : `${button.dataset.width}px`;
      }));
    },
    "open-graph-image-generator": function () {
      root.innerHTML = `${approvedPageIntro}<section class="tool-panel"><form class="og-form"><div class="control-grid stack">
        <label>Title<input id="og-title" required maxlength="90" value="Build something useful"></label>
        <label>Description<textarea id="og-description" maxlength="180">Free browser-based tools from ToolHearth.</textarea></label>
        <label>Accent color<input id="og-color" type="color" value="#66d9ef"></label><button>Generate image</button></div></form><p class="status"></p></section>
        <section class="result-panel"><canvas width="1200" height="630"></canvas><button class="og-download" type="button">Download PNG</button></section>`;
      const draw = () => {
        const canvas = root.querySelector("canvas"), ctx = canvas.getContext("2d");
        const color = root.querySelector("#og-color").value;
        ctx.fillStyle = "#17191a"; ctx.fillRect(0, 0, 1200, 630);
        ctx.fillStyle = color; ctx.fillRect(0, 0, 18, 630);
        ctx.fillStyle = color; ctx.font = "700 26px monospace"; ctx.fillText("TOOLHEARTH / OPEN GRAPH", 70, 90);
        ctx.fillStyle = "#f5f5f2"; ctx.font = "700 72px sans-serif";
        wrap(ctx, root.querySelector("#og-title").value, 70, 210, 1060, 84);
        ctx.fillStyle = "#a9adaf"; ctx.font = "30px sans-serif";
        wrap(ctx, root.querySelector("#og-description").value, 70, 470, 1020, 42);
        setStatus("Image generated.");
      };
      root.querySelector(".og-form").addEventListener("submit", (event) => { event.preventDefault(); draw(); });
      root.querySelector(".og-download").addEventListener("click", () => {
        const link = document.createElement("a"); link.download = "open-graph-image.png"; link.href = root.querySelector("canvas").toDataURL("image/png"); link.click();
      });
      draw();
    },
    "keyword-density-checker": function () {
      root.innerHTML = `${approvedPageIntro}<section class="tool-panel"><form class="density-form"><label for="density-text">Paste text</label>
        <textarea id="density-text" required placeholder="Paste an article, landing page, or document…"></textarea><button>Analyze keywords</button></form><p class="status"></p></section>
        <section class="result-panel" hidden></section>`;
      root.querySelector(".density-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const words = root.querySelector("#density-text").value.toLowerCase().match(/[a-z0-9][a-z0-9'-]*/g) || [];
        const stop = new Set("the a an and or but if in on at to for of with is are was were be been this that it as by from your you".split(" "));
        const counts = {};
        words.filter((word) => word.length > 2 && !stop.has(word)).forEach((word) => { counts[word] = (counts[word] || 0) + 1; });
        const rows = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 30);
        root.querySelector(".result-panel").hidden = false;
        root.querySelector(".result-panel").innerHTML = `<h2>Keyword report</h2>${metrics([[words.length, "Total words"], [Object.keys(counts).length, "Unique keywords"]])}
          <table><thead><tr><th>Keyword</th><th>Count</th><th>Density</th></tr></thead><tbody>${rows.map(([word, count]) =>
            `<tr><td>${escapeHtml(word)}</td><td>${count}</td><td>${((count / words.length) * 100).toFixed(2)}%</td></tr>`).join("")}</tbody></table>`;
        setStatus("Analysis complete.");
      });
    },
    "html-to-pdf": function () {
      root.innerHTML = `${approvedPageIntro}<section class="tool-panel"><form class="pdf-form"><label for="pdf-html">HTML content</label>
        <textarea id="pdf-html" required><h1>Printable document</h1><p>Edit this HTML, preview it, then choose Print / Save as PDF.</p></textarea>
        <button>Preview document</button></form><p class="status"></p></section>
        <section class="result-panel"><iframe title="Printable HTML preview"></iframe><button type="button" class="print-pdf">Print / Save PDF</button></section>`;
      const frame = root.querySelector("iframe");
      const render = () => { frame.srcdoc = root.querySelector("#pdf-html").value; setStatus("Preview ready."); };
      root.querySelector(".pdf-form").addEventListener("submit", (event) => { event.preventDefault(); render(); });
      root.querySelector(".print-pdf").addEventListener("click", () => frame.contentWindow.print());
      render();
    },
    "image-compressor": function () {
      root.innerHTML = `${approvedPageIntro}<section class="tool-panel"><label for="image-file">Choose a JPG, PNG, or WebP image</label>
        <input id="image-file" type="file" accept="image/jpeg,image/png,image/webp"><label for="image-quality">Quality</label>
        <input id="image-quality" type="range" min="20" max="95" value="78"><button type="button" class="compress-image">Compress image</button><p class="status"></p></section>
        <section class="result-panel" hidden><img class="preview" alt="Compressed preview"><br><a class="download-link" download="compressed-image.webp">Download WebP</a></section>`;
      root.querySelector(".compress-image").addEventListener("click", () => {
        const file = root.querySelector("#image-file").files[0];
        if (!file) return setStatus("Choose an image first.", true);
        const image = new Image();
        image.onload = () => {
          const canvas = document.createElement("canvas");
          const scale = Math.min(1, 2400 / Math.max(image.width, image.height));
          canvas.width = Math.round(image.width * scale); canvas.height = Math.round(image.height * scale);
          canvas.getContext("2d").drawImage(image, 0, 0, canvas.width, canvas.height);
          canvas.toBlob((blob) => {
            const url = URL.createObjectURL(blob);
            root.querySelector(".result-panel").hidden = false;
            root.querySelector(".preview").src = url; root.querySelector(".download-link").href = url;
            setStatus(`Compressed ${formatBytes(file.size)} to ${formatBytes(blob.size)}.`);
          }, "image/webp", Number(root.querySelector("#image-quality").value) / 100);
        };
        image.src = URL.createObjectURL(file);
      });
    },
    "favicon-extractor": function () {
      panel(urlForm("Public website URL", "Find favicons"));
      bindUrl("page", (data) => {
        const icons = data.icons.length ? data.icons : [new URL("/favicon.ico", data.url).href];
        root.querySelector(".result-panel").innerHTML = `<h2>Detected icons</h2><ul class="result-list">${icons.map((url) =>
          `<li><img src="${escapeHtml(url)}" alt="" width="32" height="32"> <a href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(url)}</a></li>`).join("")}</ul>`;
      });
    },
  };

  function wrap(ctx, text, x, y, maxWidth, lineHeight) {
    const words = String(text).split(/\s+/); let line = "";
    for (const word of words) {
      const test = `${line}${word} `;
      if (ctx.measureText(test).width > maxWidth && line) { ctx.fillText(line, x, y); line = `${word} `; y += lineHeight; }
      else line = test;
    }
    ctx.fillText(line, x, y);
  }

  if (apps[app]) apps[app]();
})();
