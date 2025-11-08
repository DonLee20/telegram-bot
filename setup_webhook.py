import os
import requests
from dotenv import load_dotenv

load_dotenv()

def setup_webhook():
    """Set up the webhook for the Telegram bot."""
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print("❌ BOT_TOKEN not found in .env file")
        return
    
    # For Netlify, the webhook URL will be: https://your-site-name.netlify.app/.netlify/functions/webhook
    # You need to replace this with your actual Netlify site URL
    webhook_url = input("Enter your Netlify site URL (e.g., https://your-bot-name.netlify.app): ").strip()
    
    if not webhook_url:
        print("❌ No URL provided")
        return
    
    # Ensure the URL ends with the webhook function path
    if not webhook_url.endswith('/.netlify/functions/webhook'):
        webhook_url = f"{webhook_url.rstrip('/')}/.netlify/functions/webhook"
    
    print(f"Setting webhook to: {webhook_url}")
    
    try:
        # Set webhook
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/setWebhook",
            json={"url": webhook_url}
        )
        
        if response.ok:
            result = response.json()
            if result.get('ok'):
                print("✅ Webhook set successfully!")
                print(f"Webhook URL: {webhook_url}")
                
                # Get webhook info
                info_response = requests.post(f"https://api.telegram.org/bot{bot_token}/getWebhookInfo")
                if info_response.ok:
                    info = info_response.json()
                    print(f"Webhook info: {info.get('result', {})}")
            else:
                print(f"❌ Failed to set webhook: {result.get('description', 'Unknown error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error setting webhook: {str(e)}")

def delete_webhook():
    """Delete the current webhook."""
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print("❌ BOT_TOKEN not found in .env file")
        return
    
    try:
        response = requests.post(f"https://api.telegram.org/bot{bot_token}/deleteWebhook")
        if response.ok:
            result = response.json()
            if result.get('ok'):
                print("✅ Webhook deleted successfully!")
            else:
                print(f"❌ Failed to delete webhook: {result.get('description', 'Unknown error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error deleting webhook: {str(e)}")

if __name__ == "__main__":
    print("Telegram Bot Webhook Setup")
    print("1. Set webhook")
    print("2. Delete webhook")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        setup_webhook()
    elif choice == "2":
        delete_webhook()
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice")