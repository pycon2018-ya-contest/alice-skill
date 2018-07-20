# coding: utf-8

from __future__ import unicode_literals

import json
import logging
import sys

from flask import Flask, request

from seabattle import dialog_manager as dm
from seabattle import session


app = Flask(__name__)

handler = logging.StreamHandler(stream=sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger('seabattle')
logger.addHandler(handler)
logger.setLevel(logging.INFO)


@app.route('/', methods=['POST'])
def main():
    logger.error('Request: %r', request.json)

    response = {
        'version': request.json['version'],
        'session': request.json['session'],
    }
    json_body = request.json

    user_id = json_body['session']['user_id']
    session_obj = session.get(user_id)
    dm_obj = dm.DialogManager(session_obj)

    message = json_body['request']['command'].strip()
    if not message:
        message = json_body['request']['original_utterance']

    (response_text, end_session) = dm_obj.handle_message(message)
    response['response'] = {
        'text': response_text,
        'end_session': end_session,
    }

    logger.error('Response: %r', response)
    return json.dumps(response)
