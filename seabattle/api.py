# coding: utf-8

from __future__ import unicode_literals

import json
import logging
import sys

from flask import Flask, request
from flask.logging import default_handler

from seabattle import dialog_manager as dm


app = Flask(__name__)
app.logger.removeHandler(default_handler)
app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
app.logger.setLevel(logging.INFO)


@app.route('/', methods=['POST'])
def main():
    app.logger.info('Request: %r', request.json)

    response = {
        'version': request.json['version'],
        'session': request.json['session'],
        'response': {
            'end_session': False
        }
    }
    json_body = request.json
    user_id = json_body['session']['user_id']
    message = json_body['request']['original_utterance']
    response_text = dm.handle_message(user_id, message)
    response['response']['text'] = response_text

    app.logger.info('Response: %r', response)
    return json.dumps(response)
