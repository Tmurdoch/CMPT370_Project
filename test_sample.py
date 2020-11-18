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
from Timer import Timer
import time  # For testing the timer
from GameSquare import GameSquare
from Board import Board
from Board import BoardTheme
from Colours import ColourOffset, ColourCodes, COLOUR_STRING_LOOK_UP_TABLE
from Game import Game
from PlayerType import PlayerType
from Player import Player


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
    assert not pawn1.get_moved_yet_status()
    pawn1.set_colour(piece_set_colour2)
    assert pawn1.get_colour() == piece_set_colour2
    pawn1.move()
    assert pawn1.get_moved_yet_status()

    new_piece = pawn1.promote("Knight")
    assert isinstance(new_piece, Knight)

    pawn2 = Pawn(piece_set_colour1)
    assert pawn2.get_colour() == piece_set_colour1
    new_piece2 = pawn2.promote("Queen")
    assert isinstance(new_piece2, Queen)

    pawn3 = Pawn(piece_set_colour2)
    assert pawn3.get_colour() == piece_set_colour2
    new_piece3 = pawn3.promote("Bishop")
    assert isinstance(new_piece3, Bishop)

    pawn4 = Pawn(piece_set_colour2)
    new_piece4 = pawn4.promote("King")
    assert new_piece4 is None
    assert pawn4.get_colour() == piece_set_colour2
    new_piece4 = pawn4.promote("Bishop")
    assert isinstance(new_piece4, Bishop)

    # Test the checkers coin
    checkers_coin1 = CheckersCoin(piece_set_colour3)
    assert checkers_coin1.get_colour() == piece_set_colour3
    assert not checkers_coin1.get_promotion_status()
    checkers_coin1.promote()
    assert checkers_coin1.get_promotion_status()
    checkers_coin1.set_colour(piece_set_colour1)
    assert checkers_coin1.get_colour() == piece_set_colour1


def test_piece_set():
    # checkers = 1, chess = 0
    piece_set_colour = "White"
    piece_set1 = PieceSet(1, piece_set_colour)

    # Test initial conditions for Checkers
    assert piece_set1.get_number_of_captured_pieces() == 0
    # Chess = 0, Checkers = 1
    assert piece_set1.get_piece_set_type() == 1
    assert piece_set1.get_colour() == piece_set_colour
    assert piece_set1.get_number_of_live_pieces() == 12
    assert (piece_set1.get_live_pieces()[0]).get_colour() == piece_set_colour
    assert piece_set1.get_live_pieces()[5].get_colour() == piece_set_colour
    assert piece_set1.get_live_pieces()[11].get_colour() == piece_set_colour

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
                                        len(piece_set1.get_live_pieces()) - 1])
    assert piece_set1.get_number_of_live_pieces() == 10
    assert piece_set1.get_number_of_captured_pieces() == 2

    # Make sure colour is preserved
    assert piece_set1.get_colour() == piece_set_colour

    # chess = 0, checkers = 1
    piece_set_colour = "Black"
    piece_set2 = PieceSet(0, piece_set_colour)

    # Test initial conditions for Chess
    assert piece_set2.get_number_of_captured_pieces() == 0
    # Chess = 0, Checkers = 1
    assert piece_set2.get_piece_set_type() == 0
    assert piece_set2.get_colour() == piece_set_colour
    assert piece_set2.get_number_of_live_pieces() == 16


