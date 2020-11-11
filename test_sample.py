# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import pytest
import random
from unittest import mock
from PieceSet import PieceSet
from Pieces import King, Queen, Knight, Bishop, Rook, Pawn, CheckersCoin
from Move import CheckersMove, ChessMove
from PossibleMoves import PossibleMoves
from GameSquare import GameSquare
from Board import Board
from Board import BoardTheme


def test_pieces():
    piece_set_colour1 = "Red"
    piece_set_colour2 = "White"
    piece_set_colour3 = "Black"

    # Test the king
    king1 = King(piece_set_colour1)
    assert king1.get_colour() == piece_set_colour1
    king1.set_colour(piece_set_colour2)
    assert king1.get_colour() == piece_set_colour2

    # Test the queen
    queen1 = Queen(piece_set_colour3)
    assert queen1.get_colour() == piece_set_colour3
    queen1.set_colour(piece_set_colour2)
    assert queen1.get_colour() == piece_set_colour2

    # Test the knight
    knight1 = Knight(piece_set_colour1)
    assert knight1.get_colour() == piece_set_colour1
    knight1.set_colour(piece_set_colour3)
    assert knight1.get_colour() == piece_set_colour3

    # Test the bishop
    bishop1 = Bishop(piece_set_colour1)
    assert bishop1.get_colour() == piece_set_colour1
    bishop1.set_colour(piece_set_colour2)
    assert bishop1.get_colour() == piece_set_colour2

    # Test the rook
    rook1 = Rook(piece_set_colour3)
    assert rook1.get_colour() == piece_set_colour3
    rook1.set_colour(piece_set_colour2)
    assert rook1.get_colour() == piece_set_colour2

    # Test the pawn
    pawn1 = Pawn(piece_set_colour3)
    assert pawn1.get_colour() == piece_set_colour3
    assert not pawn1.get_promotion_status()
    assert not pawn1.get_moved_yet_status()
    assert pawn1.get_promoted_to() is None
    pawn1.set_colour(piece_set_colour2)
    assert pawn1.get_colour() == piece_set_colour2
    pawn1.move()
    assert pawn1.get_moved_yet_status()

    assert pawn1.promote("Knight")
    assert pawn1.get_promotion_status()
    assert isinstance(pawn1.get_promoted_to(), Knight)
    assert not pawn1.promote("Queen")

    pawn2 = Pawn(piece_set_colour1)
    assert pawn2.get_colour() == piece_set_colour1
    assert not pawn2.get_promotion_status()
    assert pawn2.promote("Queen")
    assert pawn2.get_promotion_status()
    assert isinstance(pawn2.get_promoted_to(), Queen)

    pawn3 = Pawn(piece_set_colour2)
    assert pawn3.get_colour() == piece_set_colour2
    assert not pawn3.get_promotion_status()
    assert pawn3.promote("Bishop")
    assert pawn3.get_promotion_status()
    assert isinstance(pawn3.get_promoted_to(), Bishop)

    pawn4 = Pawn(piece_set_colour2)
    assert not pawn4.promote("King")
    assert pawn4.get_colour() == piece_set_colour2
    assert not pawn4.get_promotion_status()
    assert pawn4.promote("Rook")
    assert pawn4.get_promotion_status()
    assert isinstance(pawn4.get_promoted_to(), Rook)

    # Test the checkers coin
    checkers_coin1 = CheckersCoin(piece_set_colour3)
    assert checkers_coin1.get_colour() == piece_set_colour3
    assert not checkers_coin1.get_promotion_status()
    checkers_coin1.promote()
    assert checkers_coin1.get_promotion_status()
    checkers_coin1.set_colour(piece_set_colour1)
    assert checkers_coin1.get_colour() == piece_set_colour1


