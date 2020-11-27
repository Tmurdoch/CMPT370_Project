# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from build_bishop_moves import build_bishop_moves
from build_rook_moves import build_rook_moves


def build_queen_moves(input_game_square, input_game):
    """
    Build the list of possible moves for a Queen.
    :param input_game_square: GameSquare: The origin game square that you want to build a list of moves for.
    :param input_game: The input game, required to get the game board and game type
    :return list_of_candidate_game_squares: GameSquare[]: List of destination squares the queen can legally move to
    """

    # The queen can be moved any number of unoccupied squares in a straight line vertically, horizontally,
    # or diagonally. This a combination of the way a rook moves and the way bishop moves.

    return build_rook_moves(input_game_square, input_game) + build_bishop_moves(input_game_square, input_game)
