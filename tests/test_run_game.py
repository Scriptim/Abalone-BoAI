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

"""Unit tests for `abalone.game`"""

import unittest
from typing import List, Tuple, Union

from abalone.abstract_player import AbstractPlayer
from abalone.enums import Direction, Player, Space
from abalone.game import Game
from abalone.run_game import run_game


class TestRunGame(unittest.TestCase):
    """Test case for `abalone.run_game`."""

    class _TestRunGamePlayerBlack(AbstractPlayer):
        moves = [
            (Space.A5, Direction.NORTH_WEST),
            (Space.B5, Direction.NORTH_WEST),
            (Space.C5, Direction.NORTH_WEST),
            (Space.D5, Direction.NORTH_WEST),
            (Space.E5, Direction.NORTH_WEST),
            (Space.F5, Direction.NORTH_WEST),
            ((Space.H5, Space.G5), Direction.SOUTH_WEST),
            (Space.F4, Direction.NORTH_WEST),
            (Space.I5, Direction.SOUTH_EAST),
            (Space.G4, Direction.NORTH_EAST),
            ((Space.H4, Space.H5), Direction.SOUTH_EAST),
            (Space.G5, Direction.WEST),
            (Space.C4, Direction.SOUTH_EAST)
        ]

        def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]]) \
                -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:
            return self.moves[len(moves_history) // 2]

    class _TestRunGamePlayerWhite(AbstractPlayer):
        moves = [
            (Space.G5, Direction.WEST),
            (Space.G4, Direction.WEST),
            ((Space.G7, Space.H8), Direction.SOUTH_EAST),
            ((Space.F7, Space.H9), Direction.SOUTH_EAST),
            ((Space.E7, Space.G9), Direction.SOUTH_EAST),
            ((Space.D7, Space.F9), Direction.SOUTH_EAST),
            (Space.E9, Direction.SOUTH_WEST),
            (Space.D8, Direction.SOUTH_WEST),
            ((Space.A5, Space.C7), Direction.NORTH_WEST),
            (Space.D7, Direction.SOUTH_WEST),
            (Space.I9, Direction.WEST),
            (Space.I8, Direction.WEST)
        ]

        def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]]) \
                -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:
            return self.moves[len(moves_history) // 2]

    class _TestRunGameIllegalMoveExceptionPlayer(AbstractPlayer):
        def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]]) \
                -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:
            return Space.E1, Direction.EAST

    class _TestRunGameExceptionPlayer(AbstractPlayer):
        def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]]) \
                -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:
            raise Exception()

    def test_run_game(self):
        """Test `abalone.run_game.run_game`"""
        final_state = list(run_game(self._TestRunGamePlayerBlack(), self._TestRunGamePlayerWhite()))[-1]
        self.assertTupleEqual(final_state[0].get_score(), (11, 8))
        self.assertEqual(final_state[0].turn, Player.WHITE)
        self.assertEqual(len(final_state[1]), 25)
        self.assertTupleEqual(final_state[1][-1], (Space.C4, Direction.SOUTH_EAST))

        # should not raise exceptions
        states = list(run_game(self._TestRunGameIllegalMoveExceptionPlayer(), self._TestRunGamePlayerWhite()))
        self.assertEqual(len(states), 1)
        states = list(run_game(self._TestRunGameExceptionPlayer(), self._TestRunGamePlayerWhite()))
        self.assertEqual(len(states), 1)


if __name__ == '__main__':
    unittest.main()
