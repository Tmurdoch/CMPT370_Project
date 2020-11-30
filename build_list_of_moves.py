# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

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



