# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import random
from unittest import mock
from PieceSet import PieceSet
from Pieces import King, Queen, Knight, Bishop, Rook, Pawn, CheckersCoin
import build_list_of_moves
from Timer import Timer
import time  # For testing the timer
from GameSquare import GameSquare
from Board import Board, BoardTheme
from Colours import ColourOffset, ColourCodes, COLOUR_STRING_LOOK_UP_TABLE
from Game import Game
from PlayerType import PlayerType
from Player import Player


def test_pieces():
    """
    Unit testing each of the pieces
    """
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
    assert not checkers_coin1.is_promoted()
    checkers_coin1.promote()
    assert checkers_coin1.is_promoted()
    checkers_coin1.set_colour(piece_set_colour1)
    assert checkers_coin1.get_colour() == piece_set_colour1


def test_piece_set():
    """
    Unit testing the piece set
    """
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
    """
    Testing the possible moves class
    """
    # make sure that game is created correctly
    # chess = 0
    my_game = Game(0, ColourCodes.WHITE_BLACK)
    assert my_game.get_dark_player() is None
    assert my_game.get_light_player() is None
    assert my_game.get_current_player() is None

    # create dark player
    my_game.build_dark_player(
        "Player1", PlayerType.HUMAN, Timer(60, enabled=True))
    assert my_game.get_dark_player().get_piece_set().get_colour() == \
        COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.WHITE_BLACK][ColourOffset.OFFSET_DARK]

    # create light player
    my_game.build_light_player(
        "Player2", PlayerType.HUMAN, Timer(60, enabled=True))
    assert my_game.get_light_player().get_piece_set().get_colour() == \
        COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.WHITE_BLACK][ColourOffset.OFFSET_LIGHT]

    # check if players are correctly assigned
    assert my_game.get_current_player() is my_game.get_light_player()
    # my_game.change_current_player()
    # assert my_game.get_current_player() is my_game.get_dark_player()
    assert my_game.get_board().get_size() == 8

    # set up the pieces in the board
    dark_set = my_game.get_dark_player().get_piece_set().get_live_pieces()
    light_set = my_game.get_light_player().get_piece_set().get_live_pieces()
    # ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"

    # TEST CHESS PIECES POSSIBLE MOVES

    # pc_moves_{...} have all 5 lists of tuples
    # each representing the board location in index_piece_test
    # these are list expected (row, col) if a piece is at an index_piece_test location
    pc_moves_rook = [sorted([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                             (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]),
                     sorted([(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
                             (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]),
                     sorted([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                             (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]),
                     sorted([(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
                             (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)]),
                     sorted([(3, 0), (3, 1), (3, 2), (3, 3), (3, 5), (3, 6), (3, 7),
                             (0, 4), (1, 4), (2, 4), (4, 4), (5, 4), (6, 4), (7, 4)])]

    pc_moves_knight = [sorted([(2, 1), (1, 2)]), sorted([(5, 1), (6, 2)]),
                       sorted([(1, 5), (2, 6)]), sorted([(6, 5), (5, 6)]),
                       sorted([(2, 2), (1, 3), (1, 5), (2, 6), (4, 6), (5, 5), (5, 3), (4, 2)])]

    pc_moves_bishop = [sorted([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]),
                       sorted([(6, 1), (5, 2), (4, 3), (3, 4),
                               (2, 5), (1, 6), (0, 7)]),
                       sorted([(7, 0), (6, 1), (5, 2), (4, 3),
                               (3, 4), (2, 5), (1, 6)]),
                       sorted([(0, 0), (1, 1), (2, 2), (3, 3),
                               (4, 4), (5, 5), (6, 6)]),
                       sorted([(2, 3), (1, 2), (0, 1), (2, 5), (1, 6), (0, 7), (4, 5),
                               (5, 6), (6, 7), (4, 3), (5, 2), (6, 1), (7, 0)])]

    pc_moves_queen = [sorted([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                              (1, 0), (2, 0), (3, 0), (4,
                                                       0), (5, 0), (6, 0), (7, 0),
                              (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]),
                      sorted([(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
                              (0, 0), (1, 0), (2, 0), (3,
                                                       0), (4, 0), (5, 0), (6, 0),
                              (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7)]),
                      sorted([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                              (1, 7), (2, 7), (3, 7), (4,
                                                       7), (5, 7), (6, 7), (7, 7),
                              (7, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)]),
                      sorted([(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
                              (0, 7), (1, 7), (2, 7), (3,
                                                       7), (4, 7), (5, 7), (6, 7),
                              (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]),
                      sorted([(3, 0), (3, 1), (3, 2), (3, 3), (3, 5), (3, 6), (3, 7),
                              (0, 4), (1, 4), (2, 4), (4,
                                                       4), (5, 4), (6, 4), (7, 4),
                              (2, 3), (1, 2), (0, 1), (2,
                                                       5), (1, 6), (0, 7), (4, 5),
                              (5, 6), (6, 7), (4, 3), (5, 2), (6, 1), (7, 0)
                              ])]

    pc_moves_pawn = [sorted([]), sorted([(5, 0), (6, 0)]),
                     sorted([]), sorted([(6, 7), (5, 7)]), sorted([(1, 4), (2, 4)])]

    pc_moves_king = [sorted([(0, 1), (1, 0), (1, 1)]), sorted([(6, 0), (7, 1), (6, 1)]),
                     sorted([(0, 6), (1, 6), (1, 7)]), sorted(
                         [(7, 6), (6, 6), (6, 7)]),
                     sorted([(2, 3), (2, 4), (2, 5), (4, 3), (4, 4), (4, 5), (3, 3), (3, 5)])]

    # location on board (row, col) -> board corners and middle
    index_piece_test = [(0, 0), (7, 0), (0, 7), (7, 7), (3, 4)]

    # goes through a piece set
    # goes through specified indexes in index_piece
    # checks what piece it is and then creates a possible moves list
    # converts the possible moves list to a tuple list and compare to
    # the fixed list of moves like pc_moves_...
    # both are sorted first then compared
    for pieces in dark_set:
        for test_tuple in range(len(index_piece_test)):
            my_game.get_board().get_game_square(
                index_piece_test[test_tuple][0], index_piece_test[test_tuple][1]).put_piece_here(pieces)
            if type(my_game.get_board().get_game_square(
                    index_piece_test[test_tuple][0],
                    index_piece_test[test_tuple][1]).get_occupying_piece()).__name__ is "King":
                pm_gs = build_list_of_moves.build_list_of_moves(
                    my_game.get_board().get_game_square(index_piece_test[test_tuple][0],
                                                        index_piece_test[test_tuple][1]),
                    my_game)
                assert sorted([x.get_row_and_column()
                               for x in pm_gs]) == pc_moves_king[test_tuple]
            if type(my_game.get_board().get_game_square(
                    index_piece_test[test_tuple][0],
                    index_piece_test[test_tuple][1]).get_occupying_piece()).__name__ is "Queen":
                pm_gs = build_list_of_moves.build_list_of_moves(
                    my_game.get_board().get_game_square(index_piece_test[test_tuple][0],
                                                        index_piece_test[test_tuple][1]),
                    my_game)
                assert sorted([x.get_row_and_column()
                               for x in pm_gs]) == pc_moves_queen[test_tuple]
            if type(my_game.get_board().get_game_square(
                    index_piece_test[test_tuple][0],
                    index_piece_test[test_tuple][1]).get_occupying_piece()).__name__ is "Bishop":
                pm_gs = build_list_of_moves.build_list_of_moves(
                    my_game.get_board().get_game_square(index_piece_test[test_tuple][0],
                                                        index_piece_test[test_tuple][1]),
                    my_game)
                assert sorted([x.get_row_and_column()
                               for x in pm_gs]) == pc_moves_bishop[test_tuple]
            if type(my_game.get_board().get_game_square(
                    index_piece_test[test_tuple][0],
                    index_piece_test[test_tuple][1]).get_occupying_piece()).__name__ is "Knight":
                pm_gs = build_list_of_moves.build_list_of_moves(
                    my_game.get_board().get_game_square(index_piece_test[test_tuple][0],
                                                        index_piece_test[test_tuple][1]),
                    my_game)
                assert sorted([x.get_row_and_column()
                               for x in pm_gs]) == pc_moves_knight[test_tuple]
            if type(my_game.get_board().get_game_square(
                    index_piece_test[test_tuple][0],
                    index_piece_test[test_tuple][1]).get_occupying_piece()).__name__ is "Rook":
                pm_gs = build_list_of_moves.build_list_of_moves(
                    my_game.get_board().get_game_square(index_piece_test[test_tuple][0],
                                                        index_piece_test[test_tuple][1]),
                    my_game)
                assert sorted([x.get_row_and_column()
                               for x in pm_gs]) == pc_moves_rook[test_tuple]
            if type(my_game.get_board().get_game_square(
                    index_piece_test[test_tuple][0],
                    index_piece_test[test_tuple][1]).get_occupying_piece()).__name__ is "Pawn":
                pm_gs = build_list_of_moves.build_list_of_moves(
                    my_game.get_board().get_game_square(index_piece_test[test_tuple][0],
                                                        index_piece_test[test_tuple][1]),
                    my_game)
                assert sorted([x.get_row_and_column()
                               for x in pm_gs]) == pc_moves_pawn[test_tuple]
            my_game.get_board().get_game_square(
                index_piece_test[test_tuple][0],
                index_piece_test[test_tuple][1]).remove_occupying_piece()

    # build a chess game with all pieces on the board
    my_game.get_board().build_chess_board(dark_set, light_set)

    # checks standard fresh game of chess move list

    # rooks
    lomrook = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(7, 0), my_game)
    assert sorted([x.get_row_and_column() for x in lomrook]) == sorted([])
    lomrook2 = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(7, 7), my_game)
    assert sorted([x.get_row_and_column() for x in lomrook2]) == sorted([])

    # knights
    lomknight = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(7, 1), my_game)
    assert sorted([x.get_row_and_column()
                   for x in lomknight]) == sorted([(5, 2), (5, 0)])
    lomknight2 = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(7, 6), my_game)
    assert sorted([x.get_row_and_column()
                   for x in lomknight2]) == sorted([(5, 7), (5, 5)])

    # bishops
    lombishop = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(7, 2), my_game)
    assert sorted([x.get_row_and_column() for x in lombishop]) == sorted([])
    lombishop2 = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(7, 5), my_game)
    assert sorted([x.get_row_and_column() for x in lombishop2]) == sorted([])

    # queen
    lomqueen = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(7, 3), my_game)
    assert sorted([x.get_row_and_column() for x in lomqueen]) == sorted([])

    # king
    lomking = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(7, 4), my_game)
    assert sorted([x.get_row_and_column() for x in lomking]) == sorted([])

    # pawns
    for col in range(my_game.get_board().get_size()):
        lompawn = build_list_of_moves.build_list_of_moves(
            my_game.get_board().get_game_square(6, col), my_game)
        assert sorted([x.get_row_and_column()
                       for x in lompawn]) == sorted([(5, col), (4, col)])

    # moving pieces -> get your BOARD then get (ROW, COL) of DESTINATION then set piece from another square
    # then remove the piece where you got the piece
    # move rook 7, 0 to 4, 3 for testing
    my_game.get_board().get_game_square(4, 3).put_piece_here(my_game.get_board().
                                                             get_game_square(7, 0).get_occupying_piece())
    my_game.get_board().get_game_square(7, 0).remove_occupying_piece()

    # move rook 2 from 7, 7 to 4, 6
    my_game.get_board().get_game_square(4, 6).put_piece_here(my_game.get_board().
                                                             get_game_square(7, 7).get_occupying_piece())
    my_game.get_board().get_game_square(7, 7).remove_occupying_piece()

    # move bishop from 7, 2 to 7, 0
    my_game.get_board().get_game_square(7, 0).put_piece_here(my_game.get_board().
                                                             get_game_square(7, 2).get_occupying_piece())
    my_game.get_board().get_game_square(7, 2).remove_occupying_piece()

    # move queen from 7, 3 to 4, 4
    my_game.get_board().get_game_square(4, 4).put_piece_here(my_game.get_board().
                                                             get_game_square(7, 3).get_occupying_piece())
    my_game.get_board().get_game_square(7, 3).remove_occupying_piece()

    # move enemy pawn from 1, 0 to 5, 1
    my_game.get_board().get_game_square(5, 1).put_piece_here(my_game.get_board().
                                                             get_game_square(1, 0).get_occupying_piece())
    my_game.get_board().get_game_square(1, 0).remove_occupying_piece()

    # move king from 4, 0 to 7, 4
    my_game.get_board().get_game_square(4, 0).put_piece_here(my_game.get_board().
                                                             get_game_square(7, 4).get_occupying_piece())
    my_game.get_board().get_game_square(7, 4).remove_occupying_piece()

    # test the moved positions
    lomrook = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(4, 3), my_game)
    assert sorted([x.get_row_and_column() for x in lomrook]) == sorted([(3, 3), (2, 3), (1, 3), (5, 3),
                                                                        (4, 2), (4, 1)])
    lomrook2 = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(4, 6), my_game)
    assert sorted([x.get_row_and_column() for x in lomrook2]) == sorted([(3, 6), (2, 6), (1, 6), (5, 6),
                                                                         (4, 7), (4, 5)])
    lomqueen = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(4, 4), my_game)
    assert sorted([x.get_row_and_column() for x in lomqueen]) == sorted([(3, 4), (2, 4), (1, 4), (5, 4),
                                                                         (4, 5), (3, 5), (2,
                                                                                          6), (1, 7),
                                                                         (3, 3), (2, 2), (1,
                                                                                          1), (5, 5),
                                                                         (5, 3)])
    lompawn = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(6, 0), my_game)
    assert sorted([x.get_row_and_column()
                   for x in lompawn]) == sorted([(5, 0), (5, 1)])
    lomking = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(4, 0), my_game)
    assert sorted([x.get_row_and_column() for x in lomking]) == sorted(
        [(3, 0), (5, 0), (4, 1), (5, 1), (3, 1)])

    # test castling
    # move knight from 7, 1 to 5, 0
    my_game.get_board().get_game_square(5, 0).put_piece_here(my_game.get_board().
                                                             get_game_square(7, 1).get_occupying_piece())
    my_game.get_board().get_game_square(7, 1).remove_occupying_piece()

    # move Bishop from 7, 1 to 5, 0
    my_game.get_board().get_game_square(5, 5).put_piece_here(my_game.get_board().
                                                             get_game_square(7, 5).get_occupying_piece())
    my_game.get_board().get_game_square(7, 5).remove_occupying_piece()

    # move knight from 7, 1 to 5, 0
    my_game.get_board().get_game_square(5, 6).put_piece_here(my_game.get_board().
                                                             get_game_square(7, 6).get_occupying_piece())
    my_game.get_board().get_game_square(7, 6).remove_occupying_piece()

    # move king from 4, 0 to 7, 4
    my_game.get_board().get_game_square(7, 4).put_piece_here(my_game.get_board().
                                                             get_game_square(4, 0).get_occupying_piece())
    my_game.get_board().get_game_square(4, 0).remove_occupying_piece()

    # move enemy rook from 0, 7 to 7, 7
    my_game.get_board().get_game_square(7, 7).put_piece_here(my_game.get_board().
                                                             get_game_square(0, 7).get_occupying_piece())
    my_game.get_board().get_game_square(0, 7).remove_occupying_piece()

    # move bishop from 7, 0 to 4, 0
    my_game.get_board().get_game_square(4, 0).put_piece_here(my_game.get_board().
                                                             get_game_square(7, 0).get_occupying_piece())
    my_game.get_board().get_game_square(7, 0).remove_occupying_piece()

    # move rook from 4, 3 to 7, 0
    my_game.get_board().get_game_square(7, 0).put_piece_here(my_game.get_board().
                                                             get_game_square(4, 3).get_occupying_piece())
    my_game.get_board().get_game_square(4, 3).remove_occupying_piece()

    lomking = build_list_of_moves.build_list_of_moves(
        my_game.get_board().get_game_square(7, 4), my_game)
    assert sorted([x.get_row_and_column()
                   for x in lomking]) == sorted([(7, 3), (7, 5), (7, 0)])

    # -----------TEST CHECKERS PIECES POSSIBLE MOVES ----------------------------------------------------
    # checkers = 1
    my_game_2 = Game(1, ColourCodes.RED_BLACK)
    assert my_game_2.get_dark_player() is None
    assert my_game_2.get_light_player() is None
    assert my_game_2.get_current_player() is None

    # create dark player
    my_game_2.build_dark_player(
        "Player1", PlayerType.HUMAN, Timer(60, enabled=True))
    assert my_game_2.get_dark_player().get_piece_set().get_colour() == \
        COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.RED_BLACK][ColourOffset.OFFSET_DARK]

    # create light player
    my_game_2.build_light_player(
        "Player2", PlayerType.HUMAN, Timer(60, enabled=True))
    assert my_game_2.get_light_player().get_piece_set().get_colour() == \
        COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.RED_BLACK][ColourOffset.OFFSET_LIGHT]

    # check if players are correctly assigned
    assert my_game_2.get_current_player() is my_game_2.get_light_player()
    # my_game_2.change_current_player()
    # assert my_game_2.get_current_player() is my_game_2.get_dark_player()
    assert my_game_2.get_board().get_size() == 8

    # set up the pieces in the board

    dark_set2 = my_game_2.get_dark_player().get_piece_set().get_live_pieces()
    light_set2 = my_game_2.get_light_player().get_piece_set().get_live_pieces()

    # goes through a piece set
    # goes through specified indexes in index_piece
    # checks what piece it is and then creates a possible moves list
    # converts the possible moves list to a tuple list and compare to
    # the fixed list of moves like pc_moves_...
    # both are sorted first then compared

    pc_moves_coin = [sorted([]), sorted([(6, 1)]), sorted(
        []), sorted([(6, 5), (6, 7)]), sorted([(3, 2), (3, 4)])]
    # edge cases
    index_piece_test2 = [(0, 1), (7, 0), (0, 7), (7, 6), (4, 3)]

    for test_tuple in range(len(index_piece_test2)):
        my_game_2.get_board().get_game_square(
            index_piece_test2[test_tuple][0], index_piece_test2[test_tuple][1]).put_piece_here(dark_set2[0])
        if type(my_game_2.get_board().get_game_square(
                index_piece_test2[test_tuple][0],
                index_piece_test2[test_tuple][1]).get_occupying_piece()).__name__ is "CheckersCoin":
            pm_gs = build_list_of_moves.build_list_of_moves(
                my_game_2.get_board().get_game_square(index_piece_test2[test_tuple][0],
                                                      index_piece_test2[test_tuple][1]),
                my_game_2)
            assert sorted([x.get_row_and_column()
                           for x in pm_gs]) == pc_moves_coin[test_tuple]
        my_game_2.get_board().get_game_square(
            index_piece_test2[test_tuple][0],
            index_piece_test2[test_tuple][1]).remove_occupying_piece()

    # build a chess game with all pieces on the board
    my_game_2.get_board().build_checkers_board(dark_set2, light_set2)

    # move enemy coin from 1, 0 to 4, 1
    my_game_2.get_board().get_game_square(4, 1).put_piece_here(my_game_2.get_board().
                                                               get_game_square(1, 0).get_occupying_piece())
    my_game_2.get_board().get_game_square(1, 0).remove_occupying_piece()

    # move enemy coin from 1, 4 to 4, 3
    my_game_2.get_board().get_game_square(4, 3).put_piece_here(my_game_2.get_board().
                                                               get_game_square(1, 4).get_occupying_piece())
    my_game_2.get_board().get_game_square(1, 4).remove_occupying_piece()

    # double jumps + more
    lomcoinb = build_list_of_moves.build_list_of_moves(
        my_game_2.get_board().get_game_square(5, 0), my_game_2)
    assert sorted([x.get_row_and_column()
                   for x in lomcoinb]) == sorted([(3, 2), (1, 0), (1, 4)])

    lomcoinb2 = build_list_of_moves.build_list_of_moves(
        my_game_2.get_board().get_game_square(5, 4), my_game_2)
    assert sorted([x.get_row_and_column() for x in lomcoinb2]
                  ) == sorted([(3, 2), (1, 0), (1, 4), (4, 5)])

    # test edge cases when coin is promoted
    # recreate the tests for checkers because pieces there are promoted

    my_game_2 = Game(1, ColourCodes.RED_BLACK)
    # create dark player
    my_game_2.build_dark_player(
        "Player1", PlayerType.HUMAN, Timer(60, enabled=True))
    assert my_game_2.get_dark_player().get_piece_set().get_colour() == \
        COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.RED_BLACK][ColourOffset.OFFSET_DARK]

    # create light player
    my_game_2.build_light_player(
        "Player2", PlayerType.HUMAN, Timer(60, enabled=True))
    assert my_game_2.get_light_player().get_piece_set().get_colour() == \
        COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.RED_BLACK][ColourOffset.OFFSET_LIGHT]

    dark_set2 = my_game_2.get_dark_player().get_piece_set().get_live_pieces()
    light_set2 = my_game_2.get_light_player().get_piece_set().get_live_pieces()

    pc_moves_coin_promoted = [sorted([(1, 0), (1, 2)]), sorted([(6, 1)]), sorted([(1, 6)]), sorted([(6, 5), (6, 7)]),
                              sorted([(3, 2), (3, 4), (5, 2), (5, 4)])]

    for test_tuple in range(len(index_piece_test2)):
        my_game_2.get_board().get_game_square(
            index_piece_test2[test_tuple][0], index_piece_test2[test_tuple][1]).put_piece_here(dark_set2[0])
        if type(my_game_2.get_board().get_game_square(
                index_piece_test2[test_tuple][0],
                index_piece_test2[test_tuple][1]).get_occupying_piece()).__name__ is "CheckersCoin":

            # promote coin first
            my_game_2.get_board().get_game_square(index_piece_test2[test_tuple][0], index_piece_test2[test_tuple][1])\
                .get_occupying_piece().promote()

            # check the moves
            pm_gs = build_list_of_moves.build_list_of_moves(
                my_game_2.get_board().get_game_square(index_piece_test2[test_tuple][0],
                                                      index_piece_test2[test_tuple][1]),
                my_game_2)
            assert sorted([x.get_row_and_column() for x in pm_gs]
                          ) == pc_moves_coin_promoted[test_tuple]
        my_game_2.get_board().get_game_square(
            index_piece_test2[test_tuple][0],
            index_piece_test2[test_tuple][1]).remove_occupying_piece()

    # build a chess game with all pieces on the board
    my_game_2.get_board().build_checkers_board(dark_set2, light_set2)

    # move enemy coin from 1, 0 to 4, 1
    my_game_2.get_board().get_game_square(4, 1).put_piece_here(my_game_2.get_board().
                                                               get_game_square(1, 0).get_occupying_piece())
    my_game_2.get_board().get_game_square(1, 0).remove_occupying_piece()

    # move enemy coin from 1, 4 to 4, 3
    my_game_2.get_board().get_game_square(4, 3).put_piece_here(my_game_2.get_board().
                                                               get_game_square(1, 4).get_occupying_piece())
    my_game_2.get_board().get_game_square(1, 4).remove_occupying_piece()

    # double jumps + more
    lomcoinb = build_list_of_moves.build_list_of_moves(
        my_game_2.get_board().get_game_square(5, 0), my_game_2)
    assert sorted([x.get_row_and_column() for x in lomcoinb]
                  ) == sorted([(3, 2), (1, 0), (1, 4), (3, 6)])

    lomcoinb2 = build_list_of_moves.build_list_of_moves(
        my_game_2.get_board().get_game_square(5, 4), my_game_2)
    assert sorted([x.get_row_and_column() for x in lomcoinb2]) == sorted(
        [(3, 2), (1, 0), (1, 4), (4, 5), (3, 6)])


