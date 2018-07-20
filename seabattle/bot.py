# coding: utf-8

from __future__ import unicode_literals

import logging
import os

from telegram import ext as telegram_ext

from seabattle import dialog_manager as dm
from seabattle import session


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def bot_handler(bot, update):
    session_obj = session.get(update.message.chat_id)
    dm_obj = dm.DialogManager(session_obj)
    (response_message, _) = dm_obj.handle_message(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=response_message)


def error_handler(bot, update, error):
    logger.error('Update "{0}" caused error "{1}"', update, error)


updater = telegram_ext.Updater(token=os.environ.get('TELEGRAM_TOKEN'))
dispatcher = updater.dispatcher
dispatcher.add_handler(telegram_ext.MessageHandler(telegram_ext.Filters.text, bot_handler))
updater.start_polling()
updater.idle()
