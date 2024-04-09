from telebot import *

token = "7028363008:AAFECfcwEXt4fHjR8bLL7cAci4hURVHKUuI"
bot = telebot.TeleBot(token)
data = {}
count = 0

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, f"Приветствую, *{message.from_user.first_name}*!", parse_mode="Markdown")
    menu(message.chat.id, "Чем я могу помочь сегодня?")
def menu(chatid, text):
    mm = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    btnsign = types.KeyboardButton("Заявка на марафон")
    btncheck = types.KeyboardButton("Мои марафоны")
    mm.add(btnsign, btncheck)
    bot.send_message(chatid, text, reply_markup=mm)

@bot.message_handler(content_types=['text'])
def answer(message):
    global data
    if (message.text == "Заявка на марафон"):
        msg = bot.send_message(message.chat.id, "Отлично! Для начала, напишите ваше полное имя: ")
        bot.register_next_step_handler(msg, name)
    if (message.text == "Мои марафоны"):
        if (len(data) == 0):
            menu(message.chat.id,"Вы еще не записывались на марафоны. Чтобы записаться, выберите нужный пункт в меню.")
        else:
            bot.send_message(message.chat.id, f'Список ваших марафонов:\n\n{'\n\n'.join(data[i] for i in range(0,count))}')
            menu(message.chat.id,"Что бы вы хотели  сделать сейчас?")

def name(message):
    runtypes = types.InlineKeyboardMarkup(row_width=1)
    btn21 = types.InlineKeyboardButton("Полумарафон (21 км)", callback_data="21")
    btn42 = types.InlineKeyboardButton("Обычный марафон (42,2 км)", callback_data="42")
    btn100 = types.InlineKeyboardButton("Ультрамарафон (100 км)", callback_data="100")
    runtypes.add(btn42, btn21, btn100)
    data[count] = f"{count + 1}. {message.text}"
    bot.send_message(message.chat.id, f"Приятно познакомиться, *{data[count].split()[2]}*! Какой марафон вы выберите?", parse_mode="Markdown",reply_markup=runtypes)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global count, chatid
    if call.message:
        if call.data == "21":
            data[count] += "\n    Полумарафон (21 км)"
        if call.data == "42":
            data[count] += "\n    Обычный марафон (42,2 км)"
        if call.data == "100":
            data[count] += "\n    Ультрамарафон (100 км)"
        bot.send_message(call.message.chat.id, "Принято, вы успешно записаны на марафон!")
        count+=1
        menu(call.message.chat.id, "Желаете выполнить что-то ещё?")

    bot.polling(none_stop=True, timeout=123)