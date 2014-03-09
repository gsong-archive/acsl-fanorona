import pytest

from fanorona import Board


@pytest.fixture
def board():
    board = Board()
    board.initialize_white_pieces(12, 17, 22)
    board.initialize_black_pieces(9, 14, 10)
    return board


def test_board_init():
    assert len(Board(10).board) == 10 * 10
    assert len(Board(20).board) == 20 * 20


def test_board_position(board):
    assert board.position_for(1) == (0, 4)
    assert board.position_for(13) == (2, 2)
    assert board.position_for(21) == (0, 0)
    assert board.position_for(25) == (4, 0)
    assert board.position_for(5) == (4, 4)


def test_initialize_white_pieces(board):
    assert board.white_pieces == set([(1, 0), (1, 1), (1, 2)])
    board.initialize_white_pieces(22, 12, 17)
    assert board.white_pieces == set([(1, 0), (1, 1), (1, 2)])


def test_initialize_black_pieces(board):
    assert board.black_pieces == set([(3, 3,), (3, 2), (4, 3)])


def test_initialize_collision(board):
    with pytest.raises(ValueError):
        board.initialize_black_pieces(9, 14, 10, 12)


def test_legal_moves(board):
    board.initialize_black_pieces(9, 14, 10, 1, 21, 5, 25, 13)
    assert board.legal_moves_for((0, 0)) == set([(0, 1)])
    assert board.legal_moves_for((0, 4)) == set([(1, 4), (0, 3)])
    assert board.legal_moves_for((2, 2)) == set([(2, 1), (2, 3)])
    assert board.legal_moves_for((4, 0)) == set([(3, 0), (4, 1)])
    assert board.legal_moves_for((4, 4)) == set([(3, 4)])


def test_can_move_up(board):
    board.initialize_black_pieces(9, 14, 10, 5)
    assert board.can_move_up_for((3, 2)) is False
    assert board.can_move_up_for((4, 4)) is False
    assert board.can_move_up_for((1, 2))
    with pytest.raises(ValueError):
        board.can_move_up_for((3, 4))


def test_can_move_down(board):
    assert board.can_move_down_for((1, 0)) is False
    assert board.can_move_down_for((3, 3)) is False
    assert board.can_move_down_for((4, 3))
    with pytest.raises(ValueError):
        board.can_move_down_for((4, 4))


def test_can_move_left(board):
    board.initialize_black_pieces(9, 14, 10, 11)
    assert board.can_move_left_for((4, 3)) is False
    assert board.can_move_left_for((0, 2)) is False
    assert board.can_move_left_for((1, 1))
    with pytest.raises(ValueError):
        board.can_move_left_for((4, 1))


def test_can_move_right(board):
    board.initialize_black_pieces(9, 14, 10, 5)
    assert board.can_move_right_for((3, 3)) is False
    assert board.can_move_right_for((4, 4)) is False
    assert board.can_move_right_for((1, 2))
    with pytest.raises(ValueError):
        board.can_move_right_for((2, 0))


def test_possible_captures_without_validation(board):
    board.disable_validation = True
    assert board.possible_captures_for((0, 0)) == set([
        frozenset([(0, 2), (0, 3), (0, 4)]),
        frozenset([(0, 2), (0, 3)]),
        frozenset([(0, 2)]),
        frozenset([(2, 0), (3, 0), (4, 0)]),
        frozenset([(2, 0), (3, 0)]),
        frozenset([(2, 0)]),
    ])
    assert board.possible_captures_for((4, 4)) == set(
        set([(2, 4), (1, 4), (0, 4)]),
        set([(2, 4), (1, 4)]),
        set([(2, 4)]),
        set([(4, 2), (4, 1), (4, 0)]),
        set([(4, 2), (4, 1)]),
        set([(4, 2)]),
    )