def test_possible_moves():
    # TODO: Fix these tests, Thomas and Michael were to lazy to do it when they broke them
    # make sure that game is created correctly
    # chess = 0
    my_game = Game(0, ColourCodes.WHITE_BLACK)
    assert my_game.get_dark_player() is None
    assert my_game.get_light_player() is None
    assert my_game.get_current_player() is None

    # create dark player

    my_game.build_dark_player("Player1", PlayerType.HUMAN, Timer(60, enabled=True), False)
    assert my_game.get_dark_player().get_piece_set().get_colour() == \
           COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.WHITE_BLACK][ColourOffset.OFFSET_DARK]

    # create light player
    my_game.build_light_player("Player2", PlayerType.HUMAN, Timer(60, enabled=True), False)
    assert my_game.get_light_player().get_piece_set().get_colour() == \
           COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.WHITE_BLACK][ColourOffset.OFFSET_LIGHT]

    # check if players are correctly assigned
    assert my_game.get_current_player() is my_game.get_light_player()
    my_game.change_current_player()
    assert my_game.get_current_player() is my_game.get_dark_player()
    assert my_game.get_board().get_size() == 8

    # set up the pieces in the board
    dark_set = my_game.get_dark_player().get_piece_set().get_live_pieces()
    light_set = my_game.get_light_player().get_piece_set().get_live_pieces()

    board = my_game.get_board()
    board.build_chess_board(dark_set, light_set)
    # board.print_game_board()

    lomrook = PossibleMoves(board.get_game_square(7, 0), my_game).build_list_of_moves()
    print("Rook (7,0) possible moves: ", [x.get_row_and_column() for x in lomrook])
    lomknight = PossibleMoves(board.get_game_square(7, 1), my_game).build_list_of_moves()
    print("\nKnight (7, 1) possible moves: ", [x.get_row_and_column() for x in lomknight])
    lombishop = PossibleMoves(board.get_game_square(7, 2), my_game).build_list_of_moves()
    print("\nBishop (7, 2) possible moves: ", [x.get_row_and_column() for x in lombishop])

    # moving pieces -> get your BOARD then get (ROW, COL) of DESTINATION then set piece from another square
    # then remove the piece where you got the piece
    # move rook 7, 0 to 4, 3 for testing
    board.get_game_square(4, 3).put_piece_here(board.get_game_square(7, 0).get_occupying_piece())
    board.get_game_square(7, 0).remove_occupying_piece()

    # move rook 2 from 7, 7 to 4, 6
    board.get_game_square(4, 6).put_piece_here(board.get_game_square(7, 7).get_occupying_piece())
    board.get_game_square(7, 7).remove_occupying_piece()

    lomrook = PossibleMoves(board.get_game_square(4, 3), my_game).build_list_of_moves()
    print("Rook (4,3) possible moves: ", [x.get_row_and_column() for x in lomrook])
    lomrook2 = PossibleMoves(board.get_game_square(4, 6), my_game).build_list_of_moves()
    print("Rook2 (4,6) possible moves: ", [x.get_row_and_column() for x in lomrook2])
    # move knight 7, 1 to 3,3
    # board.get_game_square(3, 3).put_piece_here(board.get_game_square(7, 1).get_occupying_piece())
    # board.get_game_square(7, 1).remove_occupying_piece()

    board.print_game_board()
    # lom = PossibleMoves(board.get_game_square(4, 3), my_game).build_list_of_moves()
    # print("\nRook (4, 3) possible moves: ", [x.get_row_and_column() for x in lom])
    # lom = PossibleMoves(board.get_game_square(3, 3), my_game).build_list_of_moves()
    # print("\nKnight (7, 1) possible moves: ", [x.get_row_and_column() for x in lom])

    # move knight 3, 3 to 5, 1
    # board.get_game_square(5, 1).put_piece_here(board.get_game_square(3, 3).get_occupying_piece())
    # board.get_game_square(3, 3).remove_occupying_piece()
    # lom = PossibleMoves(board.get_game_square(5, 1), my_game).build_list_of_moves()
    # print("\nKnight (5, 1) possible moves: ", [x.get_row_and_column() for x in lom])


def test_move():
    piece1 = King("Black")
    checkers_move = CheckersMove()
    checkers_move.set_piece(piece1)
    assert checkers_move.get_piece() == piece1


def test_timer():
    timer1_that_is_enabled = Timer(90, True)
    assert 89.9 < timer1_that_is_enabled.get_time_remaining_s() < 90.1
    assert timer1_that_is_enabled.get_enabled()
    timer1_that_is_enabled.start()
    time.sleep(1)
    assert 88.9 < timer1_that_is_enabled.get_time_remaining_s() < 89.1
    timer1_that_is_enabled.stop()
    time.sleep(1)  # Should not have changed here
    assert 88.9 < timer1_that_is_enabled.get_time_remaining_s() < 89.1

    timer2_that_is_enabled = Timer(59, True)
    assert timer2_that_is_enabled.little_time_left()

    timer3_that_is_disabled = Timer(90, False)
    assert not timer3_that_is_disabled.get_enabled()

    timer4_that_is_enabled = Timer(-1, True)
    assert timer4_that_is_enabled.timed_out()

    chess_move = ChessMove()
    chess_move.set_castled()
    try:
        chess_move.set_castled()
    except RuntimeError:
        assert True


