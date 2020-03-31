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
from typing import List, Tuple

from abalone.enums import Direction, Marble, Player, Space
from abalone.game import Game, IllegalMoveException


class TestGame(unittest.TestCase):
    """Test case for `abalone.game.Game`."""

    def test_switch_player(self):
        """Test `abalone.game.Game.switch_player`"""
        game = Game()
        game.switch_player()
        self.assertIs(game.turn, Player.WHITE)
        game.switch_player()
        self.assertIs(game.turn, Player.BLACK)

    def test_get_marble(self):
        """Test `abalone.game.Game.get_marble`"""
        game = Game()
        self.assertIs(game.get_marble(Space.A1), Marble.BLACK)
        self.assertIs(game.get_marble(Space.E1), Marble.BLANK)
        self.assertIs(game.get_marble(Space.I5), Marble.WHITE)
        self.assertRaises(Exception, lambda: game.get_marble(Space.OFF))

    def test_set_marble(self):
        """Test `abalone.game.Game.set_marble`"""
        game = Game()
        game.set_marble(Space.A1, Marble.BLACK)
        self.assertIs(game.get_marble(Space.A1), Marble.BLACK)
        game.set_marble(Space.A1, Marble.WHITE)
        self.assertIs(game.get_marble(Space.A1), Marble.WHITE)
        game.set_marble(Space.A1, Marble.BLANK)
        self.assertIs(game.get_marble(Space.A1), Marble.BLANK)
        self.assertRaises(Exception, lambda: game.set_marble(Space.OFF, Marble.BLANK))

    def test_get_score(self):
        """Test `abalone.game.Game.get_score`"""
        game = Game()
        self.assertTupleEqual(game.get_score(), (14, 14))
        game.set_marble(Space.A1, Marble.BLANK)
        self.assertTupleEqual(game.get_score(), (13, 14))

    def test_move(self):
        """Test `abalone.game.Game.move` including `abalone.game.Game.move_inline` and\
        `abalone.game.Game.move_broadside`"""

        game = Game()

        def assert_states(states: List[Tuple[Space, Marble]]) -> None:
            for space, marble in states:
                self.assertIs(game.get_marble(space), marble)

        # inline
        game.move(Space.B1, Direction.NORTH_EAST)
        assert_states([(Space.B1, Marble.BLANK), (Space.C2, Marble.BLACK)])
        game.move(Space.B2, Direction.NORTH_WEST)
        assert_states([(Space.D2, Marble.BLACK), (Space.C2, Marble.BLACK), (Space.B2, Marble.BLANK)])
        game.move(Space.A2, Direction.NORTH_EAST)
        assert_states([(Space.D5, Marble.BLACK), (Space.C4, Marble.BLACK), (Space.B3, Marble.BLACK),
                       (Space.A2, Marble.BLANK)])
        # "Only own marbles may be moved"
        self.assertRaises(IllegalMoveException, lambda: game.move(Space.G5, Direction.SOUTH_EAST))
        # "Only lines of up to three marbles may be moved"
        self.assertRaises(IllegalMoveException, lambda: game.move(Space.C2, Direction.EAST))
        # "Own marbles must not be moved off the board"
        self.assertRaises(IllegalMoveException, lambda: game.move(Space.B6, Direction.SOUTH_WEST))

        # sumito
        game.set_marble(Space.C7, Marble.WHITE)
        game.move(Space.A5, Direction.NORTH_EAST)
        assert_states([(Space.D8, Marble.WHITE), (Space.C7, Marble.BLACK), (Space.B6, Marble.BLACK),
                       (Space.A5, Marble.BLANK)])
        game.set_marble(Space.A5, Marble.WHITE)
        game.move(Space.C7, Direction.SOUTH_WEST)
        assert_states([(Space.A5, Marble.BLACK), (Space.B6, Marble.BLACK), (Space.C7, Marble.BLANK)])
        game.set_marble(Space.C1, Marble.WHITE)
        game.move(Space.C4, Direction.WEST)
        assert_states([(Space.C1, Marble.BLACK), (Space.C2, Marble.BLACK), (Space.C3, Marble.BLACK),
                       (Space.C4, Marble.BLANK)])
        game.set_marble(Space.A1, Marble.WHITE)
        game.set_marble(Space.A2, Marble.WHITE)
        game.move(Space.A5, Direction.WEST)
        assert_states([(Space.A1, Marble.WHITE), (Space.A2, Marble.BLACK), (Space.A3, Marble.BLACK),
                       (Space.A4, Marble.BLACK), (Space.A5, Marble.BLANK)])
        game.set_marble(Space.C4, Marble.WHITE)
        # "Marbles must be pushed to an empty space or off the board"
        self.assertRaises(IllegalMoveException, lambda: game.move(Space.C1, Direction.EAST))
        # "Only lines that are shorter than the player's line can be pushed"
        self.assertRaises(IllegalMoveException, lambda: game.move(Space.A2, Direction.WEST))
        game.set_marble(Space.B1, Marble.WHITE)
        # "Only lines that are shorter than the player's line can be pushed"
        self.assertRaises(IllegalMoveException, lambda: game.move(Space.C1, Direction.SOUTH_EAST))

        # broadside
        game.move((Space.C1, Space.D2), Direction.NORTH_WEST)
        assert_states([(Space.D1, Marble.BLACK), (Space.E2, Marble.BLACK), (Space.C1, Marble.BLANK),
                       (Space.D2, Marble.BLANK)])
        # "Elements of boundaries must not be `Space.OFF`"
        self.assertRaises(IllegalMoveException, lambda: game.move((Space.OFF, Space.E2), Direction.EAST))
        self.assertRaises(IllegalMoveException, lambda: game.move((Space.E2, Space.OFF), Direction.EAST))
        # "Only two or three neighboring marbles may be moved with a broadside move"
        game.set_marble(Space.C4, Marble.BLACK)
        game.set_marble(Space.D5, Marble.BLANK)
        self.assertRaises(IllegalMoveException, lambda: game.move((Space.E2, Space.E2), Direction.EAST))
        self.assertRaises(IllegalMoveException, lambda: game.move((Space.C2, Space.C5), Direction.NORTH_EAST))
        # "The direction of a broadside move must be sideways"
        self.assertRaises(IllegalMoveException, lambda: game.move((Space.D1, Space.E2), Direction.NORTH_EAST))
        # "Only own marbles may be moved"
        self.assertRaises(IllegalMoveException, lambda: game.move((Space.G5, Space.G7), Direction.NORTH_EAST))
        self.assertRaises(IllegalMoveException, lambda: game.move((Space.C1, Space.F3), Direction.NORTH_WEST))
        # "With a broadside move, marbles can only be moved to empty spaces"
        self.assertRaises(IllegalMoveException, lambda: game.move((Space.A2, Space.A4), Direction.NORTH_EAST))
        self.assertRaises(IllegalMoveException, lambda: game.move((Space.A2, Space.A4), Direction.SOUTH_EAST))
        self.assertRaises(IllegalMoveException, lambda: game.move((Space.C2, Space.C3), Direction.SOUTH_WEST))

    def test_generate_legal_moves(self):
        """Test `abalone.game.Game.generate_legal_moves` including\
        `abalone.game.Game.generate_own_marble_lines`"""

        game = Game()
        legal_moves = list(game.generate_legal_moves())

        self.assertIn((Space.A1, Direction.NORTH_EAST), legal_moves)
        self.assertIn((Space.A1, Direction.NORTH_WEST), legal_moves)
        self.assertIn(((Space.B1, Space.B2), Direction.NORTH_WEST), legal_moves)
        self.assertNotIn((Space.A1, Direction.SOUTH_EAST), legal_moves)
        self.assertNotIn((Space.B1, Direction.SOUTH_EAST), legal_moves)
        self.assertNotIn((Space.C1, Direction.SOUTH_EAST), legal_moves)
        self.assertNotIn((Space.D1, Direction.EAST), legal_moves)
        self.assertNotIn((Space.I5, Direction.SOUTH_WEST), legal_moves)
        self.assertNotIn(((Space.C3, Space.C5), Direction.SOUTH_EAST), legal_moves)

        game.switch_player()
        legal_moves = list(game.generate_legal_moves())

        self.assertIn((Space.G5, Direction.EAST), legal_moves)
        self.assertIn((Space.I9, Direction.SOUTH_EAST), legal_moves)
        self.assertIn(((Space.G5, Space.G7), Direction.SOUTH_WEST), legal_moves)
        self.assertNotIn((Space.I5, Direction.NORTH_EAST), legal_moves)
        self.assertNotIn(((Space.C3, Space.C5), Direction.NORTH_WEST), legal_moves)


if __name__ == '__main__':
    unittest.main()
