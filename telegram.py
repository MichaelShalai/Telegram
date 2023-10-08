from telethon.sync import TelegramClient, events
from telethon.tl.types import InputMessagesFilterVideo
from tqdm import tqdm
import fire
import os.path

# Printing download progress
def callback(current, total):
    global pbar
    global prev_curr
    pbar.update(current-prev_curr)
    prev_curr = current

async def findChannelID(client: TelegramClient, channelTitle):
    async for dialog in client.iter_dialogs():
        # print(dialog.title)
        # if not dialog.is_group and dialog.is_channel:
        if channelTitle == dialog.title:
            return dialog.id

async def findChannelEntity(client: TelegramClient, channelTitle):
    channelID = await findChannelID(client, channelTitle)
    channelEntity = await client.get_entity(channelID)
    return channelEntity

async def _main(client: TelegramClient, channel, directory):
  global pbar
  global prev_curr

  chat = await findChannelEntity(client, channel)

  # messages = await client.get_messages(chat, 1, filter=InputMessagesFilterVideo)
  # Get all the photos
  messages = await client.get_messages(chat, None, filter=InputMessagesFilterVideo)

  # Reverse to get chronological order.
  messages.reverse()

  offset = 0
  for idx, message in enumerate(messages, start=offset):
    filename = message.date.strftime("%Y-%m-%d") + " " + message.file.name
    if (os.path.isfile(directory + filename)):
      print(("{idx:04d}. '{filename}' - skipped").format(idx = idx+1, filename = filename))
      continue
    print(("{idx:04d}. '{filename}' - downloading...").format(idx = idx+1, filename = filename))
    prev_curr = 0
    pbar = tqdm(total=message.document.size, unit='B', unit_scale=True)
    path = await message.download_media(directory + filename, progress_callback=callback)
    pbar.close()

def telegram(api_id, api_hash, channel, session='default', directory='Videos/'):
  with TelegramClient(session, api_id, api_hash) as client:
      client.loop.run_until_complete(_main(client, channel, directory))

if __name__ == '__main__':
  fire.Fire(telegram)
