

import os
import logging
import telegram.ext as tg
from telegram.ext import CommandHandler

logging.basicConfig(
    format="%(name)s:%(levelname)s - %(message)s",  # %(asctime)s -
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

TOKEN = os.environ.get('TOKEN', None)
HEROKU_URL = os.environ.get('HEROKU_URL', '')
PORT = int(os.environ.get('PORT', 8443))


updater = tg.Updater(TOKEN, use_context=True)

dispatcher = updater.dispatcher


def start(update, context):
    text = "/start - " + str(update.effective_user.id) +\
        " - " + str(update.effective_user.first_name) + \
        " " + str(update.effective_user.last_name)

    LOGGER.info(text)

    update.effective_message.reply_text(text)


def main():
    dp = dispatcher
    bot_me = dp.bot.get_me()
    LOGGER.info("\n"+"-"*20+f"\nbot username: {bot_me.username} \nbot full_name: {bot_me.full_name}\n"+"-"*20)

    dp.add_handler(CommandHandler('start', start))

    LOGGER.info("Using webhooks.")

    updater.bot.delete_webhook()

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path='TOKEN')
    # cert=None,
    # key=None,
    # clean=False,
    # webhook_url=HEROKU_URL + "/" + TOKEN)
    updater.bot.set_webhook(HEROKU_URL + "/" + 'TOKEN')

    # updater.idle()


if __name__ == '__main__':
    main()
