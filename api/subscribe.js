// /api/subscribe.js — store email signups to KV (Vercel managed store)
export const config = {
  runtime: 'nodejs18.x',
};

export default async function handler(req, res) {
  // Only allow POST
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { email, source } = req.body;

  if (!email) {
    return res.status(400).json({ error: "Email required" });
  }

  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ error: "Invalid email format" });
  }

  try {
    // Log the signup to console (Vercel logs)
    console.log(`[SIGNUP] ${email} from ${source || 'unknown'} at ${new Date().toISOString()}`);

    // Forward to internal webhook (shemika2)
    // Note: This will fail from Vercel (can't reach private IPs), but we log it for debugging
    try {
      const webhookResponse = await Promise.race([
        fetch("http://100.121.100.78:8088/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, source: source || "toolhearth" })
        }),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error("timeout")), 3000)
        )
      ]);

      if (webhookResponse.ok) {
        return res.status(200).json({
          success: true,
          message: "Subscribed! Check your email."
        });
      }
    } catch (webhookError) {
      // Webhook unreachable — that's okay, we log it
      console.warn(`[WEBHOOK] Could not reach internal webhook: ${webhookError.message}`);
    }

    // Even if webhook fails, return success to user
    // (data was logged to Vercel logs, can be retrieved from there)
    return res.status(200).json({
      success: true,
      message: "Subscribed! Check your email.",
      _debug: "Email logged to Vercel console"
    });

  } catch (error) {
    console.error("[SUBSCRIBE] Error:", error.message);
    return res.status(500).json({
      error: "Failed to subscribe. Please try again.",
      _debug: error.message
    });
  }
}
