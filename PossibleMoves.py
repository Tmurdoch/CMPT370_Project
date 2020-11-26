# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

import copy
from GameType import GameType
from build_bishop_moves import build_bishop_moves
from build_coin_moves import build_coin_moves
from build_king_moves import build_king_moves
from build_knight_moves import build_knight_moves
from build_pawn_moves import build_pawn_moves
from build_queen_moves import build_queen_moves
from build_rook_moves import build_rook_moves


def build_list_of_moves(input_game_square, input_game):
    """
    For a given game square, this function builds a list of all the legal game squares you can move to. Note: Even on
    success, the list of possible moves might be an empty list.  An empty list means that piece has no legal moves.
    :param input_game_square: GameSquare: The origin game square that you want to build a list of moves for.
    :param input_game: The input game, required to get the game board and game type
    :return list_of_candidate_game_squares: GameSquare[]: List of destination squares you can legally move to
    """
    input_piece = input_game_square.get_occupying_piece()
    input_game_type = input_game.get_game_type()

    if input_game_type == GameType.CHECKERS:
        list_of_candidate_game_squares = build_coin_moves(input_game_square, input_game)

    elif input_game_type == GameType.CHESS:

        if type(input_piece).__name__ == "King":
            list_of_candidate_game_squares = build_king_moves(input_game_square, input_game)

        elif type(input_piece).__name__ == "Queen":
            list_of_candidate_game_squares = build_queen_moves(input_game_square, input_game)

        elif type(input_piece).__name__ == "Bishop":
            list_of_candidate_game_squares = build_bishop_moves(input_game_square, input_game)

        elif type(input_piece).__name__ == "Knight":
            list_of_candidate_game_squares = build_knight_moves(input_game_square, input_game)

        elif type(input_piece).__name__ == "Rook":
            list_of_candidate_game_squares = build_rook_moves(input_game_square, input_game)

        elif type(input_piece).__name__ == "Pawn":
            list_of_candidate_game_squares = build_pawn_moves(input_game_square, input_game)

        else:
            # Could not identify the type of piece
            raise Exception("Could not identify the type of piece")

    else:
        raise Exception("Game mode " + input_game_type.lower() + " is neither chess nor checkers")

    return list_of_candidate_game_squares

# TODO: Not sure what the below functions do or where they should go...


def temp_move(origin_square, destination_square):
    """
    mimics a movement of a piece in the board.
    once used should use undo temp to undo the move
    origin_square: gamesquare where the piece is comming form
    destination_square: gamesquare where the piece is going
    return: piece or None from the destination_sqaure
    """
    previous_destination_piece = None
    # make a copy of the piece on destination if there is one
    if destination_square.get_occupying_piece() is not None:
        previous_destination_piece = copy.deepcopy(
            destination_square.get_occupying_piece())
    destination_square.put_piece_here(origin_square.get_occupying_piece())
    origin_square.remove_occupying_piece()
    return previous_destination_piece


def undo_temp_move(previous_origin_square, previous_destination_square, previous_destination_piece):
    """
    Undo the move that temp_move did
    previous_origin_square: gamesquare what you had for origin_square from temp_move
    previous_destination_square: gamesquare what you had for destination_square from temp_move
    previous_destination_square: None or a piece previously on the destination_square
    """
    previous_origin_square.put_piece_here(
        previous_destination_square.get_occupying_piece())
    previous_destination_square.put_piece_here(previous_destination_piece)


