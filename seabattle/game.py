# coding: utf-8

from __future__ import unicode_literals

import random
import string
import re

from transliterate import translit


class Game(object):
    position_re = re.compile('([a-zа-я]+)\s*(\w+)', re.UNICODE)

    str_numbers = ['один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять', 'десять']

    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    def __init__(self, size=10):
        assert(size <= 10)

        self.size = size
        self.field = []
        self.enemy_field = []

        self.last_shot_position = None
        self.last_enemy_shot_position = None

    def start_new_game(self, field=None):
        """
        0 - пусто
        1 - корабль
        2 - попадание
        """
        if field is None:
            self.generate_field()
        else:
            self.field = field

        self.enemy_field = [0] * self.size ** 2

        self.last_shot_position = None
        self.last_enemy_shot_position = None

    def generate_field(self):
        self.field = [0] * self.size ** 2

        for length in self.ships:
            self.place_ship(length)

        for i in range(0, len(self.field)):
            if self.field[i] == 2:
                self.field[i] = 0

    def print_field(self):
        mapping = [' ', '0', 'x']

        print '---'
        for y in range(self.size):
            print '|%s|' % ''.join(mapping[x] for x in self.field[y * self.size: y * self.size + self.size])
        print '---'

    def place_ship(self, length):
        def _try_to_place():
            x = random.randint(1, self.size)
            y = random.randint(1, self.size)
            direction = random.choice([1, self.size])

            index = self.calc_index((x, y))
            values = self.field[index:None if direction != 1 else index + self.size - index % self.size:direction][:length]

            if len(values) < length or any(values):
                return False

            for i in range(0, length):
                current_index = index + direction * i

                for j in [0, 1, -1]:
                    if (current_index % self.size in (0, self.size - 1)
                            and (current_index + j) % self.size in (0, self.size - 1)):
                        continue

                    for k in [0, self.size, -self.size]:
                        neighbour_index = current_index + k + j

                        if (neighbour_index < 0
                                or neighbour_index >= len(self.field)
                                or self.field[neighbour_index] == 1):
                            continue

                        self.field[neighbour_index] = 2

                self.field[current_index] = 1

            return True

        while not _try_to_place():
            pass

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
        x, y = self.calc_position(last_index)

        def _is_dead(line, index):
            for i in line[index:]:
                if i == 1:
                    return True

            for i in line[index::-1]:
                if i == 1:
                    return True

            return False

        return _is_dead(self.field[x::self.size], y) and _is_dead(self.field[y*self.size:(y+1)*self.size], x)

    def do_shot(self):
        index = random.choice([i for i, v in enumerate(self.enemy_field) if v == 0])

        self.last_shot_position = self.calc_position(index)
        return self.last_shot_position

    def repeat(self):
        return self.last_shot_position

    def handle_enemy_reply(self, message):
        assert(self.last_shot_position is not None)

        index = self.calc_index(self.last_shot_position)

        if message in ['hit', 'kill']:
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
            raise ValueError('Can\'t parse entire position: %s' % str_position)

        pair = match.groups()

        x = pair[0].strip()
        # преобразуем в кириллицу
        x = translit(x, 'ru')
        # преобразуем в координату
        x = ord(x) - ord('а') + 1

        y = pair[1].strip()
        if y.isdigit():
            y = int(y)
        else:
            try:
                y = self.str_numbers.index(y) + 1
            except ValueError:
                raise ValueError('Can\'t parse Y point: %s' % y)

        return x, y

    def convert_from_position(self, position):
        return '%s%s' % (unichr(position[0] + ord('а') - 1), position[1])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
