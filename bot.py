

import os
# import logging
# import telegram.ext as tg
# from telegram.ext import CommandHandler

# logging.basicConfig(
#     format="%(name)s:%(levelname)s - %(message)s",  # %(asctime)s -
#     level=logging.INFO)
# LOGGER = logging.getLogger(__name__)

# TOKEN = os.environ.get('TOKEN', None)
# HEROKU_URL = os.environ.get('HEROKU_URL', '')
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
PORT = int(os.environ.get('PORT', 8443))


# updater = tg.Updater(TOKEN, use_context=True)

# dispatcher = updater.dispatcher


# def start(update, context):
#     text = "/start - " + str(update.effective_user.id) +\
#         " - " + str(update.effective_user.first_name) + \
#         " " + str(update.effective_user.last_name)

#     LOGGER.info(text)

#     update.effective_message.reply_text(text)


# def main():
#     dp = dispatcher
#     bot_me = dp.bot.get_me()
#     LOGGER.info("\n"+"-"*20+f"\nbot username: {bot_me.username} \nbot full_name: {bot_me.full_name}\n"+"-"*20)

#     dp.add_handler(CommandHandler('start', start))

#     LOGGER.info("Using webhooks.")

#     updater.bot.delete_webhook()

#     updater.start_webhook(
#         listen="0.0.0.0",
#         port=PORT,
#         url_path='TOKEN')
#     # cert=None,
#     # key=None,
#     # clean=False,
#     # webhook_url=HEROKU_URL + "/" + TOKEN)
#     updater.bot.set_webhook(HEROKU_URL + "/" + 'TOKEN')

#     # updater.idle()


# if __name__ == '__main__':
#     main()


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n",
                     str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(
            self.path).encode('utf-8'))

    def do_POST(self):
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(
            self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=PORT):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
