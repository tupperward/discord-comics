import requests, os
from datetime import datetime
from discord import SyncWebhook

today = datetime.now()
url = f"https://cad-comic.com/wp-content/uploads/{today.year}/{today.month}/Strip{today.year}{today.month}{today.day}a.x42600.png"

def use_webhook(webhook_url: str, message: str):
  hook = SyncWebhook.from_url(webhook_url)
  try:
    hook.send(content=message)
  except Exception as err:
    print(err)  

with requests.get(url) as res:
  if res.status_code == 200:
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    use_webhook(webhook_url=webhook_url, message=url)
  else:
    print(f"HTTP {res.status_code}: Request failed")