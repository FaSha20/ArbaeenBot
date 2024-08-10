from bale import *
from check_id_code import *
from decouple import config
bot = Bot(token=config('MAIN_TOKEN'))


database = dict()


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

	if message.content == '/start': 

		database = dict()
		database['id'] = message.author.first_name
		await message.reply(
			f"سلام {message.author.first_name}, به دستیار بروزرسانی اطلاعات موکب‌های اربعین خوش آمدید 👋\nلطفا *کد شناسایی موکب* خود را وارد کنید:",
		)
		def answer_checker(m: Message):
			return message.author == m.author and bool(message.text)
		answer_obj: Message = await bot.wait_for('message', check=answer_checker)

		if check_id_code(answer_obj.text):
			database['mukeb_name'] = ""
			reply_markup = InlineKeyboardMarkup()
			reply_markup.add(InlineKeyboardButton(text="صفر", callback_data="food_0"), row=1)
			reply_markup.add(InlineKeyboardButton(text="ده تا صد نفر", callback_data="food_10"), row=2)
			reply_markup.add(InlineKeyboardButton(text="بیشتر از صد نفر", callback_data="food_100"), row=3)
			return await answer_obj.reply(
				f' موکب شما شناسایی شد.\n 🍲 لطفا ظرفیت *پذیرایی* موکب برای امروز را اعلام بفرمایید',
				components=reply_markup
			)
		else:
			return await answer_obj.reply(
				f' موکب با این شماره *شناسایی نشد*. لطفا از صحت کد ورودی اطمینان یافته و دوباره امتحان کنید',
				components=MenuKeyboardMarkup().add(MenuKeyboardButton('/start'))
			)		
	
	
	# else:
	# 	reply_markup = InlineKeyboardMarkup()
	# 	reply_markup.add(InlineKeyboardButton(text="صفر", callback_data="food_0"), row=1)
	# 	reply_markup.add(InlineKeyboardButton(text="ده تا صد نفر", callback_data="food_10"), row=2)
	# 	reply_markup.add(InlineKeyboardButton(text="بیشتر از صد نفر", callback_data="food_100"), row=3)
	# 	await message.reply(
	# 		f"*سلام {message.author.first_name}, به بات همیار اربعین خوش اومدی :)*",
			
	# 	)
		

@bot.event
async def on_callback(callback: CallbackQuery):
	print("on call back")

	if callback.data == "food_0":
		database["food_cap"] = 0
		reply_markup = InlineKeyboardMarkup()
		reply_markup.add(InlineKeyboardButton(text="صفر", callback_data="rest_0"), row=1)
		reply_markup.add(InlineKeyboardButton(text="ده تا صد نفر", callback_data="rest_10"), row=2)
		reply_markup.add(InlineKeyboardButton(text="بیشتر از صد نفر", callback_data="rest_100"), row=3)
		await callback.message.reply(
			f"💤 لطفا ظرفیت *استراحتگاهی* موکب برای امروز را اعلام بفرمایید",
			components=reply_markup
		)
	
	elif callback.data == "food_10":
		database["food_cap"] = 10
		reply_markup = InlineKeyboardMarkup()
		reply_markup.add(InlineKeyboardButton(text="صفر", callback_data="rest_0"), row=1)
		reply_markup.add(InlineKeyboardButton(text="ده تا صد نفر", callback_data="rest_10"), row=2)
		reply_markup.add(InlineKeyboardButton(text="بیشتر از صد نفر", callback_data="rest_100"), row=3)
		await callback.message.reply(
			f"💤 لطفا ظرفیت *استراحتگاهی* موکب برای امروز را اعلام بفرمایید",
			components=reply_markup
		)

	elif callback.data == "food_100":
		database["food_cap"] = 100
		reply_markup = InlineKeyboardMarkup()
		reply_markup.add(InlineKeyboardButton(text="صفر", callback_data="rest_0"), row=1)
		reply_markup.add(InlineKeyboardButton(text="ده تا صد نفر", callback_data="rest_10"), row=2)
		reply_markup.add(InlineKeyboardButton(text="بیشتر از صد نفر", callback_data="rest_100"), row=3)
		await callback.message.reply(
			f"💤 لطفا ظرفیت *استراحتگاهی* موکب برای امروز را اعلام بفرمایید",
			components=reply_markup
		)
		
	elif callback.data == "rest_0":
		database["rest_cap"] = 0
		reply_markup = InlineKeyboardMarkup()
		reply_markup.add(InlineKeyboardButton(text="ثبت", callback_data="register"), row=1)
		reply_markup.add(InlineKeyboardButton(text="ویرایش", callback_data="edit"), row=2)
		await callback.message.reply(
			f'*اطلاعات دریافت شده*\n نام موکب : {""}\n ظرفیت پذیرایی: {database["food_cap"]}\n ظرفیت استراحتگاهی: {database["rest_cap"]}\n ',
			components=reply_markup
		)
	
	elif callback.data == "rest_10":
		database["rest_cap"] = 10
		reply_markup = InlineKeyboardMarkup()
		reply_markup.add(InlineKeyboardButton(text="ثبت", callback_data="register"), row=1)
		reply_markup.add(InlineKeyboardButton(text="ویرایش", callback_data="edit"), row=2)
		await callback.message.reply(
			f'*اطلاعات دریافت شده*\n نام موکب : {""}\n ظرفیت پذیرایی: {database["food_cap"]}\n ظرفیت استراحتگاهی: {database["rest_cap"]}\n ',
			components=reply_markup
		)

	elif callback.data == "rest_100":
		database["rest_cap"] = 100
		reply_markup = InlineKeyboardMarkup()
		reply_markup.add(InlineKeyboardButton(text="ثبت", callback_data="register"), row=1)
		reply_markup.add(InlineKeyboardButton(text="ویرایش", callback_data="edit"), row=2)
		await callback.message.reply(
			f'*اطلاعات دریافت شده*\n نام موکب : {""}\n ظرفیت پذیرایی: {database["food_cap"]}\n ظرفیت استراحتگاهی: {database["rest_cap"]}\n ',
			components=reply_markup
		)
	
	elif callback.data == "edit":
		reply_markup = InlineKeyboardMarkup()
		reply_markup.add(InlineKeyboardButton(text="صفر", callback_data="food_0"), row=1)
		reply_markup.add(InlineKeyboardButton(text="ده تا صد نفر", callback_data="food_10"), row=2)
		reply_markup.add(InlineKeyboardButton(text="بیشتر از صد نفر", callback_data="food_100"), row=3)
		return await callback.message.reply(
			f' 🍲 لطفا *ظرفیت پذیرایی* موکب برای امروز را اعلام بفرمایید',
			components=reply_markup
		)
	
	elif callback.data == "register":
		update_record(database)
		await callback.message.reply(
			f"*اطلاعات با موفقیت ثبت شد. متشکریم از زمانی که اختصاص دادید 🙏 *"
		)


bot.run()

