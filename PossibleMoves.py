# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

GAME_TYPE_CHESS = 0
GAME_TYPE_CHECKERS = 1

import copy

def build_list_of_moves(input_game_square, input_game):
    """
    For a given game square, this function builds a list of all the legal game squares you can move to. Note: Even on
    success, the list of possible moves might be an empty list.  An empty list means that piece has no legal moves.
    :param input_game_square: GameSquare: The origin game square that you want to build a list of moves for.
    :param input_game: The input game, required to get the game board and game type
    :return list_of_candidate_game_squares: GameSquare[]: List of destination squares you can legally move to
    """
    input_piece = input_game_square.get_occupying_piece()
    input_row = input_game_square.get_row()
    input_col = input_game_square.get_col()
    input_game_type = input_game.get_game_type()
    input_board = input_game.get_board()
    list_of_candidate_game_squares = []

    if input_game_type == GAME_TYPE_CHECKERS:
        # First check for normal movement with no capture
        # Check the square immediately forward and to the left
        if input_row > 0 and input_col > 0:
            if input_board.get_game_square(input_row - 1, input_col - 1).get_occupying_piece() is None:
                list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                  input_col - 1))

        # Check the square immediately forward and to the right
        if input_row > 0 and input_col < input_board.get_size() - 1:
            if input_board.get_game_square(input_row - 1, input_col + 1).get_occupying_piece() is None:
                list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                  input_col + 1))

        # TODO: If the coin is promoted, it can also move backwards

        # Check for possible jumps moves
        checkers_jump(input_board, input_piece, input_game_square, list_of_candidate_game_squares)

        return list_of_candidate_game_squares

    elif input_game_type == GAME_TYPE_CHESS:

        if type(input_piece).__name__ == "King":
            # A king can move one square in any direction (horizontally, vertically, or diagonally),
            # unless the square is already occupied by a friendly piece, or the move would place the king in check

            # Check the square immediately below the kings current position
            if input_row + 1 < input_board.get_size():
                if input_board.get_game_square(input_row + 1, input_col).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row + 1, input_col).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row + 1, input_col))
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 1, input_col))

            # Check the square immediately above the kings current position
            if input_row - 1 >= 0:
                if input_board.get_game_square(input_row - 1,
                                               input_col).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row - 1, input_col).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row - 1, input_col))
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row - 1, input_col))

            # Check the square immediately left of the kings current position
            if input_col - 1 >= 0:
                if input_board.get_game_square(input_row,
                                               input_col - 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row, input_col - 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row, input_col - 1))
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row, input_col - 1))

            # Check the square immediately right of the kings current position
            if input_col + 1 < input_board.get_size():
                if input_board.get_game_square(input_row,
                                               input_col + 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row, input_col + 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row, input_col + 1))
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row, input_col + 1))

            # Check the square immediately down and to the left of the kings current position
            if input_row + 1 < input_board.get_size() and input_col - 1 >= 0:
                if input_board.get_game_square(input_row + 1, input_col - 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row + 1, input_col - 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row + 1, input_col - 1))
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row + 1, input_col - 1))

            # Check the square immediately down and to the right of the kings current position
            if input_row + 1 < input_board.get_size() and input_col + 1 < input_board.get_size():
                if input_board.get_game_square(input_row + 1, input_col + 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row + 1, input_col + 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row + 1, input_col + 1))
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row + 1, input_col + 1))

            # Check the square immediately up and to the left of the kings current position
            if input_row - 1 >= 0 and input_col - 1 >= 0:
                if input_board.get_game_square(input_row - 1, input_col - 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row - 1, input_col - 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row - 1, input_col - 1))
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row - 1, input_col - 1))

            # Check the square immediately up and to the right of the kings current position
            if input_row - 1 >= 0 and input_col + 1 < input_board.get_size():
                if input_board.get_game_square(input_row - 1, input_col + 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row - 1, input_col + 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row - 1, input_col + 1))
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row - 1, input_col + 1))

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
                                list_of_candidate_game_squares.append(input_board.get_game_square(7, 7))

                # Queen-side
                if input_board.get_game_square(7, 3).get_occupying_piece() is None and \
                        input_board.get_game_square(7, 2).get_occupying_piece() is None and \
                        input_board.get_game_square(7, 1).get_occupying_piece() is None and \
                        input_board.get_game_square(7, 0).get_occupying_piece() is not None:
                    if type(input_board.get_game_square(7, 0).get_occupying_piece()).__name__ == "Rook":
                        if input_board.get_game_square(7, 0).get_occupying_piece() \
                                .get_colour() is input_piece.get_colour():
                            if not input_board.get_game_square(7, 0).get_occupying_piece().get_moved_yet_status():
                                list_of_candidate_game_squares.append(input_board.get_game_square(7, 0))

            # TODO: Review the list of candidate moves, and filter out any that would place the king in check

        elif type(input_piece).__name__ == "Queen":
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
                        list_of_candidate_game_squares.append(input_board.get_game_board()[row_pos][input_col])
                        break
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_board()[row_pos][input_col])

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
                        list_of_candidate_game_squares.append(input_board.get_game_board()[row_neg][input_col])
                        break
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_board()[row_neg][input_col])

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
                        list_of_candidate_game_squares.append(input_board.get_game_board()[input_row][col_pos])
                        break
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_board()[input_row][col_pos])

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

        elif type(input_piece).__name__ == "Bishop":
            # The bishop can be moved any number of unoccupied squares in a straight line diagonally.
            # Stop if we see a piece. If piece is unfriendly add the capture move to the list. Here are the step taken:
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

        elif type(input_piece).__name__ == "Knight":
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
                        list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 2, input_col + 1))
                elif input_board.get_game_square(input_row - 2, input_col + 1).get_occupying_piece() is None:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 2, input_col + 1))

            # moves up then left
            if ((input_row - 2) >= 0) and ((input_col - 1) >= 0):
                if input_board.get_game_square(input_row - 2, input_col - 1).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row - 2, input_col - 1).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # Capture move, add it to the list
                        list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 2, input_col - 1))
                elif input_board.get_game_square(input_row - 2, input_col - 1).get_occupying_piece() is None:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 2, input_col - 1))

            # moves down then right
            if ((input_row + 2) <= input_board.get_size() - 1) \
                    and ((input_col + 1) <= input_board.get_size() - 1):
                if input_board.get_game_square(input_row + 2, input_col + 1).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row + 2, input_col + 1).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # Capture move, add it to the list
                        list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 2, input_col + 1))
                elif input_board.get_game_square(input_row + 2, input_col + 1).get_occupying_piece() is None:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 2, input_col + 1))

            # moves down then left
            if ((input_row + 2) <= input_board.get_size() - 1) and ((input_col - 1) >= 0):
                if input_board.get_game_square(input_row + 2, input_col - 1).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row + 2, input_col - 1).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # Capture move, add it to the list
                        list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 2, input_col - 1))
                elif input_board.get_game_square(input_row + 2, input_col - 1).get_occupying_piece() is None:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 2, input_col - 1))

            # moves right then up
            if ((input_row - 1) >= 0) and ((input_col + 2) <= input_board.get_size() - 1):
                if input_board.get_game_square(input_row - 1, input_col + 2).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row - 1, input_col + 2).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # Capture move, add it to the list
                        list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1, input_col + 2))
                elif input_board.get_game_square(input_row - 1, input_col + 2).get_occupying_piece() is None:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1, input_col + 2))

            # moves right then down
            if ((input_row + 1) <= input_board.get_size() - 1) \
                    and ((input_col + 2) <= input_board.get_size() - 1):
                if input_board.get_game_square(input_row + 1, input_col + 2).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row + 1, input_col + 2).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # Capture move, add it to the list
                        input_board.get_game_square(input_row - 1, input_col + 2)
                        list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 1, input_col + 2))
                elif input_board.get_game_square(input_row + 1, input_col + 2).get_occupying_piece() is None:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 1, input_col + 2))

            # moves left then up
            if ((input_row - 1) >= 0) and ((input_col - 2) >= 0):
                if input_board.get_game_square(input_row - 1, input_col - 2).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row - 1, input_col - 2).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # Capture move, add it to the list
                        list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1, input_col - 2))
                elif input_board.get_game_square(input_row - 1, input_col - 2).get_occupying_piece() is None:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1, input_col - 2))

            # moves left then down
            if ((input_row + 1) <= input_board.get_size() - 1) and ((input_col - 2) >= 0):
                if input_board.get_game_square(input_row + 1, input_col - 2).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row + 1, input_col - 2).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # Capture move, add it to the list
                        list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 1, input_col - 2))
                elif input_board.get_game_square(input_row + 1, input_col - 2).get_occupying_piece() is None:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 1, input_col - 2))

        elif type(input_piece).__name__ == "Rook":
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
                        list_of_candidate_game_squares.append(input_board.get_game_board()[row_pos][input_col])
                        break
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_board()[row_pos][input_col])

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
                        list_of_candidate_game_squares.append(input_board.get_game_board()[row_neg][input_col])
                        break
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_board()[row_neg][input_col])

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
                        list_of_candidate_game_squares.append(input_board.get_game_board()[input_row][col_pos])
                        break
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(input_board.get_game_board()[input_row][col_pos])

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
                        list_of_candidate_game_squares.append(input_board.get_game_board()[input_row][col_neg])
                        break
                else:
                    # Square was empty, add it to the list
                    list_of_candidate_game_squares.append(
                        input_board.get_game_board()[input_row][col_neg])

        elif type(input_piece).__name__ == "Pawn":
            # Normally a pawn moves by advancing a single square,
            #  but the first time a pawn moves, it has the option of advancing two squares. Pawns may not use the
            #  initial two-square advance to jump over an occupied square, or to capture. Any piece immediately
            #  in front of a pawn, friend or foe, blocks its advance.

            # Normal non-capture movements
            # forward 1 step and 2 step
            if input_row - 1 >= 0:
                # 1 step forward
                if input_board.get_game_square(input_row - 1, input_col).get_occupying_piece() is None:
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1, input_col))

                # 2 steps forward (assuming we have not moved yet)
                if not input_piece.get_moved_yet_status():
                    if input_board.get_game_square(input_row - 2, input_col).get_occupying_piece() is None:
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row - 2, input_col))

            if input_row - 1 >= 0 and 0 <= input_col <= input_board.get_size() - 1:

                if input_col == 0:
                    # left most case (edge case for column 0)
                    if input_board.get_game_square(input_row - 1,
                                                   input_col + 1).get_occupying_piece() is not None:
                        if input_board.get_game_square(input_row - 1, input_col + 1).get_occupying_piece() \
                                .get_colour() is not input_piece.get_colour():
                            # Capture move, add it to the list
                            list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                              input_col + 1))

                elif input_col == input_board.get_size() - 1:
                    # right most case (edge case for column 7)
                    if input_board.get_game_square(input_row - 1,
                                                   input_col - 1).get_occupying_piece() is not None:
                        if input_board.get_game_square(input_row - 1, input_col - 1).get_occupying_piece() \
                                .get_colour() is not input_piece.get_colour():
                            # Capture move, add it to the list
                            list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                              input_col - 1))

                else:
                    # Now we are working with middle pawns. Checks for both front diagonals and
                    # if there is a non friendly add it to the list.
                    # First check the front left
                    if input_board.get_game_square(input_row - 1,
                                                   input_col - 1).get_occupying_piece() is not None:
                        if input_board.get_game_square(input_row - 1, input_col - 1).get_occupying_piece() \
                                .get_colour() is not input_piece.get_colour():
                            # Capture move, add it to the list
                            list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                              input_col - 1))
                    # front right
                    if input_board.get_game_square(input_row - 1,
                                                   input_col + 1).get_occupying_piece() is not None:
                        if input_board.get_game_square(input_row - 1, input_col + 1).get_occupying_piece() \
                                .get_colour() is not input_piece.get_colour():
                            # Capture move, add it to the list
                            list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                              input_col + 1))
                # TODO: Look for "en passant" pawn capture opportunity.

        else:
            # Could not identify the type of piece
            raise Exception("Could not identify the type of piece")

        return list_of_candidate_game_squares

    else:
        # Game mode is neither "chess" nor "checkers"
        return input_game_type.lower()