def make_move_and_check(origin_gamesquare, destination_gamesquare, game):
    """
    This mimics moving the a piece from an origin to a destination
    origin_square: gamesquare where the piece is comming form
    destination_square: gamesquare where the piece is going
    return: True if the move cause a check and False if it does not
    """
    board = game.get_board()
    # my temp move
    prev_piece_from_destination = temp_move(
        origin_gamesquare, destination_gamesquare)

    # board switches as if i have actually made that move
    board.switch_sides()

    # my king location
    my_king = None

    # enemy moves currently at the bottom of the board
    # get all their moves
    # also look for where my king is
    enemy_moves = []
    for row in board.get_game_board():
        for gamesquare in row:
            if gamesquare.get_occupying_piece() is not None:
                # get moves of enemy pieces
                if gamesquare.get_occupying_piece().get_colour() is not destination_gamesquare.get_occupying_piece().get_colour():
                    enemy_moves += build_list_of_moves(gamesquare, game)
                # find my king
                if gamesquare.get_occupying_piece().get_colour() is destination_gamesquare.get_occupying_piece().get_colour():
                    if type(gamesquare.get_occupying_piece()).__name__ is "King":
                        my_king = gamesquare

    # make sure you find your king
    if my_king is not None:
        for an_enemy_move in enemy_moves:
            if (my_king.get_row(), my_king.get_col()) == (an_enemy_move.get_row(), an_enemy_move.get_col()):
                # we have to return everything back before the move
                board.switch_sides()
                undo_temp_move(
                    origin_gamesquare, destination_gamesquare, prev_piece_from_destination)
                return True
    else:
        # we have to return everything back before the move
        board.switch_sides()
        undo_temp_move(origin_gamesquare, destination_gamesquare,
                       prev_piece_from_destination)
        raise Exception("Did not find the King")

    # we have to return everything back before the move
    board.switch_sides()
    undo_temp_move(origin_gamesquare, destination_gamesquare,
                   prev_piece_from_destination)
    return False


def filter_check_moves(my_gamesquare, game, list_of_moves_to_be_filtered):
    """
    This creates a filtered list of gamesquares from list_of_moves_to_be_filtered that filter
    all the moves that cause a check
    my_gamesquare: a gamesquare where the piece is moving from
    game: a chess game
    list_of_moves_to_be_filtered: list of gamesquares that is from build_list_of_moves
    returns: filtered_moves which is a list of gamesquares
    """
    # new list
    filtered_moves = []

    # check every move if moves cause a check
    for my_move in list_of_moves_to_be_filtered:
        if not make_move_and_check(my_gamesquare, my_move, game):
            filtered_moves.append(my_move)

    return filtered_moves


# For testing -------------------------------------------


def build_enemy_list_of_moves(gamesquare, game):
    # all of enemy list of moves
    enemy_moves = []
    tmp_game = copy.deepcopy(game)
    tmp_gamesquare = copy.deepcopy(gamesquare)
    board = tmp_game.get_board()

    # switch board to identify enemy moves
    board.switch_sides()

    # checks every game piece in the switched board
    # for every moves that the enemy can make
    for row in board.get_game_board():
        for col in row:
            if col.get_occupying_piece() is not None:
                if col.get_occupying_piece().get_colour() is not tmp_gamesquare.get_occupying_piece().get_colour():
                    # add the game square one by one to the enemy moves
                    enemy_moves += build_list_of_moves(col, tmp_game)
    # switch board back to normal
    board.switch_sides()

    return enemy_moves


def is_king_checked(your_king_gamesquare, game):
    # get all enemy moves
    # compare enemy moves to king position
    # all of enemy list of moves
    enemy_moves = []
    board = game.get_board()

    # switch board to identify enemy moves
    board.switch_sides()

    # checks every game piece in the switched board
    # for every moves that the enemy can make
    for row in board.get_game_board():
        for gamesquare in row:
            if gamesquare.get_occupying_piece() is not None:
                if gamesquare.get_occupying_piece().get_colour() is not your_king_gamesquare.get_occupying_piece().get_colour():
                    # add the game square one by one to the enemy moves
                    enemy_moves += build_list_of_moves(gamesquare, game)

    # check if one of the enemy moves is equal to your kings gamesquare
    for move in enemy_moves:
        if (move.get_row(), move.get_col()) == (your_king_gamesquare.get_row(), your_king_gamesquare.get_col()):
            board.switch_sides()
            return True
    board.switch_sides()
    return False

# -----------------------------------------------------------
