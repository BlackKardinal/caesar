import telebot
import configure
import random
from telebot import types

caesar = telebot.TeleBot(configure.config['token'])

@caesar.message_handler(commands = ['start'])
def hello(message):
	caesar.send_message(message.chat.id, 'Тебя приветствует\n🔱 Шифр Цезаря 2.0 🔱\n\nЯ использую секретный алфавит, доступный только мне. После кодирования, ты получишь <b>засекреченую фразу и ключ</b>. Эти данные пригодятся тебе для расшифровки.', parse_mode = 'HTML')
	kb = types.InlineKeyboardMarkup(row_width = 1)
	c = types.InlineKeyboardButton(text='зашифровать', callback_data='code')
	dc = types.InlineKeyboardButton(text='расшифровать', callback_data='decode')
	kb.add(c, dc)
	caesar.send_message(message.chat.id, '🧐 Скажи, что ты хочешь сделать?', reply_markup = kb)

@caesar.callback_query_handler(func=lambda c:c.data)
def answer_callback(callback):
	activiti = callback.data
	if activiti == 'code':
		phrase = caesar.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.id, text = '✳️✳️✳️ Твой выбор - <b>ЗАШИФРОВАТЬ</b>\nВведи фразу, которую нужно закодировать:', parse_mode = 'HTML')
		caesar.register_next_step_handler(phrase, f_code)
	elif activiti == 'decode':
		phrase_code = caesar.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.id, text = '✅✅✅ Твой выбор - РАСШИФРОВАТЬ\nВведи зашифрованную фразу:')
		caesar.register_next_step_handler(phrase_code, f_decode)

# кодирование фразы
def f_code(message):
	f = message.text.lower()
	caesar.send_message(message.chat.id, 'Кодирую...')
	code = random.randint(3,36)
	alphabet = ['a'# любой алфавит]
  f = list(f)

	# ищем индексы букв введенной фразы (в списке алфавит), результат список f_index
	f_index = []
	for i in f:
		for z in alphabet:
			if i == z:
				n = alphabet.index(z)
				f_index.append(n)

	# меняем алфавит на кодированный, результат список alphabet
	alphabet_code = []
	i = 0
	while i < code:
		z = alphabet.pop(0)
		alphabet_code.append(z)
		i += 1
	alphabet.extend(alphabet_code)

	# ищем индексы фразы в измененном алфавите
	f_index_code = []
	f_code = ''
	for i in f_index:
		n = alphabet[i]
		f_index_code.append(n)
	for i in f_index_code:
		f_code += i

	caesar.send_message(message.chat.id, 'Шифр-фраза: \n⬇️⬇️⬇️\n\n' + str(f_code) + '\n\n⬆️⬆️⬆️\nрасшифровать - @caesar_code_bot')
	caesar.send_message(message.chat.id, '👊😎 Готово!\n📩 перешли сообщение выше адресату\nНЕ ЗАБУДЬ СООБЩИТЬ КЛЮЧ ➡️ ' + str(code+1))
	caesar.send_message(message.chat.id, 'Благодарю что воспользовался 🔱Цезарем!\nНачать заново - /start')

# декодирование фразы
# получение фразы, запрос ключа
def f_decode(message):
	user_info = {}
	user_info ['f'] = message.text
	caesar.send_message(message.chat.id, 'Ок, фразу запомнил, но нужно еще кое-что...')
	send = caesar.send_message(message.chat.id, 'Мне понадобится ключ 🔑. Это случайное число, которое ты (или отправитель) получил при шифровании фразы. Введи его ниже: ')
	caesar.register_next_step_handler(send, ff_decode, user_info)

# получение ключа и проверка на валидность
def ff_decode(message, user_info):
	user_info['code'] = message.text
	caesar.send_message(message.chat.id, 'Ключ получен🔑, проверяю...')
	f = user_info['f']
	code = user_info['code']
	try:
		if int(code) >= 3 and int(code) <=36:
			caesar.send_message(message.chat.id, 'Ключ принят🔑, дешифрую...')
			alphabet = ['a'# любой алфавит]
      f = list(f)
			code = int(code)
			
			# меняем алфавит
			alphabet_code = []
			i = 0
			while i < code-1:
				z = alphabet.pop(0)
				alphabet_code.append(z)
				i += 1
			alphabet.extend(alphabet_code)

			# ищем индексы букв введенной фразы (в списке измененного алфавит), результат список f_index
			f_index = []
			for i in f:
				for z in alphabet:
					if i == z:
						n = alphabet.index(z)
						f_index.append(n)

			# подставляем оригинальный алфавит
      alphabet = ['a'# любой алфавит]			
      f_decode = []
			f_obj_decode = ''
			for i in f_index:
				n = alphabet[i]
				f_decode.append(n)
			for i in f_decode:
				f_obj_decode += i

			caesar.send_message(message.chat.id,'Твое сообщение:\n⬇️⬇️⬇️\n\n' + str(f_obj_decode) + '\n\n⬆️⬆️⬆️\n')
			caesar.send_message(message.chat.id,'Благодарю что воспользовался 🔱Цезарем!\nНачать заново - /start')

		else:
			caesar.send_message(message.chat.id, 'А, мы в угадайку играем?\n🤡Ну что ж, игра началась, удачи!\n\nНачать заново - /start')
	except ValueError:
		caesar.send_message(message.chat.id, '🤥Ты хочешь меня обмануть?\nЯ просил число!🤬\nА-та-та, давай-ка по новой!\n\nНачать заново - /start')

# отлавливаем мусор и перенаправляем в диалог
@caesar.message_handler(content_types = ['text'])
def trash(message):
	caesar.send_message(message.chat.id, 'Для использования 🔱Цезаря - нажми /start')




caesar.polling(none_stop = True, interval = 0)
