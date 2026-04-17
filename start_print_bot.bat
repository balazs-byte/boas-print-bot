@echo off
echo Starting DYMO Web API...
start "" "C:\Program Files (x86)\DYMO\DYMO Connect\DYMO.WebApi.Win.Host.exe"
timeout /t 3

echo Starting Cloudflare tunnel...
set SHOPIFY_STORE=boas-marketplace.myshopify.com
set SHOPIFY_CLIENT_ID=efa41f3e11a5524681f9e46772c8f9ad
set SHOPIFY_CLIENT_SECRET=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

start "" /b %USERPROFILE%\Downloads\cloudflared.exe tunnel --url http://localhost:5000 > %USERPROFILE%\Downloads\tunnel.log 2>&1
echo Waiting for tunnel to start...
timeout /t 8

echo Extracting tunnel URL...
python %USERPROFILE%\Downloads\register_webhook.py

echo Starting Flask...
cd %USERPROFILE%\Downloads
python print_bot.py
