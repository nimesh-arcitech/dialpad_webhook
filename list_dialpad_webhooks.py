"""
List all existing Dialpad webhooks
"""
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("DIALPAD_API_KEY")

if not API_KEY:
    print("❌ Error: DIALPAD_API_KEY not found in .env file")
    exit(1)

print("="*60)
print("Listing Dialpad Webhooks")
print("="*60)
print()

response = requests.get(
    "https://dialpad.com/api/v2/webhooks",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
)

if response.status_code == 200:
    webhooks = response.json()
    
    if isinstance(webhooks, list):
        if len(webhooks) == 0:
            print("📭 No webhooks found")
        else:
            print(f"📬 Found {len(webhooks)} webhook(s):")
            print()
            for i, webhook in enumerate(webhooks, 1):
                print(f"{i}. Webhook ID: {webhook.get('id')}")
                print(f"   URL: {webhook.get('hook_url')}")
                print(f"   Events: {', '.join(webhook.get('events', []))}")
                print(f"   Created: {webhook.get('created_at', 'N/A')}")
                print()
    else:
        print("📋 Webhook details:")
        print(json.dumps(webhooks, indent=2))
else:
    print(f"❌ Error: {response.status_code}")
    print(f"   {response.text}")

print("="*60)