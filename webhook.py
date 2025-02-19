from discord import SyncWebhook
import re, feedparser, os, logging

def retrieve_latest_entry(url):
  try:
    feed = feedparser.parse(url)
  except Exception as e:
    logging.error(f'Could not parse feed at {url}: {e}')
  try:
    latest_entry = feed.entries[0]
  except Exception as e:
    logging.error(f'Could not find latest entry: {e}')

  return latest_entry

def url_stripper(entry):

  amuniversal_pattern = r'https?://assets\.amuniversal\.com/[^"]+'
  comicskingdom_pattern = r'https?://safr\.kingfeatures\.com/[^"]+'
  ck_pattern = r'https?://wp\.comicskingdom\.com/[^"]+'
  url_patterns = [amuniversal_pattern, comicskingdom_pattern, ck_pattern]

  all_urls = []

  for pattern in url_patterns:
      try:
        url_regex = re.compile(pattern)
        entry_description = re.sub(r'#\d+;', '', entry.description)  # Strip decimal code Unicode characters
        urls = url_regex.findall(entry_description)
        all_urls.extend(urls)
      except Exception as e:
        logging.error(f'Could not find url in {entry_description}: {e}')

  logging.info(f'Found URL: {all_urls[0]}')
  return all_urls[0]

def use_webhook(webhook_url: str, message):
  hook = SyncWebhook.from_url(webhook_url)
  try:
    hook.send(content=message)
  except Exception as e:
    logging.error(f'Failed to send URL to webhook {webhook_url}: {e}')

if __name__ == "__main__":
  # Construct the webhook
  logging.info('Starting Job')
  webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
  rss_url = os.environ.get('RSS_URL')

  latest_entry = retrieve_latest_entry(rss_url)
  use_webhook(webhook_url, url_stripper(latest_entry))
  logging.info('Job Complete')
