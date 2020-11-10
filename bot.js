// 'use strict';

require('dotenv').config()

const token = process.env.TOKEN;
const port = (process.env.PORT || 8443);
const url = process.env.HEROKU_URL;
console.log("port: " + port)
console.log("url: " + url)
const TeleBot = require('telebot');
const usePlugins = [];

let bot;

//-----------------------------------
// on server or web dyno: ok
// no heroku[router] logs

bot = new TeleBot({
  token,
  usePlugins,
  webHook: {
    port: port
    , url: `${url}/bot${token}`
    // , host: url 
  }
});

// async function get_webinfo() {
//   let info = await bot.getWebhookInfo()
//   console.log(info)

// }
// get_webinfo()


// bot.getMe().then(function (me) { //self check
//   const botName = me.username;
//   console.log('---\nHello! My name is %s!', me.first_name);
//   console.log(`And my username is @${botName}\n---`);
//   return botName;
// })

bot.on('text', msg => bot.sendMessage(msg.from.id, " test nodejs bot").then(
  console.log('text test nodejs bot')
));

bot.start();




//-----------------------------------
// on server dyno: error
//heroku[router]: at=error code=H14 desc="No web processes running" method=POST path="/token" host=test-tgbot5.herokuapp.com request_id=02b62f1e-0316-4bb0-a62b-7cf218de4e1a fwd="91.108.6.84" dyno= connect= service= status=503 bytes= protocol=https

// on web dyno: ok
//heroku[router]: at=info method=POST path="/token" host=test-tgbot5.herokuapp.com request_id=9e050492-ce02-438a-bcea-bc8955356463 fwd="91.108.6.84" dyno=web.1 connect=0ms service=6ms status=200 bytes=96 protocol=https

// const TelegramBot = require("node-telegram-bot-api");
// // Heroku routes from port :443 to $PORT
// // Add URL of your app to env variable or enable Dyno Metadata
// // to get this automatically
// // See: https://devcenter.heroku.com/articles/dyno-metadata
// // const url = process.env.HEROKU_URL //|| 'https://<app-name>.herokuapp.com:443';
// bot = new TelegramBot(token, {
//   webHook: {
//     port: process.env.PORT,

//   }
// });


// // This informs the Telegram servers of the new webhook.
// // Note: we do not need to pass in the cert, as it already provided
// bot.setWebHook(`${url}/bot${token}`);


// // Just to ping!
// bot.on('message', function onMessage(msg) {
//   bot.sendMessage(msg.chat.id, 'I am alive on Heroku!');
// });