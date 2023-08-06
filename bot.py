import telebot
from bridges_api import getCapcha, sendCode
TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


bot = telebot.TeleBot(TOKEN, parse_mode = None)

user_code_dict = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, 
    '''Hello, this is Tor bridges bot
    Type /get to provide a bdridges
    ''')
    
@bot.message_handler(commands=['get'])
def getCaptcha(message):
    captcha, code = getCapcha()
    chat_id = message.chat.id
    
    user_code_dict[chat_id] = code
    
    msg = bot.send_photo(chat_id, captcha)
    
    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(chat_id, 'Type a captcha:', reply_markup=markup)
    
    bot.register_next_step_handler(msg, getCaptchaValue)
    
def getCaptchaValue(message):
    captcha = message.text
    code = user_code_dict[message.chat.id]
    bridges = sendCode(code, captcha)
    
    msg = bot.reply_to(message, bridges)
    
    
print('Bot started')
# Polling cycle
bot.infinity_polling()