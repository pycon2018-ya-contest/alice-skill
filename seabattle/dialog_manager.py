# coding: utf-8

from __future__ import unicode_literals

import logging

from rasa_nlu.data_router import DataRouter

from seabattle import game


logger = logging.getLogger(__name__)
router = DataRouter('mldata/')
# mapping: user_id -> user payload dictionary
sessions = {}

AFTER_SHOT_MESSAGES = {
    'miss': '%(opponent)s, мимо я хожу %(shot)s',
    'hit': '%(opponent)s, ранил',
    'kill': '%(opponent)s, убил',
}


def _handle_newgame(user_id, message):
    session_obj = sessions.get(user_id)
    if session_obj is None:
        session_obj = {'game': game.Game()}
        sessions[user_id] = session_obj
    game_obj = session_obj['game']
    game_obj.start_new_game()
    opponent = message.split()[-1].lower().capitalize()
    session_obj['opponent'] = opponent
    return 'новая игра c ' + opponent


def _handle_letsstart(user_id, message):
    session_obj = sessions.get(user_id)
    if session_obj is None:
        return 'Необходимо инициализировать новую игру'
    opponent = session_obj['opponent']
    game_obj = session_obj['game']
    position = game_obj.do_shot()
    shot = game_obj.convert_from_position(position)
    return '%s, я хожу %s' % (opponent, shot)


def _handle_miss(user_id, message):
    session_obj = sessions.get(user_id)
    if session_obj is None:
        return 'Необходимо инициализировать новую игру'
    opponent = session_obj['opponent']
    game_obj = session_obj['game']
    # handle miss
    game_obj.handle_enemy_reply('miss')
    # handle shot
    enemy_shot = message.split()[-1]
    enemy_position = game_obj.convert_to_position(enemy_shot)
    answer = game_obj.handle_enemy_shot(enemy_position)
    response_dict = {'opponent': opponent}
    # if opponent missed do shot
    if answer == 'miss':
        position = game_obj.do_shot()
        shot = game_obj.convert_from_position(position)
        response_dict['shot'] = shot
    return AFTER_SHOT_MESSAGES[answer] % response_dict


def _handle_hit(user_id, message):
    session_obj = sessions.get(user_id)
    if session_obj is None:
        return 'Необходимо инициализировать новую игру'
    opponent = session_obj['opponent']
    game_obj = session_obj['game']
    # handle hit
    game_obj.handle_enemy_reply('hit')
    position = game_obj.do_shot()
    shot = game_obj.convert_from_position(position)
    return '%s, я хожу %s' % (opponent, shot)


def _handle_kill(user_id, message):
    session_obj = sessions.get(user_id)
    if session_obj is None:
        return 'Необходимо инициализировать новую игру'
    opponent = session_obj['opponent']
    game_obj = session_obj['game']
    # handle kill
    game_obj.handle_enemy_reply('kill')
    position = game_obj.do_shot()
    shot = game_obj.convert_from_position(position)
    return '%s, я хожу %s' % (opponent, shot)


def _handle_dontunderstand(user_id, message):
    return 'реакция на не поняла'


def handle_message(user_id, message):
    data = router.extract({'q': message})
    router_response = router.parse(data)
    logger.info('Router response %r', router_response)
    if router_response['intent']['confidence'] < 0.7:
        intent_name = 'dontunderstand'
    else:
        intent_name = router_response['intent']['name']
    handler_name = '_handle_' + intent_name
    return globals()[handler_name](user_id, message)
