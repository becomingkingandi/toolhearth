// /api/subscribe.js — proxy to internal email webhook
export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { email, source } = req.body;

  if (!email) {
    return res.status(400).json({ error: "Email required" });
  }

  try {
    const webhookUrl = process.env.EMAIL_WEBHOOK_URL || "http://100.121.100.78:8088/signup";

    const response = await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, source: source || "toolhearth" }),
      timeout: 10000
    });

    const data = await response.json();

    if (!response.ok) {
      console.error(`[email-api] webhook error: ${response.status}`, data);
      return res.status(response.status || 500).json(data);
    }

    return res.status(200).json({ success: true, message: "Subscribed!" });
  } catch (error) {
    console.error("[email-api] error:", error.message);
    return res.status(500).json({
      error: "Failed to subscribe. Please try again later.",
      details: error.message
    });
  }
}
