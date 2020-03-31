# -*- coding: utf-8 -*-

# Copyright 2020 Scriptim (https://github.com/Scriptim)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This module is an example implementation for a player that ask the user for moves via the command line."""

from typing import List, Tuple, Union

import inquirer

from abalone.abstract_player import AbstractPlayer
from abalone.enums import Direction, Space
from abalone.game import Game


def _prompt_move_type() -> str:
    return inquirer.prompt([
        inquirer.List('move_type',
                      message='What type of move do you want to perform?',
                      choices=['In-line', 'Broadside']
                      )
    ])['move_type']


def _prompt_marble1(move_type: str, legal_moves: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]]) -> Space:
    marble1_candidates = set()
    if move_type == 'In-line':
        message = 'Select the trailing marble'
        for legal_move in legal_moves:
            if isinstance(legal_move[0], Space):
                marble1_candidates.add(legal_move[0])
    else:
        message = 'Select the first of the outermost marbles'
        for legal_move in legal_moves:
            if isinstance(legal_move[0], tuple):
                marble1_candidates.add(legal_move[0][0])
                marble1_candidates.add(legal_move[0][1])
    marble1_candidates = list(map(lambda space: space.name, marble1_candidates))
    marble1_candidates.sort()
    marble1 = inquirer.prompt([
        inquirer.List('marble1',
                      message=message,
                      choices=marble1_candidates,
                      carousel=True
                      )
    ])['marble1']
    return Space[marble1]


def _prompt_marble2(marble1: Space, legal_moves: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]]) -> Space:
    marble2_candidates = set()
    for legal_move in legal_moves:
        if isinstance(legal_move[0], tuple) and marble1 in legal_move[0]:
            if legal_move[0][0] is marble1:
                marble2_candidates.add(legal_move[0][1])
            else:
                marble2_candidates.add(legal_move[0][0])
    marble2_candidates = list(map(lambda space: space.name, marble2_candidates))
    marble2_candidates.sort()
    marble2 = inquirer.prompt([
        inquirer.List('marble2',
                      message='Select the second of the outermost marbles',
                      choices=marble2_candidates,
                      carousel=True
                      )
    ])['marble2']
    return Space[marble2]


def _prompt_direction(marbles: Union[Space, Tuple[Space, Space]],
                      legal_moves: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]]) -> Direction:
    direction_candidates = set()
    for legal_move in legal_moves:
        if marbles == legal_move[0] or (isinstance(marbles, tuple) and marbles[::-1] == legal_move[0]):
            direction_candidates.add(legal_move[1])
    direction_candidates = list(map(lambda space: space.name, direction_candidates))
    direction_candidates.sort()
    direction = inquirer.prompt([
        inquirer.List('direction',
                      message='Select the direction of movement',
                      choices=direction_candidates,
                      carousel=True
                      )
    ])['direction']
    return Direction[direction]


class HumanPlayer(AbstractPlayer):

    def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]]) \
            -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:
        legal_moves = list(game.generate_legal_moves())
        move_type = _prompt_move_type()
        marble1 = _prompt_marble1(move_type, legal_moves)

        if move_type == 'In-line':
            marbles = marble1
        else:
            marbles = (marble1, _prompt_marble2(marble1, legal_moves))

        return marbles, _prompt_direction(marbles, legal_moves)
