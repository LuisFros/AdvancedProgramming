import requests
import datetime
import os
import json


class Telegram:
    def __init__(self, token, heroku, id):
        self.url = "https://api.telegram.org/bot{}".format(token)
        self.token = token
        self.heroku = heroku
        self.id = id
        if heroku is not None:
            self.set_webhook()

    def set_webhook(self):
        ulr = "https://api.telegram.org/bot{}/setWebhook".format(self.token)
        print(requests.get(ulr, json={"url": self.heroku}))

    def send_message(self, message, chat_id):
        a = requests.get(self.url + "/sendMessage",
                         params={'chat_id': chat_id, 'text': message})
        print(a.json())


def tel_main(heroku="https://stiffbot.herokuapp.com/"):
    token_telegram = '364334979:AAHSmP5uXT-o5TyW484P4XrviQMLGb_pLlk'
    aux = Telegram(token_telegram, heroku, 378309523)
    return aux

