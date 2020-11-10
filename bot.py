

# import os
# import logging
# import telegram.ext as tg
# from telegram.ext import CommandHandler

# logging.basicConfig(
#     format="%(name)s:%(levelname)s - %(message)s",  # %(asctime)s -
#     level=logging.INFO)
# LOGGER = logging.getLogger(__name__)

# TOKEN = os.environ.get('TOKEN', None)
# HEROKU_URL = os.environ.get('HEROKU_URL', '')
# PORT = int(os.environ.get('PORT', 8443))


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


import http.server
import requests
import os
from urllib.parse import unquote, parse_qs
import threading
from socketserver import ThreadingMixIn

memory = {}

form = '''<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name=viewport content="width=device-width, initial-scale=1">
    <meta name="robots" content="abdennour,nanodegree,python,fullstack,udacity,toumi" />
    <title>Shortner links</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">
  </head>
  <body>
    <main class="container mt-5">
       <div>
            <form method="POST">
                <section>
                   <h2>Shortener</h2>
                   <div class="form-group">
                     <label for="longuri">Long URI: </label>
                     <input name="longuri" id="longuri" class="form-control" placeholder="Your long Link http://...">
                   </div>
                   <div class="form-group">
                     <label for="shortname">Short name:</label>
                     <input name="shortname" id="shortname" class="form-control" placeholder="my-link">
                   </div>
                   <button type="submit" class="btn btn-primary">Save it!</button>
                </section>
             </form>
             <hr>
             <section>
               <h2>URIs I know about</h2>
               <pre>
                 {}
               </pre>
             </section>
       </div>
    </main>
  </body>
</html>
'''


def CheckURI(uri, timeout=5):
    '''Check whether this URI is reachable, i.e. does it return a 200 OK?
    This function returns True if a GET request to uri returns a 200 OK, and
    False if that GET request returns any other response, or doesn't return
    (i.e. times out).
    '''
    try:
        r = requests.get(uri, timeout=timeout)
        # If the GET request returns, was it a 200 OK?
        return r.status_code == 200
    except requests.RequestException:
        # If the GET request raised an exception, it's not OK.
        return False


class ThreadHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    "This is an HTTPServer that supports thread-based concurrency."


class Shortener(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # A GET request will either be for / (the root path) or for /some-name.
        # Strip off the / and we have either empty string or a name.
        name = unquote(self.path[1:])

        if name:
            if name in memory:
                # We know that name! Send a redirect to it.
                self.send_response(303)
                self.send_header('Location', memory[name])
                self.end_headers()
            else:
                # We don't know that name! Send a 404 error.
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("I don't know '{}'.".format(name).encode())
        else:
            # Root path. Send the form.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # List the known associations in the form.
            known = "\n".join("{} : {}".format(key, memory[key])
                              for key in sorted(memory.keys()))
            self.wfile.write(form.format(known).encode())

    def do_POST(self):
        # Decode the form data.
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)
        longuri = params["longuri"][0]
        shortname = params["shortname"][0]

        if CheckURI(longuri):
            # This URI is good!  Remember it under the specified name.
            memory[shortname] = longuri

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            # Didn't successfully fetch the long URI.
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(
                "Couldn't fetch URI '{}'. Sorry!".format(longuri).encode())


if __name__ == '__main__':
    server_address = ('', int(os.environ.get('PORT', '8000')))
    httpd = ThreadHTTPServer(server_address, Shortener)
    httpd.serve_forever()
