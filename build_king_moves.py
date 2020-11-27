# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch


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
    king_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row + 1, input_col)

    # Check the square immediately above the kings current position
    king_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row - 1, input_col)

    # Check the square immediately left of the kings current position
    king_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row, input_col - 1)

    # Check the square immediately right of the kings current position
    king_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row, input_col + 1)

    # Check the square immediately down and to the left of the kings current position
    king_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row + 1, input_col - 1)

    # Check the square immediately down and to the right of the kings current position
    king_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row + 1, input_col + 1)

    # Check the square immediately up and to the left of the kings current position
    king_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row - 1, input_col - 1)

    # Check the square immediately up and to the right of the kings current position
    king_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row - 1, input_col + 1)

    # Check for Castle opportunity
    #   Requirements for Castling:
    #   - Neither the king nor the chosen rook has previously moved.
    #   - There are no pieces between the king and the chosen rook.
    #   - The king is not currently in check.
    #   - The king does not pass through a square that is attacked by an enemy piece.
    #   - The king does not end up in check. (True of any legal move.)

    if not input_piece.get_moved_yet_status():
        # The king has not moved yet, we can go ahead and check for castle opportunities

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

    # TODO: Review the list of candidate squares, and filter out any that would place the king in check

    return candidate_game_squares


def king_move_adder(input_board, candidate_game_squares, input_piece_colour, candidate_row, candidate_col):
    """
    Evaluates possible game squares to see if they are possible moves for the king.
    :param input_piece_colour: string: The colour of the input piece, used to check if other pieces are friendly
    :param candidate_game_squares:  GameSquare[]: The running list of candidate game squares
    :param input_board: Board: The game board we are working with
    :param candidate_row: int: The row of the square we are considering moving to
    :param candidate_col: int: The col of the square we are considering moving to
    Does not return anything, just appends new moves to the list
    """
    if 0 <= candidate_row < input_board.get_size() and 0 <= candidate_col < input_board.get_size():
        # The candidate square is on the board
        if input_board.get_game_square(candidate_row, candidate_col).get_occupying_piece() is not None:
            # There is a piece at the candidate square, check the for enemy piece
            if input_board.get_game_square(candidate_row, candidate_col).get_occupying_piece() \
                    .get_colour() is not input_piece_colour:
                # Enemy piece, add the capture move
                candidate_game_squares.append(input_board.get_game_square(candidate_row, candidate_col))
            else:
                pass  # Piece is friendly, no moves to add
        else:
            # Square was empty, add it to the list
            candidate_game_squares.append(input_board.get_game_square(candidate_row, candidate_col))