from decouple import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

token = config('TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keys = [
        [InlineKeyboardButton("Click here1", url="google.com"),InlineKeyboardButton("Click there2", url="navaapp.com")],
        [InlineKeyboardButton("Click here3", url="google.com"),InlineKeyboardButton("Click there4", url="navaapp.com")]
    ]
    markup = InlineKeyboardMarkup(keys)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="سلام به بات اربعین خوش آمدید :)",
        reply_to_message_id=update.effective_message.id,
        reply_markup=markup)

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    with open("pictures\OIP.jfif", "rb") as f:
        img = f.read()
    img_url = "https://wallpapers.com/images/hd/golden-tower-hossain-shrine-karbala-bhs0e0a3mtobwbxe.jpg"
    
    keys = [
        [InlineKeyboardButton("Click here1", url="google.com"),InlineKeyboardButton("Click there2", url="navaapp.com")],
        [InlineKeyboardButton("Click here3", url="google.com"),InlineKeyboardButton("Click there4", url="navaapp.com")]
    ]
    reply_markup = ReplyKeyboardMarkup(keys)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id, 
        photo=img,
        reply_to_message_id=update.effective_message.id,
        caption="هله بالزوار الحسین علیه السلام :)",
        reply_markup=reply_markup
    )


if __name__ == "__main__":
    bot = Application.builder().token(token).build()
    
    bot.add_handlers([
        CommandHandler('start', start),
        CommandHandler("photo", photo)
    ])

    bot.run_polling()