def checkers_jump(input_board, input_piece, input_game_square, list_moves):
    """
    Iterative function to identify any checkers jumps
    Used to help build the list of checkers jump moves
    Does not return anything, just keeps appending to the list of candidate moves
    :param input_piece: Piece: The original piece we are moving, doesn't change as we recurse
    :param input_board: GameBoard: The game board
    :param input_game_square: GameSquare: The input game square
    :param list_moves: The working list of candidate game squares
    """
    # Check for the jump and up and to the left
    if input_game_square.get_row() - 2 >= 0 and input_game_square.get_col() - 2 >= 0:
        # The square jump squares are on the board, check if there is a coin there
        if input_board.get_game_square(input_game_square.get_row() - 1,
                                       input_game_square.get_col() - 1).get_occupying_piece() is not None:
            # There is a coin there, check if its an enemy piece
            if input_board.get_game_square(input_game_square.get_row() - 1,
                                           input_game_square.get_col() - 1).get_occupying_piece().get_colour() is not \
                    input_piece.get_colour():
                # It is an enemy piece, check if the jump spot is clear
                if input_board.get_game_square(input_game_square.get_row() - 2,
                                               input_game_square.get_col() - 2).get_occupying_piece() is None:
                    # Legal jump identified, add it to the list
                    list_moves.append(
                        input_board.get_game_square(input_game_square.get_row() - 2, input_game_square.get_col() - 2))
                    # Iterate and check if coin can jump more
                    checkers_jump(input_board, input_piece,
                                  input_board.get_game_square(input_game_square.get_row() - 2,
                                                              input_game_square.get_col() - 2), list_moves)

    # Check for the jump up and to the right
    if input_game_square.get_row() - 2 >= 0 and input_game_square.get_col() + 2 < input_board.get_size():
        # The square jump squares are on the board, check if there is a coin there
        if input_board.get_game_square(input_game_square.get_row() - 1,
                                       input_game_square.get_col() + 1).get_occupying_piece() is not None:
            # There is a coin there, check if its an enemy piece
            if input_board.get_game_square(input_game_square.get_row() - 1,
                                           input_game_square.get_col() + 1).get_occupying_piece().get_colour() is not \
                    input_piece.get_colour():
                # It is an enemy piece, check if the jump spot is clear
                if input_board.get_game_square(input_game_square.get_row() - 2,
                                               input_game_square.get_col() + 2).get_occupying_piece() is None:
                    # Legal jump identified, add it to the list
                    list_moves.append(
                        input_board.get_game_square(input_game_square.get_row() - 2, input_game_square.get_col() + 2))
                    # Iterate and check if coin can jump more from there
                    checkers_jump(input_board, input_piece,
                                  input_board.get_game_square(input_game_square.get_row() - 2,
                                                              input_game_square.get_col() + 2), list_moves)

    if input_piece.get_promotion_status():
        # The coin is promoted and can also jump backwards.
        # TODO: If the coin is promoted, we need to also check for the backwards jumps.
        #  Can't just add on the same logic used for forward jumps or it will result in an infinite loop.
        pass

    return


