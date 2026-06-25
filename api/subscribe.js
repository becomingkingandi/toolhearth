// /api/subscribe.js — capture email signups
export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { email, source } = req.body;

  if (!email || !email.includes("@")) {
    return res.status(400).json({ error: "Valid email required" });
  }

  // Log to Vercel logs (visible in Vercel dashboard)
  console.log(JSON.stringify({
    type: "SIGNUP",
    email: email.toLowerCase(),
    source: source || "toolhearth",
    timestamp: new Date().toISOString()
  }));

  return res.status(200).json({
    success: true,
    message: "Subscribed! Check your email."
  });
}
