# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch


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
    list_of_candidate_game_squares = []

    # Compared to other chess pieces, the knight's movement is unique: it may move two squares vertically and
    # one square horizontally, or two squares horizontally and one square vertically (with both forming the
    # shape of an L). While moving, the knight can jump over pieces to reach its destination.
    # Here are the steps taken in checking for kngiht movements:
    #   1. check if the possible move (row, col) is in the board or check for bounds
    #   2. check if game square has a piece
    #   3. check if it has a non friendly piece if so add to list of moves
    #   4. if game sqaure is empty add it to list of moves

    # moves up then right
    if ((input_row - 2) >= 0) and ((input_col + 1) <= input_board.get_size() - 1):
        if input_board.get_game_square(input_row - 2, input_col + 1).get_occupying_piece() is not None:
            if (input_board.get_game_square(input_row - 2, input_col + 1).get_occupying_piece()
                    .get_colour() is not input_piece.get_colour()):
                # Capture move, add it to the list
                list_of_candidate_game_squares.append(
                    input_board.get_game_square(input_row - 2, input_col + 1))
        elif input_board.get_game_square(input_row - 2, input_col + 1).get_occupying_piece() is None:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_square(input_row - 2, input_col + 1))

    # moves up then left
    if ((input_row - 2) >= 0) and ((input_col - 1) >= 0):
        if input_board.get_game_square(input_row - 2, input_col - 1).get_occupying_piece() is not None:
            if (input_board.get_game_square(input_row - 2, input_col - 1).get_occupying_piece()
                    .get_colour() is not input_piece.get_colour()):
                # Capture move, add it to the list
                list_of_candidate_game_squares.append(
                    input_board.get_game_square(input_row - 2, input_col - 1))
        elif input_board.get_game_square(input_row - 2, input_col - 1).get_occupying_piece() is None:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_square(input_row - 2, input_col - 1))

    # moves down then right
    if ((input_row + 2) <= input_board.get_size() - 1) \
            and ((input_col + 1) <= input_board.get_size() - 1):
        if input_board.get_game_square(input_row + 2, input_col + 1).get_occupying_piece() is not None:
            if (input_board.get_game_square(input_row + 2, input_col + 1).get_occupying_piece()
                    .get_colour() is not input_piece.get_colour()):
                # Capture move, add it to the list
                list_of_candidate_game_squares.append(
                    input_board.get_game_square(input_row + 2, input_col + 1))
        elif input_board.get_game_square(input_row + 2, input_col + 1).get_occupying_piece() is None:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_square(input_row + 2, input_col + 1))

    # moves down then left
    if ((input_row + 2) <= input_board.get_size() - 1) and ((input_col - 1) >= 0):
        if input_board.get_game_square(input_row + 2, input_col - 1).get_occupying_piece() is not None:
            if (input_board.get_game_square(input_row + 2, input_col - 1).get_occupying_piece()
                    .get_colour() is not input_piece.get_colour()):
                # Capture move, add it to the list
                list_of_candidate_game_squares.append(
                    input_board.get_game_square(input_row + 2, input_col - 1))
        elif input_board.get_game_square(input_row + 2, input_col - 1).get_occupying_piece() is None:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_square(input_row + 2, input_col - 1))

    # moves right then up
    if ((input_row - 1) >= 0) and ((input_col + 2) <= input_board.get_size() - 1):
        if input_board.get_game_square(input_row - 1, input_col + 2).get_occupying_piece() is not None:
            if (input_board.get_game_square(input_row - 1, input_col + 2).get_occupying_piece()
                    .get_colour() is not input_piece.get_colour()):
                # Capture move, add it to the list
                list_of_candidate_game_squares.append(
                    input_board.get_game_square(input_row - 1, input_col + 2))
        elif input_board.get_game_square(input_row - 1, input_col + 2).get_occupying_piece() is None:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_square(input_row - 1, input_col + 2))

    # moves right then down
    if ((input_row + 1) <= input_board.get_size() - 1) \
            and ((input_col + 2) <= input_board.get_size() - 1):
        if input_board.get_game_square(input_row + 1, input_col + 2).get_occupying_piece() is not None:
            if (input_board.get_game_square(input_row + 1, input_col + 2).get_occupying_piece()
                    .get_colour() is not input_piece.get_colour()):
                # Capture move, add it to the list
                input_board.get_game_square(
                    input_row - 1, input_col + 2)
                list_of_candidate_game_squares.append(
                    input_board.get_game_square(input_row + 1, input_col + 2))
        elif input_board.get_game_square(input_row + 1, input_col + 2).get_occupying_piece() is None:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_square(input_row + 1, input_col + 2))

    # moves left then up
    if ((input_row - 1) >= 0) and ((input_col - 2) >= 0):
        if input_board.get_game_square(input_row - 1, input_col - 2).get_occupying_piece() is not None:
            if (input_board.get_game_square(input_row - 1, input_col - 2).get_occupying_piece()
                    .get_colour() is not input_piece.get_colour()):
                # Capture move, add it to the list
                list_of_candidate_game_squares.append(
                    input_board.get_game_square(input_row - 1, input_col - 2))
        elif input_board.get_game_square(input_row - 1, input_col - 2).get_occupying_piece() is None:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_square(input_row - 1, input_col - 2))

    # moves left then down
    if ((input_row + 1) <= input_board.get_size() - 1) and ((input_col - 2) >= 0):
        if input_board.get_game_square(input_row + 1, input_col - 2).get_occupying_piece() is not None:
            if (input_board.get_game_square(input_row + 1, input_col - 2).get_occupying_piece()
                    .get_colour() is not input_piece.get_colour()):
                # Capture move, add it to the list
                list_of_candidate_game_squares.append(
                    input_board.get_game_square(input_row + 1, input_col - 2))
        elif input_board.get_game_square(input_row + 1, input_col - 2).get_occupying_piece() is None:
            # Square was empty, add it to the list
            list_of_candidate_game_squares.append(
                input_board.get_game_square(input_row + 1, input_col - 2))

    return list_of_candidate_game_squares
