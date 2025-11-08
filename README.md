# Telegram Bot on Netlify

This is a Telegram bot that runs 24/7 using Netlify's serverless functions and webhooks.

## 🚀 Features

- Serverless Telegram bot using Netlify Functions
- Webhook-based architecture for 24/7 operation
- Automatic scaling and high availability
- Zero server maintenance

## 📋 Prerequisites

- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))
- Netlify account (free tier works)
- Git repository (GitHub, GitLab, etc.)

## 🔧 Setup Instructions

### 1. Clone and Setup

1. Clone this repository
2. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
3. Add your bot token to `.env`:
   ```
   BOT_TOKEN=your_bot_token_here
   ```

### 2. Deploy to Netlify

#### Option A: Deploy from Git
1. Push your code to a Git repository
2. Connect your repo to Netlify:
   - Go to [Netlify](https://netlify.com)
   - Click "New site from Git"
   - Connect your repository
   - Deploy settings will be auto-detected from `netlify.toml`

#### Option B: Manual Deploy
1. Install Netlify CLI:
   ```bash
   npm install -g netlify-cli
   ```
2. Deploy:
   ```bash
   netlify deploy --prod
   ```

### 3. Configure Webhook

After deployment, set up the webhook:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the setup script:
   ```bash
   python setup_webhook.py
   ```

3. Enter your Netlify site URL when prompted (e.g., `https://your-bot-name.netlify.app`)

## 📝 Available Commands

- `/start` - Welcome message
- `/help` - Help information
- `/ping` - Check if bot is alive
- Any text message - Bot will echo it back

## 🛠️ Project Structure

```
telegram-bot/
├── bot.py                    # Main bot code (for local testing)
├── netlify/
│   └── functions/
│       └── webhook.py       # Serverless function handler
├── requirements.txt          # Python dependencies
├── netlify.toml             # Netlify configuration
├── runtime.txt              # Python version specification
├── setup_webhook.py         # Webhook setup utility
├── .env.example             # Environment variables template
└── README.md               # This file
```

## 🔍 How It Works

1. **Webhook Architecture**: Instead of polling, the bot uses Telegram's webhook system
2. **Serverless Functions**: Netlify Functions handle incoming webhook requests
3. **24/7 Operation**: Netlify's infrastructure ensures your bot is always available
4. **Auto-scaling**: Handles traffic spikes automatically

## 🚨 Important Notes

- **Free Tier Limits**: Netlify's free tier includes 125,000 function invocations/month
- **Execution Time**: Functions have a 10-second timeout on free tier
- **Cold Starts**: First request may be slower due to cold starts
- **Webhook URL**: Must be HTTPS (Netlify provides SSL automatically)

## 🔄 Updating Your Bot

1. Make changes to `netlify/functions/webhook.py`
2. Commit and push to your repository
3. Netlify will automatically deploy the changes
4. The webhook will automatically use the new code

## 🧪 Local Testing

For local development:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot locally (polling mode)
python bot.py
```

## 📊 Monitoring

Check your bot's webhook status:
```bash
python setup_webhook.py
# Choose option to get webhook info
```

Monitor function usage in your [Netlify dashboard](https://app.netlify.com).

## 🆘 Troubleshooting

### Bot not responding?
1. Check if webhook is set: `python setup_webhook.py`
2. Verify Netlify function logs in your dashboard
3. Ensure BOT_TOKEN is set in Netlify environment variables

### Function timeouts?
- Optimize your bot code for faster execution
- Consider breaking complex operations into smaller parts
- Upgrade to paid plan for longer timeouts

### Rate limiting?
- Netlify free tier has function invocation limits
- Consider upgrading if you exceed 125,000 requests/month

## 📚 Additional Resources

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [Netlify Functions Documentation](https://docs.netlify.com/functions/overview/)

## 🤝 Contributing

Feel free to submit issues and pull requests to improve this template!

## 📄 License

This project is open source and available under the MIT License.