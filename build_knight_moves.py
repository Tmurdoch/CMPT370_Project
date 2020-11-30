# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

from chess_move_adder import chess_move_adder


def build_knight_moves(input_game_square, input_game):
    """
    Build the list of possible moves for a Knight
    :param input_game_square: GameSquare: The origin game square that you want to build a list of moves for.
    :param input_game: The input game, required to get the game board and game type
    :return list_of_candidate_game_squares: GameSquare[]: List of destination squares the knight can legally move to
    """

    input_piece = input_game_square.get_occupying_piece()
    input_row = input_game_square.get_row()
    input_col = input_game_square.get_col()
    input_board = input_game.get_board()
    candidate_game_squares = []

    # Compared to other chess pieces, the knight's movement is unique: it may move two squares vertically and
    # one square horizontally, or two squares horizontally and one square vertically (with both forming the
    # shape of an L). While moving, the knight can jump over pieces to reach its destination.

    # moves up then right
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row - 2, input_col + 1)

    # moves up then left
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row - 2, input_col - 1)

    # moves down then right
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row + 2, input_col + 1)

    # moves down then left
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row + 2, input_col - 1)

    # moves right then up
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row - 1, input_col + 2)

    # moves right then down
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row + 1, input_col + 2)

    # moves left then up
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row - 1, input_col - 2)

    # moves left then down
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row + 1, input_col - 2)

    return candidate_game_squares
