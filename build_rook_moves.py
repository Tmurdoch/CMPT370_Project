# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch


def build_rook_moves(input_game_square, input_game):
    """
    Build the list of possible moves for a Rook
    :param input_game_square: GameSquare: The origin game square that you want to build a list of moves for.
    :param input_game: The input game, required to get the game board and game type
    :return list_of_candidate_game_squares: GameSquare[]: List of destination squares the rook can legally move to
    """

    input_piece = input_game_square.get_occupying_piece()
    input_row = input_game_square.get_row()
    input_col = input_game_square.get_col()
    input_board = input_game.get_board()
    list_of_candidate_game_squares = []

    # The rook can be moved any number of unoccupied squares in a straight line vertically or horizontally

    # First check fow check for horizontal movements, again stop if we see a piece.  If piece is unfriendly
    # add the capture move to the list.

    # Vertical UP
    # check from piece to top row -- (row, col) -> (0, col)
    row_pos = input_row
    while row_pos != 0:
        row_pos -= 1
        if input_board.get_game_board()[row_pos][input_col].get_occupying_piece() is not None:
            if input_board.get_game_board()[row_pos][input_col].get_occupying_piece().get_colour() == \
                    input_piece.get_colour():
                break
            if input_board.get_game_board()[row_pos][input_col].get_occupying_piece().get_colour() != \
                    input_piece.get_colour():
                # Capture move, add it to the list
                list_of_candidate_game_squares.append(
                    input_board.get_game_board()[row_pos][input_col])
                break
        else:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_board()[row_pos][input_col])

    # Vertical DOWN
    # check from piece to bot row -- (row, col) -> (7, col)
    row_neg = input_row
    while row_neg != input_board.get_size() - 1:
        row_neg += 1
        if input_board.get_game_board()[row_neg][input_col].get_occupying_piece() is not None:
            if input_board.get_game_board()[row_neg][input_col].get_occupying_piece().get_colour() == \
                    input_piece.get_colour():
                break
            if input_board.get_game_board()[row_neg][input_col].get_occupying_piece().get_colour() != \
                    input_piece.get_colour():
                # Capture move, add it to the list
                list_of_candidate_game_squares.append(
                    input_board.get_game_board()[row_neg][input_col])
                break
        else:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_board()[row_neg][input_col])

    # Now check for horizontal movements, again stop if we see a piece.  If piece is unfriendly add the capture
    # move to the list.

    # Horizontal RIGHT
    # check from piece to right col -- (row, col) -> (row, 7)
    col_pos = input_col
    while col_pos != input_board.get_size() - 1:
        col_pos += 1
        if input_board.get_game_board()[input_row][col_pos].get_occupying_piece() is not None:
            if input_board.get_game_board()[input_row][col_pos].get_occupying_piece().get_colour() == \
                    input_piece.get_colour():
                break
            if input_board.get_game_board()[input_row][col_pos].get_occupying_piece().get_colour() != \
                    input_piece.get_colour():
                # Capture move, add it to the list
                list_of_candidate_game_squares.append(
                    input_board.get_game_board()[input_row][col_pos])
                break
        else:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_board()[input_row][col_pos])

    # Horizontal LEFT
    # check from piece to left col -- (row, col) -> (row, 0)
    col_neg = input_col
    while col_neg != 0:
        col_neg -= 1
        if input_board.get_game_board()[input_row][col_neg].get_occupying_piece() is not None:
            if input_board.get_game_board()[input_row][col_neg].get_occupying_piece().get_colour() == \
                    input_piece.get_colour():
                break
            if input_board.get_game_board()[input_row][col_neg].get_occupying_piece().get_colour() != \
                    input_piece.get_colour():
                # Capture move, add it to the list
                list_of_candidate_game_squares.append(
                    input_board.get_game_board()[input_row][col_neg])
                break
        else:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_board()[input_row][col_neg])

    return list_of_candidate_game_squares
