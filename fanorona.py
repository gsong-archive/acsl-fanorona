#!/usr/bin/env python

from functools import wraps
from itertools import (
    chain, combinations, izip, izip_longest, product, repeat, starmap
)
from operator import add, sub


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def valid_piece(for_location=False):
    def decorator(func):
        @wraps(func)
        def wrapped(obj, pos):
            _pos = pos
            if for_location:
                _pos = obj.position_for(pos)
            if obj.validate_piece_existence and \
                    not _pos in (obj.white_pieces | obj.black_pieces):
                raise ValueError(
                    'There is no piece at {}'.format(obj.location_for(_pos))
                )
            return func(obj, pos)
        return wrapped
    return decorator


def not_subset(all_sets):
    def filter_func(fset):
        is_not_subset = True
        for fs in [x for x in all_sets if x is not fset]:
            if fset & fs == fset:
                is_not_subset = False
                break
        return is_not_subset
    return filter_func


def position_to_location(board):
    def map_func(pset):
        return frozenset(map(board.location_for, pset))
    return map_func


class Board(object):
    WHITE = 'white'
    BLACK = 'black'

    def __init__(self, size=5):
        self.size = size
        self.white_pieces = set()
        self.black_pieces = set()
        self.validate_piece_existence = True

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

    def position_for(self, location):
        return self.board[location - 1]

    def location_for(self, position):
        return self.board.index(position) + 1

    def frozenset(self, iterable):
        return frozenset(iterable) & set(self.board)

    def possible_axis_elements(
        self, seed, func, outer_start, inner_start, modifier
    ):
        """
        Gives the coordinate points along the same axis for pieces that can
        potentially be captured.

        seed: the coordinate point (x or y) of the piece we're interested in
        func: `operator.add` or `operator.sub`, depending on if we're
                interested in moving up or down, left or right along the axis.
                Up and right are `add`, down and left are `sub`.
        outer_start, inner_start, modifier: Shenanigan numbers to be able to
                calculate the coordinate ponts properly, either `3, 2, 1` or
                `2, 1, 2` depending on the direction you're moving.

        For example, to calculate what could be captured by moving a piece up:
        ```
        >>> from fanorona import Board
        >>> b = Board()
        >>> from operator import add
        >>> b.possible_axis_elements(3, add, 3, 2, 1)
        [[5], [5, 6], [5, 6, 7]]
        ```

        So if a piece started out at y=3, it can possibly capture pieces on the
        same x-coordinate at y=5, y=[5, 6], or y=[5, 6, 7]. Notice that this
        function makes no attempt to figure out how large the board size is, so
        it's up to you to filter out results that are out of bounds.
        """
        max = self.size - 2
        elements = []
        for i in xrange(outer_start, max + outer_start):
            elements.append(
                map(
                    func,
                    repeat(seed, i - max + modifier),
                    range(inner_start, i)
                )
            )
        return elements

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

        if color.lower() == self.WHITE:
            self.check_collision_with(self.BLACK, positions)
        else:
            self.check_collision_with(self.WHITE, positions)

        pieces = getattr(self, color)
        pieces.clear()
        pieces.update(positions)

    def initialize_white_pieces(self, *nums):
        self.initialize_pieces(self.WHITE, *nums)

    def initialize_black_pieces(self, *nums):
        self.initialize_pieces(self.BLACK, *nums)

    @valid_piece()
    def legal_moves_for(self, position):
        x, y = position
        possibles = set(
            [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        ) & set(self.board)
        return possibles - (self.white_pieces | self.black_pieces)

    @valid_piece()
    def can_move_up_for(self, position):
        x, y = position
        return (x, y + 1) in self.legal_moves_for(position)

    @valid_piece()
    def can_move_down_for(self, position):
        x, y = position
        return (x, y - 1) in self.legal_moves_for(position)

    @valid_piece()
    def can_move_left_for(self, position):
        x, y = position
        return (x - 1, y) in self.legal_moves_for(position)

    @valid_piece()
    def can_move_right_for(self, position):
        x, y = position
        return (x + 1, y) in self.legal_moves_for(position)

    @valid_piece()
    def possible_captures_for(self, position):
        x, y = position
        captures = set()

        if self.can_move_up_for(position):
            # possible top captures
            elements = self.possible_axis_elements(y, add, 3, 2, 1)
            captures = self.add_to_captures(captures, [x], elements)

            # possible bottom captures
            elements = self.possible_axis_elements(y, sub, 2, 1, 2)
            captures = self.add_to_captures(captures, [x], elements)

        if self.can_move_down_for(position):
            # possible top captures
            elements = self.possible_axis_elements(y, add, 2, 1, 2)
            captures = self.add_to_captures(captures, [x], elements)

            # possible bottom captures
            elements = self.possible_axis_elements(y, sub, 3, 2, 1)
            captures = self.add_to_captures(captures, [x], elements)

        if self.can_move_left_for(position):
            # possible right captures
            elements = self.possible_axis_elements(x, add, 2, 1, 2)
            captures = self.add_to_captures(captures, elements, [y])

            # possible left captures
            elements = self.possible_axis_elements(x, sub, 3, 2, 1)
            captures = self.add_to_captures(captures, elements, [y])

        if self.can_move_right_for(position):
            # possible right captures
            elements = self.possible_axis_elements(x, add, 3, 2, 1)
            captures = self.add_to_captures(captures, elements, [y])

            # possible left captures
            elements = self.possible_axis_elements(x, sub, 2, 1, 2)
            captures = self.add_to_captures(captures, elements, [y])

        return captures

    @valid_piece()
    def captures_for(self, position):
        opponent = self.black_pieces
        if position in self.black_pieces:
            opponent = self.white_pieces
        opponent_combos = chain(
            *starmap(
                combinations,
                product([opponent], range(1, len(opponent) + 1))
            )
        )
        opponent_set = set()
        for combo in opponent_combos:
            opponent_set.add(frozenset(combo))
        all = opponent_set & self.possible_captures_for(position)
        return set(filter(not_subset(all), all))

    @valid_piece(for_location=True)
    def captures_for_location(self, location):
        captures = self.captures_for(self.position_for(location))
        return set(map(position_to_location(self), captures))

    def all_captures_for(self, color):
        all_captures = {}
        for piece in getattr(self, color):
            captures = self.captures_for(piece)
            if captures:
                all_captures[piece] = captures
        return all_captures

    @property
    def all_captures_for_white(self):
        return self.all_captures_for(self.WHITE)

    @property
    def all_captures_for_black(self):
        return self.all_captures_for(self.BLACK)

    def all_captures_by_location_for(self, color):
        all_captures_by_position = self.all_captures_for(color)
        all_captures = {}
        for pos, captures in all_captures_by_position.iteritems():
            all_captures[self.location_for(pos)] = set(
                map(position_to_location(self), captures)
            )
        return all_captures

    @property
    def all_captures_by_location_for_white(self):
        return self.all_captures_by_location_for(self.WHITE)

    @property
    def all_captures_by_location_for_black(self):
        return self.all_captures_by_location_for(self.BLACK)
