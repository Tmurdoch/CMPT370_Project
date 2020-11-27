# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

def build_queen_moves(input_game_square, input_game):
    """
    Build the list of possible moves for a Queen
    :param input_game_square: GameSquare: The origin game square that you want to build a list of moves for.
    :param input_game: The input game, required to get the game board and game type
    :return list_of_candidate_game_squares: GameSquare[]: List of destination squares the queen can legally move to
    """
    input_piece = input_game_square.get_occupying_piece()
    input_row = input_game_square.get_row()
    input_col = input_game_square.get_col()
    input_board = input_game.get_board()
    list_of_candidate_game_squares = []

    # The queen can be moved any number of unoccupied squares in a straight line vertically, horizontally,
    # or diagonally, will stop until sees a peace

    # First check for vertical movements, stop if we see a piece.  If piece is unfriendly add the capture
    # move to the list.

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
            if input_board.get_game_board()[input_row][
                col_neg].get_occupying_piece().get_colour() == \
                    input_piece.get_colour():
                break
            if input_board.get_game_board()[input_row][
                col_neg].get_occupying_piece().get_colour() != \
                    input_piece.get_colour():
                list_of_candidate_game_squares.append(
                    input_board.get_game_board()[input_row][col_neg])
                break
        else:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_board()[input_row][col_neg])

    # Now check for diagonal movements, again stop if we see a piece.  If piece is unfriendly add the capture
    # move to the list.  Here are the step taken:
    #   1. check if the row or column are out of bounds
    #   2. check specific corner from piece
    #   3. will stop until sees a peace
    #   4. if piece friendly stop
    #   5. if non friendly add add (row, col) to possible moves but also stops
    #   6. if empty then add it to list and keep going

    # Top Right
    row_pos = input_row
    col_pos = input_col

    stopper = False
    if row_pos != 0:
        for row in range(row_pos - 1, -1, -1):
            if col_pos != input_board.get_size() - 1:
                if not stopper:
                    for col in range(col_pos + 1, input_board.get_size()):
                        if abs(row_pos - row) == abs(col_pos - col):
                            if input_board.get_game_board()[row][col].get_occupying_piece() is not None:
                                if input_board.get_game_board()[row][col].get_occupying_piece() \
                                        .get_colour() == input_piece.get_colour():
                                    stopper = True
                                    break
                                if input_board.get_game_board()[row][col].get_occupying_piece() \
                                        .get_colour() != input_piece.get_colour():
                                    list_of_candidate_game_squares.append(
                                        input_board.get_game_board()[row][col])
                                    stopper = True
                                    break
                            else:
                                # Square was empty, add it to the list
                                list_of_candidate_game_squares.append(
                                    input_board.get_game_board()[row][col])
                else:
                    break
    # Top Left
    row_pos = input_row
    col_neg = input_col

    stopper = False
    if row_pos != 0:
        for row in range(row_pos - 1, -1, -1):
            if col_neg != 0:
                if not stopper:
                    for col in range(col_neg - 1, -1, -1):
                        if abs(row_pos - row) == abs(col_neg - col):
                            if input_board.get_game_board()[row][col].get_occupying_piece() is not None:
                                if input_board.get_game_board()[row][col].get_occupying_piece() \
                                        .get_colour() == input_piece.get_colour():
                                    stopper = True
                                    break
                                if input_board.get_game_board()[row][col].get_occupying_piece() \
                                        .get_colour() != input_piece.get_colour():
                                    list_of_candidate_game_squares.append(
                                        input_board.get_game_board()[row][col])
                                    stopper = True
                                    break
                            else:
                                # Square was empty, add it to the list
                                list_of_candidate_game_squares.append(
                                    input_board.get_game_board()[row][col])
                else:
                    break
    # Bottom Right
    row_neg = input_row
    col_pos = input_col

    stopper = False
    if row_neg != input_board.get_size() - 1:
        for row in range(row_neg + 1, input_board.get_size()):
            if col_pos != input_board.get_size() - 1:
                if not stopper:
                    for col in range(col_pos + 1, input_board.get_size()):
                        if abs(row_neg - row) == abs(col_pos - col):
                            if input_board.get_game_board()[row][col].get_occupying_piece() is not None:
                                if input_board.get_game_board()[row][col].get_occupying_piece() \
                                        .get_colour() == input_piece.get_colour():
                                    stopper = True
                                    break
                                if input_board.get_game_board()[row][col].get_occupying_piece() \
                                        .get_colour() != input_piece.get_colour():
                                    list_of_candidate_game_squares.append(
                                        input_board.get_game_board()[row][col])
                                    stopper = True
                                    break
                            else:
                                # Square was empty, add it to the list
                                list_of_candidate_game_squares.append(
                                    input_board.get_game_board()[row][col])
                else:
                    break

    # Bottom Left
    row_neg = input_row
    col_neg = input_col

    stopper = False
    if row_neg != input_board.get_size():
        for row in range(row_neg + 1, input_board.get_size()):
            if col_neg != 0:
                if not stopper:
                    for col in range(col_neg - 1, -1, -1):
                        if abs(row_neg - row) == abs(col_neg - col):
                            if input_board.get_game_board()[row][col].get_occupying_piece() is not None:
                                if input_board.get_game_board()[row][col].get_occupying_piece() \
                                        .get_colour() == input_piece.get_colour():
                                    stopper = True
                                    break
                                if input_board.get_game_board()[row][col].get_occupying_piece() \
                                        .get_colour() != input_piece.get_colour():
                                    list_of_candidate_game_squares.append(
                                        input_board.get_game_board()[row][col])
                                    stopper = True
                                    break
                            else:
                                # Square was empty, add it to the list
                                list_of_candidate_game_squares.append(
                                    input_board.get_game_board()[row][col])
                else:
                    break

    return list_of_candidate_game_squares
