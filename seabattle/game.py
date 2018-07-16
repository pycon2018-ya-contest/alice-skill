# coding: utf-8

from __future__ import unicode_literals

import random
import string
import re

from transliterate import translit


class Game(object):
    """
    >>> game = Game()
    >>> game.start_new_game()
    >>> game.calc_index((4, 7))
    63
    >>> game.calc_position(63)
    (4, 7)
    >>> game.convert_to_position('a10')
    (1, 10)
    >>> game.convert_to_position('f 7')
    (6, 7)
    >>> game.convert_to_position('ф 5')
    (6, 5)
    >>> game.convert_from_position((1, 1))
    u'a1'
    >>> game.convert_from_position((6, 5))
    u'f5'
    >>> game.handle_enemy_shot((4, 7))
    u'hit'
    >>> game.handle_enemy_shot((4, 7))
    u'hit'
    >>> game.handle_enemy_shot((4, 2))
    u'miss'
    >>> shot = game.do_shot()
    >>> shot == game.repeat()
    True
    >>> game.handle_enemy_reply('miss')
    """
    position_re = re.compile('(\D+)(\d+)', re.UNICODE)

    def __init__(self, size=10):
        assert(size <= len(string.lowercase))

        self.size = size
        self.field = []
        self.enemy_field = []

        self.last_shot_position = None
        self.last_enemy_shot_position = None

    def start_new_game(self):
        """
        0 - пусто
        1 - корабль
        2 - попадание
        """
        self.field = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                      1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 1, 0, 1, 0, 1, 0, 0,
                      1, 1, 0, 1, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 1, 0, 1, 1, 1, 0, 0,
                      0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 1, 0, 0, 1, 1, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

        self.enemy_field = [0] * self.size ** 2

        self.last_shot_position = None
        self.last_enemy_shot_position = None

    def handle_enemy_shot(self, position):
        index = self.calc_index(position)

        if self.field[index] in (1, 2):
            self.field[index] = 2

            if self.is_dead_ship(index):
                return 'dead'
            else:
                return 'hit'
        else:
            return 'miss'

    def is_dead_ship(self, last_index):
        return False

    def do_shot(self):
        index = random.choice([i for i, v in enumerate(self.enemy_field) if v == 0])

        self.last_shot_position = self.calc_position(index)
        return self.last_shot_position

    def repeat(self):
        return self.last_shot_position

    def handle_enemy_reply(self, message):
        index = self.calc_index(self.last_shot_position)

        if message == 'hit':
            self.enemy_field[index] = 2
        elif message == 'miss':
            self.enemy_field[index] = 0

    def calc_index(self, position):
        x, y = position
        return (y - 1) * self.size + x - 1

    def calc_position(self, index):
        y = index / self.size + 1
        x = index % self.size + 1

        return x, y

    def convert_to_position(self, str_position):
        match = self.position_re.match(str_position)

        if match is None:
            raise ValueError('Can\'t parse position: %s' % str_position)

        pair = match.groups()

        x = pair[0].strip()
        y = int(pair[1].strip())

        # преобразуем в латиницу
        x = translit(x, 'ru', reversed=True)
        # преобразуем в координату
        x = ord(x) - ord('a') + 1

        return x, y

    def convert_from_position(self, position):
        return '%s%s' % (chr(position[0] + ord('a') - 1), position[1])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
