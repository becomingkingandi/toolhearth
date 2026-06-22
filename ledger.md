# The Ledger — trust but verify

*Every conclusion, both sides. Claude updates this as each task concludes; you check it. This is the same record Claude carries in memory across **every** chat. Last updated 2026-05-27.*

## How to read this

**"Done + verified"** means Claude opened the actual output and read it end-to-end — not "a script exited 0." Each line names *how* it was checked. If something isn't on this list with a check, treat it as **not done**.

---

## Decisions — locked

| Date | Decision |
|------|----------|
| 05-21 | **Launch order:** PLR Shipped first, then Hustle 101 |
| 05-21 | PLR Shipped's real product = the Claude-powered ebook **factory** (not a static site) |
| 05-21 | PLR Shipped checkout = **Lemon Squeezy** |
| 05-21 | **qixex** = an AI-native writing assistant (Grammarly competitor) |
| 05-21 | All AI-generated files are **kept** — training corpus for a future model |
| 05-21 | The 9 Hustle-derived course PDFs get rewritten + de-branded for Gumroad |
| 05-21 | **Video:** you record entry/hero clips + avatar source; the avatar does the bulk |
| 05-21 | Video storage = `/Volumes/4TBNVME/video-library/`; upload via the `social/` poster queue |

---

## Done + verified — Claude's side

| Work | How it was verified |
|------|---------------------|
| **PLR Shipped factory stood up** | Ran the full pipeline end-to-end. Produced *"The Cold Email Playbook"* (2,958 words). Read ebook line-by-line — clean structure, rebrandable, hedged claims, zero AI-voice tells. Rewired editor off metered API onto `claude -p` ($0/ebook). |
| **Pre-launch re-verification** | All 30 PLR ebooks + 8 courses read end-to-end by 8 parallel agents (every file, in full) + hard automated scan. **6 of 38 clean, 32 flagged.** |
| **30 PLR ebooks — de-fabbed + verified** | 25 de-fabbed with validated tool, long-tail hand-corrected, then **all 30 read end-to-end by independent agents — 30/30 clean.** |
| ~~8 courses "verified"~~ | ⚠️ **Earlier "verified" was WRONG.** Only **1 of 8 clean**. 7 have fabricated stats; one (`marketing_agency`) half-built; one (`wealth_building`) has IP-risk framing. Fix in progress. |
| **Wealth course Modules 6-10** | Read all five end-to-end. Caught 3 generic AI filler. Re-expanded 6/7/9 via `claude -p`. Re-read — clean. |
| **PLR storefront (Stitch design) restored** | Rendering verified. Superseded by 5/27 production deploy. |
| **PLR Shipped LIVE at `plrshipped.com`** | Deployed to Vercel (project `plrshipped`, team `patrick-4916s-projects`); Namecheap DNS → Vercel; SSL provisioned. Pricing: Charter $19, Monthly $29, Lifetime $249 → LS checkout URLs live. `curl -L https://plrshipped.com` → HTTP 200. ⚠️ `www.plrshipped.com` returns **HTTP 401** (Vercel SSO still on for www). |
| **PLAN-RECONSTRUCTED.md** | Written from documented record, cross-checked against source files. |
| **Avatar / voice script** | Written: `~/Code/launch-work/marketing/patrick-avatar-script.md` |
| **LAN-direct push/pull m5 ↔ m2** | Round-trip rsync verified both directions via LAN IPs. `route get` confirmed traffic on `en1`, not Tailscale. |
| **Cheat-sheet tabs restored** | All 8 tabs HTTP 200. New tabs: 📚 Reference, 📦 CLI Sheets. |
| **wife (Shemika's MacBook) wired to tailnet** | `100.122.238.46`. `ssh wife` + `wife-pull/push/get/put` work from m2/m5. ⚠️ wife currently asleep → ssh times out. |
| **n8n W5 Daily Brief crash fixed** | Ollama JSON body broke on special chars. Patched with `JSON.stringify().slice(1,-1)`. Webhook test → SUCCESS. |
| **OSINT MCP rewired to native venv** | Switched to `~/Code/GITHUB/osint-tools-mcp-server/.venv`. Registered in `~/.claude.json` ✅. ⚠️ `~/.qwen/settings.json` still points to dead docker. |

---

## Open — Claude owes

- [ ] **Fix `www.plrshipped.com` 401** — disable SSO on www subdomain or set up www → apex redirect
- [ ] **Refresh `/plrshipped` status tab** — still says *"need Patrick to paste 3 buy URLs"* (SKUs went live 5/27)
- [ ] **PLR source dir missing from m2** — `~/Code/launch-work/saas/plr-factory/` gone. Canonical assets on m5 at `~/Desktop/PLR/`. Restore or update references.
- [ ] **PLR ebooks: verify PDFs shipped from clean versions** — confirm PDFs built from clean `.plrshipped.md` not pre-fix originals
- [ ] **Verify 6 social posters upload** — built, never test-run
- [ ] **OSINT residual** — update `~/.qwen/settings.json` to native venv; wrap `theharvester` on PATH; clone + wire SpiderFoot, GHunt, Blackbird

---

## Open — you owe (Patrick)

- [ ] Create the **ops Gmail** account
- [ ] Record the entry videos + the avatar source clip
- [ ] Review `~/Code/launch-work/PLAN-RECONSTRUCTED.md`
- [ ] **Wake Shemika's Mac for SSH-while-asleep:**
  - Terminal: `sudo pmset -c sleep 0 womp 1 displaysleep 10 && sudo pmset -b sleep 15 displaysleep 5 womp 1`
  - System Settings → Battery → Options → toggle ON "Wake for network access"
- [ ] **OSINT fork direction** — fork `frishtik/osint-tools-mcp-server` to `becomingkingandi`?
- [ ] **xml-translator rebuild — yes or no?** (lost in 5/17 m2 reload)
- [ ] No-rush calls: legal/ToS · Phase B (Hustle 101 lead-magnets) · video generator choice
- [ ] **2 course calls:** `marketing_agency_course` — write 15 missing lessons or cut? · `wealth_building_course` — drop risky "11 named books" framing?

---

*Any chat, any day — both sides can open this and see what is actually done and what is still owed. That is the trust-but-verify contract.*
