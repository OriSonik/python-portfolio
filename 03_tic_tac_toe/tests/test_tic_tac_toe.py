import sys
from pathlib import Path

import pytest


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from tic_tac_toe import TicTacToeGame


def test_parse_move_accepts_row_column_format():
    game = TicTacToeGame()

    assert game.parse_move("A1") == 0
    assert game.parse_move("A2") == 1
    assert game.parse_move("A3") == 2
    assert game.parse_move("B1") == 3
    assert game.parse_move("B2") == 4
    assert game.parse_move("B3") == 5
    assert game.parse_move("C1") == 6
    assert game.parse_move("C2") == 7
    assert game.parse_move("C3") == 8


def test_parse_move_accepts_column_row_format():
    game = TicTacToeGame()

    assert game.parse_move("1A") == 0
    assert game.parse_move("2B") == 4
    assert game.parse_move("3C") == 8


def test_parse_move_is_case_insensitive():
    game = TicTacToeGame()

    assert game.parse_move("a1") == 0
    assert game.parse_move("b2") == 4
    assert game.parse_move("c3") == 8


def test_parse_move_returns_quit_for_q():
    game = TicTacToeGame()

    assert game.parse_move("q") == "quit"
    assert game.parse_move("Q") == "quit"


@pytest.mark.parametrize(
    "move",
    ["", "A", "1", "AA", "11", "D1", "A4", "ABC", "7Z"],
)
def test_parse_move_rejects_invalid_input(move):
    game = TicTacToeGame()

    assert game.parse_move(move) is None


def test_make_move_places_marker_on_empty_field():
    game = TicTacToeGame()

    result = game.make_move(0, "X")

    assert result is True
    assert game.board[0] == "X"


def test_make_move_rejects_taken_field():
    game = TicTacToeGame()

    game.make_move(0, "X")
    result = game.make_move(0, "O")

    assert result is False
    assert game.board[0] == "X"


def test_available_moves_excludes_taken_fields():
    game = TicTacToeGame()

    game.make_move(0, "X")
    game.make_move(4, "O")

    assert 0 not in game.available_moves()
    assert 4 not in game.available_moves()
    assert len(game.available_moves()) == 7


@pytest.mark.parametrize("marker", ["X", "O"])
@pytest.mark.parametrize("win_line", TicTacToeGame.WIN_LINES)
def test_check_winner_detects_all_win_lines_for_both_markers(marker, win_line):
    game = TicTacToeGame()
    game.board = [" " for _ in range(9)]

    for index in win_line:
        game.board[index] = marker

    assert game.check_winner() == marker


def test_check_winner_returns_none_without_winner():
    game = TicTacToeGame()
    game.board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]

    assert game.check_winner() is None


def test_is_draw_returns_true_when_board_is_full_without_winner():
    game = TicTacToeGame()
    game.board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]

    assert game.is_draw() is True


def test_is_draw_returns_false_when_winner_exists():
    game = TicTacToeGame()
    game.board = ["X", "X", "X", "O", "O", " ", " ", " ", " "]

    assert game.is_draw() is False


def test_find_tactical_move_finds_winning_move():
    game = TicTacToeGame()
    game.board = ["X", "X", " ", "O", " ", " ", " ", " ", "O"]

    assert game.find_tactical_move("X") == 2


def test_smart_ai_takes_winning_move():
    game = TicTacToeGame()
    game.board = ["O", "O", " ", "X", " ", "X", " ", " ", " "]

    assert game.get_smart_ai_move(ai_marker="O", opponent_marker="X") == 2


def test_smart_ai_blocks_opponent_winning_move():
    game = TicTacToeGame()
    game.board = ["X", "X", " ", "O", " ", " ", " ", " ", " "]

    assert game.get_smart_ai_move(ai_marker="O", opponent_marker="X") == 2


def test_smart_ai_takes_center_when_no_tactical_move_exists():
    game = TicTacToeGame()

    assert game.get_smart_ai_move(ai_marker="O", opponent_marker="X") == 4