def test_timer():
    """
    Unit testing the timer
    This test has a sleep() call within that slows it down
    """
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


def test_board():
    """
    Board unit testing
    """
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
        assert my_board.get_game_square(
            row, col) in my_board.get_game_board()[row]
        assert my_board.get_game_square(
            row, col) in [r for r in my_board.get_game_board()[row]]
        # test if the initialized board square in board has None for occupying_piece
        assert my_board.get_game_square(row, col).get_occupying_piece() is None
        # test theme is black white at default
        assert my_board.get_board_theme() is BoardTheme.BlackWhite


def test_game_square():
    """
    Initial testing for 8by8 board of game squares
    """
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
    """
    Test mock board and adding pieces and moving them
    """
    my_board = Board(8)
    # chess = 0
    black_set = PieceSet(0, "Black")
    black_pieces = black_set.get_live_pieces()
    spec_piece = [3, 4, 0, 7, 2, 5, 1, 6]
    for i in range(8):
        my_board.get_game_square(0, spec_piece[i]).put_piece_here(
            type(black_pieces[i]).__name__)
    for i in range(8):
        my_board.get_game_square(1, i).put_piece_here(
            type(black_pieces[i + 8]).__name__ + ' ')
    # chess = 0
    white_set = PieceSet(0, "White")
    white_pieces = white_set.get_live_pieces()
    for i in range(8):
        my_board.get_game_square(7, spec_piece[i]).put_piece_here(
            type(white_pieces[i]).__name__)
    for i in range(8):
        my_board.get_game_square(6, i).put_piece_here(
            type(white_pieces[i + 8]).__name__ + ' ')

    pawn = my_board.get_game_square(6, 3).get_occupying_piece()
    my_board.get_game_square(6, 3).remove_occupying_piece()
    my_board.get_game_square(4, 3).put_piece_here(pawn)


