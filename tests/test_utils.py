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

"""Unit tests for `abalone.utils`"""

import unittest

from abalone.enums import Direction, Space
from abalone.utils import line_from_to, line_to_edge, neighbor


class TestMethods(unittest.TestCase):
    """Test case for global methods in `abalone.utils`."""

    def test_line_from_to(self):
        """Test `abalone.utils.line_from_to`"""
        self.assertTupleEqual(line_from_to(Space.A1, Space.D4),
                              ([Space.A1, Space.B2, Space.C3, Space.D4], Direction.NORTH_EAST))
        self.assertTupleEqual(line_from_to(Space.E6, Space.E9),
                              ([Space.E6, Space.E7, Space.E8, Space.E9], Direction.EAST))
        self.assertTupleEqual(line_from_to(Space.C7, Space.C4),
                              ([Space.C7, Space.C6, Space.C5, Space.C4], Direction.WEST))
        self.assertTupleEqual(line_from_to(Space.D2, Space.E3), ([Space.D2, Space.E3], Direction.NORTH_EAST))
        self.assertEqual(line_from_to(Space.A1, Space.B4), (None, None))
        self.assertEqual(line_from_to(Space.F2, Space.F2), (None, None))
        self.assertRaises(Exception, lambda: line_from_to(Space.OFF, Space.A1))
        self.assertRaises(Exception, lambda: line_from_to(Space.A1, Space.OFF))
        self.assertRaises(Exception, lambda: line_from_to(Space.OFF, Space.OFF))

    def test_line_to_edge(self):
        """Test `abalone.utils.line_to_edge`"""
        self.assertSequenceEqual(line_to_edge(Space.C4, Direction.SOUTH_EAST), [Space.C4, Space.B4, Space.A4])
        self.assertSequenceEqual(line_to_edge(Space.G3, Direction.NORTH_EAST), [Space.G3, Space.H4, Space.I5])
        self.assertSequenceEqual(line_to_edge(Space.E3, Direction.WEST), [Space.E3, Space.E2, Space.E1])
        self.assertSequenceEqual(line_to_edge(Space.A1, Direction.WEST), [Space.A1])
        self.assertRaises(Exception, lambda: line_to_edge(Space.OFF, Direction.EAST))

    def test_neighbor(self):
        """Test `abalone.utils.neighbor`"""
        self.assertIs(neighbor(Space.OFF, Direction.NORTH_EAST), Space.OFF)
        self.assertIs(neighbor(Space.B2, Direction.NORTH_EAST), Space.C3)
        self.assertIs(neighbor(Space.B2, Direction.EAST), Space.B3)
        self.assertIs(neighbor(Space.B2, Direction.SOUTH_EAST), Space.A2)
        self.assertIs(neighbor(Space.B2, Direction.SOUTH_WEST), Space.A1)
        self.assertIs(neighbor(Space.B2, Direction.WEST), Space.B1)
        self.assertIs(neighbor(Space.B2, Direction.NORTH_WEST), Space.C2)
        self.assertIs(neighbor(Space.A1, Direction.NORTH_EAST), Space.B2)
        self.assertIs(neighbor(Space.A1, Direction.SOUTH_EAST), Space.OFF)
        self.assertIs(neighbor(Space.I5, Direction.NORTH_EAST), Space.OFF)
        self.assertIs(neighbor(Space.H4, Direction.NORTH_WEST), Space.OFF)
        self.assertIs(neighbor(Space.G3, Direction.WEST), Space.OFF)
        self.assertIs(neighbor(Space.A5, Direction.EAST), Space.OFF)
        self.assertIs(neighbor(Space.A1, Direction.WEST), Space.OFF)


if __name__ == '__main__':
    unittest.main()
