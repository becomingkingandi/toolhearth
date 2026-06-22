# m2 Tools & CLI Inventory

Full production machine. Everything below is installed and on PATH.

---

## AI / ML

| CLI | What it does | Key command |
|-----|-------------|-------------|
| `claude` | Claude Code (Max plan, free) | `claude` in any project dir |
| `qwen` | Qwen local via Ollama (Node 22 wrapper) | `qwen` — points at local Ollama |
| `ollama` | Local LLM server — runs models on MPS | `ollama run llama3.2`, `ollama list` |
| `huggingface-cli` | HF model downloads, repo management | `huggingface-cli download model/id` |
| `hf` | HF CLI alias | same as above |
| `mlx.launch` | Apple MLX distributed inference | `mlx.launch script.py` |
| `whisper-cli` | Local speech-to-text (whisper.cpp) | `whisper-cli -m model.bin -f audio.wav` |
| `whisper-server` | REST API for whisper | `whisper-server -m model.bin --port 8178` |
| `tiny-agents` | Anthropic tiny-agents runner | `tiny-agents run agent.json` |

**ComfyUI** — running at http://localhost:8188
- Models: Flux 1-dev (fp8), SDXL 1.0
- Image gen API: `POST http://127.0.0.1:8188/prompt`

---

## Media Processing

| CLI | What it does |
|-----|-------------|
| `ffmpeg` | Video/audio encode, convert, extract, stream |
| `ffprobe` | Media file inspection |
| `ffplay` | Media playback |
| `yt-dlp` | Download video/audio from YouTube, 1000+ sites |
| `whisper-cli` | Speech-to-text from audio files |
| `rubberband` | Audio time-stretch and pitch-shift |
| `flac` / `metaflac` | FLAC audio encode/decode/tag |
| `lame` | MP3 encoder |
| `mpg123` | MP3 decoder/player |
| `sndfile-convert` | Audio format conversion |
| `djxl` / `cjxl` | JPEG XL encode/decode |
| `dwebp` / `cwebp` | WebP encode/decode |
| `img2webp` | Convert images to WebP |
| `gif2webp` | Convert GIF to WebP |
| `pandoc` | Universal document converter (md→pdf, docx, html…) |
| `tesseract` | OCR — extract text from images |

---

## Web & Deployment

| CLI | What it does |
|-----|-------------|
| `vercel` | Deploy to Vercel, manage projects/domains |
| `gh` | GitHub CLI — PRs, issues, repos, gists |
| `deno` | Deno runtime (TypeScript/JS, no node_modules) |
| `node` / `npm` / `npx` | Node.js 26, npm 11 |
| `uvicorn` | ASGI server for FastAPI/Starlette |
| `fastapi` | FastAPI dev server CLI |
| `uv` / `uvx` | Ultra-fast Python package manager (replaces pip/venv) |
| `httpx` | HTTP client CLI |
| `wsdump` | WebSocket REPL client |

---

## Network & Security

| CLI | What it does |
|-----|-------------|
| `tailscale` | Tailscale VPN management — status, up, down, ping |
| `nmap` | Network scanner — ports, OS detection, service version |
| `ncat` | Netcat — TCP/UDP connections, port forwarding |
| `nping` | Packet generation and analysis |
| `ndiff` | Compare nmap scan results |
| `subfinder` | Subdomain enumeration (OSINT) |
| `mosh` | SSH replacement — survives connection drops |
| `age` / `age-keygen` | Simple file encryption |
| `gpg` / `gpgme` | PGP encryption, signing, key management |
| `openssl` | TLS/SSL tools, cert inspection, crypto |
| `gnutls-cli` | TLS client — test certs and connections |

---

## Database

| CLI | What it does | URL |
|-----|-------------|-----|
| `neo4j` | Neo4j server management | :7474 (browser), :7687 (bolt) |
| `cypher-shell` | Neo4j Cypher REPL | `cypher-shell -u neo4j` |

---

## Infrastructure / Containers

| CLI | What it does |
|-----|-------------|
| `docker` / `docker-compose` | Container management |
| `colima` | macOS container runtime (Docker Desktop replacement) |
| `lima` / `limactl` | Linux VMs on macOS |
| `kubectl.lima` | Kubernetes via Lima VM |
| `podman.lima` | Podman via Lima VM |

---

## Dev Tools

| CLI | What it does |
|-----|-------------|
| `git` | Version control |
| `gh` | GitHub CLI |
| `rg` | ripgrep — fast recursive search (better than grep) |
| `fzf` | Fuzzy finder — pipe anything through it |
| `tmux` | Terminal multiplexer — persistent sessions |
| `protoc` | Protocol Buffers compiler |
| `make` | Build automation |
| `figlet` | ASCII art text (banners) |

---

## Fleet — SSH & Remote Desktop

### SSH Quick Reference