def test_game():
    """
    Unit testing of the Game class
    """
    # TODO: Finish up Game Saving and Loading one or the other does not work properly

    # game types chess = 0 checkers = 1
    gt_chess = 0
    gt_checkers = 1
    # Piece Set colours for players
    gc_wb = ColourCodes.WHITE_BLACK
    gc_rb = ColourCodes.RED_BLACK

    # create a chess and checkers game
    my_chess_game = Game(gt_chess, gc_wb)
    my_checkers_game = Game(gt_checkers, gc_rb)

    # pl - player light pd player dark
    pt_human = PlayerType.HUMAN
    pt_ai = PlayerType.AI

    # Timer set at 60 and to be inactive
    timer = Timer(60, False)

    # Test if the game is initialized correctly

    # Test chess initialization
    assert my_chess_game.get_dark_player() is None
    assert my_chess_game.get_light_player() is None
    assert my_chess_game.get_current_player() is None
    assert my_chess_game.get_board().get_size() == 8
    assert my_chess_game.get_game_type() == 0

    # Test checkers initialization
    assert my_checkers_game.get_dark_player() is None
    assert my_checkers_game.get_light_player() is None
    assert my_checkers_game.get_current_player() is None
    assert my_checkers_game.get_board().get_size() == 8
    assert my_checkers_game.get_game_type() == 1

    # build the players in game

    # chess player light human 1st turn
    my_chess_game.build_light_player("Light HU", pt_human, timer)

    # chess player dark ai 2nd turn
    my_chess_game.build_dark_player("Dark AI", pt_ai, timer)

    # checkers player light ai 1st turn
    my_checkers_game.build_light_player("Light AI", pt_ai, timer)

    # checkers player dark human 2nd turn
    my_checkers_game.build_dark_player("Dark HU", pt_human, timer)

    # Test chess after player initialization
    assert my_chess_game.get_dark_player().get_piece_set().get_colour() is "Black"
    assert my_chess_game.get_light_player().get_piece_set().get_colour() is "White"
    assert my_chess_game.get_current_player().get_piece_set().get_colour() is "White"
    assert my_chess_game.get_board().get_size() == 8
    assert my_chess_game.get_game_type() == 0

    # Test checkers after player initialization
    assert my_checkers_game.get_dark_player().get_piece_set().get_colour() is "Black"
    assert my_checkers_game.get_light_player().get_piece_set().get_colour() is "Red"
    assert my_checkers_game.get_current_player().get_piece_set().get_colour() is "Red"
    assert my_checkers_game.get_board().get_size() == 8
    assert my_checkers_game.get_game_type() == 1

    # Build Chess Board on my_chess_game using the games light and dark player piece set
    my_chess_game.get_board().build_chess_board(my_chess_game.get_light_player().get_piece_set().get_live_pieces(),
                                                my_chess_game.get_dark_player().get_piece_set().get_live_pieces())

    # Build Checkers Board on my_checkers_game using the games light and dark player piece set
    my_checkers_game.get_board().build_checkers_board(
        my_checkers_game.get_light_player().get_piece_set().get_live_pieces(),
        my_checkers_game.get_dark_player().get_piece_set().get_live_pieces())

    # test saving
    # chess
    # my_chess_game.save_to_file()

    # test loading
    # load_chess_game = Game(gt_chess, gc_wb)
    # load_chess_game.load_from_file()

    # test saving
    # checkers
    # my_checkers_game.save_to_file()

    # test loading
    # load_checkers_game = Game(gt_checkers, gc_rb)
    # load_checkers_game.load_from_file()

    # do assert testing from above to check if files are the same


def test_player():
    """
    Unit testing of the Player class
    """

    # game types chess = 0 checkers = 1
    gt_chess = 0
    gt_checkers = 1

    # all player types
    player_type_human = PlayerType.HUMAN
    player_type_ai = PlayerType.AI

    # Timer set at 60 and to be inactive
    timer1 = Timer(60, False)
    timer2 = Timer(30, False)

    # build the players in game
    # chess player human
    pt_human = Player("Human 1", "Red", gt_chess, player_type_human, timer1)

    # chess player ai
    pt_ai = Player("AI 1", "Blue", gt_checkers, player_type_ai, timer2)

    # test human player
    assert pt_human.get_name() == "Human 1"
    assert pt_human.get_colour() == "Red"
    assert pt_human.get_timer() == timer1
    assert pt_human.get_piece_set() is not None
    assert pt_human.get_player_type() == PlayerType.HUMAN
    assert not pt_human.get_castled()

    # test ai player
    assert pt_ai.get_name() == "AI 1"
    assert pt_ai.get_colour() == "Blue"
    assert pt_ai.get_timer() == timer2
    assert pt_ai.get_piece_set() is not None
    assert pt_ai.get_player_type() == PlayerType.AI
    assert not pt_ai.get_castled()


def test_integration_1():
    """
    Testing the integration of GameSquare.py and Boards.py
    """
    s = 8
    my_board = Board(s)
    a_game_square = GameSquare(0, 0)
    # test if the game square in the board are all game squares
    # test if the game square when initialized in the board to be None
    # test if game squares have the right row and column
    row = 0
    for row_gs in my_board.get_game_board():
        col = 0
        for col_gs in row_gs:
            assert type(col_gs) is type(a_game_square)
            assert col_gs.get_occupying_piece() is None
            assert col_gs.get_row() is row
            assert col_gs.get_col() is col
            col += 1
        row += 1

    # test switching board sides
    # my_board.switch_board_sides()
    # copy above test and make sure they have the same things


