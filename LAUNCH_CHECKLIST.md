# ToolHearth launch checklist

## Already automated

- Run `python3 build.py` to regenerate the shared shell, canonicals, metadata, and sitemap.
- Run `python3 seo_audit.py`; deployment is ready only when it exits with zero errors.
- Canonical URLs and sitemap URLs use the live `.html` routing contract.

## Required Vercel environment variables

- `RESEND_API_KEY`: Resend API key with the sending domain verified.
- `CONTACT_TO_EMAIL`: Inbox that receives website contact submissions.
- `CONTACT_FROM_EMAIL`: Optional verified sender, for example `ToolHearth <contact@toolhearth.com>`.
- `RESEND_AUDIENCE_ID`: Resend audience used for newsletter signups.

Contact and newsletter endpoints return a clear service error until these are configured; they do not falsely claim to save or send submissions.

## Search launch

1. Deploy the committed `main` branch.
2. Verify `https://toolhearth.com/sitemap.xml` and several `.html` URLs return HTTP 200.
3. Submit the sitemap in Google Search Console and Bing Webmaster Tools.
4. Request indexing for the homepage and the strongest calculator/service pages.

## Monetization

- Keep `ads.txt` free of placeholder seller IDs.
- Add an advertising seller record only after an ad network supplies the exact verified value.
- Replace research links on comparison pages with approved, disclosed affiliate links only after joining each program.
- Confirm privacy disclosures before enabling analytics or advertising cookies.
