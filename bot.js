const token = process.env.TOKEN;
const port = (process.env.PORT || 8443);
const TeleBot = require('telebot');

const Bot = require('node-telegram-bot-api');
let bot;

if (process.env.NODE_ENV === 'production') {
  bot = new TeleBot({
    token: token,
    webhook: {
      // Self-signed certificate:
      // key: './key.pem',
      // cert: './cert.pem',
      //url: 'https://....',
      host: '0.0.0.0',
      port: port
    }
  });
  bot.setWebHook(process.env.HEROKU_URL + "/" + bot.token);
}
else {
  bot = new Bot(token, { polling: true });
}

console.log('Bot server started in the ' + process.env.NODE_ENV + ' mode');
console.log('heroku url' + process.env.HEROKU_URL);

bot.on('message', (msg) => {
  const name = msg.from.first_name;
  bot.sendMessage(msg.chat.id, 'Hello, ' + name + '!').then(() => {
    // reply sent!
  });
});
bot.on('text', msg => bot.sendMessage(msg.from.id, msg.text));
bot.start();


module.exports = bot;