def test_integration_2():
    """
    Testing the integration of GameSquare.py, Boards.py, and Pieces.py, PieceSet.py
    """

    # ------Chess-----------
    # Game Type 0 is Chess
    my_board = Board(8)
    lp_chess_pieces = PieceSet(0, "White")
    dp_chess_pieces = PieceSet(0, "Black")

    # indexes of pieces based on where they are on the board
    # king, queen...
    spec_piece = [4, 3, 0, 7, 2, 5, 1, 6]

    # set up board player 1 pieces
    # pieces are set up to row 7 and row 6
    i = 0
    for col in spec_piece:
        my_board.get_game_board()[7][col].put_piece_here(
            dp_chess_pieces.get_live_pieces()[i])
        i += 1
    for col in range(8):
        my_board.get_game_board()[6][col].put_piece_here(
            dp_chess_pieces.get_live_pieces()[i])
        i += 1

    # set up board player 2 pieces
    # pieces are set up to row 0 and row 1
    i = 0
    for col in spec_piece:
        my_board.get_game_board()[0][col].put_piece_here(
            lp_chess_pieces.get_live_pieces()[i])
        i += 1
    for col in range(8):
        my_board.get_game_board()[1][col].put_piece_here(
            lp_chess_pieces.get_live_pieces()[i])
        i += 1
    a_game_square = GameSquare(0, 0)

    # TESTS STARTS FOR CHESS
    # test if the game square in the board are all game squares after adding the pieces to each game square
    # test if the game square received the pieces
    # check if a square has a piece to check if it is one of the pieces in string
    # test if game squares have the right row and column
    row = 0
    for row_gs in my_board.get_game_board():
        col = 0
        for col_gs in row_gs:
            assert type(col_gs) is type(a_game_square)
            if col_gs.get_occupying_piece() is not None:
                pieces_string = ["King", "Queen",
                                 "Bishop", "Rook", "Knight", "Pawn"]
                pieces_colour = ["White", "Black"]
                assert type(col_gs.get_occupying_piece()
                            ).__name__ in pieces_string
                assert col_gs.get_occupying_piece().get_colour() in pieces_colour
            assert col_gs.get_row() is row
            assert col_gs.get_col() is col
            col += 1
        row += 1

    # test for switching sides
    # list of String names of pieces in chess
    chess_r7 = [["Rook", "Knight", "Bishop", "Queen",
                 "King", "Bishop", "Knight", "Rook"], ["Pawn"]]
    # for player 1 Dark Bottom Current Player
    # index for chess_r7 to get the correct name in row 6 or 7
    for rows in [0, 1]:
        # index of column in both chess_r7 and the board
        for col in range(len(chess_r7[rows])):
            # for correct row in the board
            if rows == 0:
                row = 7
            else:
                row = 6
            # check if each peace are the correct colour and at the right spot
            assert my_board.get_game_square(
                row, col).get_occupying_piece().get_colour() == "Black"
            assert type(my_board.get_game_square(
                row, col).get_occupying_piece()).__name__ is chess_r7[rows][col]

    # for player 2 Light Top
    # index for chess_r7 to get the correct name in row 0 or 1
    for rows in [0, 1]:
        # index of column in both chess_r7 and the board
        for col in range(len(chess_r7[rows])):
            # for correct row in the board
            if rows == 0:
                row = 0
            else:
                row = 1
            # check if each peace are the correct colour and at the right spot
            assert my_board.get_game_square(
                row, col).get_occupying_piece().get_colour() == "White"
            assert type(my_board.get_game_square(
                row, col).get_occupying_piece()).__name__ is chess_r7[rows][col]

    # SWITCHING SIDES
    my_board.switch_sides()

    # since board rotated king and queen switch position
    chess_r7_switch = [["Rook", "Knight", "Bishop", "King",
                        "Queen", "Bishop", "Knight", "Rook"], ["Pawn"]]
    # for player 1 Dark TOP
    # index for chess_r7 to get the correct name in row 6 or 7
    for rows in [0, 1]:
        # index of column in both chess_r7_switch and the board
        for col in range(len(chess_r7_switch[rows])):
            # for correct row in the board
            if rows == 0:
                row = 0
            else:
                row = 1
            # check if each peace are the correct colour and at the right spot
            assert my_board.get_game_square(
                row, col).get_occupying_piece().get_colour() == "Black"
            assert type(my_board.get_game_square(
                row, col).get_occupying_piece()).__name__ is chess_r7_switch[rows][col]

    # for player 2 Light Bottom Current Player
    # index for chess_r7_switch to get the correct name in row 0 or 1
    for rows in [0, 1]:
        # index of column in both chess_r7_switch and the board
        for col in range(len(chess_r7_switch[rows])):
            # for correct row in the board
            if rows == 0:
                row = 7
            else:
                row = 6
            # check if each peace are the correct colour and at the right spot
            assert my_board.get_game_square(
                row, col).get_occupying_piece().get_colour() == "White"
            assert type(my_board.get_game_square(
                row, col).get_occupying_piece()).__name__ is chess_r7_switch[rows][col]

    # -----Checkers-----
    # Game Type 1 is Checkers
    my_board_checkers = Board(8)
    lp_checkers_pieces = PieceSet(1, "White")
    dp_checkers_pieces = PieceSet(1, "Black")

    # list of index inside piece set for light player and dark player
    # 0, 4, 8 are indexes in the list of checkers pieces in pieceSet for a player
    # used so we can evenly take away checkers and put it in the board
    checker_indexes = [[0, 4, 8], [0, 4, 8]]
    # iterating through columns 0, 2, 4, 6
    # these are the column index where the piece will be set
    for col in range(0, 8, 2):
        # put the checkrs piece from dark or light player piece set using specific index
        # in specific row, col in board
        # 7, 6 are for the dark player and 1 is for light player these
        # these numbers are specific rows where player piece start from edge column
        my_board_checkers.get_game_square(7, col).put_piece_here(dp_checkers_pieces
                                                                 .get_live_pieces()[checker_indexes[0][0]])
        my_board_checkers.get_game_square(5, col).put_piece_here(lp_checkers_pieces
                                                                 .get_live_pieces()[checker_indexes[1][1]])
        my_board_checkers.get_game_square(1, col).put_piece_here(dp_checkers_pieces
                                                                 .get_live_pieces()[checker_indexes[0][2]])
        checker_indexes[0][0] += 1
        checker_indexes[1][1] += 1
        checker_indexes[0][2] += 1

    # iterating through columns 1, 3, 5, 7
    # these are the column index where the piece will be set
    for col in range(1, 8, 2):
        # put the checkrs piece from dark or light player piece set using specific index
        # in specific row, col in board
        # 6 is for the dark player and 2, 0 are for light player
        # these numbers are specific rows where player piece start from edge column
        my_board_checkers.get_game_square(6, col).put_piece_here(dp_checkers_pieces
                                                                 .get_live_pieces()[checker_indexes[0][1]])
        my_board_checkers.get_game_square(2, col).put_piece_here(lp_checkers_pieces
                                                                 .get_live_pieces()[checker_indexes[1][2]])
        my_board_checkers.get_game_square(0, col).put_piece_here(lp_checkers_pieces
                                                                 .get_live_pieces()[checker_indexes[1][0]])
        checker_indexes[0][1] += 1
        checker_indexes[1][2] += 1
        checker_indexes[1][0] += 1

    # TESTS STARTS FOR CHECKERS
    # test if the game square in the board are all game squares after adding the pieces to each game square
    # test if the game square received the pieces
    # check if a square has a piece to check if it is one of the pieces in string
    # test if game squares have the right row and column
    row = 0
    for row_gs in my_board_checkers.get_game_board():
        col = 0
        for col_gs in row_gs:
            assert type(col_gs) is type(a_game_square)
            if col_gs.get_occupying_piece() is not None:
                pieces_colour = ["White", "Black"]
                assert type(col_gs.get_occupying_piece()
                            ).__name__ is "CheckersCoin"
                assert col_gs.get_occupying_piece().get_colour() in pieces_colour
            assert col_gs.get_row() is row
            assert col_gs.get_col() is col
            col += 1
        row += 1

    assert my_board_checkers.get_game_square(
        7, 0).get_occupying_piece().get_colour() is "Black"
    my_board_checkers.switch_sides()
    assert my_board_checkers.get_game_square(
        7, 0).get_occupying_piece().get_colour() is "White"


def test_integration_3():
    """
    Testing Player.py and PieceSet.py
    Note: Does not follow the test plan
    """
    # testing Player.py and PieceSet.py
    p1_name = "DarkPlayer"
    p2_name = "LightPlayer"
    # need to be in the look up table in Colours.py
    p1_colour = "Black"
    p2_colour = "White"
    # Game type can be 0 -> chess or 1 -> checkers
    game_type_chess = 0
    game_type_checkers = 1
    # player type can be PlayerType.{HUMAN, AI}
    # HUMAN = 1, AI = 0
    p1_type = PlayerType.HUMAN
    p2_type = PlayerType.AI
    # Timer set at 60 and to be inactive
    timer = Timer(60, False)

    # tests if correct player and pieces are made when a player is created
    # tests for attributes
    # checks for pieces to be correctly made
    # What kind of pieces is in the set depending on the game type
    # chess will have its 16 pieces and checkers will have its 12 pieces
    # makes sure kinds of pieces are in there

    # tests for CHESS and HUMAN
    player1 = Player(p1_name, p1_colour, game_type_chess, p1_type, timer)
    player1_pieceset = player1.get_piece_set()
    assert player1_pieceset.get_colour() is p1_colour
    assert not player1.get_castled()
    assert player1.get_name() is p1_name
    assert player1.get_player_type() is 1
    assert player1.get_timer() is timer
    assert player1_pieceset.get_number_of_live_pieces() == 16
    assert player1_pieceset.get_number_of_captured_pieces() == 0
    assert player1_pieceset.get_captured_pieces() == []
    for pieces in player1_pieceset.get_live_pieces():
        assert type(pieces).__name__ in [
            "Rook", "Knight", "Bishop", "Queen", "King", "Pawn"]

    # tests for CHESS and AI
    player2 = Player(p2_name, p2_colour, game_type_chess, p2_type, timer)
    player2_pieceset = player2.get_piece_set()
    assert player2_pieceset.get_colour() is p2_colour
    assert not player2.get_castled()
    assert player2.get_name() is p2_name
    assert player2.get_player_type() is 0
    assert player2.get_timer() is timer
    assert player2_pieceset.get_number_of_live_pieces() == 16
    assert player2_pieceset.get_number_of_captured_pieces() == 0
    assert player2_pieceset.get_captured_pieces() == []
    for pieces in player2_pieceset.get_live_pieces():
        assert type(pieces).__name__ in [
            "Rook", "Knight", "Bishop", "Queen", "King", "Pawn"]

    # tests for CHECKERS and HUMAN
    player1 = Player(p1_name, p1_colour, game_type_checkers, p1_type, timer)
    player1_pieceset = player1.get_piece_set()
    assert player1_pieceset.get_colour() is p1_colour
    assert player1.get_name() is p1_name
    assert player1.get_player_type() is 1
    assert player1.get_timer() is timer
    assert player1_pieceset.get_number_of_live_pieces() == 12
    assert player1_pieceset.get_number_of_captured_pieces() == 0
    assert player1_pieceset.get_captured_pieces() == []
    for pieces in player1_pieceset.get_live_pieces():
        assert type(pieces).__name__ in ["CheckersCoin"]

    # tests for CHECKERS and AI
    player2 = Player(p2_name, p2_colour, game_type_checkers, p2_type, timer)
    player2_pieceset = player2.get_piece_set()
    assert player2_pieceset.get_colour() is p2_colour
    assert player2.get_name() is p2_name
    assert player2.get_player_type() is 0
    assert player2.get_timer() is timer
    assert player2_pieceset.get_number_of_live_pieces() == 12
    assert player2_pieceset.get_number_of_captured_pieces() == 0
    assert player2_pieceset.get_captured_pieces() == []
    for pieces in player2_pieceset.get_live_pieces():
        assert type(pieces).__name__ in ["CheckersCoin"]


