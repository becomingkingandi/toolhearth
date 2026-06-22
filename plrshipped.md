# PLR Shipped — launch status

> Last edit: 2026-05-27 by Claude · Site: **LIVE** at plrshipped.com

---

## Live URLs

| What | URL |
|------|-----|
| Site (apex) | https://plrshipped.com → redirects to /plrshipped |
| www redirect | https://www.plrshipped.com → 308 → apex |
| Charter checkout ($19/mo) | https://plrshipped.lemonsqueezy.com/checkout/buy/58312a87-d3cf-4608-811f-7f9ce0175f00 |
| Monthly checkout ($29/mo) | https://plrshipped.lemonsqueezy.com/checkout/buy/184f2670-f48c-47bd-918e-ef8d9e5876c6 |
| Lifetime checkout ($249) | https://plrshipped.lemonsqueezy.com/checkout/buy/41609c50-c4ff-4090-8031-041797b974e0 |

---

## Pricing — locked

| Tier | Price | Notes |
|------|-------|-------|
| Public | $29/mo | All-access ("MOST POPULAR" card) |
| Charter (first 100) | $19/mo | Locked for life |
| Founding (50 seats) | $249 | One-time, all current + future ebooks forever |

---

## What's done

| Piece | Status | Notes |
|-------|--------|-------|
| 30 PLR ebooks (de-fab'd, end-to-end verified) | ✅ DONE | Canonical on m5 `~/Desktop/PLR/` |
| 30 PDFs | ✅ DONE | m5 `~/Desktop/PLR/` |
| 30 book covers | ✅ DONE | m5 `~/Desktop/PLR/` |
| Site deployed to Vercel | ✅ LIVE | Project `plrshipped` under team `patrick-4916s-projects` |
| apex DNS + SSL | ✅ LIVE | A 216.198.79.1 + 64.29.17.1; cert provisioned |
| www → apex redirect | ✅ LIVE | 308 added via Vercel API 2026-05-27 |
| 3 LS checkout URLs wired in site source | ✅ LIVE | See URLs above |
| SSO / preview protection off | ✅ | Disabled at project level |

---

## Open — owed by Claude

- [ ] **LS price re-verify** — LS API returning stale prices ($29.99/$249.99/$9.99) vs UI. Prices must match: Monthly $29, Charter $19, Lifetime $249
- [ ] **Webhook listener** — `100 charter / 50 lifetime` cap counter needs Lemon Squeezy webhook handler on m2
- [ ] **PLR source dir on m2** — `~/Code/launch-work/saas/plr-factory/` lost in reload. Pull from m5 via `wife-get` or update references
- [ ] **Caps webhook** — Lemon Squeezy `order_created` / `subscription_created` listener → decrement charter/lifetime seats

---

## Open — owed by Patrick

- [ ] Confirm LS prices ($19/$29/$249) via your LS dashboard before first traffic push
- [ ] Seed platform tokens for social publish (X_BEARER_TOKEN etc.) — campaigns pipeline blocked
- [ ] Record avatar video for AI-disclosure page

---

## Brief assigned to Hermes

`~/Code/scripts/briefs/plr-shipped-checkout-v1.md` — verify LS products published + prices, confirm site checkout URLs, update this tab. **Patrick: assign this in Hermes TUI when ready.**

---

## Vercel project info

```
Project:  plrshipped  (prj_L2xrZHKLWZ8h3zsXAu3QstzOoahD)
Team:     patrick-4916s-projects
Token:    ~/.vault/runtime.env → VERCEL_TOKEN
LS key:   ~/.vault/runtime.env → LEMON_SQUEEZY_API_KEY
```

---

## File layout

```
m5 ~/Desktop/PLR/
  plrshipped-library-2026-05.zip  ← deliverable bundle (30 PDFs + covers)
  <slug>.pdf                       ← 30 PDFs (canonical)
  covers/<slug>.jpg                ← 30 covers

m2 ~/Code/launch-work/saas/plr-factory/    ← MISSING (lost in reload)
  data/plr-output/<slug>/ebook.plrshipped.md  ← 30 cleaned ebook sources

~/Code/scripts/briefs/plr-shipped-checkout-v1.md  ← pending Hermes brief
```
