// /api/contact.js — capture contact form submissions
export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { name, email, subject, message } = req.body;

  if (!email || !email.includes("@") || !message) {
    return res.status(400).json({ error: "Email and message required" });
  }

  // Log to Vercel logs
  console.log(JSON.stringify({
    type: "CONTACT",
    name: name || "Anonymous",
    email: email.toLowerCase(),
    subject: subject || "Contact Form",
    message: message.substring(0, 200),
    timestamp: new Date().toISOString()
  }));

  return res.status(200).json({
    success: true,
    message: "Thanks! We'll be in touch soon."
  });
}
