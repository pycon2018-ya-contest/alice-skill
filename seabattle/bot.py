# coding: utf-8

import logging
import os

from telegram import ext as telegram_ext

from seabattle import dialog_manager as dm


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def bot_handler(bot, update):
    (response_message, _) = dm.handle_message(update.message.chat_id, update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=response_message)


def error_handler(bot, update, error):
    logger.error('Update "{0}" caused error "{1}"', update, error)


updater = telegram_ext.Updater(token=os.environ.get('TELEGRAM_TOKEN'))
dispatcher = updater.dispatcher
dispatcher.add_handler(telegram_ext.MessageHandler(telegram_ext.Filters.text, bot_handler))
updater.start_polling()
updater.idle()