def test_integration_4():
    """
    Testing the integration of Player.py, PieceSet.py, Pieces.py, and Game.py
    Note: Does not follow the test plan
    """

    # game types chess = 0 checkers = 1
    gt_chess = 0
    gt_checkers = 1
    # Piece Set colours for players
    gc_wb = ColourCodes.WHITE_BLACK
    gc_rb = ColourCodes.RED_BLACK

    # create a chess and checkers game
    my_chess_game = Game(gt_chess, gc_wb)
    my_checkers_game = Game(gt_checkers, gc_rb)

    # test if game is initialized correctly
    # for chess game
    assert my_chess_game.get_game_type() == gt_chess
    assert my_chess_game.get_light_player() is None
    assert my_chess_game.get_dark_player() is None
    assert my_chess_game.get_current_player() is None

    # for checkers game
    assert my_checkers_game.get_game_type() == gt_checkers
    assert my_checkers_game.get_light_player() is None
    assert my_checkers_game.get_dark_player() is None
    assert my_checkers_game.get_current_player() is None

    # pl - player light pd player dark
    pt_human = PlayerType.HUMAN
    pt_ai = PlayerType.AI

    # Timer set at 60 and to be inactive
    timer = Timer(60, False)

    # build the players in game

    # chess player light human 1st turn
    my_chess_game.build_light_player("Light HU", pt_human, timer)
    pl_chess = my_chess_game.get_light_player()
    pc_chess = my_chess_game.get_current_player()

    # chess player dark ai 2nd turn
    my_chess_game.build_dark_player("Dark AI", pt_ai, timer)
    pd_chess = my_chess_game.get_dark_player()

    # checkers player light ai 1st turn
    my_checkers_game.build_light_player("Light AI", pt_ai, timer)
    pl_checkers = my_checkers_game.get_light_player()
    pc_checkers = my_checkers_game.get_current_player()

    # checkers player dark human 2nd turn
    my_checkers_game.build_dark_player("Dark HU", pt_human, timer)
    pd_checkers = my_checkers_game.get_dark_player()

    # TESTS
    # - Attribute Test
    #   test if built correctly
    #   check correct game type
    #   check for colour for right players
    #   check their pieces

    # -- CHESS
    # --- main game testing
    assert my_chess_game.get_game_type() == gt_chess
    assert pl_chess.get_colour(
    ) is COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.WHITE_BLACK][ColourOffset.OFFSET_LIGHT]
    assert pd_chess.get_colour(
    ) is COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.WHITE_BLACK][ColourOffset.OFFSET_DARK]
    assert pc_chess.get_colour(
    ) is COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.WHITE_BLACK][ColourOffset.OFFSET_LIGHT]

    # --- player light human testing
    assert not pl_chess.get_castled()
    assert pl_chess.get_name() is "Light HU"
    assert pl_chess.get_player_type() is 1
    assert pl_chess.get_timer() is timer
    assert pl_chess.get_piece_set().get_number_of_live_pieces() == 16
    assert pl_chess.get_piece_set().get_number_of_captured_pieces() == 0
    assert pl_chess.get_piece_set().get_captured_pieces() == []
    for pieces in pl_chess.get_piece_set().get_live_pieces():
        assert type(pieces).__name__ in [
            "Rook", "Knight", "Bishop", "Queen", "King", "Pawn"]

    # --- player dark ai testing
    assert not pd_chess.get_castled()
    assert pd_chess.get_name() is "Dark AI"
    assert pd_chess.get_player_type() is 0
    assert pd_chess.get_timer() is timer
    assert pd_chess.get_piece_set().get_number_of_live_pieces() == 16
    assert pd_chess.get_piece_set().get_number_of_captured_pieces() == 0
    assert pd_chess.get_piece_set().get_captured_pieces() == []
    for pieces in pd_chess.get_piece_set().get_live_pieces():
        assert type(pieces).__name__ in [
            "Rook", "Knight", "Bishop", "Queen", "King", "Pawn"]

    # --- current player
    assert not pc_chess.get_castled()
    assert pc_chess.get_name() is "Light HU"
    assert pc_chess.get_player_type() is 1
    assert pc_chess.get_timer() is timer
    assert pc_chess.get_piece_set().get_number_of_live_pieces() == 16
    assert pc_chess.get_piece_set().get_number_of_captured_pieces() == 0
    assert pc_chess.get_piece_set().get_captured_pieces() == []
    for pieces in pc_chess.get_piece_set().get_live_pieces():
        assert type(pieces).__name__ in [
            "Rook", "Knight", "Bishop", "Queen", "King", "Pawn"]
    assert pc_chess is pl_chess

    # -- CHECKERS
    assert my_checkers_game.get_game_type() == gt_checkers
    assert pl_checkers.get_colour(
    ) is COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.RED_BLACK][ColourOffset.OFFSET_LIGHT]
    assert pd_checkers.get_colour(
    ) is COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.RED_BLACK][ColourOffset.OFFSET_DARK]
    assert pc_checkers.get_colour(
    ) is COLOUR_STRING_LOOK_UP_TABLE[ColourCodes.RED_BLACK][ColourOffset.OFFSET_LIGHT]

    # --- player light ai testing
    assert pl_checkers.get_name() is "Light AI"
    assert pl_checkers.get_player_type() is 0
    assert pl_checkers.get_timer() is timer
    assert pl_checkers.get_piece_set().get_number_of_live_pieces() == 12
    assert pl_checkers.get_piece_set().get_number_of_captured_pieces() == 0
    assert pl_checkers.get_piece_set().get_captured_pieces() == []
    for pieces in pl_checkers.get_piece_set().get_live_pieces():
        assert type(pieces).__name__ in ["CheckersCoin"]

    # --- player dark human testing
    assert pd_checkers.get_name() is "Dark HU"
    assert pd_checkers.get_player_type() is 1
    assert pd_checkers.get_timer() is timer
    assert pd_checkers.get_piece_set().get_number_of_live_pieces() == 12
    assert pd_checkers.get_piece_set().get_number_of_captured_pieces() == 0
    assert pd_checkers.get_piece_set().get_captured_pieces() == []
    for pieces in pd_checkers.get_piece_set().get_live_pieces():
        assert type(pieces).__name__ in ["CheckersCoin"]

    # --- current player testing
    assert pc_checkers.get_name() is "Light AI"
    assert pc_checkers.get_player_type() is 0
    assert pc_checkers.get_timer() is timer
    assert pc_checkers.get_piece_set().get_number_of_live_pieces() == 12
    assert pc_checkers.get_piece_set().get_number_of_captured_pieces() == 0
    assert pc_checkers.get_piece_set().get_captured_pieces() == []
    for pieces in pc_checkers.get_piece_set().get_live_pieces():
        assert type(pieces).__name__ in ["CheckersCoin"]
    assert pc_checkers is pl_checkers

    # - Test change in player
    #   check if players are correctly assigned after changing players
    #   change current player

    # -- CHESS
    assert pc_chess is pl_chess
    # my_chess_game.change_current_player()
    # pc_chess = my_chess_game.get_current_player()
    # assert pc_chess is not pl_chess
    # assert pc_chess is pd_chess

    # -- CHECKERS
    assert pc_checkers is pl_checkers
    # my_checkers_game.change_current_player()
    # pc_checkers = my_checkers_game.get_current_player()
    # assert pc_checkers is not pl_checkers
    # assert pc_checkers is pd_checkers


