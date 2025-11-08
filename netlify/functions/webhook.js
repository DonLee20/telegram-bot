// Netlify Function: Telegram Webhook (Node.js)
// Netlify supports Node.js functions natively. This function handles Telegram updates
// and replies via the Bot API without any external libraries.

// Helpers
const apiBase = (token) => `https://api.telegram.org/bot${token}`;

async function sendMessage(token, payload) {
  const res = await fetch(`${apiBase(token)}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return res.json();
}

async function answerCallbackQuery(token, callbackQueryId) {
  const res = await fetch(`${apiBase(token)}/answerCallbackQuery`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ callback_query_id: callbackQueryId })
  });
  return res.json();
}

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

    // Handle callback queries from inline buttons
    if (update.callback_query) {
      const cq = update.callback_query;
      const chatId = cq.message?.chat?.id;
      const data = cq.data || "";
      if (!chatId) {
        await answerCallbackQuery(BOT_TOKEN, cq.id);
        return { statusCode: 200, body: JSON.stringify({ ok: true }) };
      }

      // Acknowledge the callback to stop loading animation
      await answerCallbackQuery(BOT_TOKEN, cq.id);

      if (data === "more_info") {
        const text = "📋 **Available Commands:**\n\n▪️ /start - Show main menu with links\n▪️ /help - Show this help message\n\n💡 Use these commands to navigate the bot!";
        const resp = await sendMessage(BOT_TOKEN, { chat_id: chatId, text, parse_mode: "Markdown" });
        return { statusCode: 200, body: JSON.stringify(resp) };
      } else if (data === "no_action") {
        const text = "🌍 Xynx's world is amazing! Stay tuned for more updates!";
        const resp = await sendMessage(BOT_TOKEN, { chat_id: chatId, text });
        return { statusCode: 200, body: JSON.stringify(resp) };
      }

      return { statusCode: 200, body: JSON.stringify({ ok: true }) };
    }

    // Handle text messages/commands
    const message = update.message || update.edited_message;
    if (!message || !message.chat || typeof message.chat.id === "undefined") {
      return { statusCode: 200, body: JSON.stringify({ ok: true }) };
    }

    const chatId = message.chat.id;
    const text = message.text || "";

    if (text.startsWith("/start")) {
      const message_text = "🏢 **ZeroCodeStudios** 🏢\n━━━━━━━━━━━━━━━━━━━━━\n\n👨‍💻 **Founder - Deyo** 👨‍💻\n\n👨‍💼 **Founder - Xynx** 👨‍💼\n\n━━━━━━━━━━━━━━━━━━━━━";

      const reply_markup = {
        inline_keyboard: [
          [{ text: "🚀 Join Our Channel 🚀", url: "https://t.me/zerocodestudios" }],
          [{ text: "🌐 Deyo's Website 🌐", url: "https://deyo.lol/" }],
          [{ text: "🌐 Xynx's World 🌐", callback_data: "no_action" }],
          [{ text: "💫 More Info 💫", callback_data: "more_info" }]
        ]
      };

      const resp = await sendMessage(BOT_TOKEN, {
        chat_id: chatId,
        text: message_text,
        reply_markup,
        parse_mode: "Markdown"
      });
      return { statusCode: 200, body: JSON.stringify(resp) };
    }

    if (text.startsWith("/help")) {
      const help_text = "😎 **Yo, Chill Brat!** 😎\n\n🚀 There's a **LOT** more to come! 🚀\n\n✨ **Stay tuned for:**\n▪️ Amazing features\n▪️ Cool updates\n▪️ Epic surprises\n\n🎯 **Available Commands:**\n▪️ /start - Show main menu\n▪️ /help - Show this message\n\n💫 **Keep exploring! The best is yet to come!** 💫";
      const resp = await sendMessage(BOT_TOKEN, { chat_id: chatId, text: help_text, parse_mode: "Markdown" });
      return { statusCode: 200, body: JSON.stringify(resp) };
    }

    if (text.startsWith("/ping")) {
      const resp = await sendMessage(BOT_TOKEN, { chat_id: chatId, text: "🏓 Pong!" });
      return { statusCode: 200, body: JSON.stringify(resp) };
    }

    // Echo other text
    const resp = await sendMessage(BOT_TOKEN, { chat_id: chatId, text: `You said: ${text}` });
    return { statusCode: 200, body: JSON.stringify(resp) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: String(err) }) };
  }
}