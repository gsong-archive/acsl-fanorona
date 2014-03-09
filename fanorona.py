#!/usr/bin/env python

from itertools import chain, cycle, izip, izip_longest, product, repeat
from operator import add, sub


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def valid_piece(func):
    def wrapped(obj, pos):
        if (not obj.disable_validation) and \
                (not pos in (obj.white_pieces | obj.black_pieces)):
            raise ValueError(
                'There is no piece at {}'.format(obj.location_for(pos))
            )
        return func(obj, pos)

    return wrapped


class Board(object):
    def __init__(self, size=5):
        self.size = size
        self.white_pieces = set()
        self.black_pieces = set()
        self.disable_validation = False

    @property
    def board(self):
        x = range(self.size) * self.size
        y = chain(
            *izip(
                *grouper(range(self.size - 1, -1, -1) * self.size, self.size)
            )
        )
        return zip(x, y)

    @property
    def white(self):
        return self.white_pieces

    @property
    def black(self):
        return self.black_pieces

    def position_for(self, num):
        return self.board[num - 1]

    def location_for(self, position):
        return self.board.index(position) + 1

    def frozenset(self, iterable):
        return frozenset(iterable) & set(self.board)

    def add_to_captures(self, captures, x, y):
        x, y = list(x), list(y)
        if len(x) > len(y):
            for e in x:
                captures.add(self.frozenset(product(e, y)))
        else:
            for e in y:
                captures.add(self.frozenset(product(x, e)))
        captures = filter(None, captures)
        return set(captures)

    def check_collision_with(self, color, positions):
        color = getattr(self, color)
        if color & set(positions):
            raise ValueError('Cannot place two pieces on the same position')

    def initialize_pieces(self, color, *nums):
        positions = []
        for num in nums:
            positions.append(self.position_for(num))

        if color.lower() == 'white':
            self.check_collision_with('black', positions)
        else:
            self.check_collision_with('white', positions)

        pieces = getattr(self, color)
        pieces.clear()
        pieces.update(positions)

    def initialize_white_pieces(self, *nums):
        self.initialize_pieces('white', *nums)

    def initialize_black_pieces(self, *nums):
        self.initialize_pieces('black', *nums)

    @valid_piece
    def legal_moves_for(self, position):
        x, y = position
        possibles = set(
            [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        ) & set(self.board)
        return possibles - (self.white_pieces | self.black_pieces)

    @valid_piece
    def can_move_up_for(self, position):
        x, y = position
        return (x, y + 1) in self.legal_moves_for(position)

    @valid_piece
    def can_move_down_for(self, position):
        x, y = position
        return (x, y - 1) in self.legal_moves_for(position)

    @valid_piece
    def can_move_left_for(self, position):
        x, y = position
        return (x - 1, y) in self.legal_moves_for(position)

    @valid_piece
    def can_move_right_for(self, position):
        x, y = position
        return (x + 1, y) in self.legal_moves_for(position)

    @valid_piece
    def possible_captures_for(self, position):
        x, y = position
        max = self.size - 2

        captures = set()
        if self.can_move_up_for(position):
            # possible top captures
            y_list = []
            for i in xrange(3, max + 3):
                y_list.append(map(add, repeat(y, i - max + 1), range(2, i)))
            captures = self.add_to_captures(captures, [x], y_list)

            # possible bottom captures
            y_list = []
            for i in xrange(2, max + 2):
                y_list.append(map(sub, repeat(y, i - max + 2), range(1, i)))
            captures = self.add_to_captures(captures, [x], y_list)

#         if self.can_move_down_for(position):
#             # possible top captures
#             captures = self.add_to_captures(
#                 captures, xrange(2, max + 2), cycle([x]),
#                 map(add, repeat(y, i - max + 2), range(1, i))
#             )
# 
#             # possible bottom captures
#             captures = self.add_to_captures(
#                 captures, xrange(3, max + 3), cycle([x]),
#                 map(sub, repeat(y, i - max + 1), range(2, i))
#             )
# 
#         if self.can_move_left_for(position):
#             # possible left captures
#             for i in xrange(3, max + 3):
#                 captures.add(
#                     self.frozenset(
#                         zip(
#                             map(sub, repeat(x, i - max + 1), range(2, i)),
#                             cycle([y])
#                         )
#                     )
#                 )
# 
#             # possible right captures
#             for i in xrange(2, max + 2):
#                 captures.add(
#                     self.frozenset(
#                         zip(
#                             map(add, repeat(x, i - max + 2), range(1, i)),
#                             cycle([y])
#                         )
#                     )
#                 )
# 
#         captures = set(filter(None, captures))
        import pdb
        pdb.set_trace()