def test_board():
    for x in range(1, 101):
        my_board = Board(x)
        row = random.randint(0, x - 1)
        col = random.randint(0, x - 1)
        # test size of the board
        assert my_board.get_size() == x
        # test if row and col are correct
        assert len(my_board.get_game_board()) == x
        assert len(my_board.get_game_board()[x - 1]) == x
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


def test_show_board():
    # Test mock board and adding pieces and moving them
    my_board = Board(8)
    # chess = 0
    black_set = PieceSet(0, "Black")
    black_pieces = black_set.get_live_pieces()
    spec_piece = [3, 4, 0, 7, 2, 5, 1, 6]
    for i in range(8):
        my_board.get_game_square(0, spec_piece[i]).put_piece_here(type(black_pieces[i]).__name__)
    for i in range(8):
        my_board.get_game_square(1, i).put_piece_here(type(black_pieces[i + 8]).__name__ + ' ')
    # chess = 0
    white_set = PieceSet(0, "White")
    white_pieces = white_set.get_live_pieces()
    for i in range(8):
        my_board.get_game_square(7, spec_piece[i]).put_piece_here(type(white_pieces[i]).__name__)
    for i in range(8):
        my_board.get_game_square(6, i).put_piece_here(type(white_pieces[i + 8]).__name__ + ' ')
    # my_board.print_game_board()

    print("\n\nMoving Pawn(6, 3) to (4,3)")
    pawn = my_board.get_game_square(6, 3).get_occupying_piece()
    my_board.get_game_square(6, 3).remove_occupying_piece()
    my_board.get_game_square(4, 3).put_piece_here(pawn)
    # my_board.print_game_board()


def test_game():
    # TODO: How to build a player has changed, need to update this to reflect those changes
    # chess = 0
    my_game = Game(0, ColourCodes.WHITE_BLACK)
    assert my_game.get_dark_player() is None
    assert my_game.get_light_player() is None
    assert my_game.get_current_player() is None
    # my_game.build_dark_player("Player1", PlayerType.HUMAN, Timer(60, enabled=True), False)
    # assert my_game.get_dark_player().get_piece_set().get_colour() == \
    #       COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.WHITE_BLACK][ColourOffset.OFFSET_DARK]
    # my_game.build_light_player("Player2", PlayerType.HUMAN, Timer(60, enabled=True), False)
    # assert my_game.get_light_player().get_piece_set().get_colour() == \
    #        COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.WHITE_BLACK][ColourOffset.OFFSET_LIGHT]
    # assert my_game.get_current_player() is my_game.get_light_player()
    # my_game.change_current_player()
    # assert my_game.get_current_player() is my_game.get_dark_player()
    assert my_game.get_board().get_size() == 8

    # dark_set = my_game.get_dark_player().get_piece_set().get_live_pieces()
    # light_set = my_game.get_light_player().get_piece_set().get_live_pieces()
    spec_piece = [3, 4, 0, 7, 2, 5, 1, 6]
    """
    board = my_game.get_board()
    i = 0
    for r in board.get_game_board():
        r[7].put_piece_here(light_set[i])
        r[0].put_piece_here(dark_set[i])
        i += 1
    board.print_game_board()
    my_game.save_to_file()

    load_game = Game("Chess", ColourCodes.WHITE_BLACK)
    load_game.load_from_file()
    load_game.get_board().print_game_board()
    """


def test_player():
    pt = PlayerType.AI
    t = Timer(1, False)
    # chess = 0
    p = Player("Joel", "White", 0, pt, t)
    assert (p.get_name() == 'Joel')
    assert (p.get_player_type() == 0)
    assert (p.get_timer() == t)
    assert (not p.get_castled())
    p.castle()
    assert (p.get_castled())


# if __name__ == '__main__':
    # test_show_board()
