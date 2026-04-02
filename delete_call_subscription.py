"""
Simple Dialpad Call Event Subscription Deleter
Deletes call event subscriptions using environment variables from .env file
"""
import requests
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment
API_KEY = os.getenv("DIALPAD_API_KEY")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")

# Validate required variables
if not API_KEY:
    print("❌ Error: DIALPAD_API_KEY not found in .env file")
    print("Please add your API key to .env:")
    print("DIALPAD_API_KEY=your_api_key_here")
    exit(1)

# Check for subscription ID from environment or command line argument
if len(sys.argv) > 1:
    SUBSCRIPTION_ID = sys.argv[1]
elif not SUBSCRIPTION_ID:
    print("❌ Error: SUBSCRIPTION_ID not provided")
    print()
    print("Please provide subscription ID in one of two ways:")
    print("1. Add to .env file:")
    print("   SUBSCRIPTION_ID=your_subscription_id")
    print()
    print("2. Pass as command line argument:")
    print("   python delete_call_subscription.py 5045683266789376")
    exit(1)

print("="*60)
print("Deleting Dialpad Call Event Subscription")
print("="*60)
print(f"Subscription ID: {SUBSCRIPTION_ID}")
print()

# Confirm deletion
print("⚠️  WARNING: This action cannot be undone!")
confirm = input("Are you sure you want to delete this subscription? (yes/no): ")

if confirm.lower() not in ['yes', 'y']:
    print("❌ Deletion cancelled")
    exit(0)

print()
print("Deleting subscription...")

# Delete call event subscription via Dialpad API
response = requests.delete(
    f"https://dialpad.com/api/v2/subscriptions/call/{SUBSCRIPTION_ID}",
    headers={
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
)

if response.status_code == 200 or response.status_code == 204:
    print(f"✅ Subscription deleted successfully!")
    print(f"   Subscription ID: {SUBSCRIPTION_ID}")
    print()
    
    # Some APIs return empty response on successful deletion
    if response.text:
        print("Response:")
        print(f"   {response.text}")
        print()
else:
    print(f"❌ Error: {response.status_code}")
    print(f"   {response.text}")
    
    if response.status_code == 404:
        print()
        print("💡 Tip: Subscription not found. It may have already been deleted.")
        print("   Use list_call_subscriptions.py to see available subscriptions.")
    
    exit(1)

print("="*60)