from bale import *
bot = Bot(token="152238739:EU8ukOoTPGfSknbp2zqZfzAFu5I8l8ah5Rn7NznW")
    

@bot.event
async def on_ready():
	print(bot.user.username, "is Ready!")

@bot.event
async def on_update(update: Update):
	if(update.message != None):
		print(update.message.text)
	else: 
	    print(update.message)

@bot.event
async def on_message(message: Message):
	if message.content == '/start': # to get caption or text of message
		await message.reply(
			f"*سلام {message.author.first_name}, به بات همیار اربعین خوش اومدی :)*",
			components=MenuKeyboardMarkup().add(MenuKeyboardButton('مداحی و  محتوای صوتی')).add(MenuKeyboardButton('گمشدگان و پیداشدگان')).add(MenuKeyboardButton('تجربیات اربعین'))
		)
	
	elif  message.photos:
		print(message)
		file = open('./savedImages/attachment.png', 'wb')
		await message.document.save_to_memory(file)
		return await message.reply("تصویر شما ذخیره شد")
	
	elif message.content == 'مداحی و  محتوای صوتی':
		reply_markup = InlineKeyboardMarkup()
		reply_markup.add(InlineKeyboardButton(text="محمود کریمی", callback_data="karimi"), row=1)
		reply_markup.add(InlineKeyboardButton(text="مهدی رسولی", callback_data="rasouli"), row=1)
		reply_markup.add(InlineKeyboardButton(text="مجید بنی فاطمه", callback_data="banifatemeh"), row=2)
		reply_markup.add(InlineKeyboardButton(text="سعید حدادیان", callback_data="haddadian"), row=2)
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
		await message.reply(
			f"لطفا دستور معتبر وارد کنید :)",
			components=MenuKeyboardMarkup().add(MenuKeyboardButton('مداحی و  محتوای صوتی')).add(MenuKeyboardButton('گمشدگان و پیداشدگان')).add(MenuKeyboardButton('تجربیات اربعین'))
		)
		

@bot.event
async def on_callback(callback: CallbackQuery):
	print("on call back")
	if callback.data == "karimi":
		reply_markup = InlineKeyboardMarkup()
		reply_markup.add(InlineKeyboardButton(text="محمود کریمی", callback_data="karimi"), row=1)
		reply_markup.add(InlineKeyboardButton(text="مهدی رسولی", callback_data="rasouli"), row=1)
		reply_markup.add(InlineKeyboardButton(text="مجید بنی فاطمه", callback_data="banifatemeh"), row=2)
		reply_markup.add(InlineKeyboardButton(text="سعید حدادیان", callback_data="haddadian"), row=2)
		await callback.message.reply(
			f"* مداحی‌ها*",
			components=reply_markup
		)
		file = open('madahi\\Karimi\\saghi_teflan_hosein.mp3', 'rb').read()
		audio = InputFile(file)
		await callback.message.reply_audio(audio=audio, caption="این مداحی شماست :)")
	elif callback.data == "rasouli":
		file = open('madahi\\Helali\\آقام آقام آقام آقام حسین.mp3', 'rb').read()
		audio = InputFile(file)
		await callback.message.reply_audio(audio=audio, caption="این مداحی شماست :)")
		


bot.run()

