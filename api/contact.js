// /api/contact.js — send contact form to email webhook
export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { name, email, subject, message } = req.body;

  if (!email || !message) {
    return res.status(400).json({ error: "Email and message required" });
  }

  try {
    const webhookUrl = process.env.EMAIL_WEBHOOK_URL || "http://100.121.100.78:8088/signup";

    // Send contact info as a special signup with contact details in source
    const contactData = `contact|${name || "Anonymous"}|${subject || "Contact Form"}`;

    const response = await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        source: contactData
      }),
      timeout: 10000
    });

    const data = await response.json();

    if (!response.ok) {
      console.error(`[contact-api] webhook error: ${response.status}`, data);
      return res.status(response.status || 500).json(data);
    }

    // TODO: also email the message to support@toolhearth.com
    console.log(`[contact-api] contact from ${email}: ${subject}`);

    return res.status(200).json({ success: true, message: "Thanks! We'll be in touch soon." });
  } catch (error) {
    console.error("[contact-api] error:", error.message);
    return res.status(500).json({
      error: "Failed to send. Please email support@toolhearth.com",
      details: error.message
    });
  }
}
