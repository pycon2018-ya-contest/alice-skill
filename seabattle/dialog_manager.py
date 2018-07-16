# coding: utf-8

import logging

from rasa_nlu.data_router import DataRouter

from seabattle import game


logger = logging.getLogger(__name__)
router = DataRouter('projects/')
# mapping: user_id -> user payload dictionary
sessions = {}


def _handle_newgame(user_id, message):
    game_obj = sessions.get(user_id, game.Game())
    game_obj.start_new_game()
    sessions[user_id] = game_obj
    return 'новая игра ок'


def _handle_letsstart(user_id, message):
    game_obj = sessions.get(user_id)
    if game_obj is None:
        game_obj = game.Game()
        sessions[user_id] = game_obj



def _handle_miss(user_id, message):
    pass


def _handle_hit(user_id, message):
    pass


def _handle_kill(user_id, message):
    pass


def handle_message(user_id, message):
    data = router.extract({'q': message})
    router_response = router.parse(data)
    intent_name = router_response['intent']['name']
    handler_name = '_handle_' + intent_name
    return locals()[handler_name](user_id, message)