def test_piece_set():
    piece_set_colour = "White"
    piece_set1 = PieceSet("Checkers", piece_set_colour)

    # Test initial conditions for Checkers
    assert not piece_set1.get_castled()
    assert piece_set1.get_number_of_captured_pieces() == 0
    assert piece_set1.get_piece_set_type() == "Checkers"
    assert piece_set1.get_colour() == piece_set_colour
    assert piece_set1.get_number_of_live_pieces() == 12
    assert (piece_set1.get_live_pieces()[0]).get_colour() == piece_set_colour
    assert piece_set1.get_live_pieces()[5].get_colour() == piece_set_colour
    assert piece_set1.get_live_pieces()[11].get_colour() == piece_set_colour

    piece_set1.castle()
    assert piece_set1.get_castled()

    # Captured a piece
    assert piece_set1.capture_piece(piece_set1.get_live_pieces()[0])
    assert piece_set1.get_number_of_live_pieces() == 11
    assert piece_set1.get_number_of_captured_pieces() == 1

    # Fail to capture pieces, nothing should change
    assert not piece_set1.capture_piece(Rook(piece_set_colour))
    assert not piece_set1.capture_piece("Apple")
    assert piece_set1.get_number_of_live_pieces() == 11
    assert piece_set1.get_number_of_captured_pieces() == 1

    # Captured the last piece in the list of live pieces
    assert piece_set1.capture_piece(piece_set1.get_live_pieces()[
                                    len(piece_set1.get_live_pieces())-1])
    assert piece_set1.get_number_of_live_pieces() == 10
    assert piece_set1.get_number_of_captured_pieces() == 2

    # Make sure colour is preserved
    assert piece_set1.get_colour() == piece_set_colour

    piece_set_colour = "Black"
    piece_set2 = PieceSet("Chess", piece_set_colour)

    # Test initial conditions for Chess
    assert not piece_set2.get_castled()
    assert piece_set2.get_number_of_captured_pieces() == 0
    assert piece_set2.get_piece_set_type() == "Chess"
    assert piece_set2.get_colour() == piece_set_colour
    assert piece_set2.get_number_of_live_pieces() == 16


def test_possible_moves():
    piece1 = King("Black")
    moves_for_piece = PossibleMoves(piece1)
    try:
        moves_for_piece.get_moves()
    except AttributeError:
        assert True
    moves_for_piece.build_list_of_moves()
    p = moves_for_piece.get_moves()
    assert p == []


def test_move():
    piece1 = King("Black")
    checkers_move = CheckersMove()
    checkers_move.set_piece(piece1)
    assert checkers_move.get_piece() == piece1

    chess_move = ChessMove()
    chess_move.set_castled()
    try:
        chess_move.set_castled()
    except RuntimeError:
        assert True


def test_board():
    for x in range(1, 101):
        my_board = Board(x)
        row = random.randint(0, x-1)
        col = random.randint(0, x-1)
        # test size of the board
        assert my_board.get_size() == x
        # test if row and col are correct
        assert len(my_board.get_game_board()) == x
        assert len(my_board.get_game_board()[x-1]) == x
        # test if a random game square that is within the bounds of the board is
        # in the right row and right col
        assert my_board.get_game_square(row, col) in my_board.get_game_board()[row]
        assert my_board.get_game_square(row, col) in [r for r in my_board.get_game_board()[row]]
        # test if the initialized board square in board has None for occupying_piece
        assert my_board.get_game_square(row, col).get_occupying_piece() is None
        # test theme is black white at default
        assert my_board.get_board_theme() is BoardTheme.BlackWhite
        # test if changing theme of board works
        new_board_theme = random.choice(list(BoardTheme))
        my_board.set_board_theme(new_board_theme)
        assert my_board.get_board_theme() is new_board_theme


def test_game_square():

    # initial testing for 8by8 board
    gs_test_1 = GameSquare(8, 8)

    assert gs_test_1.get_col() == 8
    assert gs_test_1.get_row() == 8
    assert gs_test_1.get_occupying_piece() is None

    for x in range(1000):
        row = random.randint(0, 1000)
        col = random.randint(0, 1000)
        gsq = GameSquare(row, col)
        # test if row and col are correctly placed
        assert gsq.get_row() == row
        assert gsq.get_col() == col
        # test for occupying piece to be None when initialized
        assert gsq.get_occupying_piece() is None

        # test if replacing the occupying piece with a mock piece
        mock_piece = mock.Mock()
        mock_piece.method = mock.MagicMock(name="Piece")
        gsq.put_piece_here(mock_piece)
        assert gsq.get_occupying_piece() is mock_piece
        # test for removing occupying piece to be None
        gsq.remove_occupying_piece()
        assert gsq.get_occupying_piece() is None
        # test setting new row and col
        gsq.set_row(x)
        gsq.set_col(x)
        assert gsq.get_row() == x
        assert gsq.get_col() == x

        # test for put piece in a not None scenario
        gsq.put_piece_here(mock_piece)
        assert gsq.get_occupying_piece() is mock_piece
        mock_piece2 = mock.Mock()
        mock_piece2.method = mock.MagicMock(name="Piece2")
        result = gsq.put_piece_here(mock_piece2)
        assert gsq.get_occupying_piece() is mock_piece2
        assert result is mock_piece
        gsq.remove_occupying_piece()
        assert gsq.get_occupying_piece() is None

    # gs_test = [[GameSquare(row, col) for col in range(100)] for row in range(100)]
    # gs_test_result = [[GameSquare(row, col) for col in gs_test] for row in range(100)]
    # assert equals(gs_test[random.randrange(100)].get_occupying_piece(), None)