def test_integration_5():
    """
    Testing the integration of GameSquare.py, Boards.py, Pieces.py, PieceSet.py, Player.py, and Game.py
    basically combining test_integration_2 and test_integration_4
    Note: Does not follow the test plan
    """

    # game types chess = 0 checkers = 1
    gt_chess = 0
    gt_checkers = 1
    # Piece Set colours for players
    gc_wb = ColourCodes.WHITE_BLACK
    gc_rb = ColourCodes.RED_BLACK

    # create a chess and checkers game
    my_chess_game = Game(gt_chess, gc_wb)
    my_checkers_game = Game(gt_checkers, gc_rb)

    # test if game is initialized correctly
    # for chess game
    assert my_chess_game.get_game_type() == gt_chess
    assert my_chess_game.get_light_player() is None
    assert my_chess_game.get_dark_player() is None
    assert my_chess_game.get_current_player() is None

    # for checkers game
    assert my_checkers_game.get_game_type() == gt_checkers
    assert my_checkers_game.get_light_player() is None
    assert my_checkers_game.get_dark_player() is None
    assert my_checkers_game.get_current_player() is None

    # pl - player light pd player dark
    pt_human = PlayerType.HUMAN
    pt_ai = PlayerType.AI

    # Timer set at 60 and to be inactive
    timer = Timer(60, False)

    # build the players in game

    # chess player light human 1st turn
    my_chess_game.build_light_player("Light HU", pt_human, timer)

    # chess player dark ai 2nd turn
    my_chess_game.build_dark_player("Dark AI", pt_ai, timer)

    # checkers player light ai 1st turn
    my_checkers_game.build_light_player("Light AI", pt_ai, timer)

    # checkers player dark human 2nd turn
    my_checkers_game.build_dark_player("Dark HU", pt_human, timer)

    # Build Chess Board on my_chess_game using the games light and dark player piece set
    my_chess_game.get_board().build_chess_board(my_chess_game.get_light_player().get_piece_set().get_live_pieces(),
                                                my_chess_game.get_dark_player().get_piece_set().get_live_pieces())

    # Build Checkers Board on my_checkers_game using the games light and dark player piece set
    my_checkers_game.get_board().build_checkers_board(
        my_checkers_game.get_light_player().get_piece_set().get_live_pieces(),
        my_checkers_game.get_dark_player().get_piece_set().get_live_pieces())

    # TESTS
    # - Test for pieces on correct spots

    # -- CHESS
    # list of String names of pieces in chess
    chess_r7 = [["Rook", "Knight", "Bishop", "Queen",
                 "King", "Bishop", "Knight", "Rook"], ["Pawn"]]

    # --- player light human
    # index for chess_r7 to get the correct name in row 6 or 7
    for rows in [0, 1]:
        # index of column in both chess_r7 and the board
        for col in range(len(chess_r7[rows])):
            # for correct row in the board
            if rows == 0:
                row = 7
            else:
                row = 6
            # check if each peace are the correct colour and at the right spot
            assert my_chess_game.get_board().get_game_square(
                row, col).get_occupying_piece().get_colour() == "White"
            assert type(my_chess_game.get_board().get_game_square(row, col).get_occupying_piece()).__name__ is \
                chess_r7[rows][col]

    # --- player dark ai
    # index for chess_r7 to get the correct name in row 0 or 1
    for rows in [0, 1]:
        # index of column in both chess_r7 and the board
        for col in range(len(chess_r7[rows])):
            # for correct row in the board
            if rows == 0:
                row = 0
            else:
                row = 1
            # check if each peace are the correct colour and at the right spot
            assert my_chess_game.get_board().get_game_square(
                row, col).get_occupying_piece().get_colour() == "Black"
            assert type(my_chess_game.get_board().get_game_square(row, col).get_occupying_piece()).__name__ is \
                chess_r7[rows][col]

    # --- game suares in middle of board are empty
    # middle rows of the game board rows 2 to 5
    for row in range(2, 6):
        for col in range(my_chess_game.get_board().get_size()):
            assert my_chess_game.get_board().get_game_square(
                row, col).get_occupying_piece() is None

    # -- CHECKERS

    # test if checkers coin are correctly placed in the board for eache player

    # determines what we are looking at in a specific col
    # 0 if square has none and 1 if it has a coin
    x = 0

    # player colour index currently checking
    # y = 0 dark player y = 1 light player
    y = 0

    checker_colour = ["Black", "Red"]
    for row in range(my_checkers_game.get_board().get_size()):
        for col in range(my_checkers_game.get_board().get_size()):
            # rows 3 and 4 are middle rows that are empty
            if row == 3 or row == 4:
                assert my_checkers_game.get_board().get_game_board()[
                    row][col].get_occupying_piece() is None
                # done checking dark player
                y = 1

            # rows 0, 1, 2, 5, 6, 7 are top and bottom rows where coins are located
            else:
                # checker coin pattern
                # checks for none,coin pattern on board
                # pattern does not change at col 7
                if x == 0:
                    assert my_checkers_game.get_board().get_game_board()[
                        row][col].get_occupying_piece() is None
                    if col != my_checkers_game.get_board().get_size() - 1:
                        x = 1
                else:
                    assert type(my_checkers_game.get_board().get_game_board()[row][
                        col].get_occupying_piece()).__name__ is "CheckersCoin"
                    assert my_checkers_game.get_board().get_game_board()[row][col].get_occupying_piece().get_colour() \
                        is checker_colour[y]

                    if col != my_checkers_game.get_board().get_size() - 1:
                        x = 0

    # - Test after switching sides

    # -- CHESS
    my_chess_game.get_board().switch_sides()

    # list of String names of pieces in chess but queen and king switch because of the rotation
    chess_nr7 = [["Rook", "Knight", "Bishop", "King",
                  "Queen", "Bishop", "Knight", "Rook"], ["Pawn"]]

    # --- player light human
    # index for chess_r7 to get the correct name in row 6 or 7
    for rows in [0, 1]:
        # index of column in both chess_r7 and the board
        for col in range(len(chess_nr7[rows])):
            # for correct row in the board
            if rows == 0:
                row = 7
            else:
                row = 6
            # check if each peace are the correct colour and at the right spot
            assert my_chess_game.get_board().get_game_square(
                row, col).get_occupying_piece().get_colour() == "Black"
            assert type(my_chess_game.get_board().get_game_square(row, col).get_occupying_piece()).__name__ is \
                chess_nr7[rows][col]

    # --- player dark ai
    # index for chess_r7 to get the correct name in row 0 or 1
    for rows in [0, 1]:
        # index of column in both chess_r7 and the board
        for col in range(len(chess_nr7[rows])):
            # for correct row in the board
            if rows == 0:
                row = 0
            else:
                row = 1
            # check if each peace are the correct colour and at the right spot
            assert my_chess_game.get_board().get_game_square(
                row, col).get_occupying_piece().get_colour() == "White"
            assert type(my_chess_game.get_board().get_game_square(row, col).get_occupying_piece()).__name__ is \
                chess_nr7[rows][col]

    # --- game suares in middle of board are empty
    # middle rows of the game board rows 2 to 5
    for row in range(2, 6):
        for col in range(my_chess_game.get_board().get_size()):
            assert my_chess_game.get_board().get_game_square(
                row, col).get_occupying_piece() is None

    # -- CHECKERS
    my_checkers_game.get_board().switch_sides()

    # determines what we are looking at in a specific col
    # 0 if square has none and 1 if it has a coin
    x = 0

    # player colour index currently checking
    # y = 0 dark player y = 1 light player
    y = 0

    checker_colour = ["Red", "Black"]
    for row in range(my_checkers_game.get_board().get_size()):
        for col in range(my_checkers_game.get_board().get_size()):
            # rows 3 and 4 are middle rows that are empty
            if row == 3 or row == 4:
                assert my_checkers_game.get_board().get_game_board()[
                    row][col].get_occupying_piece() is None
                # done checking dark player
                y = 1

            # rows 0, 1, 2, 5, 6, 7 are top and bottom rows where coins are located
            else:
                # checker coin pattern
                # checks for none,coin pattern on board
                # pattern does not change at col 7
                if x == 0:
                    assert my_checkers_game.get_board().get_game_board()[
                        row][col].get_occupying_piece() is None
                    if col != my_checkers_game.get_board().get_size() - 1:
                        x = 1
                else:
                    assert type(my_checkers_game.get_board().get_game_board()[row][col].
                                get_occupying_piece()).__name__ is "CheckersCoin"
                    assert my_checkers_game.get_board().get_game_board()[row][col].get_occupying_piece().get_colour() \
                        is checker_colour[y]

                    if col != my_checkers_game.get_board().get_size() - 1:
                        x = 0


