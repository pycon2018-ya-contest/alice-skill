# coding: utf-8

from __future__ import unicode_literals

import json
import logging

from seabattle import game


logger = logging.getLogger(__name__)
MESSAGE_TEMPLATES = {
    'miss': 'Мимо. Я хожу %(shot)s',
    'hit': 'Ранил',
    'kill': 'Убил',
    'newgame': 'Инициализирована новая игра c %(opponent)s',
    'shot': 'Я хожу %(shot)s',
    'defeat': 'Я проиграл',
    'victory': 'Ура, победа!',
    'need_init': 'Пожалуйста, инициализируй новую игру и укажи соперника',
    'dontunderstand': 'Не поняла. Пожалуйста, повтори последний ход'
}


def _get_entity(entities, entity_type):
    try:
        return next(e['value'] for e in entities if e['entity'] == entity_type)
    except StopIteration:
        return None


class DialogManager(object):
    def __init__(self, session_obj, router):
        self.router = router
        self.session = session_obj
        self.game = session_obj['game']
        self.opponent = session_obj['opponent']
        self.last = session_obj['last']

    def _need_init_game(self):
        return (MESSAGE_TEMPLATES['need_init'], 'dontunderstand')

    def _dont_understand(self):
        return (MESSAGE_TEMPLATES['dontunderstand'], 'dontunderstand')

    def _handle_newgame(self, message, entities):
        self.game = game.Game()
        self.session['game'] = self.game
        self.game.start_new_game(numbers=True)
        if not entities:
            return self._need_init_game()

        self.opponent = _get_entity(entities, 'opponent_entity')
        self.session['opponent'] = self.opponent
        response_dict = {'opponent': self.opponent}
        return (MESSAGE_TEMPLATES['newgame'] % response_dict, 'newgame')

    def _handle_letsstart(self, message, entities):
        if self.game is None:
            return self._need_init_game()
        shot = self.game.do_shot()
        return (MESSAGE_TEMPLATES['shot'] % {'shot': shot}, 'miss')

    def _handle_miss(self, message, entities):
        if self.game is None:
            return self._need_init_game()

        self.game.handle_enemy_reply('miss')
        if not entities:
            return self._dont_understand()
        enemy_shot = _get_entity(entities, 'hit_entity')
        try:
            enemy_position = self.game.convert_to_position(enemy_shot)
            answer = self.game.handle_enemy_shot(enemy_position)
        except ValueError:
            return self._dont_understand()
        response_dict = {'opponent': self.opponent}
        if answer == 'miss':
            response_dict['shot'] = self.game.do_shot()
        return (MESSAGE_TEMPLATES[answer] % response_dict, answer)

    def _handle_hit(self, message, entities):
        if self.game is None:
            return self._need_init_game()

        self.game.handle_enemy_reply('hit')
        shot = self.game.do_shot()
        return (MESSAGE_TEMPLATES['shot'] % {'shot': shot}, 'miss')

    def _handle_kill(self, message, entities):
        if self.game is None:
            return self._need_init_game()

        self.game.handle_enemy_reply('kill')
        shot = self.game.do_shot()
        if self.game.is_victory():
            return (MESSAGE_TEMPLATES['victory'], 'victory')
        else:
            return (MESSAGE_TEMPLATES['shot'] % {'shot': shot}, 'miss')

    def _handle_dontunderstand(self, message, entities):
        if self.game is None:
            return self._need_init_game()

        if self.last['message_type'] == 'miss':
            shot = self.game.repeat()
            return (MESSAGE_TEMPLATES['miss'] % {'shot': shot}, 'miss')
        return (self.last['message'], 'dontunderstand')

    def _handle_victory(self, message, entities):
        self.session['game'] = self.game = None
        return (MESSAGE_TEMPLATES['defeat'], 'defeat')

    def _handle_defeat(self, message, entities):
        self.session['game'] = self.game = None
        return (MESSAGE_TEMPLATES['victory'], 'victory')

    def handle_message(self, message):
        data = self.router.extract({'q': message})
        router_response = self.router.parse(data)
        logger.error('Router response %s', json.dumps(router_response, indent=2))

        if router_response['intent']['confidence'] < 0.75:
            intent_name = 'dontunderstand'
        else:
            intent_name = router_response['intent']['name']
        entities = router_response['entities']

        handler_method = getattr(self, '_handle_' + intent_name)
        (response_message, message_type) = handler_method(message, entities)
        self.session['last'] = self.last = {
            'message': response_message,
            'message_type': message_type,
        }
        end_session = False
        if intent_name in ['victory', 'defeat']:
            end_session = True
        return (response_message, end_session)
