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

// console.log('----Production----')
// bot = new TeleBot({
//   token,
//   usePlugins,
//   pluginConfig,
//   webHook: {
//     port: port
//     , url: `${url}/bot${token}`
//     // , host: url 
//   }
// });

// // async function get_webinfo() {
// //   let info = await bot.getWebhookInfo()
// //   console.log(info)

// // }
// // get_webinfo()


// // bot.getMe().then(function (me) { //self check
// //   const botName = me.username;
// //   console.log('---\nHello! My name is %s!', me.first_name);
// //   console.log(`And my username is @${botName}\n---`);
// //   return botName;
// // })

// bot.on('text', msg => bot.sendMessage(msg.from.id, " test nodejs bot").then(
//   console.log('text test nodejs bot')
// ));

// bot.start();




const TelegramBot = require("node-telegram-bot-api");
// Heroku routes from port :443 to $PORT
// Add URL of your app to env variable or enable Dyno Metadata
// to get this automatically
// See: https://devcenter.heroku.com/articles/dyno-metadata
// const url = process.env.HEROKU_URL //|| 'https://<app-name>.herokuapp.com:443';
bot = new TelegramBot(token, {
  webHook: {
    port: process.env.PORT,

  }
});


// This informs the Telegram servers of the new webhook.
// Note: we do not need to pass in the cert, as it already provided
bot.setWebHook(`${url}/bot${TOKEN}`);


// Just to ping!
bot.on('message', function onMessage(msg) {
  bot.sendMessage(msg.chat.id, 'I am alive on Heroku!');
});