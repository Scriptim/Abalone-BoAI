#!/usr/bin/env python
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

"""This module runs a `abalone.game.Game`."""

from traceback import format_exc
from typing import Generator, List, Tuple, Union

from abstract_player import AbstractPlayer
from enums import Direction, Player, Space
from game import Game, IllegalMoveException
from utils import line_from_to


def _get_winner(score: Tuple[int, int]) -> Union[Player, None]:
    """Returns the winner of the game based on the current score.

    Args:
        score: The score tuple returned by `abalone.game.Game.get_score`

    Returns:
        Either the `abalone.enums.Player` who won the game or `None` if no one has won yet.
    """
    if 8 in score:
        return Player.WHITE if score[0] == 8 else Player.BLACK
    else:
        return None


def _format_move(turn: Player, move: Tuple[Union[Space, Tuple[Space, Space]], Direction], moves: int) -> str:
    """Formats a player's move as a string with a single line.

    Args:
        turn: The `Player` who performs the move
        move: The move as returned by `abalone.abstract_player.AbstractPlayer.turn`
        moves: The number of total moves made so far (not including this move)
    """
    marbles = [move[0]] if isinstance(move[0], Space) else line_from_to(*move[0])[0]
    marbles = map(lambda space: space.name, marbles)
    return f'{moves + 1}: {turn.name} moves {", ".join(marbles)} in direction {move[1].name}'


def run_game(black: AbstractPlayer, white: AbstractPlayer, **kwargs) \
        -> Generator[Tuple[Game, List[Tuple[Union[Space, Tuple[Space, Space]], Direction]]], None, None]:
    """Runs a game instance and prints the progress / current state at every turn.

    Args:
        black: An `abalone.abstract_player.AbstractPlayer`
        white: An `abalone.abstract_player.AbstractPlayer`
        **kwargs: These arguments are passed to `abalone.game.Game.__init__`

    Yields:
        A tuple of the current `abalone.game.Game` instance and the move history at the start of the game and after\
        every legal turn.
    """
    game = Game()
    moves_history = []
    yield game, moves_history

    while True:
        score = game.get_score()
        score_str = f'BLACK {score[0]} - WHITE {score[1]}'
        print(score_str, game, '', sep='\n')

        winner = _get_winner(score)
        if winner is not None:
            print(f'{winner.name} won!')
            break

        try:
            move = black.turn(game, moves_history) if game.turn is Player.BLACK else white.turn(game, moves_history)
            print(_format_move(game.turn, move, len(moves_history)), end='\n\n')

            game.move(*move)
            game.switch_player()
            moves_history.append(move)

            yield game, moves_history
        except IllegalMoveException as ex:
            print(f'{game.turn.name}\'s tried to perform an illegal move ({ex})\n')
            break
        except:
            print(f'{game.turn.name}\'s move caused an exception\n')
            print(format_exc())
            break


if __name__ == '__main__':  # pragma: no cover
    """Run a game from the command line with default configuration."""
    import importlib
    import sys

    if len(sys.argv) != 3:
        sys.exit(1)
    black = sys.argv[1].rsplit('.', 1)
    black = getattr(importlib.import_module(black[0]), black[1])
    white = sys.argv[2].rsplit('.', 1)
    white = getattr(importlib.import_module(white[0]), white[1])
    list(run_game(black(), white()))
