// /api/contact.js — process contact form submissions
export const config = {
  runtime: 'nodejs18.x',
};

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { name, email, subject, message } = req.body;

  if (!email || !message) {
    return res.status(400).json({ error: "Email and message required" });
  }

  try {
    // Log the contact to console
    console.log(`[CONTACT] From: ${name || "Anonymous"} <${email}>`);
    console.log(`[CONTACT] Subject: ${subject || "Contact Form"}`);
    console.log(`[CONTACT] Message: ${message}`);

    // Try to forward to webhook
    try {
      await Promise.race([
        fetch("http://100.121.100.78:8088/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email,
            source: `contact|${name || "Anonymous"}|${subject || "Contact Form"}`
          })
        }),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error("timeout")), 3000)
        )
      ]);
    } catch (webhookError) {
      console.warn(`[WEBHOOK] Could not reach webhook: ${webhookError.message}`);
    }

    // Return success to user
    return res.status(200).json({
      success: true,
      message: "Thanks! We'll be in touch soon."
    });

  } catch (error) {
    console.error("[CONTACT] Error:", error.message);
    return res.status(500).json({
      error: "Failed to send. Please email support@toolhearth.com"
    });
  }
}
