
import requests, re

class Ts3:
    def __init__(self, config, serverId):
        self.host = config["TS3_HOST"]
        self.port = config["TS3_PORT"]
        self.serverId = serverId
        self.apiKey = config["TS3_APIKEY"]
        self.motdRegex = config["TS3_MOTD_REGEX"]

    def _checkOk(self, json):
        if json["status"]["code"] != 0:
            raise RuntimeError("Invalid request: " + str(json["status"]["code"]) + " " + str(json["status"]["message"]))

    def _getMsg(self):
        resp = requests.get("http://" + self.host + ":" + str(self.port) + "/" + str(self.serverId) + "/serverinfo?api-key=" + self.apiKey)
        json = resp.json()
        self._checkOk(json)
        result = resp.json()["body"][0]["virtualserver_welcomemessage"]
        return result

    def _setMsg(self, msg):
        data = { "virtualserver_welcomemessage": msg }
        resp = requests.post("http://" + self.host + ":" + str(self.port) + "/" + str(self.serverId) + "/serveredit?api-key=" + self.apiKey, json = data)
        self._checkOk(resp.json())

    def updateQuote(self, quote):
        quote = quote.replace("\\", "\\\\")
        regex = re.compile(self.motdRegex, flags = re.IGNORECASE | re.DOTALL)
        msg = self._getMsg()
        msg = regex.sub(r'\1\n' + quote + r'\n\2', msg, count = 1)
        self._setMsg(msg)
