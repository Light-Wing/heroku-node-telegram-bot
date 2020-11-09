'use strict';

require('dotenv').config()

const token = process.env.TOKEN;
const port = (process.env.PORT || 8443);
const host = process.env.HOST;
console.log("port: " + port)
console.log("host: " + host)
const TeleBot = require('telebot');
// const usePlugins = ['commandButton']; //, 'namedButtons', 'commandButton' , 'floodProtection'
// const pluginFolder = '../plugins/';
// const pluginConfig = {
//     floodProtector: {
//         interval: 2,
//         message: 'Too many messages, relax!'
//     }
// };
//const BUTTONS = require('./buttons').buttons; //not realy needed

let bot;

console.log('----Production----')
bot = new TeleBot({
  token,
  // usePlugins,
  // pluginConfig,
  webHook: { port: "0", host: "host" }
});

async function get_webinfo() {
  let info = await bot.getWebhookInfo()
  console.log(info)

}
get_webinfo()


bot.getMe().then(function (me) { //self check
  const botName = me.username;
  console.log('---\nHello! My name is %s!', me.first_name);
  console.log(`And my username is @${botName}\n---`);
  return botName;
})

bot.on('text', msg => bot.sendMessage(msg.from.id, msg.text));

bot.start();
