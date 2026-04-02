"""
Simple Dialpad Call Event Subscription Lister
Lists all call event subscriptions using environment variables from .env file
"""
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment
API_KEY = os.getenv("DIALPAD_API_KEY")

# Validate required variables
if not API_KEY:
    print("❌ Error: DIALPAD_API_KEY not found in .env file")
    print("Please add your API key to .env:")
    print("DIALPAD_API_KEY=your_api_key_here")
    exit(1)

print("="*60)
print("Listing Dialpad Call Event Subscriptions")
print("="*60)
print()

# List call event subscriptions via Dialpad API
response = requests.get(
    "https://dialpad.com/api/v2/subscriptions/call",
    headers={
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
)

if response.status_code == 200:
    subscriptions = response.json()
    
    # Check if there are any subscriptions
    if isinstance(subscriptions, list):
        if len(subscriptions) == 0:
            print("📭 No call event subscriptions found")
        else:
            print(f"✅ Found {len(subscriptions)} call event subscription(s):")
            print()
            
            for idx, sub in enumerate(subscriptions, 1):
                print(f"Subscription #{idx}")
                print(f"   ID: {sub.get('id', 'N/A')}")
                print(f"   Hook URL: {sub.get('hook_url', 'N/A')}")
                print(f"   Event Type: {sub.get('event_type', 'N/A')}")
                print(f"   Status: {sub.get('status', 'N/A')}")
                
                # Display created date if available
                if 'created_at' in sub:
                    print(f"   Created: {sub['created_at']}")
                
                # Display any additional fields
                if 'webhook_id' in sub:
                    print(f"   Webhook ID: {sub['webhook_id']}")
                
                print()
    else:
        # Handle case where response is not a list
        print("✅ Response received:")
        print(subscriptions)
else:
    print(f"❌ Error: {response.status_code}")
    print(f"   {response.text}")
    exit(1)

print("="*60)