def temp_move(origin_square, destination_square):
    """
    mimics a movement of a piece in the board.
    once used should use undo temp to undo the move
    origin_square: gamesquare where the piece is comming form
    destination_square: gamesquare where the piece is going
    return: piece or None from the destination_sqaure
    """
    previous_destination_piece = None
    # make a copy of the piece on destination if there is one
    if destination_square.get_occupying_piece() is not None:
        previous_destination_piece = copy.deepcopy(destination_square.get_occupying_piece())
    destination_square.put_piece_here(origin_square.get_occupying_piece())
    origin_square.remove_occupying_piece()
    return previous_destination_piece


def undo_temp_move(previous_origin_square, previous_destination_square, previous_destination_piece):
    """
    Undo the move that temp_move did
    previous_origin_square: gamesquare what you had for origin_square from temp_move
    previous_destination_square: gamesquare what you had for destination_square from temp_move
    previous_destination_square: None or a piece previously on the destination_square
    """
    previous_origin_square.put_piece_here(previous_destination_square.get_occupying_piece())
    previous_destination_square.put_piece_here(previous_destination_piece)


def make_move_and_check(origin_gamesquare, destination_gamesquare, game):
    """
    This mimics moving the a piece from an origin to a destination
    origin_square: gamesquare where the piece is comming form
    destination_square: gamesquare where the piece is going
    return: True if the move cause a check and False if it does not
    """
    board = game.get_board()
    # my temp move
    prev_piece_from_destination = temp_move(origin_gamesquare, destination_gamesquare)

    # board switches as if i have actually made that move
    board.switch_sides()

    # my king location
    my_king = None

    # enemy moves currently at the bottom of the board
    # get all their moves
    # also look for where my king is
    enemy_moves = []
    for row in board.get_game_board():
        for gamesquare in row:
            if gamesquare.get_occupying_piece() is not None:
                # get moves of enemy pieces
                if gamesquare.get_occupying_piece().get_colour() is not destination_gamesquare.get_occupying_piece().get_colour():
                    enemy_moves += build_list_of_moves(gamesquare, game)
                # find my king
                if gamesquare.get_occupying_piece().get_colour() is destination_gamesquare.get_occupying_piece().get_colour():
                    if type(gamesquare.get_occupying_piece()).__name__ is "King":
                        my_king = gamesquare

    # make sure you find your king
    if my_king is not None:
        for an_enemy_move in enemy_moves:
            if (my_king.get_row(), my_king.get_col()) == (an_enemy_move.get_row(), an_enemy_move.get_col()):
                # we have to return everything back before the move
                board.switch_sides()
                undo_temp_move(origin_gamesquare, destination_gamesquare, prev_piece_from_destination)
                return True
    else:
        # we have to return everything back before the move
        board.switch_sides()
        undo_temp_move(origin_gamesquare, destination_gamesquare, prev_piece_from_destination)
        raise Exception("Did not find the King")

    # we have to return everything back before the move
    board.switch_sides()
    undo_temp_move(origin_gamesquare, destination_gamesquare, prev_piece_from_destination)
    return False


