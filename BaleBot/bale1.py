from telegram import Update, ForceReply, Bot, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from chat.chat_bot import answer_me, get_faq
from feeder import feed_data
from telegram_handlers.callback import call_back_functions
from auth import user_authentication
from db import send_user_message, send_user_message_dict, get_config, add_new_chat, get_chat_history, create_pre_chat, session, PublicData
import base64
import io, requests
import httpx
import logging, os, time
import html, random, json, datetime, os, traceback, asyncio

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('BOT_TOKEN').strip()
WEBHOOK_URL = os.environ.get('WEBHOOK_URL').strip()
TELEGRAM_SECRET = os.environ.get('TELEGRAM_SECRET', 'rvqUTYBrUOQlgSD9VI3c')
ADMIN_USER = os.environ.get('ADMIN_USER', '1849994649')
ADMIN_GROUP = os.environ.get('ADMIN_GROUP', '1849994649')
TELEGRAM_BASE_URL = os.environ.get('TELEGRAM_BASE_URL', 'https://tapi.bale.ai/')
application = Application.builder().token(TOKEN).updater(None).base_url(TELEGRAM_BASE_URL).base_file_url('https://tapi.bale.ai/file/').build()

bot = application.bot

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def split_text_into_chunks(text, chunk_size):
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]


@user_authentication()
async def start(update: Update, context: CallbackContext, db_user) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info(f'User {user} start the bot')
    await update.message.reply_chat_action('typing')
    reply_markup = None
    # keyboard = [[InlineKeyboardButton('ارسال مداحی📿', callback_data='madahi:')]]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    await send_user_message(context.bot, chat_id=update.effective_chat.id, message_slug='start', reply_markup=reply_markup)
    await update.message.reply_chat_action('typing')
    time.sleep(0.7)
    await send_user_message(context.bot, chat_id=update.effective_chat.id, message_slug='second_start', reply_markup=reply_markup)
    await update.message.reply_chat_action('typing')
    time.sleep(0.5)
    await send_user_message(context.bot, chat_id=update.effective_chat.id, message_slug='third_start', reply_markup=reply_markup)
    
@user_authentication()
async def help_command(update: Update, context: CallbackContext, user) -> None:
    """Send a message when the command /help is issued."""
    logger.info('User ask for a help')
    await send_user_message(context.bot, chat_id=update.effective_chat.id, message_slug='help')
    
    # update.message.reply_text('بازوی اربعین ۱۴۰۳ راهنمای جامع در پاسخ به تمام سوالات شماست. در این بازو شما میتوانید سوالا خود را در مورد اربعین ۱۴۰۳ بپرسید و جواب‌های مناسب دریافت کنید')
    
@user_authentication()  
async def not_support_message(update, context, user) -> None:
    await update.message.reply_text('محتوای ارسالی پشتیبانی نمیشود. لطفا متن ارسال نمایید.')
 
