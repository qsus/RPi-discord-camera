#!/usr/bin/python3

# YOUR WEBHOOK URL HERE
# example: url='https://discord.com/api/webhooks/ID/some-token'
# TODO: move to separate config file
# could be done like this - use the first one available: --webhook parameter; config.json file or .env file; hard-coded url
url=''

from time import sleep
from picamera import PiCamera
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook

def sendFile(filename, timestamp):
    from discord_webhook import DiscordWebhook
    webhook = DiscordWebhook(url=url, content=timestamp)
    file = open(filename, "rb")
    webhook.add_file(file.read(), filename)
    file.close()
    response = webhook.execute()

def wait():
    # Calculate the delay to the start of the next hour / minute
    next_hour = (datetime.now() + timedelta(hours=1)).replace(
        second=0, microsecond=0, minute=0) # ,minute=0
    delay = (next_hour - datetime.now()).seconds
    print(f"Waiting {delay} seconds...")
    sleep(delay)
    return next_hour.isoformat().replace("T", " ")

print("Starting camera...")
camera = PiCamera()
camera.start_preview()
print("Starting loops...")
isotime = wait()
for filename in camera.capture_continuous('img{timestamp:%Y-%m-%d-%H-%M}.jpg'):
    print('Captured %s' % filename)
    sendFile(filename, isotime)    
    isotime = wait()
