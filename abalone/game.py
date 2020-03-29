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

"""This module serves the representation of game states and the performing of game moves."""

from copy import deepcopy
from typing import Generator, List, Tuple, Union

import colorama
from colorama import Style

from enums import Direction, InitialPosition, Marble, Player, Space
from utils import line_from_to, line_to_edge, neighbor

colorama.init(autoreset=True)


def _space_to_board_indices(space: Space) -> Tuple[int, int]:
    """Returns the corresponding index for `self.board` of a given `abalone.enums.Space`.

    Args:
        space: The `abalone.enums.Space` for which the indices are wanted.

    Returns:
        An int tuple containing two indices for `self.board`.
    """

    xs = ['I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
    ys = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    x = xs.index(space.value[0])
    y = ys.index(space.value[1])

    # offset because lines 'F' to 'I' don't start with '1'
    if x <= 3:
        y -= 4 - x

    return x, y


def _marble_of_player(player: Player) -> Marble:
    """Returns the corresponding `abalone.enums.Marble` for a given `abalone.enums.Player`.

    Args:
        player: The `abalone.enums.Player` whose `abalone.enums.Marble` is wanted.

    Returns:
        The `abalone.enums.Marble` which belongs to `player`.
    """

    return Marble.WHITE if player is Player.WHITE else Marble.BLACK


class Game:
    """Represents the mutable state of an Abalone game."""

    def __init__(self, initial_position: InitialPosition = InitialPosition.DEFAULT, first_turn: Player = Player.BLACK):
        self.board = deepcopy(initial_position.value)
        self.turn = first_turn

    def __str__(self) -> str:  # pragma: no cover
        board_lines = list(map(lambda line: ' '.join(map(str, line)), self.board))
        string = ''
        string += Style.DIM + '    I ' + Style.NORMAL + board_lines[0] + '\n'
        string += Style.DIM + '   H ' + Style.NORMAL + board_lines[1] + '\n'
        string += Style.DIM + '  G ' + Style.NORMAL + board_lines[2] + '\n'
        string += Style.DIM + ' F ' + Style.NORMAL + board_lines[3] + '\n'
        string += Style.DIM + 'E ' + Style.NORMAL + board_lines[4] + '\n'
        string += Style.DIM + ' D ' + Style.NORMAL + board_lines[5] + Style.DIM + ' 9\n' + Style.NORMAL
        string += Style.DIM + '  C ' + Style.NORMAL + board_lines[6] + Style.DIM + ' 8\n' + Style.NORMAL
        string += Style.DIM + '   B ' + Style.NORMAL + board_lines[7] + Style.DIM + ' 7\n' + Style.NORMAL
        string += Style.DIM + '    A ' + Style.NORMAL + board_lines[8] + Style.DIM + ' 6\n' + Style.NORMAL
        string += Style.DIM + '       1 2 3 4 5' + Style.NORMAL
        return string

    def not_in_turn_player(self) -> Player:
        """Gets the `abalone.enums.Player` who is currently *not* in turn. Returns `abalone.enums.Player.WHITE` when\
        `abalone.enums.Player.BLACK` is in turn and vice versa. This player is commonly referred to as "opponent" in\
        other places.

        Returns:
            The `abalone.enums.Player` not in turn.
        """

        return Player.BLACK if self.turn is Player.WHITE else Player.WHITE

    def switch_player(self) -> None:
        """Switches the player whose turn it is."""
        self.turn = self.not_in_turn_player()

    def set_marble(self, space: Space, marble: Marble) -> None:
        """Updates the state of a `abalone.enums.Space` on the board.

        Args:
            space: The `abalone.enums.Space` to be updated.
            marble: The new state of `space` of type `abalone.enums.Marble`

        Raises:
            Exception: Cannot set state of `abalone.enums.Space.OFF`
        """

        if space is Space.OFF:
            raise Exception('Cannot set state of `Space.OFF`')

        x, y = _space_to_board_indices(space)
        self.board[x][y] = marble

    def get_marble(self, space: Space) -> Marble:
        """Returns the state of a `abalone.enums.Space`.

        Args:
            space: The `abalone.enums.Space` of which the state is to be returned.

        Returns:
            A `abalone.enums.Marble` representing the current state of `space`.

        Raises:
            Exception: Cannot get state of `abalone.enums.Space.OFF`
        """

        if space is Space.OFF:
            raise Exception('Cannot get state of `Space.OFF`')

        x, y = _space_to_board_indices(space)

        return self.board[x][y]

    def get_score(self) -> Tuple[int, int]:
        """Counts how many marbles the players still have on the board.

        Returns:
            A tuple with the number of marbles of black and white, in that order.
        """
        black = 0
        white = 0
        for row in self.board:
            for space in row:
                if space is Marble.BLACK:
                    black += 1
                elif space is Marble.WHITE:
                    white += 1
        return black, white

    def _inline_marbles_nums(self, line: List[Space]) -> Tuple[int, int]:
        """Counts the number of own and enemy marbles that are in the given line. First the directly adjacent marbles\
        of the player whose turn it is are counted and then the subsequent directly adjacent marbles of the opponent.\
        Therefore only the marbles that are relevant for an inline move are counted. This method serves as an\
        helper method for `abalone.game.Game.move_inline`.

        Args:
            line: A list of `abalone.enums.Space`s that are in a straight line.

        Returns:
            A tuple with the number of 1. own marbles and 2. opponent marbles, according to the counting method\
            described above.
        """
        own_marbles_num = 0
        while own_marbles_num < len(line) and self.get_marble(line[own_marbles_num]) is _marble_of_player(self.turn):
            own_marbles_num += 1
        opp_marbles_num = 0
        while opp_marbles_num + own_marbles_num < len(line) and self.get_marble(
                line[opp_marbles_num + own_marbles_num]) is _marble_of_player(self.not_in_turn_player()):
            opp_marbles_num += 1
        return own_marbles_num, opp_marbles_num

    def move_inline(self, caboose: Space, direction: Direction) -> None:
        """Performs an inline move. An inline move is denoted by the trailing marble ("caboose") of a straight line of\
        marbles. Marbles of the opponent can only be pushed with an inline move (as opposed to a broadside move). This\
        is possible if the opponent's marbles are directly in front of the line of the player's own marbles, and only\
        if the opponent's marbles are outnumbered ("sumito") and are moved to an empty space or off the board.

        Args:
            caboose: The `abalone.enums.Space` of the trailing marble of a straight line of up to three marbles.
            direction: The `abalone.enums.Direction` of movement.

        Raises:
            IllegalMoveException: Only own marbles may be moved
            IllegalMoveException: Only lines of up to three marbles may be moved
            IllegalMoveException: Own marbles must not be moved off the board
            IllegalMoveException: Only lines that are shorter than the player's line can be pushed
            IllegalMoveException: Marbles must be pushed to an empty space or off the board
        """

        if self.get_marble(caboose) is not _marble_of_player(self.turn):
            raise IllegalMoveException('Only own marbles may be moved')

        line = line_to_edge(caboose, direction)
        own_marbles_num, opp_marbles_num = self._inline_marbles_nums(line)

        if own_marbles_num > 3:
            raise IllegalMoveException('Only lines of up to three marbles may be moved')

        if own_marbles_num == len(line):
            raise IllegalMoveException('Own marbles must not be moved off the board')

        # sumito
        if opp_marbles_num > 0:
            if opp_marbles_num >= own_marbles_num:
                raise IllegalMoveException('Only lines that are shorter than the player\'s line can be pushed')
            push_to = neighbor(line[own_marbles_num + opp_marbles_num - 1], direction)
            if push_to is not Space.OFF:
                if self.get_marble(push_to) is _marble_of_player(self.turn):
                    raise IllegalMoveException('Marbles must be pushed to an empty space or off the board')
                self.set_marble(push_to, _marble_of_player(self.not_in_turn_player()))

        self.set_marble(line[own_marbles_num], _marble_of_player(self.turn))
        self.set_marble(caboose, Marble.BLANK)

    def move_broadside(self, boundaries: Tuple[Space, Space], direction: Direction) -> None:
        """Performs a broadside move. With a broadside move a line of adjacent marbles is moved sideways into empty\
        spaces. However, it is not possible to push the opponent's marbles. A broadside move is denoted by the two\
        outermost `abalone.enums.Space`s of the line to be moved and the `abalone.enums.Direction` of movement. With a\
        broadside move two or three marbles can be moved, i.e. the two boundary marbles are either direct neighbors or\
        there is exactly one marble in between.

        Args:
            boundaries: A tuple of the two outermost `abalone.enums.Space`s of a line of two or three marbles.
            direction: The `abalone.enums.Direction` of movement.

        Raises:
            IllegalMoveException: Elements of boundaries must not be `abalone.enums.Space.OFF`
            IllegalMoveException: Only two or three neighboring marbles may be moved with a broadside move
            IllegalMoveException: The direction of a broadside move must be sideways
            IllegalMoveException: Only own marbles may be moved
            IllegalMoveException: With a broadside move, marbles can only be moved to empty spaces
        """
        if boundaries[0] is Space.OFF or boundaries[1] is Space.OFF:
            raise IllegalMoveException('Elements of boundaries must not be `Space.OFF`')
        marbles, direction1 = line_from_to(boundaries[0], boundaries[1])
        if marbles is None or not (len(marbles) == 2 or len(marbles) == 3):
            raise IllegalMoveException('Only two or three neighboring marbles may be moved with a broadside move')
        _, direction2 = line_from_to(boundaries[1], boundaries[0])
        if direction is direction1 or direction is direction2:
            raise IllegalMoveException('The direction of a broadside move must be sideways')
        for marble in marbles:
            if self.get_marble(marble) is not _marble_of_player(self.turn):
                raise IllegalMoveException('Only own marbles may be moved')
            destination_space = neighbor(marble, direction)
            if destination_space is Space.OFF or self.get_marble(destination_space) is not Marble.BLANK:
                raise IllegalMoveException('With a broadside move, marbles can only be moved to empty spaces')
        for marble in marbles:
            self.set_marble(marble, Marble.BLANK)
            self.set_marble(neighbor(marble, direction), _marble_of_player(self.turn))

    def move(self, marbles: Union[Space, Tuple[Space, Space]], direction: Direction) -> None:
        """Performs either an inline or a broadside move, depending on the arguments passed, by calling the according\
        method (`abalone.game.Game.move_inline` or `abalone.game.Game.move_broadside`).

        Args:
            marbles: The `abalone.enums.Space`s with the marbles to be moved. Either a single space for an inline move\
                or a tuple of two spaces for a broadside move, in accordance with the parameters of\
                `abalone.game.Game.move_inline` resp. `abalone.game.Game.move_broadside`.
            direction: The `abalone.enums.Direction` of movement.

        Raises:
            Exception: Invalid arguments
        """
        if isinstance(marbles, Space):
            self.move_inline(marbles, direction)
        elif isinstance(marbles, tuple) and isinstance(marbles[0], Space) and isinstance(marbles[1], Space):
            self.move_broadside(marbles, direction)
        else:  # pragma: no cover
            # This exception should only be raised if the arguments are not passed according to the type hints. It is
            # only there to prevent a silent failure in such a case.
            raise Exception('Invalid arguments')

    def generate_own_marble_lines(self) -> Generator[Union[Space, Tuple[Space, Space]], None, None]:
        """Generates all adjacent straight lines with up to three marbles of the player whose turn it is.

        Yields:
            Either one or two `abalone.enums.Space`s according to the first parameter of `abalone.game.Game.move`.
        """
        for space in Space:
            if space is Space.OFF or self.get_marble(space) is not _marble_of_player(self.turn):
                continue
            yield space
            for direction in [Direction.NORTH_WEST, Direction.NORTH_EAST, Direction.EAST]:
                neighbor1 = neighbor(space, direction)
                if neighbor1 is not Space.OFF and self.get_marble(neighbor1) is _marble_of_player(self.turn):
                    yield space, neighbor1
                    neighbor2 = neighbor(neighbor1, direction)
                    if neighbor2 is not Space.OFF and self.get_marble(neighbor2) is _marble_of_player(self.turn):
                        yield space, neighbor2

    def generate_legal_moves(self) -> Generator[Tuple[Union[Space, Tuple[Space, Space]], Direction], None, None]:
        """Generates all possible moves that the player whose turn it is can perform. The yielded values are intended\
        to be passed as arguments to `abalone.game.Game.move`.

        Yields:
            A tuple of 1. either one or a tuple of two `abalone.enums.Space`s and 2. a `abalone.enums.Direction`
        """
        for marbles in self.generate_own_marble_lines():
            for direction in Direction:
                copy = deepcopy(self)
                try:
                    copy.move(marbles, direction)
                except IllegalMoveException:
                    continue
                yield marbles, direction


class IllegalMoveException(Exception):
    """Exception that is raised if a player tries to perform an illegal move."""
