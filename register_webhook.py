import re
import time
import requests
import os

SHOP = os.environ["SHOPIFY_STORE"]
CLIENT_ID = os.environ["SHOPIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SHOPIFY_CLIENT_SECRET"]

# Read tunnel URL from log
tunnel_url = None
for _ in range(10):
    try:
        with open(os.path.expanduser("~/Downloads/tunnel.log"), "r") as f:
            content = f.read()
        match = re.search(r'https://[a-z0-9\-]+\.trycloudflare\.com', content)
        if match:
            tunnel_url = match.group(0)
            break
    except:
        pass
    time.sleep(2)

if not tunnel_url:
    print("Could not find tunnel URL, exiting")
    exit(1)

print(f"Tunnel URL: {tunnel_url}")

# Get Shopify token
r1 = requests.post(
    f"https://{SHOP}/admin/oauth/access_token",
    json={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
)
token = r1.json()["access_token"]

# Delete old webhooks
r_list = requests.get(
    f"https://{SHOP}/admin/api/2025-01/webhooks.json",
    headers={"X-Shopify-Access-Token": token}
)
for wh in r_list.json().get("webhooks", []):
    if "product-created" in wh["address"]:
        requests.delete(
            f"https://{SHOP}/admin/api/2025-01/webhooks/{wh['id']}.json",
            headers={"X-Shopify-Access-Token": token}
        )
        print(f"Deleted old webhook {wh['id']}")

# Register new webhook
r2 = requests.post(
    f"https://{SHOP}/admin/api/2025-01/webhooks.json",
    headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
    json={"webhook": {
        "topic": "products/create",
        "address": f"{tunnel_url}/webhook/product-created",
        "format": "json"
    }}
)
print(f"Webhook registered: {r2.status_code}")
