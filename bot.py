import telebot
import config
import datetime
import json
import traceback

bot = telebot.TeleBot('1592405315:AAE0tmMhVvfVCpOTVtVzTxObVJmvNnYATIk')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Привет', 'Пока')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('USD', 'EUR', 'RUR')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

@bot.message_handler(commands=['exchange'])
def exchange_message(message):
    bot.send_message(message.chat.id, 'Click on the currency of choice:', reply_markup=keyboard2)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('get-'):
        get_ex_callback(query)
def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    send_exchange_result(query.message, query.data[4:])
def send_exchange_result(message, ex_code):
    bot.send_chat_action(message.chat.id, 'typing')
    ex = pb.get_exchange(ex_code)
    bot.send_message(
        message.chat.id, serialize_ex(ex),
        reply_markup=get_update_keyboard(ex),
	parse_mode='HTML')

def get_update_keyboard(ex):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Update',
	    callback_data=json.dumps({
                't': 'u',
		'e': {
                    'b': ex['buy'],
		    's': ex['sale'],
		    'c': ex['ccy']
                }
            }).replace(' ', '')
        ),
	telebot.types.InlineKeyboardButton('Share', switch_inline_query=ex['ccy'])
    )
    return keyboard

def serialize_ex(ex_json, diff=None):
    result = '<b>' + ex_json['base_ccy'] + ' -> ' + ex_json['ccy'] + ':</b>\n\n' + \
             'Buy: ' + ex_json['buy']
    if diff:
        result += ' ' + serialize_exchange_diff(diff['buy_diff']) + '\n' + \
                  'Sell: ' + ex_json['sale'] + \
                  ' ' + serialize_exchange_diff(diff['sale_diff']) + '\n'
    else:
        result += '\nSell: ' + ex_json['sale'] + '\n'
    return result


def serialize_exchange_diff(diff):
    result = ''
    if diff > 0:
        result = '(' + str(diff) + ' <img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="↗️" src="https://s.w.org/images/core/emoji/2.3/svg/2197.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2197.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2197.svg">" src="https://s.w.org/images/core/emoji/72x72/2197.png">" src="https://s.w.org/images/core/emoji/72x72/2197.png">)'
    elif diff < 0:
        result = '(' + str(diff)[1:] + ' <img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="↘️" src="https://s.w.org/images/core/emoji/2.3/svg/2198.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2198.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2198.svg">" src="https://s.w.org/images/core/emoji/72x72/2198.png">" src="https://s.w.org/images/core/emoji/72x72/2198.png">)'
    return result

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'спасибо':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    elif message.text.lower() == 'помоги':
        bot.send_message(message.chat.id, '1) To receive a list of available currencies press /exchange.\n' +
        '2) Click on the currency you are interested in.\n' +
        '3) You will receive a message containing information regarding the source and the target currencies, ' +
        'buying rates and selling rates.\n' +
        '4) Click “Update” to receive the current information regarding the request. ' +
        'The bot will also show the difference between the previous and the current exchange rates.\n' +
        '5) The bot supports inline. Type @<botusername> in any chat and the first letters of a currency.')



@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


bot.polling()
