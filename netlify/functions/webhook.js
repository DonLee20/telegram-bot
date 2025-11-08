// Netlify Function: Telegram Webhook (Node.js)
// Netlify supports Node.js functions natively. This function handles Telegram updates
// and replies via the Bot API without any external libraries.

export async function handler(event) {
  const BOT_TOKEN = process.env.BOT_TOKEN;
  if (!BOT_TOKEN) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "BOT_TOKEN is not set in environment" })
    };
  }

  // Health check for GET requests
  if (event.httpMethod === "GET") {
    return {
      statusCode: 200,
      body: JSON.stringify({ ok: true, message: "Webhook function is up" })
    };
  }

  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  try {
    const update = JSON.parse(event.body || "{}");

    const message = update.message || update.edited_message;
    if (!message || !message.chat || typeof message.chat.id === "undefined") {
      return { statusCode: 200, body: JSON.stringify({ ok: true }) };
    }

    const chatId = message.chat.id;
    const text = message.text || "";

    let replyText;
    if (text.startsWith("/start")) {
      replyText = "Hello! I’m your Netlify-hosted Telegram bot.\nCommands: /start, /help, /ping";
    } else if (text.startsWith("/help")) {
      replyText = "Help: Use /ping to check status or send any text to echo.";
    } else if (text.startsWith("/ping")) {
      replyText = "🏓 Pong!";
    } else {
      replyText = `You said: ${text}`;
    }

    const sendMessageUrl = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
    const payload = {
      chat_id: chatId,
      text: replyText,
      parse_mode: "HTML"
    };

    const res = await fetch(sendMessageUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!data.ok) {
      return { statusCode: 500, body: JSON.stringify({ error: data }) };
    }

    return { statusCode: 200, body: JSON.stringify({ ok: true }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: String(err) }) };
  }
}