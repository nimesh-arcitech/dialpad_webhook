"""
Simple Dialpad Webhook Creator
Creates webhooks using environment variables from .env file
"""
import requests
import secrets
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment
API_KEY = os.getenv("DIALPAD_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
SECRET = os.getenv("WEBHOOK_SECRET") or secrets.token_urlsafe(32)

# Validate required variables
if not API_KEY:
    print("❌ Error: DIALPAD_API_KEY not found in .env file")
    print("Please add your API key to .env:")
    print("DIALPAD_API_KEY=your_api_key_here")
    exit(1)

if not WEBHOOK_URL:
    print("❌ Error: WEBHOOK_URL not found in .env file")
    print("Please add your webhook URL to .env:")
    print("WEBHOOK_URL=https://your-domain.com/webhook")
    exit(1)

print("="*60)
print("Creating Dialpad Webhook")
print("="*60)
print(f"Webhook URL: {WEBHOOK_URL}")
print(f"Using Secret: {'Custom' if os.getenv('WEBHOOK_SECRET') else 'Auto-generated'}")
print()

# Create webhook via Dialpad API
response = requests.post(
    "https://dialpad.com/api/v2/webhooks",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "hook_url": WEBHOOK_URL,
        "secret": SECRET
    }
)

if response.status_code == 200:
    webhook = response.json()
    print(f"✅ Webhook created successfully!")
    print(f"   Webhook ID: {webhook['id']}")
    print(f"   🔐 Secret: {SECRET}")
    print()
    print("⚠️  IMPORTANT: Save this secret in your .env file:")
    print(f"WEBHOOK_SECRET={SECRET}")
    print()
else:
    print(f"❌ Error: {response.status_code}")
    print(f"   {response.text}")
    exit(1)

print("="*60)