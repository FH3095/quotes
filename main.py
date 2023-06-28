
from ts3 import Ts3
from discord import Discord
from quotes import getQuote
from config import getConfig

config = getConfig()
quote = getQuote(config)

with open(config["QUOTE_DAY_FILE"], mode="wt", encoding = "utf-8") as quoteFile:
    quoteFile.write(quote + "\n")

#Discord(config).sendQuote(quote)

for serverId in config["TS3_IDS"]:
    ts3 = Ts3(config, serverId)
    ts3.updateQuote(quote)
