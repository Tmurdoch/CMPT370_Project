# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch
from build_rook_moves import rook_move_adder
from chess_move_adder import chess_move_adder


def build_bishop_moves(input_game_square, input_game):
    """
    Build the list of possible moves for a Bishop
    :param input_game_square: GameSquare: The origin game square that you want to build a list of moves for.
    :param input_game: The input game, required to get the game board and game type
    :return list_of_candidate_game_squares: GameSquare[]: List of destination squares the bishop can legally move to
    """

    input_piece = input_game_square.get_occupying_piece()
    input_row = input_game_square.get_row()
    input_col = input_game_square.get_col()
    input_board = input_game.get_board()
    candidate_game_squares = []

    # The bishop can be moved any number of unoccupied squares in a straight line diagonally.
    # Stop if we see a piece. If piece is unfriendly add the capture move to the list. Here are the step taken:
    #   1. check if the row or column are out of bounds
    #   2. check specific corner from piece
    #   3. will stop until sees a peace
    #   4. if piece friendly stop
    #   5. if non friendly add add (row, col) to possible moves but also stops
    #   6. if empty then add it to list and keep going

    # Top Right
    if input_row > 0:
        for row in range(input_row - 1, -1, -1):
            # If we are not in the last row, then loop up through the remaining rows
            if input_col < input_board.get_size() - 1:
                for col in range(input_col + 1, input_board.get_size()):
                    # if we are not in the last col, then loop up through all the remaining columns
                    if abs(input_row - row) == abs(input_col - col):
                        # Confirm we are on the diagonal and then check the square
                        if not rook_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), row, col):
                            break
            else:
                break

    # Top Left

    if input_row > 0:
        for row in range(input_row - 1, -1, -1):
            # If we are not in the last row, then loop up through the remaining rows
            if input_col > 0:
                for col in range(input_col - 1, -1, -1):
                    # if we are not in the last col, then loop up through all the remaining columns
                    if abs(input_row - row) == abs(input_col - col):
                        # Confirm we are on the diagonal and then check the square
                        if not rook_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), row, col):
                            break
            else:
                break

    # Bottom Right
    if input_row < input_board.get_size() - 1:
        for row in range(input_row + 1, input_board.get_size()):
            # If we are not in the last row, then loop up through the remaining rows
            if input_col < input_board.get_size() - 1:
                # if we are not in the last col, then loop up through all the remaining columns
                for col in range(input_col + 1, input_board.get_size()):
                    if abs(input_row - row) == abs(input_col - col):
                        # Confirm we are on the diagonal and then check the square
                        if not rook_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), row, col):
                            break
            else:
                break

    # Bottom Left
    if input_row < input_board.get_size():
        for row in range(input_row + 1, input_board.get_size()):
            # If we are not in the last row, then loop up through the remaining rows
            if input_col > 0:
                for col in range(input_col - 1, -1, -1):
                    # if we are not in the last col, then loop up through all the remaining columns
                    if abs(input_col - row) == abs(input_col - col):
                        # Confirm we are on the diagonal and then check the square
                        if not rook_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), row, col):
                            break
            else:
                break

    return candidate_game_squares
