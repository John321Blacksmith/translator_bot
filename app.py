import logging
from telegram import __version__ as TG_VER
from telebot.credentials import api_token
from telebot import lang_scraper


try:
	from telegram import __version_info__
except ImportError:
	__version_info__ = (0, 0, 0, 0, 0)


if __version_info__ < (20, 0, 0, 'alpha', 1):
	raise RuntimeError(
			f'This example is not compatible with your curren PTB version {TG_VER}'
		)

from telegram import ForceReply, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters


# involve logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
	)

logger = logging.getLogger(__name__)


# define a few functions-handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""This function retruns a reflected message to the user."""

	# define a user
	user = update.effective_user

	keyboard = [
		[InlineKeyboardButton('English', callback_data="английском")],
		[InlineKeyboardButton('Русский', callback_data="русском")]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)


	await update.message.reply_html(
		rf"Привет, {user.mention_html()}, я твой чат-словарь. Здесь ты можешь найти перевод русского или английского слова, выбрав язык ввода.Скоро научусь переводить и предложения :-)"
		)

	await update.message.reply_text("Выбери язык ввода: ", reply_markup=reply_markup)


async def switch_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""This function pushes the optional buttons, so the user can switch an input language."""

	# define lang buttons
	keyboard = [
		[InlineKeyboardButton('English', callback_data="английском")],
		[InlineKeyboardButton('Русский', callback_data="русском")]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)

	await update.message.reply_text("Выбери язык ввода: ", reply_markup=reply_markup)


async def lang_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""This function triggers the language input."""
	global query

	query = update.callback_query

	await query.answer()

	await query.edit_message_text(text=f'Введи любое слово на {query.data} языке.\nКликни "/switch", для смены языка ввода.')


async def return_translation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""This function returns a whole word data."""
	word = update.message.text

	if query.data == 'английском':
		input_lang = 'English'

	if query.data == 'русском':
		input_lang = 'Russian'

	word_meaning = lang_scraper.extract_meaning(word.lower(), input_lang, 'telebot//dict_configs.json')

	if not word_meaning:
		msg = "Слово не распознано. Убедись в правильности ввода.\nКликни \'/start'\', чтобы начать перевод заново.\nДля смены языка, кликни \'/switch\'"
	else:
		msg = f"""Слово: {word_meaning['word']}\n
				  Перевод: {word_meaning['meaning']}\n
				  Часть речи: {word_meaning['word_type']}\n
				  Склонение: {word_meaning['conjugate']}\n
				  Транскрипция: {word_meaning['transcription']}\n
				  Пример: {word_meaning['examples']}"""



	await update.message.reply_text(text=msg)


# a triggering function
def main() -> None:
	"""Launch the bot."""
	

	# define an application
	application = Application.builder().token(api_token).build()


	# handlers for different commands

	# render the opptional buttons
	application.add_handler(CommandHandler('start', start))

	# change language
	application.add_handler(CommandHandler('switch', switch_lang))

	# if not any of the specified commands, the echo is involved
	application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, return_translation))

	# choose the language
	application.add_handler(CallbackQueryHandler(lang_options))

	# run the bot until the CTRL-C shuts it down
	application.run_polling()


if __name__ == '__main__':
	main()