def filter_check_moves(my_gamesquare, game, list_of_moves_to_be_filtered):
    """
    This creates a filtered list of gamesquares from list_of_moves_to_be_filtered that filter
    all the moves that cause a check
    my_gamesquare: a gamesquare where the piece is moving from
    game: a chess game
    list_of_moves_to_be_filtered: list of gamesquares that is from build_list_of_moves
    returns: filtered_moves which is a list of gamesquares
    """
    # new list
    filtered_moves = []

    # check every move if moves cause a check
    for my_move in list_of_moves_to_be_filtered:
        if not make_move_and_check(my_gamesquare, my_move, game):
            filtered_moves.append(my_move)

    return filtered_moves

# For testing -------------------------------------------


def build_enemy_list_of_moves(gamesquare, game):

    # all of enemy list of moves
    enemy_moves = []
    tmp_game = copy.deepcopy(game)
    tmp_gamesquare = copy.deepcopy(gamesquare)
    board = tmp_game.get_board()

    # switch board to identify enemy moves
    board.switch_sides()

    # checks every game piece in the switched board
    # for every moves that the enemy can make
    for row in board.get_game_board():
        for col in row:
            if col.get_occupying_piece() is not None:
                if col.get_occupying_piece().get_colour() is not tmp_gamesquare.get_occupying_piece().get_colour():
                    # add the game square one by one to the enemy moves
                    enemy_moves += build_list_of_moves(col, tmp_game)
    # switch board back to normal
    board.switch_sides()

    return enemy_moves


def is_king_checked(your_king_gamesquare, game):
    # get all enemy moves
    # compare enemy moves to king position
    # all of enemy list of moves
    enemy_moves = []
    board = game.get_board()

    # switch board to identify enemy moves
    board.switch_sides()

    # checks every game piece in the switched board
    # for every moves that the enemy can make
    for row in board.get_game_board():
        for gamesquare in row:
            if gamesquare.get_occupying_piece() is not None:
                if gamesquare.get_occupying_piece().get_colour() is not your_king_gamesquare.get_occupying_piece().get_colour():
                    # add the game square one by one to the enemy moves
                    enemy_moves += build_list_of_moves(gamesquare, game)

    # check if one of the enemy moves is equal to your kings gamesquare
    for move in enemy_moves:
        if (move.get_row(), move.get_col()) == (your_king_gamesquare.get_row(), your_king_gamesquare.get_col()):
            board.switch_sides()
            return True
    board.switch_sides()
    return False

# -----------------------------------------------------------
