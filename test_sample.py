# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import pytest
from PieceSet import PieceSet
from Pieces import King, Queen, Knight, Bishop, Rook, Pawn, CheckersCoin
from Move import CheckersMove, ChessMove
from PossibleMoves import PossibleMoves


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
