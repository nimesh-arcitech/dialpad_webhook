"""
Delete a Dialpad webhook by ID
"""
import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DIALPAD_API_KEY")

if not API_KEY:
    print("❌ Error: DIALPAD_API_KEY not found in .env file")
    exit(1)

if len(sys.argv) < 2:
    print("Usage: python delete_dialpad_webhook.py <webhook_id>")
    print("To get webhook ID, run: python list_dialpad_webhooks.py")
    exit(1)

webhook_id = sys.argv[1]

print("="*60)
print(f"Deleting Webhook: {webhook_id}")
print("="*60)

response = requests.delete(
    f"https://dialpad.com/api/v2/webhooks/{webhook_id}",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
)

if response.status_code in [200, 204]:
    print(f"✅ Webhook {webhook_id} deleted successfully!")
elif response.status_code == 404:
    print(f"⚠️  Webhook {webhook_id} not found")
else:
    print(f"❌ Error: {response.status_code}")
    print(f"   {response.text}")

print("="*60)