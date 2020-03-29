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

"""This module is an abstraction of a player. Every artificial intelligence should inherit from this class."""

from abc import ABC, abstractmethod
from typing import List, Tuple, Union

from enums import Direction, Space
from game import Game


class AbstractPlayer(ABC):

    @abstractmethod
    def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]]) \
            -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:
        """This method is called from the outside to prompt this player to make a move.

        Args:
            game: The current state of the `abalone.game.Game`
            moves_history: A chronologically sorted list of all past moves, starting with the earliest. It also\
                contains the opponent's moves. The elements correspond to the return values of the\
                `abalone.abstract_player.AbstractPlayer.turn` method.

        Returns:
            The next move of this player according to the parameters of `abalone.game.Game.move`.
        """
