from discord import SyncWebhook
import re, feedparser, os

def retrieve_latest_entry(url):
  feed = feedparser.parse(url)
  latest_entry = feed.entries[0]

  return latest_entry

def url_stripper(entry):

  amuniversal_pattern = r'https?://assets\.amuniversal\.com/[^"]+'
  comicskingdom_pattern = r'https?://safr\.kingfeatures\.com/[^"]+'
  ck_pattern = r'https?://wp\.comicskingdom\.com/[^"]+'
  url_patterns = [amuniversal_pattern, comicskingdom_pattern, ck_pattern]

  all_urls = []

  for pattern in url_patterns:
      url_regex = re.compile(pattern)
      entry_description = re.sub(r'#\d+;', '', entry.description)  # Strip decimal code Unicode characters
      urls = url_regex.findall(entry_description)
      all_urls.extend(urls)

  return all_urls[0]

def use_webhook(webhook_url: str, message):
  hook = SyncWebhook.from_url(webhook_url)
  try:
    hook.send(content=message)
  except Exception as err:
    print

if __name__ == "__main__":
  # Construct the webhook
  webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
  rss_url = os.environ.get('RSS_URL')

  latest_entry = retrieve_latest_entry(rss_url)
  use_webhook(webhook_url, url_stripper(latest_entry))
