# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

from chess_move_adder import chess_move_adder


def build_king_moves(input_game_square, input_game):
    """
    Build the list of possible moves for a King
    :param input_game_square: GameSquare: The origin game square that you want to build a list of moves for.
    :param input_game: The input game, required to get the game board and game type
    :return candidate_game_squares: GameSquare[]: List of destination squares the king can legally move to
    """

    input_piece = input_game_square.get_occupying_piece()
    input_row = input_game_square.get_row()
    input_col = input_game_square.get_col()
    input_board = input_game.get_board()
    candidate_game_squares = []

    # A king can move one square in any direction (horizontally, vertically, or diagonally),
    # unless the square is already occupied by a friendly piece, or the move would place the king in check

    # Check the square immediately below the kings current position
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row + 1, input_col)

    # Check the square immediately above the kings current position
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row - 1, input_col)

    # Check the square immediately left of the kings current position
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row, input_col - 1)

    # Check the square immediately right of the kings current position
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row, input_col + 1)

    # Check the square immediately down and to the left of the kings current position
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row + 1, input_col - 1)

    # Check the square immediately down and to the right of the kings current position
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row + 1, input_col + 1)

    # Check the square immediately up and to the left of the kings current position
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row - 1, input_col - 1)

    # Check the square immediately up and to the right of the kings current position
    chess_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row - 1, input_col + 1)

    # Check for Castle opportunity
    #   Requirements for Castling:
    #   - Neither the king nor the chosen rook has previously moved.
    #   - There are no pieces between the king and the chosen rook.
    #   - The king is not currently in check.
    #   - The king does not pass through a square that is attacked by an enemy piece.
    #   - The king does not end up in check. (True of any legal move.)

    if not input_piece.get_moved_yet_status():
        # The king has not moved yet, we can go ahead and check for castle opportunities
        # playets have different king side and queenside when the board is switched
        # light - > ['Rook  '], ['E     '], ['E     '], ['E     '], ['King  '], ['E     '], ['E     '], ['Rook  ']
        # switch row
        # dark - > ['Rook  '], ['E     '], ['E     '], ['King  '], ['E     '], ['E     '], ['E     '], ['Rook  ']
        # for light player
        if input_game.get_current_player() is input_game.get_light_player():
            # King-side
            if input_board.get_game_square(7, 5).get_occupying_piece() is None and \
                    input_board.get_game_square(7, 6).get_occupying_piece() is None and \
                    input_board.get_game_square(7, 7).get_occupying_piece() is not None:
                if type(input_board.get_game_square(7, 7).get_occupying_piece()).__name__ == "Rook":
                    if input_board.get_game_square(7, 7).get_occupying_piece() \
                            .get_colour() is input_piece.get_colour():
                        if not input_board.get_game_square(7, 7).get_occupying_piece().get_moved_yet_status():
                            candidate_game_squares.append(
                                input_board.get_game_square(7, 7))

            # Queen-side
            if input_board.get_game_square(7, 3).get_occupying_piece() is None and \
                    input_board.get_game_square(7, 2).get_occupying_piece() is None and \
                    input_board.get_game_square(7, 1).get_occupying_piece() is None and \
                    input_board.get_game_square(7, 0).get_occupying_piece() is not None:
                if type(input_board.get_game_square(7, 0).get_occupying_piece()).__name__ == "Rook":
                    if input_board.get_game_square(7, 0).get_occupying_piece() \
                            .get_colour() is input_piece.get_colour():
                        if not input_board.get_game_square(7, 0).get_occupying_piece().get_moved_yet_status():
                            candidate_game_squares.append(
                                input_board.get_game_square(7, 0))
        # for dark player
        if input_game.get_current_player() is input_game.get_dark_player():
            # King-side
            if input_board.get_game_square(7, 1).get_occupying_piece() is None and \
                    input_board.get_game_square(7, 2).get_occupying_piece() is None and \
                    input_board.get_game_square(7, 0).get_occupying_piece() is not None:
                if type(input_board.get_game_square(7, 0).get_occupying_piece()).__name__ == "Rook":
                    if input_board.get_game_square(7, 0).get_occupying_piece() \
                            .get_colour() is input_piece.get_colour():
                        if not input_board.get_game_square(7, 0).get_occupying_piece().get_moved_yet_status():
                            candidate_game_squares.append(
                                input_board.get_game_square(7, 0))

            # Queen-side
            if input_board.get_game_square(7, 4).get_occupying_piece() is None and \
                    input_board.get_game_square(7, 5).get_occupying_piece() is None and \
                    input_board.get_game_square(7, 6).get_occupying_piece() is None and \
                    input_board.get_game_square(7, 7).get_occupying_piece() is not None:
                if type(input_board.get_game_square(7, 7).get_occupying_piece()).__name__ == "Rook":
                    if input_board.get_game_square(7, 7).get_occupying_piece() \
                            .get_colour() is input_piece.get_colour():
                        if not input_board.get_game_square(7, 7).get_occupying_piece().get_moved_yet_status():
                            candidate_game_squares.append(
                                input_board.get_game_square(7, 7))

    # TODO: Review the list of candidate squares, and filter out any that would place the king in check

    return candidate_game_squares
