
import requests

class Discord:
    def __init__(self, config):
        self.webhook = config["DISCORD_WEBHOOK"]

    def sendQuote(self, quote):
        resp = requests.post(self.webhook, json = {"content": quote})
        resp.raise_for_status()
