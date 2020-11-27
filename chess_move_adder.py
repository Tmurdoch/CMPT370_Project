# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch


def chess_move_adder(input_board, candidate_game_squares, input_piece_colour, candidate_row, candidate_col):
    """
    Evaluates possible game squares to see if they are possible.  Used the following chess pieces:
        - King
        - Knight
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
