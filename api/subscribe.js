// /api/subscribe.js — add email signups to a configured Resend audience.
export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { email, company } = req.body || {};

  if (company) {
    return res.status(200).json({ success: true });
  }
  if (!/^\S+@\S+\.\S+$/.test(email || "")) {
    return res.status(400).json({ error: "Valid email required" });
  }

  const apiKey = process.env.RESEND_API_KEY;
  const audienceId = process.env.RESEND_AUDIENCE_ID;
  if (!apiKey || !audienceId) {
    return res.status(503).json({ error: "Newsletter signup is not configured" });
  }

  const response = await fetch(`https://api.resend.com/audiences/${audienceId}/contacts`, {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      email: String(email).trim().toLowerCase(),
      unsubscribed: false,
    }),
  });

  if (!response.ok && response.status !== 409) {
    return res.status(502).json({ error: "Newsletter signup failed" });
  }

  return res.status(200).json({
    success: true,
    message: "Subscribed successfully."
  });
}
