from bale import *
bot = Bot(token="152238739:EU8ukOoTPGfSknbp2zqZfzAFu5I8l8ah5Rn7NznW")
    
from DAO import * 

@bot.event
async def on_ready():
	print(bot.user.username, "is Ready!")

@bot.event
async def on_update(update: Update):
	# if(update.message):
	# 	print(update.message.text)
	# else: 
	print(update.message)

@bot.event
async def on_message(message: Message):
	if message.content == '/start': # to get caption or text of message
		reply_markup = InlineKeyboardMarkup()
		reply_markup.add(InlineKeyboardButton(text="what is python-bale-bot?", callback_data="python-bale-bot:help"))
		reply_markup.add(InlineKeyboardButton(text="package site", url="https://python-bale-bot.ir"), row=2)
		reply_markup.add(InlineKeyboardButton(text="package GitHub", url="https://python-bale-bot.ir/github"), row=2)
		await message.reply(
			f"*Hi {message.author.first_name}, Welcome to python-bale-bot bot*",
			components=reply_markup
		)

	elif message.content == "/keyboard":
		await message.reply(
			f"*Hi {message.author.first_name}, Welcome to python-bale-bot bot*",
			components=MenuKeyboardMarkup().add(MenuKeyboardButton('/start')).add(MenuKeyboardButton('/photo')).add(MenuKeyboardButton('/voice'))
		)
        

	# elif message.content in [
	# 	'package site',
	# 	'package github'
	# ]:
	# 	await message.reply(
	# 		"{} is {}".format(message.content, {"package site": 'https://python-bale-bot.ir', "package github": 'https://python-bale-bot.ir/github'}[message.content]),
	# 		components=MenuKeyboardMarkup() # to remove menu keyboards
	# 	)
		
		
	elif message.content == "/photo":
		file = open('/photos/photo.png', 'rb').read()
		photo = InputFile(file)
		return await message.reply_photo(photo=photo, caption="This is a simple photo")

	elif  message.photos:
		print(message)
		file = open('./savedImages/attachment.png', 'wb')
		await message.document.save_to_memory(file)
		return await message.reply("I saved this image!")
	
	elif message.content == "/voice":
		reply_markup = InlineKeyboardMarkup()
		reply_markup.add(InlineKeyboardButton(text="محمود کریمی", callback_data="karimi"), row=2)
		reply_markup.add(InlineKeyboardButton(text="مهدی رسولی", callback_data="rasouli"), row=2)
		await message.reply(
			f"* کدام مداحی را ترجیح میدهی؟*",
			components=reply_markup
		)
		
	
	elif  message.audio:
		print(message)
		file = open('./savedAudios/attachment.mp3', 'wb')
		await message.document.save_to_memory(file)
		file = open('./savedAudios/attachment.mp3', 'rb').read()
		return await message.reply_audio(audio=InputFile(file), caption="صوت شما در سیستم ذخیره شد :)")
	
	else:
		await message.reply("سلام قدرتمند :)")
		

@bot.event
async def on_callback(callback: CallbackQuery):
	print("on call back")
	if callback.data == "karimi":
		client = create_connection()
		data = get_voice(client)
		file = data.getvalue()
		audio = InputFile(file)
		await callback.message.reply_audio(audio=audio, caption="این مداحی شماست :)")
	elif callback.data == "rasouli":
		file = open('madahi\\Helali\\آقام آقام آقام آقام حسین.mp3', 'rb').read()
		audio = InputFile(file)
		await callback.message.reply_audio(audio=audio, caption="این مداحی شماست :)")
bot.run()

