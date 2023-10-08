# Telegram Client: Video Downloader

Sequentially downloads all videos from your friend's Telegram channel.
Requires `api_id` and `api_hash` from https://my.telegram.org/.
See also: https://core.telegram.org/api/obtaining_api_id.

## Installation
```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade telethon
python3 -m pip install --upgrade tqdm
python3 -m pip install --upgrade fire
```

## Usage
```
python3 telegram.py --api_id=12345678 --api_hash=abcdefghijklmnopqrstuvwxyz123456 --session=default --channel="My Telegram Friend's Name" --directory=Videos/
```