async def error_callback(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    try:
        # collect error message
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = "".join(tb_list)
        message = (
            f"*An exception was raised while handling an update*\n"
            f"```{tb_string}```"
        )
        print(message)

        # split text into multiple messages due to 4096 character limit
        for message_chunk in split_text_into_chunks(message, 4096):
            try:
                await context.bot.send_message(ADMIN_USER, message_chunk)
            except Exception as e:
                # answer has invalid characters, so we send it without parse_mode
                await context.bot.send_message(ADMIN_USER, message_chunk)
    except:
        await context.bot.send_message(ADMIN_USER, "Some error in error handler")

async def response_user_handler(update: Update, context: CallbackContext, user, text) -> None:
    chat =  update.effective_chat
    sent_msg = await context.bot.send_message(chat_id=chat.id, text='در حال نوشتن...')
    await update.message.reply_chat_action('typing')
    pre_chat = create_pre_chat(user, text)
    pre_def_message = await get_faq(text)
    # logger.info("Pre define message: {}".format(pre_def_message))
    if pre_def_message:
        logger.info('FAQ was found')
        # time.sleep(delay)
        text_message = await send_user_message_dict(bot=context.bot, chat_id=user.chat_id, document=pre_def_message)
        await sent_msg.delete()
        db_chat = add_new_chat(user=user, user_input=text, response={'answer': text_message}, message_id=sent_msg.message_id, openai_callback=None)
        pre_chat.chat_id = db_chat.id
        session.commit()
        return
    
    logger.info(f'User {chat.id} ask something')
    history = get_chat_history(user_id = user.id)
    logger.info(f'[{chat}] Total user history {len(history)}')
    answer, openai_callback = await answer_me(user, text, history)
    logger.info(answer)
    db_chat = add_new_chat(user=user, user_input=text, response=answer, message_id=sent_msg.message_id, openai_callback=openai_callback)

    logger.info('Going to update text')
    reply_markup = None
    await sent_msg.edit_text(text=answer['answer'].replace('***', '*').replace('**', '*').replace('#', '') + '\n\nاگر سوال دیگه‌ای هست در خدمتم', reply_markup=reply_markup)
    pre_chat.chat_id = db_chat.id
    session.commit()
    logger.info(f'[{db_chat}] Chat info: total words: {db_chat.total_words}, input tokens: {db_chat.llm_input_token} output: {db_chat.llm_output_token}')

@user_authentication()
async def call_back_data_handler(update: Update, context: CallbackContext, user) -> None:
    command, data = update.callback_query.data.split(':')
    await call_back_functions[command](update, context, user, data)

@user_authentication()
async def chat_bot_handler(update: Update, context: CallbackContext, user) -> None:
    await response_user_handler(update=update, context=context, user=user, text=update.message.text)
    
async def add_public_data_handler(update: Update, context: CallbackContext) -> None:
    config = get_config('PublicData')
    data = update.message.to_dict()
    page_content = data.get('text') if data.get('text') else data.get('caption')
    if not update.message or page_content is None or config is None:
        print(f'Skipping... {update.message.chat.id}')
        return
    metadata = data
    metadata['time'] = datetime.datetime.now().isoformat()
    metadata['source'] = update.message.chat.title
    updates = {'update': update.to_dict(), 'message': data, 'metadata': metadata}
    obj = PublicData(chat_id=update.message.chat.id, title= update.message.chat.title, text=page_content, updates_data=updates)
    session.add(obj)
    session.commit()
    if update.message.chat.id not in config.config['channel_ids']:
        print(f'Not Channel...  {update.message.chat.id}')
        return
    keyboard = [[InlineKeyboardButton('اضافه شود➕', callback_data='public_content:s=1&pid={}'.format(obj.id))],
                [InlineKeyboardButton('پاک شود➖', callback_data='public_content:s=0&pid={}'.format(obj.id))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(ADMIN_GROUP, text=f'نام کانال یا منبع: {update.message.chat.title}\n{page_content}', reply_markup=reply_markup)

@user_authentication()  
async def voice_handler(update: Update, context, user) -> None:
    
    file_obj = await context.bot.get_file(update.message.voice.file_id)
    sent_msg = await update.message.reply_text('در حال پردازش صدا...')
    with io.BytesIO() as fh:
        await file_obj.download_to_memory(out=fh, read_timeout=20, write_timeout=20, connect_timeout=20, pool_timeout=20)
        fh.seek(0)  # Reset cursor position to the start of the file
        file_data = fh.read()
        
    response = await speech_to_text(file_data)
    text = response['data']['data']['result']
    if not text.strip():
        await sent_msg.edit_text('صدا واضح نیست و صحبتی را متوجه نشدم')
        return
    await sent_msg.delete()
    await response_user_handler(update=update, context=context, user=user, text=text)
    
async def media_admin_handler(update, context) -> None:
    await context.bot.send_message(ADMIN_USER, text=f'Data received ```[{update.message}]```')

async def pre_setup() -> None:
    """Start the bot."""
    global application
    # webhook_url = f'https://tapi.bale.ai/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}/{TOKEN}{TELEGRAM_SECRET}'
    # r = requests.get(webhook_url)  # Set the webhook URL
    logger.info(f'Setting webhook. Result: {WEBHOOK_URL}/{TOKEN}{TELEGRAM_SECRET}')
    try:
        result = await bot.set_webhook(url=f'{WEBHOOK_URL}/{TOKEN}{TELEGRAM_SECRET}')
        logger.info(f'Setting webhook. Result: {result}')
    except Exception as e:
        logger.error(f'Error in adding webhook {e}')
    # Run the Flask app on a specific port

    # Create the Updater and pass it your bot's token.
    # TOKEN = os.environ.get('BOT_TOKEN')

    # on different commands - answer in Telegram
    application.add_handler(MessageHandler(filters.Regex("^/start"), start))
    application.add_handler(MessageHandler(filters.Regex("^/help"), help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, chat_bot_handler))
    application.add_handler(MessageHandler(filters.ChatType.GROUP, add_public_data_handler))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, not_support_message))
    application.add_handler(MessageHandler(filters.VOICE & filters.ChatType.PRIVATE, voice_handler))
    
    application.add_handler(MessageHandler( (filters.PHOTO & filters.VIDEO & filters.AUDIO & filters.ChatType.PRIVATE), media_admin_handler))
    
    application.add_handler(CallbackQueryHandler(call_back_data_handler))
    
    application.add_error_handler(error_callback)

    

    if os.environ.get('POLLING', 'false') == 'true':
        # Start the Bot
        logger.warning('POLING MODE')
        application.start_polling()
    
    await application.initialize()
    await application.start()
