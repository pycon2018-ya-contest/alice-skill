# coding: utf-8

import json
import logging
import os

from telegram import ext as telegram_ext
from rasa_nlu.data_router import DataRouter


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)
router = DataRouter('projects/')


def bot_handler(bot, update):
    data = router.extract({'q': update.message.text})
    response = router.parse(data)
    bot.send_message(chat_id=update.message.chat_id, text=json.dumps(response, indent=2))
    # '{}:{}'.format(
    #    response['intent']['name'],
    #    response['entities'][0]['value'] if response['entities'] else '-',
    #    response['entities'][0]['entity'] if response['entities'] else '-',
    # ))


def error_handler(bot, update, error):
    logger.error('Update "{0}" caused error "{1}"', update, error)


updater = telegram_ext.Updater(token=os.environ.get('TELEGRAM_TOKEN'))
dispatcher = updater.dispatcher
dispatcher.add_handler(telegram_ext.MessageHandler(telegram_ext.Filters.text, bot_handler))
updater.start_polling()
updater.idle()
