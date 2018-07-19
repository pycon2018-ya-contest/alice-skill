# coding: utf-8
from __future__ import unicode_literals
from seabattle.game import Game

import pytest


@pytest.fixture
def game():
    g = Game()
    g.start_new_game()

    return g


@pytest.fixture
def game_with_field(game):
    field = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
             1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 1, 0, 1, 0, 1, 0, 0,
             1, 1, 0, 1, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 1, 0, 1, 1, 1, 0, 0,
             0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 1, 0, 0, 1, 1, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

    game.start_new_game(field=field)

    return game


def test_helper_functions(game):
    assert game.calc_index((4, 7)) == 63

    assert game.calc_position(63) == (4, 7)

    assert game.convert_to_position('a10') == (1, 10)
    assert game.convert_to_position('d 7') == (5, 7)
    assert game.convert_to_position('д 5') == (5, 5)
    assert game.convert_to_position('g 3') == (4, 3)

    assert game.convert_to_position('d пять') == (5, 5)

    with pytest.raises(ValueError):
        game.convert_to_position('д пятнадцать')

    assert game.convert_from_position((1, 1)) == 'а1'
    assert game.convert_from_position((6, 5)) == 'е5'


def test_shot(game):
    pass


def test_dead_ship(game_with_field):
    assert game_with_field.handle_enemy_shot((7, 1)) == 'dead'

    assert game_with_field.handle_enemy_shot((1, 5)) == 'hit'
    assert game_with_field.handle_enemy_shot((2, 5)) == 'dead'

    assert game_with_field.handle_enemy_shot((1, 2)) == 'hit'
    assert game_with_field.handle_enemy_shot((2, 2)) == 'hit'
    assert game_with_field.handle_enemy_shot((3, 2)) == 'dead'


def test_repeat(game):
    shot = game.do_shot()
    assert shot == game.repeat()


def test_handle_shot(game_with_field):
    assert game_with_field.handle_enemy_shot((4, 7)) == 'hit'
    assert game_with_field.handle_enemy_shot((4, 7)) == 'miss'

    assert game_with_field.handle_enemy_shot((4, 2)) == 'miss'


def test_handle_reply(game):
    game.do_shot()
    game.handle_enemy_reply('miss')