def test_integration_6():
    """
    Testing the integration of GameSquare.py, Boards.py, Pieces.py, PieceSet.py, Player.py, Game.py, build_list_of_moves.py
    Note: Does not follow the test plan
    """
    # game types chess = 0 checkers = 1
    gt_chess = 0
    gt_checkers = 1
    # Piece Set colours for players
    gc_wb = ColourCodes.WHITE_BLACK
    gc_rb = ColourCodes.RED_BLACK

    # create a chess and checkers game
    my_chess_game = Game(gt_chess, gc_wb)
    my_checkers_game = Game(gt_checkers, gc_rb)

    # pl - player light pd player dark
    pt_human = PlayerType.HUMAN
    pt_ai = PlayerType.AI

    # Timer set at 60 and to be inactive
    timer = Timer(60, False)

    # build the players in game

    # chess player light human 1st turn
    my_chess_game.build_light_player("Light HU", pt_human, timer)

    # chess player dark ai 2nd turn
    my_chess_game.build_dark_player("Dark AI", pt_ai, timer)

    # checkers player light ai 1st turn
    my_checkers_game.build_light_player("Light AI", pt_ai, timer)

    # checkers player dark human 2nd turn
    my_checkers_game.build_dark_player("Dark HU", pt_human, timer)

    # Build Chess Board on my_chess_game using the games light and dark player piece set
    my_chess_game.get_board().build_chess_board(my_chess_game.get_light_player().get_piece_set().get_live_pieces(),
                                                my_chess_game.get_dark_player().get_piece_set().get_live_pieces())

    # Build Checkers Board on my_checkers_game using the games light and dark player piece set
    my_checkers_game.get_board().build_checkers_board(
        my_checkers_game.get_light_player().get_piece_set().get_live_pieces(),
        my_checkers_game.get_dark_player().get_piece_set().get_live_pieces())

    # -----TESTS-----
    # test if the possible moves at  the start of the game is normal
    # test row 7 and 6 where the current player takes a turn

    # Testing Chess
    # pieces on rows 7 and 6 respectively
    # ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
    # ["Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn", "Pawn"]
    # expected possible moves at the start of the game for the pieces on rows 7 and 6 respectively
    chess_r7_pm = [[], [(5, 0), (5, 2)], [], [], [], [], [(5, 5), (5, 7)], []]
    chess_r6_pm = [[(5, 0), (4, 0)], [(5, 1), (4, 1)], [(5, 2), (4, 2)], [(5, 3), (4, 3)],
                   [(5, 4), (4, 4)], [(5, 5), (4, 5)], [(5, 6), (4, 6)], [(5, 7), (4, 7)]]
    # light player
    for row in range(7, 5, -1):
        for col in range(0, 8):
            assert my_chess_game.get_board().get_game_square(
                row, col).get_occupying_piece().get_colour() is "White"
            if row == 7:
                my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(row, col),
                                                                   my_chess_game)
                assert sorted([x.get_row_and_column()
                               for x in my_moves]) == sorted(chess_r7_pm[col])
            if row == 6:
                my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(row, col),
                                                                   my_chess_game)
                assert sorted([x.get_row_and_column()
                               for x in my_moves]) == sorted(chess_r6_pm[col])

    # switch player
    my_chess_game.get_board().switch_sides()
    # current player change to dark player
    # only difference should be the switch possition of the King and Queen
    # but at the start of the turn nothing changes on the expected possible moves

    # dark player
    for row in range(7, 5, -1):
        for col in range(0, 8):
            assert my_chess_game.get_board().get_game_square(
                row, col).get_occupying_piece().get_colour() is "Black"
            if row == 7:
                my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(row, col),
                                                                   my_chess_game)
                assert sorted([x.get_row_and_column()
                               for x in my_moves]) == sorted(chess_r7_pm[col])
            if row == 6:
                my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(row, col),
                                                                   my_chess_game)
                assert sorted([x.get_row_and_column()
                               for x in my_moves]) == sorted(chess_r6_pm[col])

    # One more switch
    my_chess_game.get_board().switch_sides()

    # back to light player
    # should be the same as before the first switch
    # light player
    for row in range(7, 5, -1):
        for col in range(0, 8):
            assert my_chess_game.get_board().get_game_square(
                row, col).get_occupying_piece().get_colour() is "White"
            if row == 7:
                my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(row, col),
                                                                   my_chess_game)
                assert sorted([x.get_row_and_column()
                               for x in my_moves]) == sorted(chess_r7_pm[col])
            if row == 6:
                my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(row, col),
                                                                   my_chess_game)
                assert sorted([x.get_row_and_column()
                               for x in my_moves]) == sorted(chess_r6_pm[col])

    # testing Checkers

    # light player
    # the row that will have the piece are 7, 6, 5
    # there will be a max of 4 coins in a given row
    checkers_r7_pv = [[], [], [], []]
    checkers_r6_pv = [[], [], [], []]
    checkers_r5_pv = [[(4, 1)], [(4, 1), (4, 3)], [
        (4, 3), (4, 5)], [(4, 5), (4, 7)]]

    # start is where checkers start at each row
    start = 0
    for row in range(7, 4, -1):
        col_count = 0
        for col in range(start, 8, 2):
            assert my_checkers_game.get_board().get_game_square(
                row, col).get_occupying_piece().get_colour() is "Red"
            if row == 7:
                my_moves = build_list_of_moves.build_list_of_moves(my_checkers_game.get_board().get_game_square(row, col),
                                                                   my_checkers_game)
                assert sorted([x.get_row_and_column() for x in my_moves]) == sorted(
                    checkers_r7_pv[col_count])
                start = 1
            elif row == 6:
                my_moves = build_list_of_moves.build_list_of_moves(my_checkers_game.get_board().get_game_square(row, col),
                                                                   my_checkers_game)
                assert sorted([x.get_row_and_column() for x in my_moves]) == sorted(
                    checkers_r6_pv[col_count])
                start = 0
            elif row == 5:
                my_moves = build_list_of_moves.build_list_of_moves(my_checkers_game.get_board().get_game_square(row, col),
                                                                   my_checkers_game)
                assert sorted([x.get_row_and_column() for x in my_moves]) == sorted(
                    checkers_r5_pv[col_count])
            col_count += 1

    # switch checkers player
    my_checkers_game.get_board().switch_sides()

    # dark player
    # should have the same possible moves start as the light player
    # switched sides
    start = 0
    for row in range(7, 4, -1):
        col_count = 0
        for col in range(start, 8, 2):
            assert my_checkers_game.get_board().get_game_square(row,
                                                                col).get_occupying_piece().get_colour() is "Black"
            if row == 7:
                my_moves = build_list_of_moves.build_list_of_moves(my_checkers_game.get_board().get_game_square(row, col),
                                                                   my_checkers_game)
                assert sorted([x.get_row_and_column() for x in my_moves]) == sorted(
                    checkers_r7_pv[col_count])
                start = 1
            elif row == 6:
                my_moves = build_list_of_moves.build_list_of_moves(my_checkers_game.get_board().get_game_square(row, col),
                                                                   my_checkers_game)
                assert sorted([x.get_row_and_column() for x in my_moves]) == sorted(
                    checkers_r6_pv[col_count])
                start = 0
            elif row == 5:
                my_moves = build_list_of_moves.build_list_of_moves(my_checkers_game.get_board().get_game_square(row, col),
                                                                   my_checkers_game)
                assert sorted([x.get_row_and_column() for x in my_moves]) == sorted(
                    checkers_r5_pv[col_count])
            col_count += 1

    # switch it back to light first
    my_checkers_game.get_board().switch_sides()

    # light player is at bottom again
    # make sure nothing changed
    start = 0
    for row in range(7, 4, -1):
        col_count = 0
        for col in range(start, 8, 2):
            assert my_checkers_game.get_board().get_game_square(row,
                                                                col).get_occupying_piece().get_colour() is "Red"
            if row == 7:
                my_moves = build_list_of_moves.build_list_of_moves(my_checkers_game.get_board().get_game_square(row, col),
                                                                   my_checkers_game)
                assert sorted([x.get_row_and_column() for x in my_moves]) == sorted(
                    checkers_r7_pv[col_count])
                start = 1
            elif row == 6:
                my_moves = build_list_of_moves.build_list_of_moves(my_checkers_game.get_board().get_game_square(row, col),
                                                                   my_checkers_game)
                assert sorted([x.get_row_and_column() for x in my_moves]) == sorted(
                    checkers_r6_pv[col_count])
                start = 0
            elif row == 5:
                my_moves = build_list_of_moves.build_list_of_moves(my_checkers_game.get_board().get_game_square(row, col),
                                                                   my_checkers_game)
                assert sorted([x.get_row_and_column() for x in my_moves]) == sorted(
                    checkers_r5_pv[col_count])
            col_count += 1

    # Testing pieces interaction with enemy pieces

    # testing Chess
    # list of moves in particular row
    # ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
    # chess row5 test all row
    chess_r5_tar = [[(4, 0), (3, 0), (2, 0), (1, 0)],
                    [(3, 0), (3, 2), (4, 3), (7, 2), (7, 0)],
                    [(4, 1), (3, 0), (4, 3), (3, 4), (2, 5), (1, 6)],
                    [(4, 3), (3, 3), (2, 3), (1, 3), (4, 4), (3, 5),
                     (2, 6), (1, 7), (4, 2), (3, 1), (2, 0)],
                    [(4, 3), (4, 4), (4, 5)],
                    [(4, 6), (3, 7), (4, 4), (3, 3), (2, 2), (1, 1)],
                    [(3, 7), (3, 5), (4, 4), (7, 5), (7, 7)],
                    [(4, 7), (3, 7), (2, 7), (1, 7)]]
    chess_r2_tar = [[(4, 0), (3, 0), (5, 0), (1, 0)],
                    [(0, 0), (0, 2), (1, 3), (4, 0), (4, 2), (3, 3)],
                    [(1, 1), (1, 3), (3, 1), (3, 3), (4, 0), (4, 4), (5, 5)],
                    [(1, 2), (1, 3), (1, 4), (3, 2), (3, 3), (3, 4),
                     (4, 1), (4, 3), (4, 5), (5, 0), (5, 6), (5, 3)],
                    [(1, 3), (1, 4), (1, 5), (3, 3), (3, 4), (3, 5)],
                    [(1, 4), (1, 6), (3, 4), (3, 6), (4, 3), (4, 7), (5, 2)],
                    [(0, 5), (0, 7), (4, 5), (4, 7), (3, 4), (1, 4)],
                    [(4, 7), (3, 7), (5, 7), (1, 7)]]
    # move pieces from prev_row to rows 5 to 2
    # prev_row is where the pecies are currently
    prev_row = 7
    for row in range(5, 1, -3):
        # gets all pieces
        for col in range(8):
            # move piece from (prev_row, col) to (row, col))
            my_chess_game.get_board().get_game_square(row, col).put_piece_here(my_chess_game.get_board().
                                                                               get_game_square(prev_row,
                                                                                               col).get_occupying_piece())
            # remove piece from (prev_row, col)
            my_chess_game.get_board().get_game_square(
                prev_row, col).remove_occupying_piece()
            # prev row now goes to the row because it just relocated the pieces there

        prev_row = 5
        for col2 in range(8):
            # check pieces possible moves in their new positions
            if row == 5:
                my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(row, col2),
                                                                   my_chess_game)
                assert sorted([x.get_row_and_column()
                               for x in my_moves]) == sorted(chess_r5_tar[col2])
            elif row == 2:
                my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(row, col2),
                                                                   my_chess_game)
                assert sorted([x.get_row_and_column()
                               for x in my_moves]) == sorted(chess_r2_tar[col2])

    # testing Checkers

    # test predetermined scenarios
    # checkers row 5 all possible moves
    checkers_r5_apm = [[(3, 2), (1, 0), (1, 4)],
                       [(3, 0), (1, 2), (3, 4), (1, 2), (1, 6)],
                       [(3, 2), (1, 0), (1, 4), (3, 6), (1, 4)],
                       [(3, 4), (1, 2), (1, 6)]]
    # moves checker pieces on row 2 to row 4
    for coin in my_checkers_game.get_board().get_game_board()[2]:
        if coin.get_occupying_piece() is not None:
            my_checkers_game.get_board(). \
                get_game_square(4, coin.get_col()). \
                put_piece_here(my_checkers_game.get_board().get_game_square(
                    2, coin.get_col()).get_occupying_piece())
            my_checkers_game.get_board().get_game_square(
                2, coin.get_col()).remove_occupying_piece()

    # moves checker pieces on row 1 to row 3 and -1 to col as if they are moving bot right
    for coin in my_checkers_game.get_board().get_game_board()[1]:
        if coin.get_occupying_piece() is not None:
            my_checkers_game.get_board(). \
                get_game_square(2, coin.get_col() + 1). \
                put_piece_here(my_checkers_game.get_board().get_game_square(
                    1, coin.get_col()).get_occupying_piece())
            my_checkers_game.get_board().get_game_square(
                1, coin.get_col()).remove_occupying_piece()

    # counter
    x = 0
    for coin in my_checkers_game.get_board().get_game_board()[5]:
        if coin.get_occupying_piece() is not None:
            my_moves = build_list_of_moves.build_list_of_moves(
                coin, my_checkers_game)
            assert sorted([x.get_row_and_column()
                           for x in my_moves]) == sorted(checkers_r5_apm[x])
            x += 1


# ---------------------------------------------------------------------------