| Alias | What it is | LAN IP | User |
|-------|------------|--------|------|
| `ssh studio` or `ssh m2` | m2 Mac Studio (headless AI server) | 10.0.0.243 | m2max |
| `ssh m5` *(from m2)* | m5 MacBook Pro (workstation) | 10.0.0.44 | m5maxl |
| `ssh racerboi` or `ssh racerboi1` | RacerBoi#1 — Kubuntu Linux box | 10.0.0.192 | marq |
| `ssh shemika1` | Shemika1 server | tailnet only | shemika1 |
| `ssh shemika2` | Shemika2 server | tailnet only | shemika2 |

All aliases work from m2 and m5. RacerBoi has the full fleet config too.

### Remote Desktop — RacerBoi#1 (Kubuntu)

| Mode | Address | Protocol | Password |
|------|---------|----------|----------|
| **Home (LAN)** | `vnc://10.0.0.192` | VNC :5900 | RacerBoi#1 |
| **Away (Tailscale)** | `vnc://100.93.249.127` | VNC :5900 | RacerBoi#1 |
| **Away (hostname)** | `vnc://marq-wi6.tail0661ca.ts.net` | VNC :5900 | RacerBoi#1 |
| **RDP (any)** | `10.0.0.192:3389` or `100.93.249.127:3389` | RDP | RacerBoi#1 |

Tailscale node name: **marq-wi6** · Tailnet IP: **100.93.249.127**

### Remote Desktop — m2 Mac Studio

| Mode | Address |
|------|---------|
| **Home (LAN)** | `vnc://10.0.0.243` |
| **Away (Tailscale)** | `vnc://100.114.240.73` |

---

## File & Compression

| CLI | What it does |
|-----|-------------|
| `zstd` / `zstdmt` | Fast compression (Zstandard) |
| `lz4` | Extremely fast compression |
| `xz` / `lzma` | High-ratio compression |
| `age` | File encryption |
| `pdfinfo` / `pdftotext` / `pdfimages` | PDF inspection and extraction |
| `pandoc` | Convert between document formats |
| `qrencode` | Generate QR codes from CLI |

---

## Local Agents & Custom Bins (`~/.local/bin`)

| CLI | What it does |
|-----|-------------|
| `cua-driver` | macOS GUI automation — AX tree, click, type |
| `research-bot` | Custom research agent |
| `wife` | Custom CLI (context: Shemika messages/commands) |
| `uv` / `uvx` | Python env manager |

---

## Excel Dashboard Auto-Builder (`~/xlsdashboard/` on m5)

Scripts: `~/xlsdashboard/analyze_schema.py` + `~/xlsdashboard/generate_vba.py`

**One-liner — analyze + generate in one shot:**
```bash
python3 ~/xlsdashboard/analyze_schema.py ~/yourfile.xlsx | \
  python3 ~/xlsdashboard/generate_vba.py - ~/DashboardModule.bas
```

**Step by step:**
```bash
# 1. See what columns were detected
python3 ~/xlsdashboard/analyze_schema.py ~/yourfile.xlsx

# 2. Save schema, then generate
python3 ~/xlsdashboard/analyze_schema.py ~/yourfile.xlsx > /tmp/schema.json
python3 ~/xlsdashboard/generate_vba.py /tmp/schema.json ~/DashboardModule.bas
```

**Then in Excel:**
1. File → Save As → **Excel Macro-Enabled Workbook (.xlsm)**
2. Excel menu → Preferences → Security → **Enable all macros** + **Trust access to VBA project object model**
3. Data sheet tab must be named **`Data`** (rename if needed)
4. Tools → Macro → **Visual Basic Editor**
5. File → **Import File** → select `DashboardModule.bas`
6. Run → Run Macro → **`BuildSalesDashboard`** → Run

**Column roles detected automatically:**

| Role | Detected by header contains |
|------|---------------------------|
| `period_col` | "month", "date", "quarter", "year", "week" |
| `id_col` | "id", "order", "invoice", "transaction" |
| `primary_measure` | Numeric + "amount", "sales", "revenue", "units" |
| `target_measure` | Numeric + "target", "goal", "budget", "forecast" |
| `dimensions` | Categorical cols with < 50% unique values |

**Common fixes:**

| Problem | Fix |
|---------|-----|
| "Field not found" error | Column name mismatch — edit `PivotFields("...")` in `.bas` |
| KPI cards show 0 | Click **Data → Refresh All** after macro runs |
| No module in VBE | Import failed — re-do File → Import File |

---

## Generation Stack Summary

| Tool | Type | Status | Use for |
|------|------|--------|---------|
| ComfyUI + Flux 1-dev | Image (local) | Running :8188 | Hero images, mockups, backgrounds |
| ComfyUI + SDXL 1.0 | Image (local) | Ready | Alternative image gen |
| OpenAI DALL-E 3 | Image (cloud) | Key active | Quick concepts |
| Higgsfield Ultra | Video (cloud) | ~2,389 credits | AI video, avatar composites |
| DeepSeek | Text (cloud) | Key active | Copy, content, briefs |
| Ollama | Text (local) | Running :11434 | Private/offline LLM inference |
| Whisper | Speech→Text (local) | Installed | Transcription, voice input |
