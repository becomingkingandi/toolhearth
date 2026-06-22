# m2 / SHEMIKA cheat sheet

**Last updated:** 2026-06-20  
**Changes:** TrueNAS docker stack (NocoDB :8081, Metabase :3001, core stack), BigSet CLI, todos folder system on m5. Previous: 2026-06-19 TrueNAS tailnet node.

**→ [✅ Today's Todos](/todos) · [⚡ Live Status](/today)**

---

## Tailnet nodes

| Alias | Tailscale IP (away) | LAN IP (home) | Role | OS |
|-------|---------------------|---------------|------|----|
| `m5` | `100.127.124.12` | `10.0.0.210` ✓ verified | Workstation (laptop) | macOS |
| `m2` / `studio` | `100.114.240.73` | `10.0.0.216` ✓ verified | AI brain (headless) | macOS Tahoe |
| `shemika1` | `100.124.135.115` | `10.0.0.124`† | Worker: workflows + messaging | Ubuntu |
| `shemika2` | `100.121.100.78` | `10.0.0.142`† (tailscale CurAddr) | Worker: ML + monitoring | Ubuntu |
| `wife` / `shemikas-macbook-pro` | `100.122.238.46` | `10.0.0.94`† | Shemika's MacBook | macOS |
| `truenas` | `100.88.37.0` | `10.0.0.242` ✓ verified | Storage (TrueNAS Scale) | Debian 12 |
| `ctab14` | `100.67.237.124` | — | Android (often offline) | Android |
| `iphone172` | `100.101.181.2` | — | iPhone (often offline) | iOS |

> Tailscale IPs follow devices. New IP = device re-joined tailnet (machine ID regenerated). Old m2 was `100.86.179.116` — dead.
> † LAN IPs for shemika1/2/wife = best-guess from m2 ARP cache + tailscale CurAddr. Verify: `ssh <alias>home 'hostname'` when both on home LAN. Rediscover: on m2 run `arp -an | grep 10.0.0` and `tailscale status --peers --json | jq '.Peer[]|{Name:.HostName,Cur:.CurAddr}'`.

---

## Service URLs — every listening port, every node

### m2 — AI brain (away: `100.114.240.73`, home: `10.0.0.216`)

Live scan 2026-06-02. System ports omitted.

| Port | Service | Process | URL — away | URL — home |
|------|---------|---------|------------|------------|
| 22 | SSH | sshd | `ssh m2away` | `ssh m2home` |
| 53 | Lima VM DNS | limactl | — local only | — |
| 3283 | Apple Remote Desktop | ARDAgent | — | — |
| 3000 / 3030 / 8081 | Colima SSH tunnel fwds | ssh mux | — | — |
| 4445 | PLR Shipped static server | node | http://100.114.240.73:4445/ | http://10.0.0.216:4445/ |
| **5174** | **PLR Shipped Vite dev** | node/vite | http://100.114.240.73:5174/ | http://10.0.0.216:5174/ |
| **7474** | **Neo4j browser** | java | http://100.114.240.73:7474/ | http://10.0.0.216:7474/ |
| **7475** | **OpenWebUI chat** | python3 | http://100.114.240.73:7475/ | http://10.0.0.216:7475/ |
| **7687** | Neo4j Bolt | java | `bolt://100.114.240.73:7687` | `bolt://10.0.0.216:7687` |
| **8188** | **ComfyUI image gen** | Python | http://100.114.240.73:8188/ | http://10.0.0.216:8188/ |
| **8642** | **Hermes gateway** | python3/hermes_cli | http://100.114.240.73:8642/ | http://10.0.0.216:8642/ |
| **8888** | **Cheat sheet** (this page) | python3/serve.py | http://100.114.240.73:8888/ | http://10.0.0.216:8888/ |
| 9090 | real-estate-toolkit backend | python3/server.py | http://100.114.240.73:9090/ | http://10.0.0.216:9090/ |
| **11434** | **Ollama API** | ollama | http://100.114.240.73:11434/ | http://10.0.0.216:11434/ |

### m5 — workstation (away: `100.127.124.12`, home: `10.0.0.210`)

Notable ports only.

| Port | Service | Notes |
|------|---------|-------|
| 7265 | Raycast | Local API |
| **11434** | **Ollama** | Local model serving |
| 15292 / 15393 / 16494 | Adobe Creative Cloud | System |

### shemika1 (`100.124.135.115`) — workflows + messaging worker

Live scan 2026-06-02.

| Port | Service | Notes | URL |
|------|---------|-------|-----|
| 22 | SSH | `ssh shemika1` | — |
| 53 | pihole DNS (docker) | Ad blocking | — |
| 139 / 445 | Samba | File shares | — |
| **1883** | **EMQX MQTT** | TCP plain | `mqtt://100.124.135.115:1883` |
| **3000** | n8n / Grafana | Confirm which | http://100.124.135.115:3000/ |
| 3389 | RDP | Ubuntu XRDP | — |
| 5432 | PostgreSQL | localhost only | — |
| **5678** | **n8n workflow editor** | Primary UI | http://100.124.135.115:5678/ |
| **8000** | **Main backend API** | FastAPI/uvicorn classifier | http://100.124.135.115:8000/ |
| **8080** | **wormhole_server** | python3 relay | http://100.124.135.115:8080/ |
| **8081** | **AIS proxy** | node ais_proxy.js | http://100.124.135.115:8081/ |
| 8083 | EMQX WebSocket | `ws://…:8083/mqtt` | — |
| 8084 | EMQX WebSocket SSL | `wss://…:8084/mqtt` | — |
| 8883 | EMQX MQTT SSL | `mqtts://…:8883` | — |
| 11434 | Ollama | localhost only | — |
| **18081** | EMQX HTTP API | Management/prometheus | http://100.124.135.115:18081/ |
| **18083** | **EMQX dashboard** | Admin UI | http://100.124.135.115:18083/ |
| 61613 | EMQX STOMP | STOMP protocol | — |
| *(freqtrade)* | freqtrade trading bot | ftuser process, SQLite DB | — |

### shemika2 (`100.121.100.78`) — ML + monitoring worker

Live scan 2026-06-02.

| Port | Service | Notes | URL |
|------|---------|-------|-----|
| 22 | SSH | `ssh shemika2` | — |
| 53 | pihole DNS (docker) | Ad blocking | — |
| 139 / 445 | Samba | File shares | — |
| **3001** | **uptime-kuma** (docker) | Monitoring dashboard | http://100.121.100.78:3001/ |
| **3002** | docker → nginx:80 | Web service / AIS relay frontend | http://100.121.100.78:3002/ |
| 3389 | RDP | Ubuntu XRDP | — |
| 6379 | Redis | localhost only (ollama user) | — |
| **8081** | **pihole web UI** (docker) | DNS admin | http://100.121.100.78:8081/ |
| **8123** | **Home Assistant** | Home automation | http://100.121.100.78:8123/ |
| **9000** | websocket_server (docker) | `ws://100.121.100.78:9000` | — |
| **11434** | **Ollama** | Publicly bound (all interfaces) | http://100.121.100.78:11434/ |
| **18555** | WorldMonitor / AIS relay | node ais-relay.cjs | http://100.121.100.78:18555/ |

### Common across nodes

- **22** SSH on every node
- **53** DNS — m2 uses Lima/colima; shemika1/2 run pihole (docker)
- **11434** Ollama — m2 + shemika2 exposed on tailnet; shemika1 + m5 localhost only
- **3389** RDP — shemika1 + shemika2 (Ubuntu XRDP)

---

## Local Ollama models on m2

18 GB at `~/data/ollama-models/` (moved off 4TBNVME 2026-05-17). Final trimmed set — only models passing tool-call probe.

| Model | Size | Role |
|-------|------|------|
| **qwen3-coder:30b** | 18 GB | SHEMIKA primary brain — tool calling, code, agent workflows |
| **nomic-embed-text** | 274 MB | Embeddings for RAG / Chroma |

**Dropped:** hermes-3-70b (no tools template), deepseek-r1:14b, qwen2.5vl:7b, llama3.2:3b (no/poor tools support).

---

## Credentials

| Where | What |
|-------|------|
| `~/Desktop/MASTER_KEY_VAULT.xlsx` (m5) | Master keys |
| `ssh m2 cat .neo4j-password` | Neo4j password (random, mode 600) |
| `ssh m2 cat .shemika/state/credentials.json` | SHEMIKA creds (mode 600) |

---

## SHEMIKA layout

| Node | Role | Services |
|------|------|----------|
| **m2** | Brain | Hermes gateway, Ollama, Neo4j (knowledge graph + tailnet ref), OpenWebUI, 8 C-suite agents in `~/.claude/agents/` |
| **shemika1** | Workflows + messaging | n8n, EMQX, Postgres, classifier.py, custom FastAPI :8000 |
| **shemika2** | ML + monitoring | WorldMonitor, Redis, websocket server, uptime-kuma |

State on m2: `~/.shemika/state/` (rebrand_map, pipeline_locks, domains, credentials)

---

## Websites — domain portfolio

**36 domains total.** Source of truth: `~/.shemika/state/domains.json` + human-readable ledger `~/Obsidian/work/active/domain-portfolio-ledger.md`.

### Live / built (7)

| Domain | Brand | Purpose | Template |
|--------|-------|---------|----------|
| https://qixex.com | qixex | AI tools master catalog | vercel |
| https://thehustle101.com | The Hustle 101 | Mastermind / coaching landing | stripe |
| https://bypassbots.com | Bypass Bots | Resume Humanizer SaaS | superhuman |
| https://headshotforged.com | Headshot Forged | AI Headshot Studio | — |
| https://nuravitals.com | Nūra Wellness | Supplements (primary) | — |
| https://milegazette.com | MileGazette | Faceless YouTube travel | — |
| https://plrshipped.com | PLR Shipped | PLR ebook store w/ resale rights | — |

### Reserved / needs build (7)

| Domain | Brand | Status | Purpose |
|--------|-------|--------|---------|
| shopnura.com | Nūra Wellness | `reserved` | Shopify store |
| beatrejection.com | Beat Rejection | `reserved` | Bypassbots sibling |
| 3787mccree.com | HQ | `needs_build` | Corporate / About Us |
| letsmakeonemillion.com | Let's Make One Million | `needs_build` | Motivational / course funnel |
| makemilli.com | Make Milli | `needs_build` | Short brand redirect |
| cowgirlsandpoodles.com | Holding Company | `needs_port` | Corporate parent |
| pricetlg.com | (TBD) | `unassigned` | Pricing/deals tool |

### Dropped / expired (22)

- `mypdfbrain.com` — pre-launch, never active
- `funnelinstant.com` — decommissioned 2026-05-17
- `nurasupp.com`, `passatsbot.com`, `headshotmint.com`, `pdfanswer.fan` — redirect-only legacy
- `theonetravelshow.com`, `thetravelmoneyshow.com` — pre-MileGazette travel brand
- `fremant.com`, `plinvia.com` — purchased by previous session, purpose TBD
- `cthulha.com` — **expired** (not renewed)

Full archive + drop reasons in `domains.json`.

---

## Current pipeline state

| Pipeline | Status | Notes |
|----------|--------|-------|
| `travel_channel` | 🔓 **UNLOCKED** | Rebrand to MileGazette complete. Brand LOCKED 2026-05-14. Old domains no longer resolve. Workers may publish under MileGazette brand. |
| Squarespace sister | `needs_build` | Does not block content gen |

---

## Pre-reload backup

`/Volumes/4TBNVME/m2-backups/2026-05-16/pre-reload/` on m2:

- `claude-full.tar.gz`, `vault.tar.gz`, `hermes-full.tar.gz`, `LaunchAgents.tar.gz`, `shemika-data-state.tar.gz`
- `ghost-dirs/`: mccree-atlanta, seedance-mcp, videogen-mcp, bambu-mcp, qwen-builds, etc.

---

## How we work — roles

| You say | Claude does | You do | Hermes does |
|---------|-------------|--------|-------------|
| "Build X" | Writes the brief | Fire it in Hermes TUI | Builds it |
| "Is X done?" | Reads it end-to-end, signs off or sends fixes | Ship it or send fixes back | — |
| "I hit the cap" | — | Queue briefs in Hermes, Claude audits when back | Keeps building |
| "New API key" | Checks cost + fit, approves or rejects | Wire it in if approved | — |
| "Hermes is stuck" | Reads the error, writes a fix brief | Fire the fix in Hermes TUI | Retries on the fix |

- **Something scheduled broke** — Telegram pings you with error. Paste to Claude. Done.
- **Emergency stop** — Text `biggudadi` to SHEMIKA on Telegram. Everything halts. Text `resume` to start again.
- **Anything over $50** — Claude flags before it moves. You say yes or no.

---

## API routing — where builds run

| Situation | Goes to | Cost |
|-----------|---------|------|
| Everything by default | DeepSeek v4-flash | ~free |
| DeepSeek is down | Ollama on m2 (auto-switches) | $0 |
| Build has passwords / PII | Ollama on m2 (stays local) | $0 |
| Anthropic API | **NEVER. Not for anything.** | — |

**3 free keys worth refreshing** (20 min, all free tiers):

| Provider | URL | Best for |
|----------|-----|----------|
| Groq | groq.com | Simple scheduled jobs |
| Gemini | aistudio.google.com | Anything with images |
| OpenRouter | openrouter.ai | Routes to any model as backup |

Once refreshed, paste keys into `~/.hermes/.env` and tell Claude. Claude updates routing.

---

## Quick commands

### Home vs Away routing

**Rule:** Same LAN → use `*home` alias (LAN IP, no encryption overhead, no DERP relay).  
**Away from home** → use `*away` alias (tailscale, works from anywhere).

`*home` aliases fail to resolve / time out when off-LAN. Legacy aliases (`m2`/`shemika1`/`shemika2`/`wife`) point at tailscale IPs (same as `*away`).

#### Every SSH target — paired aliases

| Target | Home (LAN — fast) | Away (tailscale — anywhere) |
|--------|-------------------|-----------------------------|
| **m2** (brain) | `ssh m2home` → `10.0.0.216` | `ssh m2away` → `100.114.240.73` |
| **m5** (workstation) | `ssh m5home` → `10.0.0.210` | `ssh m5away` → `100.127.124.12` |
| **truenas** (storage) | `ssh truenas-lan` → `10.0.0.242` ✓ | `ssh truenas` → `100.88.37.0` |
| **shemika1** (workers) | `ssh shemika1home` → `10.0.0.124`† | `ssh shemika1away` → `100.124.135.115` |
| **shemika2** (workers) | `ssh shemika2home` → `10.0.0.142`† | `ssh shemika2away` → `100.121.100.78` |
| **wife** (Shemika's Mac) | `ssh wifehome` → `10.0.0.94`† | `ssh wifeaway` → `100.122.238.46` |

† = best-guess LAN IPs. Confirm first use: `ssh <alias>home 'hostname'`. If wrong box, edit `~/.ssh/config` (look for `home-vs-away aliases` block) on both m2 and m5.

#### Symmetry

Aliases live in **both** machines' `~/.ssh/config`:

- **On m5**: `m2home`/`m2away`, `shemika{1,2}{home,away}`, `wife{home,away}`
- **On m2**: `m5home`/`m5away`, `shemika{1,2}{home,away}`, `wife{home,away}`

#### Confirm LAN vs Tailscale

```bash
# Must say `en0` or `en1` (not `utun*` for Tailscale)
route -n get 10.0.0.216 | grep interface   # from m5 → m2
route -n get 10.0.0.210 | grep interface   # from m2 → m5
```

If `utun*`, Tailscale is hijacking LAN route.

#### rsync / scp / file transfer

```bash
# Home (fast LAN) — pushing m5 → m2
rsync -avP ~/big-folder/ m2home:~/big-folder/

# Away (tailscale) — same command, different alias
rsync -avP ~/big-folder/ m2away:~/big-folder/

# Pulling m2 → m5 (run from m5)
rsync -avP m2home:~/Downloads/file.zip ~/Downloads/   # home
rsync -avP m2away:~/Downloads/file.zip ~/Downloads/   # away
```

- Drop `-z` (compression) on LAN — pure overhead at gigabit speeds
- Keep `-z` on tailscale

#### Web UI URLs — copy-paste pair

| Service | Home (faster) | Away |
|---------|---------------|------|
| Cheat sheet (this page) | http://10.0.0.216:8888/ | http://100.114.240.73:8888/ |
| Neo4j browser | http://10.0.0.216:7474/ | http://100.114.240.73:7474/ |
| OpenWebUI chat | http://10.0.0.216:7475/ | http://100.114.240.73:7475/ |
| Ollama API | http://10.0.0.216:11434/ | http://100.114.240.73:11434/ |
| SHEMIKA dashboard | http://10.0.0.216:9119/ | http://100.114.240.73:9119/ |
| n8n editor (shemika1) | http://10.0.0.124:5678/ † | http://100.124.135.115:5678/ |
| EMQX dashboard (shemika1) | http://10.0.0.124:18083/ † | http://100.124.135.115:18083/ |
| shemika1 backend | http://10.0.0.124:8000/ † | http://100.124.135.115:8000/ |
| uptime-kuma (shemika2) | http://10.0.0.142:3001/ † | http://100.121.100.78:3001/ |

† = LAN IP best-guess; verify with `ssh shemika1home 'hostname'`.

---

### Legacy SSH shortcuts (tailscale-only)

```bash
ssh m2          # legacy alias for 100.114.240.73 (= m2away)
ssh shemika1    # = shemika1away
ssh shemika2    # = shemika2away
ssh wife        # = wifeaway
ssh m5          # from m2, = m5away
```

---

### Common ops

```bash
# Status of all m2 services
ssh m2away launchctl list | grep -E "patrick|claude|hermes|openwebui|homebrew"

# sheat — open TODO dashboard
alias sheat="open http://100.121.100.78:8888/todos"

# ⚡live — live status page
alias live="open http://100.121.100.78:8888/today"

# Ollama models
ssh m2away ollama list

# Neo4j device graph (tailnet)
ssh m2away cypher-shell -u neo4j -p "$(ssh m2away cat .neo4j-password)" \
  'MATCH (n:Device) RETURN n.hostname, n.tailscale_ipv4, n.online ORDER BY n.hostname'

# max-resume state
ssh m2away ls ~/.claude/state/max-resume/pending/

# tail Hermes log
ssh m2away tail -f ~/.hermes/logs/gateway.log
```

> Replace `m2away` with `m2home` when on home LAN.

---

### Alicia voice (TTS via F5-TTS)

Defined as functions in `~/.zshrc` on m5. Reload: `source ~/.zshrc`.

```bash
# Simple line (no embedded quotes)
alicia "Good morning Patrick"
alica   "typo-tolerant alias for alicia"

# Multi-line text or anything with quotes / apostrophes
alicia-long << 'EOF'
Anything goes here.
Multiple lines.
"Double quotes" and 'apostrophes' work fine.
$variables won't expand because of single-quoted EOF.
EOF
```

Output WAVs → `~/Desktop/alicia-HHMMSS.wav` → autoplay at 0.75x.  
Engine: F5-TTS at `~/Code/GITHUB/F5-TTS/` on m2.  
Reference clip: `iCloud/ClaudeSync/vault/voice/shamika/shamika-04.wav` (Alicia, personal-use approval only).

#### ask-alicia — pipe Ollama answer through Alicia voice

```bash
ask-alicia "why is the sky blue"
ask-alicia "what should I make for dinner"
ask-alicia "give me one weird octopus fact"
```

Flow: m5 → SSH m2 → Ollama (qwen2.5:7b, 2 sentences) → shamika-say.sh renders WAV → SCP back to m5 Desktop → autoplay at 0.75x. ~15-25s. Fully local.

Change model in `~/.zshrc`: replace `qwen2.5:7b` with any model in `ollama list`.

---

### Hummingbot — quick API probes

Base URL: `http://100.124.135.115:8002`  
Auth: `hummingbot` / (vault: `~/.vault/shemika-creds.env`)

```bash
# Strategies / controllers available
curl -s -u hummingbot:PASS http://100.124.135.115:8002/controllers/ | python3 -m json.tool

# Exchanges / connectors wired
curl -s -u hummingbot:PASS http://100.124.135.115:8002/connectors/ | python3 -m json.tool

# Accounts with credentials
curl -s -u hummingbot:PASS http://100.124.135.115:8002/accounts/

# Swagger explorer UI
open http://100.124.135.115:8002/docs
```

**Current state:** 21 strategies + 40+ exchanges wired, but `master_account` has zero credentials → no trading. To go live: add API keys via `/accounts/add-credential/master_account/<exchange>`.

---

### Sync commands — clipboard + files between m5 ↔ remote

Naming: **`<target>-<verb>`**

| Target | Box |
|--------|-----|
| `sh1` | shemika1 |
| `sh2` | shemika2 |
| `m2m` | m2 (Mac) |
| `wife` | Shemika's MacBook |

| Verb | Direction |
|------|-----------|
| `pull` | remote clipboard → m5 clipboard |
| `push` | m5 clipboard → remote |
| `get` | remote file/dir → m5 current dir |
| `put` | m5 file/dir → remote (default: `~/`) |

#### Full command table

| Target | Pull text | Push text | Get file | Put file |
|--------|-----------|-----------|----------|----------|
| **shemika1** | `sh1-pull` | `sh1-push` | `sh1-get PATH` | `sh1-put FILE` |
| **shemika2** | `sh2-pull` | `sh2-push` | `sh2-get PATH` | `sh2-put FILE` |
| **m2** | `m2m-pull` | `m2m-push` | `m2m-get PATH` | `m2m-put FILE` |
| **wife** | `wife-pull` | `wife-push` | `wife-get PATH` | `wife-put FILE` |

Tab-complete: type `sh1-` + Tab.

#### Examples

```bash
# Copy on m5 (⌘C), send to shemika1's ~/.clipboard
sh1-push

# Pull shemika2's clipboard onto m5
sh2-pull

# Push file to m2 home dir
m2m-put ~/Desktop/notes.md

# Get folder from shemika1 into current m5 dir
sh1-get /home/shemika1/data/exports/

# Pull all PDFs from Shemika's MacBook home
wife-get '~/*.pdf'

# Push file to her MacBook
wife-put ~/Desktop/for-shemika.pdf
```

#### Worked example — m5 ↔ m2 Downloads over LAN

| Box | LAN IP | User | Tailscale IP |
|-----|--------|------|--------------|
| m5 | `10.0.0.210` | `m5maxl` | `100.127.124.12` |
| m2 | `10.0.0.216` | `m2max` | `100.114.240.73` |

Confirm LAN:

```bash
# on m5
route -n get 10.0.0.216 | grep interface
# on m2
route -n get 10.0.0.210 | grep interface
# Must say en1, NOT utun*
```

Push m5 → m2 (run on m5):

```bash
rsync -avP ~/Downloads/mydog.txt m2max@10.0.0.216:~/Downloads/
```

Pull m2 → m5 (run on m5):

```bash
rsync -avP m2max@10.0.0.216:~/Downloads/mydog.txt ~/Downloads/
```

Push m2 → m5 (run on m2):

```bash
rsync -avP ~/Downloads/mydog.txt m5maxl@10.0.0.210:~/Downloads/
```

Pull m5 → m2 (run on m2):

```bash
rsync -avP m5maxl@10.0.0.210:~/Downloads/mydog.txt ~/Downloads/
```

| Piece | Meaning |
|-------|---------|
| `m2max@10.0.0.216` | m2 LAN IP + user — forces route over `en1`, NOT Tailscale |
| `~/Downloads/` (trailing slash) | Drops file INTO `Downloads/` on destination |
| `-a` | Archive mode (perms, times, recursion) |
| `-v` | Verbose |
| `-P` | Progress bar + resume partials |
| no `-z` | Compression dropped — pure overhead at gigabit LAN speeds |

**Trailing-slash gotcha:**
- `~/Downloads/` (with slash) → file goes INTO the folder ✓
- `~/Downloads` (no slash) → file is RENAMED to `Downloads` ✗

When to use LAN vs Tailscale:
- **LAN IP** — both boxes at home, same network. Faster, no encryption overhead.
- **`m2m-put`/`m2m-get` wrappers (Tailscale)** — m5 away from home, or any cross-LAN box.

**Verified working:** 2026-05-27 — round-trip with probe files, both directions via `en1`, not `utun*`.

#### Under the hood

- **Clipboard** = SSH + `pbcopy`/`pbpaste` for Mac targets; Linux targets write to `~/.clipboard` and m5 reads back
- **Files** = `rsync -avzP`
- **Spaces in filenames** — fine with `wife-get '~/Downloads/Some File.pdf'`. Requires homebrew rsync 3.x on m5 (Apple's `/usr/bin/rsync` is 2.6.9 and word-splits on spaces)
- All defined as zsh functions in `~/.zshrc` on m5

#### Legacy aliases (still work)

`pull1`, `push1`, `pull2`, `push2`, `pullm2`, `pushm2` → clipboard  
`pf1`, `gf1`, `pf2`, `gf2`, `pfm2`, `gfm2` → files  
`getlinux1`, `putlinux1`, `getlinux2`, `putlinux2` → clipboard

---

### Raw rsync — when wrappers aren't enough

| Flag | What it does |
|------|--------------|
| `-a` | Archive mode (perms, times, symlinks, recursion) |
| `-v` | Verbose |
| `-z` | Compress on wire (good for tailnet/slow networks) |
| `-P` | Progress bar + resume partials |
| `-n` | Dry run (show what WOULD happen, don't copy) |
| `--delete` | Mirror — delete files in DEST not in SRC |
| `--exclude=PATTERN` | Skip matching files (repeatable) |
| `--include=PATTERN` | Force-include even if excluded |
| `--bwlimit=KBPS` | Bandwidth cap (e.g. `1000` = 1MB/s) |
| `-e "ssh -p 2222"` | Custom SSH command |

**Common patterns:**

```bash
# Dry-run first
rsync -avzPn ~/Code/myproject/ shemika1:~/myproject/

# Mirror (deletes orphans on destination)
rsync -avzP --delete ~/Code/myproject/ shemika1:~/myproject/

# Skip node_modules / .git / build artifacts
rsync -avzP --exclude=node_modules --exclude=.git --exclude=dist \
  ~/Code/myproject/ shemika1:~/myproject/

# Cap bandwidth to 5MB/s
rsync -avzP --bwlimit=5000 ~/big-folder/ m2:~/big-folder/

# Pull whole home dir
rsync -avzP --exclude=.cache --exclude=Library shemika1:~/ ~/shemika1-backup/

# Two-way: pull THEN push
gf1 ~/work/notes.md ~/Desktop/   # pull
pf1 ~/Desktop/notes.md ~/work/   # push back
```

**Trailing slash gotcha:**
- `rsync -av  SRC/   DEST/` → copies CONTENTS of SRC into DEST
- `rsync -av  SRC    DEST/` → copies SRC ITSELF as subdirectory inside DEST
- When unsure: dry-run with `-n` first.

---

## Known issues / TODO

| Issue | Status |
|-------|--------|
| ~~Ollama persistence: launchd can't read `/Volumes/4TBNVME` on Tahoe (TCC)~~ | **RESOLVED 2026-05-17.** Models moved to `~/data/ollama-models/`. Plist updated. Reboot-survival verified. |
| m2 console-only tasks | iCloud per-app toggles, FDA grants, Claude Code `/login` rotation |

---

## What was deliberately removed (post-reload)

- `com.patrick.mlx-ollama-shim` — MLX shim (source gone, Metal works)
- `com.patrick.m2-watchdog` — redundant with launchd KeepAlive
- `com.patrick.neo-resurgens` — non-AI HTTP file server
- `com.patrick.tailnet-ref-server` — replaced by Neo4j + watcher
- `com.patrick.claude.max-resume-rearm` (plist on disk, intentionally unloaded)

---

## TrueNAS Docker stack (at 100.88.37.0 / 10.0.0.242)

**SSH:** `sshpass -p 'RacerBoi#1' ssh truenas_admin@100.88.37.0` or `ssh -i ~/.ssh/id_truenas ...`  
**Web UI:** `https://100.88.37.0` or `https://10.0.0.242` (root / RacerBoi#1)  
**Pool:** `tank` — 4×14TB RAID-Z2, 24T free  
**Docker compose files:** `/mnt/tank/apps/`

### Core stack (always on)

| Container | Port | What |
|-----------|------|------|
| Postgres | 5432 | DB (user n8n, db n8n) |
| Redis | 6379 | Cache |
| MinIO | 9000/9001 | S3-compatible storage |
| n8n | 5678 | Workflow automation |
| Portainer | 9443 | Docker management |
| Watchtower | — | Auto-updates containers |
| Stirling-PDF | 8080 | PDF tools |

### Tools stack (deployed 2026-06-20)

| Container | Port | What |
|-----------|------|------|
| NocoDB | 8081 | Airtable clone — product DB, orders, suppliers |
| Metabase | 3001 | BI dashboards — sales/profit connected to Postgres |

### Sentinel (on shemika2, not TrueNAS)

**Port:** 9000 — security monitoring (Kismet WiFi, OSINT, RuView presence). Docker container, needs WiFi dongle for monitor mode + API keys.

---

## New tools on shemika2

| Tool | Where | What |
|------|-------|------|
| BigSet | npm global (`@adamexu/bigset`) | Build datasets from web — `bigset create "trending travel gadgets" --csv` |
| NocoDB | ~/Code/nocodb (1.6 GB) | Airtable clone — on TrueNAS :8081 |
| Metabase | ~/Code/metabase (2.3 GB) | BI — on TrueNAS :3001 |
| Twenty CRM | ~/Code/twenty (334 MB) | Open source CRM (not deployed) |
| Appsmith | ~/Code/appsmith (1.4 GB) | Internal tool builder (not deployed) |
| Invoice Ninja | ~/Code/invoiceninja (4.4 GB) | Invoicing / billing (not deployed) |

### BigSet quick start

```bash
# Requires TinyFish API key + OpenRouter key (OpenRouter in ~/.hermes/.env)
bigset create "fintech startups in the bay area" --rows 10 --wait --csv fintech.csv
bigset list
bigset export <datasetId> --csv out.csv
```

---

## TODOs folder system (on m5 Desktop)

**Location:** `~/Desktop/todos/`  
**System:** Dated subfolders per due-date. Plain text files = action items.  
**Monday HTML:** `~/Desktop/todos/monday.html` — clickable full task list.

```
todos/
├── monday.html              # Open this first
├── 2026-06-22/              # Due Monday
├── 2026-06-25/              # Due Thursday
├── 2026-06-29/              # Due next week
└── 2026-07-06/              # Longer term
```

---

## Hermes cron output dirs

**Location:** `~/.hermes/cron/output/` — migrated to category/named hierarchy 2026-06-12.  
**Categories:** marketing, finance, executive, comms, daily, ops, store, trovIr, archive.  
**Each job_id dir** is a REVERSE symlink into the named dir. Files land via symlink. Zero maintenance.

---

## MCP servers

| Name | Type | Tools | What it does |
|------|------|-------|--------------|
| **`shemika-rag`** | Python | kb_search, kb_add, kb_list, kb_collection_info | Semantic search/write to Chroma KB (216 chunks) |
| **`shemika-csuite`** | Python | ask_cdo, ask_cfo, ask_clo, ask_cmo, ask_coo, ask_cpo, ask_cto, ask_chief_of_staff, list_csuite | SHEMIKA delegates to 8 C-suite agents (qwen3-coder + role prompt) |
| `seedance` | Node/tsx | 6 video gen tools | `~/Code/mcp-servers/seedance-mcp/` — has `.env` ✓ |
| `videogen` | Node/tsx | — | `~/Code/mcp-servers/videogen-mcp/` — needs `.env` |
| `bambu` | Python 3.12 venv | — | `~/Code/mcp-servers/bambu-mcp/` — needs `.env` |

Registered in `~/.claude.json` + Hermes. Restart Claude Code to load.

---

## SHEMIKA dashboard

| Item | Detail |
|------|--------|
| URL | http://100.114.240.73:9119/ |
| Management | Sessions, config, env vars, model selection, providers, MCP servers, plugins, billing |
| launchd | `com.patrick.shemika-dashboard` (auto-restart, tailnet-reachable) |

---

## Launch plan — 14-day sprint (D14 = 2026-05-31)

| Phase | Status | Description |
|-------|--------|-------------|
| 0 | ✅ **complete** | Hustle 101 humanize: 47 docx processed → preserved at `~/data/hustle101-humanized/` |
| 1 | ✅ **live** | Hustle 101 → Chroma RAG (460 chunks in `shemika_knowledge`) |
| 2 | ✅ **live** | C-suite agents as MCP tools |
| 3 | ✅ **live** | SHEMIKA dashboard on m2:9119 (rebranded, launchd-managed) |
| 4 | ⏳ pending | ElevenLabs voice replies via Telegram voice messages |
| 5 | ⏳ pending | Cron jobs — morning briefing (6:30 AM), evening recap, daily watchdog |
| 6 | 🟢 **bundle ready** | thehustle101.com landing + Stripe pre-order ($1,497 × 10 = $14,970) |
| 7 | ⏳ pending | Magic-link auth + customer dashboard + per-customer SHEMIKA pairing |
| + | 🟢 **bundle ready** | qixex.com SaaS umbrella + 5 wrappers + PLR Factory + 10 lifecycle emails |

Full daily roadmap: `~/Code/launch-work/14-DAY-LAUNCH-PLAN.md`

---

## Chroma vector DB

| Property | Value |
|----------|-------|
| Path | `~/data/chroma/` (m2) |
| Collection | `shemika_knowledge` — 460 chunks |
| Ingestion | `~/Code/mcp-servers/shemika-rag/ingest_hustle101.py` watches `~/data/hustle101-humanized/` |
| Embedding model | nomic-embed-text |
| Access | shemika-rag MCP (`kb_search`, `kb_add`, `kb_list`, `kb_collection_info`) |

---

## Still-open gaps

- **Ollama persistence**: needs Full Disk Access grant via console GUI. Until then runs via `nohup` and dies on reboot.
- **Trading stack repos** (freqtrade / hummingbot-api / TradingAgents / condor / worldmonitor) — on disk, no processes. On-demand only.
- **Backup ghost-dirs not restored** (in 4TBNVME tarballs): virtual_me, headshot_studio, plr, domain_hunter, business_intel, publishers, mccree-atlanta, apis, backend, qwen-builds — extract on demand.

---

## OLD SHEMIKA — DELETED 2026-05-17

`~/Code/GITHUB/nexus-hub/` removed entirely. 670 MB tarball at:

```
/Volumes/4TBNVME/m2-backups/2026-05-17/nexus-hub-final-archive.tar.gz
```

Hustle 101 humanized corpus → `~/data/hustle101-humanized/` → ingested into Chroma (the only thing from nexus-hub that mattered survived).

---

## Launch sequence

| # | What | Window | Target |
|---|------|--------|--------|
| 1 | **Hustle 101 cohort** (thehustle101.com) | D1-D14 → 2026-05-31 | $14,970 (10 × $1,497 seats) |
| 2 | **PLR Factory + qixex.com** | D15-D28 → 2026-06-14 | Recurring SaaS subs + ebook trickle |

Launch #1 plan: `~/Code/launch-work/14-DAY-LAUNCH-PLAN.md`  
Launch #2 plan: `~/Code/launch-work/saas/plr-factory/LAUNCH-PLAN.md`

D14 is Hustle-101-only. SaaS bundle stays frozen until D15.

---

## Hardware roadmap

| Item | Status | Why |
|------|--------|-----|
| GMKtec EVO-X2 (Strix Halo, 128GB, ~8-12TB) | KEEP → shemika3 | AI flagship, post-move production node |
| **UGREEN DXP8800 Plus** (i5-1235U, 8-bay, 2×TB4, 2×10GbE) | **BUY (~$900)** → primary NAS | TB4 direct to m5 = 40 Gbps, 30W idle, silent |
| Minisforum AI X1 Pro 370 | SELL eBay | Wrong chip class for AI |
| **Dell PowerEdge R530 #1** | **SELL eBay** | UGREEN replaces both Dells |
| **Dell PowerEdge R530 #2** | **SELL eBay** | UGREEN replaces both Dells |
| 8 × 14TB HDDs | KEEP ALL → into UGREEN | 4K + photography + GMKtec mirror |
| Nikon Z8 | Own | 4K recording for Hustle 101 |
| 4TB NVMe (`/Volumes/4TBNVME`) | Return to Patrick post-GMKtec | Personal drive on loan |

### UGREEN DXP8800 Plus BOM (~$1,420 total)

| Item | Source | Price | Link |
|------|--------|-------|------|
| UGREEN DXP8800 Plus 8-bay NAS (diskless) | Amazon | $1,210 | B0D22HGH4N — watch for $1,099 sale |
| 2 × NEMIX 32GB DDR5-4800 (= 64GB) | Amazon | $160 | B0FLYMJJJN — qty 2 |
| Cable Matters 2m Active TB4 (100W) | Amazon | $50 | B0CBHKVTSL |
| OS: TrueNAS Scale (free) | — | $0 | Mature ZFS vs young UGOS Pro |

**Critical RAM specs:**
- DDR5-4800 (PC5-38400). i5-1235U caps at 4800 — DDR5-5600 will downclock.
- Max RAM = 64GB (2 × 32GB). Max on day one — ZFS benefits from comfortable ARC cache.

**Architecture:**
- m5 → TB4 cable → UGREEN (40 Gbps direct)
- UGREEN 10GbE #1 → LAN/router (internet + GMKtec)
- UGREEN 10GbE #2 → reserved for shemika3 direct link
- 8 × 14TB RAIDZ2 = 84TB usable, tolerate any 2 drive failures

**Cash recovered from sells:**
- Minisforum AI X1 Pro 370: ~$1,200-1,500
- Dell R530 #1: $200-400
- Dell R530 #2: $200-400
- **Net: UGREEN fully funded + $600-1,200 surplus**

### Rack decision: NO RACK (locked 2026-05-17)

UGREEN on shelf/desk. No rack, no UPS, no switch, no patch panel. Saves ~$330.

### Production kit

Patrick has everything for recording (CFexpress, lav, lighting, etc.). Not in BOM.

---

## Marketing system (Master Launch System)

Built 2026-05-17 via 5 parallel agents. Lives at `~/Code/launch-work/marketing/`:

| File | Purpose |
|------|---------|
| `MASTER-LAUNCH-SYSTEM.md` | 605-line playbook: 7 channels, 7-day sprint template, decision tree, kill/double-down criteria, voice rules |
| `HUSTLE101-D1-D14-ACQUISITION.md` | 1,321 lines, 73 actions, 30 social posts, 10 DM variations, 6 Reddit posts |
| `PLR-FACTORY-LAUNCH-PLAYBOOK.md` | 5 forum targets, 50 named affiliates, 140 actions across D15-D28 |
| `BYPASSBOTS-GTM.md` | Students niche locked, 3 differentiators, D7 target = 10 customers |

**Live tracking dashboard:** http://100.114.240.73:9120/launches

**Test-then-scale tempo:**
1. Launch #1 (D1-D14): Hustle 101 → calibrate channels, capture metrics
2. Launch #2 (D15-D28): PLR Factory → second data point
3. Sunday retros → roll into MASTER-LAUNCH-SYSTEM.md
4. Launches #3-60 (D29+): 2-3/week using calibrated system

---

## Viewing this cheat sheet

Served from this box (shemika2):

| View | URL |
|------|-----|
| Rendered | http://100.121.100.78:8888/ |
| ✅ Today's Todos | http://100.121.100.78:8888/todos |
| Raw .md | http://100.121.100.78:8888/raw |

---

## Reference — CLI & zsh

For Patrick's machines (m2/m5 = macOS, shemika1/shemika2 = Ubuntu). Community cheat sheet: [milanaryal/cli-cheat-sheet](https://github.com/milanaryal/cli-cheat-sheet).

### zsh essentials (universal)

```bash
# Variables
NAME="Patrick"            # set (no spaces around =)
echo "$NAME"              # use (quote it)
echo "${NAME}_suffix"     # braces when appending text

# Pipes
ls | grep ".txt"          # keep only .txt
cat file | wc -l          # count lines

# Redirects
echo "hi" > file.txt      # overwrite
echo "more" >> file.txt   # append
command 2>/dev/null       # discard errors
command > out.txt 2>&1    # output + errors to out.txt

# History
history                   # show past commands
!!                        # re-run last
!ssh                      # re-run last cmd starting with "ssh"
Ctrl+R                    # search history interactively

# Globbing
ls *.txt                  # all .txt files
ls **/*.py                # all .py in subdirectories (zsh)
ls file?.txt              # one-char wildcard
```

### Filesystem navigation

```bash
pwd                       # where am I
cd ~/Code                 # go to directory
cd -                      # back to previous
cd ..                     # up one level
ls                        # list
ls -la                    # all (incl hidden) + details
ls -lt                    # by modified time, newest first
mkdir -p a/b/c            # nested directories
cp file dest/             # copy
mv file newname           # move/rename
rm file                   # delete (NO undo)
rm -rf dir/               # delete directory (DANGER — verify first)
```

### Reading files

```bash
cat file                  # dump whole file
head -20 file             # first 20 lines
tail -20 file             # last 20 lines
tail -f log.txt           # follow live (Ctrl+C to stop)
less file                 # scroll (q quit, / search)
wc -l file                # count lines
```

### Searching

```bash
grep "error" log.txt          # find lines with "error"
grep -i "error" log.txt       # case-insensitive
grep -r "TODO" ~/Code         # recursive
grep -c "error" log.txt       # count matches
find ~/Code -name "*.py"      # find files by name
find . -mtime -1              # files modified <24h
```

### Pipes + redirects combined

```bash
ps aux | grep ollama | grep -v grep        # find ollama process
ls -lt ~/Desktop | head -5                 # 5 newest on Desktop
grep -r "shemika" ~/.vault | wc -l         # count mentions
```

### Permissions

```bash
chmod +x script.sh        # make executable
chmod 600 secret.env      # owner read/write only (secrets)
chmod 755 script.sh       # owner full, others read+execute
ls -la                    # see rwx columns
```

### Processes

```bash
ps aux                    # list all running
top                       # live monitor (q to quit)
kill <PID>                # politely stop
kill -9 <PID>             # force-kill (last resort)
command &                 # background
nohup command &           # background, survives logout
```

### SSH (tailnet)

Every target has `*home` (LAN) and `*away` (tailscale) alias. Full table above.

```bash
# Home (LAN — fast, same network only)
ssh m2home                # → m2 via 10.0.0.216
ssh shemika1home          # → shemika1 via 10.0.0.124
ssh shemika2home          # → shemika2 via 10.0.0.142
ssh wifehome              # → Shemika's Mac via 10.0.0.94
ssh m5home                # → m5 via 10.0.0.210 (from m2)
ssh truenas-lan           # → TrueNAS via 10.0.0.242

# Away (tailscale — anywhere)
ssh m2away                # → m2 via 100.114.240.73
ssh shemika1away          # → shemika1 via 100.124.135.115
ssh shemika2away          # → shemika2 via 100.121.100.78
ssh wifeaway              # → Shemika's Mac via 100.122.238.46
ssh m5away                # → m5 via 100.127.124.12 (from m2)
ssh truenas               # → TrueNAS via 100.88.37.0

# Legacy (still works = *away variants)
ssh m2 ; ssh shemika1 ; ssh shemika2 ; ssh wife ; ssh m5 ; ssh truenas

# One-shot remote command
ssh m2home 'uptime'       # at home: zero tailscale overhead
ssh m2away 'uptime'       # anywhere
```

### SMB mount (m5 → TrueNAS Data share)

Mount the 24 TB Data share on m5. Auto-detects home LAN or Tailscale.

```bash
# Auto — tries LAN first, falls back to Tailscale
mount-data

# Force specific path
mount-data-home           # LAN only
mount-data-away           # Tailscale only

# Unmount
umount-data

# Mount point: ~/mnt/data/
```

Aliases in m5's `~/.zshrc`. SMB creds: user `marq`, password same as everything else.

### macOS vs Linux gotchas

Same command, different behavior. m2/m5 = BSD tools; shemika1/2 = GNU tools.

| Task | macOS (m2/m5) | Linux (shemika1/2) |
|------|--------------|--------------------|
| In-place edit | `sed -i '' 's/a/b/' f` | `sed -i 's/a/b/' f` |
| Yesterday's date | `date -v-1d` | `date -d yesterday` |
| Resolve symlink fully | (no `readlink -f`) | `readlink -f link` |
| Colored ls | `ls -G` | `ls --color` |
| Perl-style grep | (limited) | `grep -P` works |
| File stat | `stat -f "%Sm" f` | `stat -c "%y" f` |

**Rule of thumb:** Script works on m2 but breaks on shemika1 = BSD-vs-GNU flag difference, not shell problem.

zsh is the SHELL (language). Commands (`ls`, `grep`, etc.) come from the OS. shemika1/2 default to **bash** — when you SSH in, you may be in bash. Basic syntax identical; advanced features differ.

---

## Meme Coin Temperature Index

| Command | What | How |
|---------|------|-----|
| `meme-temp` | Terminal table of top meme coins with 0-100 temp score | `python3 ~/bin/meme-temp` |
| `memetemp` | Live HTML dashboard via cheat-sheet server | `curl http://localhost:8888/meme-temp` |
| `http://sheat:8888/meme-temp` | Live web view | Browser on m5 |

**Scoring:** Volume(25%) + Momentum(15%) + Price 1h(20%) + Price 6h(10%) + Price 24h(5%) + Buy Pressure(15%) + Liquidity(10%). Data from DexScreener API.

---

## Bloomberg Terminal — Personal Market Monitor

| Command | What |
|---------|------|
| `bb` | Full dashboard: crypto + stocks + commodities + forex |
| `bb --crypto` | Crypto + meme coin temperature only |
| `bb --stocks` | Equities (S&P 500, Dow, Nasdaq, AAPL, MSFT, etc) |
| `bb --commodities` | Gold, Silver, Oil, Nat Gas, Copper |
| `bb --forex` | Forex pairs |
| `bb --watch BTC` | Single ticker quote (crypto + stocks) |
| `bbdash` | Web dashboard (curl localhost:8888/bb) |
| `/bb` or `/bloomberg-term` | Live HTML dashboard |

**Data sources:** CoinGecko (crypto) + DexScreener (meme coins) + yfinance (stocks/commodities/forex).
