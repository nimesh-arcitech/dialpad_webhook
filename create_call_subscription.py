"""
Simple Dialpad Call Event Subscription Creator
Creates call event subscriptions using environment variables from .env file
"""
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment
API_KEY = os.getenv("DIALPAD_API_KEY")
ENDPOINT_ID = os.getenv("DIALPAD_ENDPOINT_ID")
CALL_STATES = os.getenv("CALL_STATES", "connected").split(",")
ENABLED = os.getenv("SUBSCRIPTION_ENABLED", "true").lower() == "true"

# Validate required variables
if not API_KEY:
    print("❌ Error: DIALPAD_API_KEY not found in .env file")
    print("Please add your API key to .env:")
    print("DIALPAD_API_KEY=your_api_key_here")
    exit(1)

if not ENDPOINT_ID:
    print("❌ Error: DIALPAD_ENDPOINT_ID not found in .env file")
    print("Please add your endpoint ID to .env:")
    print("DIALPAD_ENDPOINT_ID=your_endpoint_id_here")
    exit(1)

print("="*60)
print("Creating Dialpad Call Event Subscription")
print("="*60)
print(f"Endpoint ID: {ENDPOINT_ID}")
print(f"Call States: {', '.join(CALL_STATES)}")
print(f"Enabled: {ENABLED}")
print()

# Prepare payload
payload = {
    "call_states": CALL_STATES,
    "enabled": ENABLED,
    "endpoint_id": int(ENDPOINT_ID)
}

# Create call event subscription via Dialpad API
response = requests.post(
    "https://dialpad.com/api/v2/subscriptions/call",
    headers={
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    json=payload
)

if response.status_code == 200 or response.status_code == 201:
    subscription = response.json()
    print(f"✅ Call event subscription created successfully!")
    print(f"   Subscription ID: {subscription.get('id', 'N/A')}")
    print(f"   Hook URL: {subscription.get('hook_url', 'N/A')}")
    print(f"   Event Type: {subscription.get('event_type', 'N/A')}")
    print(f"   Status: {'Enabled' if subscription.get('enabled') else 'Disabled'}")
    print(f"   Call States: {', '.join(subscription.get('call_states', []))}")
    print()
    
    # Display additional details if available
    if 'webhook_id' in subscription:
        print(f"   Webhook ID: {subscription['webhook_id']}")
    if 'created_at' in subscription:
        print(f"   Created: {subscription['created_at']}")
    print()
else:
    print(f"❌ Error: {response.status_code}")
    print(f"   {response.text}")
    exit(1)

print("="*60)