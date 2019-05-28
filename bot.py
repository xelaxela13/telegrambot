#!/usr/bin/env python
import logging

from telegram.ext import Updater, CommandHandler
import requests
from os import getenv
import sys

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MODE = getenv('MODE', 'dev')
TOKEN = getenv('TOKEN')

if MODE == "dev":
    def run(updater):
        updater.start_polling()
elif MODE == "production":
    def run(updater):
        PORT = int(getenv("PORT", "8443"))
        HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    run(updater)
    updater.idle()


if __name__ == '__main__':
    main()
