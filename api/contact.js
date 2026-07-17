// /api/contact.js — deliver contact form submissions through Resend.
export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { name, email, subject, message, company } = req.body || {};

  if (company) {
    return res.status(200).json({ success: true });
  }
  if (!/^\S+@\S+\.\S+$/.test(email || "") || !message || message.length > 5000) {
    return res.status(400).json({ error: "Email and message required" });
  }

  const apiKey = process.env.RESEND_API_KEY;
  const to = process.env.CONTACT_TO_EMAIL;
  const from = process.env.CONTACT_FROM_EMAIL || "ToolHearth <contact@toolhearth.com>";
  if (!apiKey || !to) {
    return res.status(503).json({ error: "Contact delivery is not configured" });
  }

  const clean = (value, fallback = "") => String(value || fallback).replace(/[<>]/g, "").trim();
  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from,
      to: [to],
      reply_to: clean(email).toLowerCase(),
      subject: `[ToolHearth] ${clean(subject, "Website contact").slice(0, 120)}`,
      text: `Name: ${clean(name, "Anonymous")}\nEmail: ${clean(email)}\n\n${clean(message).slice(0, 5000)}`,
    }),
  });

  if (!response.ok) {
    return res.status(502).json({ error: "Message delivery failed" });
  }

  return res.status(200).json({
    success: true,
    message: "Thanks! We'll be in touch soon."
  });
}