def test_check():
    gt_chess = 0
    # Piece Set colours for players
    gc_wb = ColourCodes.WHITE_BLACK

    # create a chess and checkers game
    my_chess_game = Game(gt_chess, gc_wb)

    # pl - player light pd player dark
    pt_human = PlayerType.HUMAN
    pt_ai = PlayerType.AI

    # Timer set at 60 and to be inactive
    timer = Timer(60, False)

    # build the players in game

    # chess player light human 1st turn
    my_chess_game.build_light_player("Light HU", pt_human, timer)

    # chess player dark ai 2nd turn
    my_chess_game.build_dark_player("Dark AI", pt_ai, timer)

    # Build Chess Board on my_chess_game using the games light and dark player piece set
    my_chess_game.get_board().build_chess_board(my_chess_game.get_light_player().get_piece_set().get_live_pieces(),
                                                my_chess_game.get_dark_player().get_piece_set().get_live_pieces())

    # test filter moves using old tests
    my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(7, 4),
                                                       my_chess_game)
    filtered_moves = build_list_of_moves.filter_check_moves(my_chess_game.get_board().get_game_square(7, 4), my_chess_game,
                                                            my_moves)

    assert sorted([x.get_row_and_column() for x in filtered_moves]) == []

    # testing Chess
    # list of moves in particular row
    # ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
    # chess row5 test all row
    chess_r5_tar = [[(4, 0), (3, 0), (2, 0), (1, 0)],
                    [(3, 0), (3, 2), (4, 3), (7, 2), (7, 0)],
                    [(4, 1), (3, 0), (4, 3), (3, 4), (2, 5), (1, 6)],
                    [(4, 3), (3, 3), (2, 3), (1, 3), (4, 4), (3, 5),
                     (2, 6), (1, 7), (4, 2), (3, 1), (2, 0)],
                    [(4, 3), (4, 4), (4, 5)],
                    [(4, 6), (3, 7), (4, 4), (3, 3), (2, 2), (1, 1)],
                    [(3, 7), (3, 5), (4, 4), (7, 5), (7, 7)],
                    [(4, 7), (3, 7), (2, 7), (1, 7)]]
    chess_r2_tar = [[],
                    [],
                    [],
                    [],
                    [(3, 3), (3, 4), (3, 5)],
                    [],
                    [],
                    []]
    # move pieces from prev_row to rows 5 to 2
    # prev_row is where the pecies are currently

    prev_row = 7
    for row in range(5, -1, -3):
        # gets all pieces
        for col in range(8):
            # move piece from (prev_row, col) to (row, col))
            my_chess_game.get_board().get_game_square(row, col). \
                put_piece_here(my_chess_game.get_board().get_game_square(
                    prev_row, col).get_occupying_piece())
            # remove piece from (prev_row, col)
            my_chess_game.get_board().get_game_square(
                prev_row, col).remove_occupying_piece()
            # prev row now goes to the row because it just relocated the pieces there

        prev_row = 5
        for col2 in range(8):
            # check pieces possible moves in their new positions
            if row == 5:
                my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(row, col2),
                                                                   my_chess_game)
                filtered_moves = build_list_of_moves.filter_check_moves(my_chess_game.get_board().get_game_square(row, col2),
                                                                        my_chess_game, my_moves)
                assert sorted([x.get_row_and_column()
                               for x in filtered_moves]) == sorted(chess_r5_tar[col2])
            elif row == 2:
                my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(row, col2),
                                                                   my_chess_game)
                filtered_moves = build_list_of_moves.filter_check_moves(my_chess_game.get_board().get_game_square(row, col2),
                                                                        my_chess_game,
                                                                        my_moves)
                assert sorted([x.get_row_and_column()
                               for x in filtered_moves]) == sorted(chess_r2_tar[col2])

    # test checks and redo the board
    gt_chess = 0
    # Piece Set colours for players
    gc_wb = ColourCodes.WHITE_BLACK

    # create a chess and checkers game
    my_chess_game = Game(gt_chess, gc_wb)

    # pl - player light pd player dark
    pt_human = PlayerType.HUMAN
    pt_ai = PlayerType.AI

    # Timer set at 60 and to be inactive
    timer = Timer(60, False)

    # build the players in game

    # chess player light human 1st turn
    my_chess_game.build_light_player("Light HU", pt_human, timer)

    # chess player dark ai 2nd turn
    my_chess_game.build_dark_player("Dark AI", pt_ai, timer)

    # Build Chess Board on my_chess_game using the games light and dark player piece set
    my_chess_game.get_board().build_chess_board(my_chess_game.get_light_player().get_piece_set().get_live_pieces(),
                                                my_chess_game.get_dark_player().get_piece_set().get_live_pieces())

    # creating scenarios where king get check if a particular piece moves
    # queen checks if pawn at (1, 3) moves

    # moves queen to position
    my_chess_game.get_board().get_game_square(4, 0). \
        put_piece_here(my_chess_game.get_board().get_game_square(
            7, 3).get_occupying_piece())
    my_chess_game.get_board().get_game_square(7, 3).remove_occupying_piece()

    my_chess_game.get_board().switch_sides()
    # pawn at (6, 4)
    my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(6, 4),
                                                       my_chess_game)
    filtered_moves = build_list_of_moves.filter_check_moves(my_chess_game.get_board().get_game_square(6, 4),
                                                            my_chess_game,
                                                            my_moves)
    assert sorted([x.get_row_and_column()
                   for x in filtered_moves]) == sorted([])

    # switch back
    my_chess_game.get_board().switch_sides()

    # moves queen to un checked position with the same scenario
    my_chess_game.get_board().get_game_square(4, 1). \
        put_piece_here(my_chess_game.get_board().get_game_square(
            4, 0).get_occupying_piece())
    my_chess_game.get_board().get_game_square(4, 0).remove_occupying_piece()

    my_chess_game.get_board().switch_sides()
    # pawn at (6, 4)
    my_moves = build_list_of_moves.build_list_of_moves(my_chess_game.get_board().get_game_square(6, 4),
                                                       my_chess_game)
    filtered_moves = build_list_of_moves.filter_check_moves(my_chess_game.get_board().get_game_square(6, 4),
                                                            my_chess_game,
                                                            my_moves)
    assert sorted([x.get_row_and_column()
                   for x in filtered_moves]) == sorted([(5, 4), (4, 4)])


def test_en_passant():
    """
    Testing the en passant chess move
    Special capture move after a pawn double step
    """
    gt_chess = 0
    # Piece Set colours for players
    gc_wb = ColourCodes.WHITE_BLACK

    # create a chess and checkers game
    my_chess_game = Game(gt_chess, gc_wb)

    # pl - player light pd player dark
    pt_human = PlayerType.HUMAN
    pt_ai = PlayerType.AI

    # Timer set at 60 and to be inactive
    timer = Timer(60, False)

    # build the players in game

    # chess player light human 1st turn
    my_chess_game.build_light_player("Light HU", pt_human, timer)

    # chess player dark ai 2nd turn
    my_chess_game.build_dark_player("Dark AI", pt_ai, timer)

    dark_pawns = []
    light_pawns = []

    for piece in my_chess_game.get_dark_player().get_piece_set().get_live_pieces():
        if type(piece).__name__ is "Pawn":
            dark_pawns.append(piece)

    for piece in my_chess_game.get_light_player().get_piece_set().get_live_pieces():
        if type(piece).__name__ is "Pawn":
            light_pawns.append(piece)

    # build board as en passant scenario

    # scenario 1 for en passant
    my_chess_game.get_board().get_game_square(
        1, 3).put_piece_here(dark_pawns[0])
    my_chess_game.get_board().get_game_square(
        3, 2).put_piece_here(light_pawns[0])

    # scenario 2 for en passant
    my_chess_game.get_board().get_game_square(
        7, 1).put_piece_here(dark_pawns[1])
    my_chess_game.get_board().get_game_square(
        7, 0).put_piece_here(light_pawns[1])

    # scenario 3 for en passant
    my_chess_game.get_board().get_game_square(
        1, 7).put_piece_here(dark_pawns[2])
    my_chess_game.get_board().get_game_square(
        1, 5).put_piece_here(dark_pawns[3])
    my_chess_game.get_board().get_game_square(
        3, 6).put_piece_here(light_pawns[2])

    # scenario 4 for en passant
    my_chess_game.get_board().get_game_square(
        4, 6).put_piece_here(dark_pawns[4])
    my_chess_game.get_board().get_game_square(
        6, 5).put_piece_here(light_pawns[3])
    my_chess_game.get_board().get_game_square(
        6, 7).put_piece_here(light_pawns[4])

    # switch sides for dark player to move
    my_chess_game.get_board().switch_sides()
    # use 2 step for the dark pawn move
    my_chess_game.get_dark_player().make_move(my_chess_game.get_board().get_game_square(6, 4),
                                              my_chess_game.get_board().get_game_square(4, 4),
                                              my_chess_game.get_board())
    # sc 1
    # switch sides for light player to check if the en passant move registers
    my_chess_game.get_board().switch_sides()
    my_moves_s1 = build_list_of_moves.build_list_of_moves(
        my_chess_game.get_board().get_game_square(3, 2), my_chess_game)
    assert sorted([x.get_row_and_column()
                   for x in my_moves_s1]) == sorted([(1, 2), (2, 2), (2, 3)])
    # sc 2
    my_moves_s2 = build_list_of_moves.build_list_of_moves(
        my_chess_game.get_board().get_game_square(7, 0), my_chess_game)
    assert sorted([x.get_row_and_column()
                   for x in my_moves_s2]) == sorted([(6, 0), (5, 0)])
    # sc 3
    # do two one step move
    my_chess_game.get_board().switch_sides()
    my_chess_game.get_dark_player().make_move(my_chess_game.get_board().get_game_square(6, 0),
                                              my_chess_game.get_board().get_game_square(5, 0),
                                              my_chess_game.get_board())
    my_chess_game.get_board().switch_sides()
    my_moves_s3 = build_list_of_moves.build_list_of_moves(
        my_chess_game.get_board().get_game_square(3, 6), my_chess_game)
    assert sorted([x.get_row_and_column()
                   for x in my_moves_s3]) == sorted([(1, 6), (2, 6), (2, 7)])
    # 2nd one step
    my_chess_game.get_board().switch_sides()
    my_chess_game.get_dark_player().make_move(my_chess_game.get_board().get_game_square(5, 0),
                                              my_chess_game.get_board().get_game_square(4, 0),
                                              my_chess_game.get_board())
    my_chess_game.get_board().switch_sides()
    my_moves_s3 = build_list_of_moves.build_list_of_moves(
        my_chess_game.get_board().get_game_square(3, 6), my_chess_game)
    assert sorted([x.get_row_and_column()
                   for x in my_moves_s3]) == sorted([(1, 6), (2, 6)])
    # 1 two step from left pawn
    my_chess_game.get_board().switch_sides()
    my_chess_game.get_dark_player().make_move(my_chess_game.get_board().get_game_square(6, 2),
                                              my_chess_game.get_board().get_game_square(4, 2),
                                              my_chess_game.get_board())
    my_chess_game.get_board().switch_sides()
    my_moves_s3 = build_list_of_moves.build_list_of_moves(
        my_chess_game.get_board().get_game_square(3, 6), my_chess_game)
    assert sorted([x.get_row_and_column()
                   for x in my_moves_s3]) == sorted([(1, 6), (2, 6), (2, 5)])
    # sc 4
    # move right pawn 2 step
    my_chess_game.get_light_player().make_move(my_chess_game.get_board().get_game_square(6, 7),
                                               my_chess_game.get_board().get_game_square(4, 7),
                                               my_chess_game.get_board())
    my_chess_game.get_board().switch_sides()
    # check possible move for an en passant
    my_moves_s4 = build_list_of_moves.build_list_of_moves(
        my_chess_game.get_board().get_game_square(3, 1), my_chess_game)
    assert sorted([x.get_row_and_column()
                   for x in my_moves_s4]) == sorted([(2, 1), (1, 1), (2, 0)])
    my_chess_game.get_board().switch_sides()
    # do the other pawn to 2 step and cause en passant; should only register one
    my_chess_game.get_light_player().make_move(my_chess_game.get_board().get_game_square(6, 5),
                                               my_chess_game.get_board().get_game_square(4, 5),
                                               my_chess_game.get_board())
    my_chess_game.get_board().switch_sides()
    my_moves_s4 = build_list_of_moves.build_list_of_moves(
        my_chess_game.get_board().get_game_square(3, 1), my_chess_game)
    assert sorted([x.get_row_and_column()
                   for x in my_moves_s4]) == sorted([(2, 1), (1, 1), (2, 2)])
