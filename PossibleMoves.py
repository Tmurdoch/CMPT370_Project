# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

import random

GAME_TYPE_CHESS = 0
GAME_TYPE_CHECKERS = 1


def build_list_of_moves(input_game_square, input_game):
    """
    Determine based on the piece where it can potentially move and load it into the __squares_you_can_move_to
    attribute
    Note: Even on success, the list of possible moves for a game-square might be an empty list
    :return: 0 on success, -1 on failure
    """
    # redid refactor due to noticing variable name collisions
    input_piece = input_game_square.get_occupying_piece()
    input_row = input_game_square.get_row()
    input_col = input_game_square.get_col()
    input_game_type = input_game.get_game_type()
    input_board = input_game.get_board()

    list_of_candidate_game_squares = []
    # 1 == checkers
    if input_game_type == GAME_TYPE_CHECKERS:
        # Generate possible moves for checkers

        # normal movement no capture
        # Direction Up Left
        if input_row > 0 and input_col > 0:
            if input_board.get_game_square(input_row - 1, input_col - 1).get_occupying_piece() is None:
                list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                  input_col - 1))

        # Direction Up Right
        if input_row > 0 and input_col < input_board.get_size() - 1:
            if input_board.get_game_square(input_row - 1, input_col + 1).get_occupying_piece() is None:
                list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                  input_col + 1))

        # capture movements
        checkers_jump(input_board, input_piece, input_board.get_game_square(input_row, input_col),
                      list_of_candidate_game_squares)

        return list_of_candidate_game_squares

    # chess = 0
    elif input_game_type == GAME_TYPE_CHESS:

        if type(input_piece).__name__ == "King":
            # A king can move one square in any direction (horizontally,
            #  vertically, or diagonally), unless the square is already occupied by a friendly piece, or the move
            #  would place the king in check

            # Moves the piece to a direction
            # check if where moving is in the board
            # check if there is a piece on that square
            # if there is check its colour
            # if not the same colour add it to the list
            # if the square was empty add it to the list

            # Direction Down
            if input_row < input_board.get_size() - 1:
                if input_board.get_game_square(input_row + 1, input_col).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row + 1, input_col).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row + 1, input_col))
                else:
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 1, input_col))

            # Direction Up
            if input_row > 0:
                if input_board.get_game_square(input_row - 1,
                                               input_col).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row - 1, input_col).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row - 1, input_col))
                else:
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row - 1, input_col))

            # Direction Left
            if input_col > 0:
                if input_board.get_game_square(input_row,
                                               input_col - 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row, input_col - 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row, input_col - 1))
                else:
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row, input_col - 1))

            # Direction Right
            if input_col < input_board.get_size() - 1:
                if input_board.get_game_square(input_row,
                                               input_col + 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row, input_col + 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row, input_col + 1))
                else:
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row, input_col + 1))

            # Direction Down Left
            if input_row < input_board.get_size() - 1 and input_col > 0:
                if input_board.get_game_square(input_row + 1, input_col - 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row + 1, input_col - 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row + 1, input_col - 1))
                else:
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 1,
                                                                                      input_col - 1))

            # Direction Down Right
            if input_row < input_board.get_size() - 1 and input_col < input_board.get_size() - 1:
                if input_board.get_game_square(input_row + 1, input_col + 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row + 1, input_col + 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row + 1, input_col + 1))
                else:
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 1,
                                                                                      input_col + 1))

            # Direction Up Left
            if input_row > 0 and input_col > 0:
                if input_board.get_game_square(input_row - 1, input_col - 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row - 1, input_col - 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row - 1, input_col - 1))
                else:
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                      input_col - 1))

            # Direction Up Right
            if input_row > 0 and input_col < input_board.get_size() - 1:
                if input_board.get_game_square(input_row - 1, input_col + 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row - 1, input_col + 1).get_occupying_piece() \
                            .get_colour() is not input_piece.get_colour():
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row - 1, input_col + 1))
                else:
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                      input_col + 1))

            # Requirements for Castling
            # The castling must be kingside or queenside.
            # Neither the king nor the chosen rook has previously moved.
            # There are no pieces between the king and the chosen rook.
            # The king is not currently in check.
            # The king does not pass through a square that is attacked by an enemy piece.
            # The king does not end up in check. (True of any legal move.)

            # Castling
            # check if the king has not moved yet
            # check if spaces between the king and rook in a side to be empty
            # check if the rook is friendly
            # check if rook has not moved yet
            # TODO: create a function that will go over the enemy pieces and check for a checkmate
            #  so if checkmate it will not add to the list

            # add the location of the rook to be a possible move
            if not input_piece.get_moved_yet_status():
                # Kingside
                if input_board.get_game_square(7, 5).get_occupying_piece() is None and \
                        input_board.get_game_square(7, 6).get_occupying_piece() is None and \
                        input_board.get_game_square(7, 7).get_occupying_piece() is not None:
                    if type(input_board.get_game_square(7, 7).get_occupying_piece()).__name__ == "Rook":
                        if input_board.get_game_square(7, 7).get_occupying_piece() \
                                .get_colour() is input_piece.get_colour():
                            if not input_board.get_game_square(7, 7).get_occupying_piece().get_moved_yet_status():
                                list_of_candidate_game_squares.append(input_board.get_game_square(7, 7))

                # Queenside
                if input_board.get_game_square(7, 3).get_occupying_piece() is None and \
                        input_board.get_game_square(7, 2).get_occupying_piece() is None and \
                        input_board.get_game_square(7, 1).get_occupying_piece() is None and \
                        input_board.get_game_square(7, 0).get_occupying_piece() is not None:
                    if type(input_board.get_game_square(7, 0).get_occupying_piece()).__name__ == "Rook":
                        if input_board.get_game_square(7, 0).get_occupying_piece() \
                                .get_colour() is input_piece.get_colour():
                            if not input_board.get_game_square(7, 0).get_occupying_piece().get_moved_yet_status():
                                list_of_candidate_game_squares.append(input_board.get_game_square(7, 0))

        elif type(input_piece).__name__ == "Queen":
            # The queen can be moved any number of unoccupied squares in a straight line
            # vertically, horizontally, or diagonally, thus combining the moves of the rook and bishop
            # Vertical movements
            # check from the piece to a direction: up, down, left, right
            # will stop until sees a peace
            # if piece friendly stop
            # if non friendly add add (row, col) to possible moves but also stops
            # if empty then add it to list and keep going

            # Vertical movements

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
                    list_of_candidate_game_squares.append(input_board.get_game_board()[row_neg][input_col])

            # Horizontal movements

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
                    list_of_candidate_game_squares.append(
                        input_board.get_game_board()[input_row][col_neg])

            # check if the row or column are out of bounds
            # check specific corner from piece
            # will stop until sees a peace
            # if piece friendly stop
            # if non friendly add add (row, col) to possible moves but also stops
            # if empty then add it to list and keep going

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
                                        list_of_candidate_game_squares.append(
                                            input_board.get_game_board()[row][col])
                        else:
                            break

        elif type(input_piece).__name__ == "Bishop":
            # The bishop can be moved any number of unoccupied squares in a straight line diagonally

            # check if the row or column are out of bounds
            # check specific corner from piece
            # will stop until sees a peace
            # if piece friendly stop
            # if non friendly add add (row, col) to possible moves but also stops
            # if empty then add it to list and keep going

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
                                        list_of_candidate_game_squares.append(
                                            input_board.get_game_board()[row][col])
                        else:
                            break

        elif type(input_piece).__name__ == "Knight":

            # check if the possible move (row, col) is in the board or check for bounds
            # check if game square has a piece
            # check if it has a non friendly piece if so add to list of moves
            # if game sqaure is empty add it to list of moves

            # moves up then right
            if ((input_row - 2) >= 0) and ((input_col + 1) <= input_board.get_size() - 1):
                if input_board.get_game_square(input_row - 2, input_col + 1).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row - 2, input_col + 1).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # need to find out how to capture a piece
                        up_right_square = input_board.get_game_square(input_row - 2, input_col + 1)
                        list_of_candidate_game_squares.append(up_right_square)
                elif input_board.get_game_square(input_row - 2, input_col + 1).get_occupying_piece() is None:
                    up_right_square = input_board.get_game_square(input_row - 2, input_col + 1)
                    list_of_candidate_game_squares.append(up_right_square)

            # moves up then left
            if ((input_row - 2) >= 0) and ((input_col - 1) >= 0):
                if input_board.get_game_square(input_row - 2, input_col - 1).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row - 2, input_col - 1).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # need to find out how to capture a piece
                        up_left_square = input_board.get_game_square(input_row - 2, input_col - 1)
                        list_of_candidate_game_squares.append(up_left_square)
                elif input_board.get_game_square(input_row - 2, input_col - 1).get_occupying_piece() is None:
                    up_left_square = input_board.get_game_square(input_row - 2, input_col - 1)
                    list_of_candidate_game_squares.append(up_left_square)

            # moves down then right
            if ((input_row + 2) <= input_board.get_size() - 1) \
                    and ((input_col + 1) <= input_board.get_size() - 1):
                if input_board.get_game_square(input_row + 2, input_col + 1).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row + 2, input_col + 1).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # need to find out how to capture a piece
                        down_right_square = input_board.get_game_square(input_row + 2, input_col + 1)
                        list_of_candidate_game_squares.append(down_right_square)
                elif input_board.get_game_square(input_row + 2, input_col + 1).get_occupying_piece() is None:
                    down_right_square = input_board.get_game_square(input_row + 2, input_col + 1)
                    list_of_candidate_game_squares.append(down_right_square)

            # moves down then left
            if ((input_row + 2) <= input_board.get_size() - 1) and ((input_col - 1) >= 0):
                if input_board.get_game_square(input_row + 2, input_col - 1).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row + 2, input_col - 1).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # need to find out how to capture a piece
                        down_left_square = input_board.get_game_square(input_row + 2, input_col - 1)
                        list_of_candidate_game_squares.append(down_left_square)
                elif input_board.get_game_square(input_row + 2, input_col - 1).get_occupying_piece() is None:
                    down_left_square = input_board.get_game_square(input_row + 2, input_col - 1)
                    list_of_candidate_game_squares.append(down_left_square)

            # moves right then up
            if ((input_row - 1) >= 0) and ((input_col + 2) <= input_board.get_size() - 1):
                if input_board.get_game_square(input_row - 1, input_col + 2).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row - 1, input_col + 2).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # need to find out how to capture a piece
                        right_up_square = input_board.get_game_square(input_row - 1, input_col + 2)
                        list_of_candidate_game_squares.append(right_up_square)
                elif input_board.get_game_square(input_row - 1, input_col + 2).get_occupying_piece() is None:
                    right_up_square = input_board.get_game_square(input_row - 1, input_col + 2)
                    list_of_candidate_game_squares.append(right_up_square)

            # moves right then down
            if ((input_row + 1) <= input_board.get_size() - 1) \
                    and ((input_col + 2) <= input_board.get_size() - 1):
                if input_board.get_game_square(input_row + 1, input_col + 2).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row + 1, input_col + 2).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # need to find out how to capture a piece
                        right_down_square = input_board.get_game_square(input_row + 1, input_col + 2)
                        list_of_candidate_game_squares.append(right_down_square)
                elif input_board.get_game_square(input_row + 1, input_col + 2).get_occupying_piece() is None:
                    right_down_square = input_board.get_game_square(input_row + 1, input_col + 2)
                    list_of_candidate_game_squares.append(right_down_square)

            # moves left then up
            if ((input_row - 1) >= 0) and ((input_col - 2) >= 0):
                if input_board.get_game_square(input_row - 1, input_col - 2).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row - 1, input_col - 2).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # need to find out how to capture a piece
                        left_up_square = input_board.get_game_square(input_row - 1, input_col - 2)
                        list_of_candidate_game_squares.append(left_up_square)
                elif input_board.get_game_square(input_row - 1, input_col - 2).get_occupying_piece() is None:
                    left_up_square = input_board.get_game_square(input_row - 1, input_col - 2)
                    list_of_candidate_game_squares.append(left_up_square)

            # moves left then down
            if ((input_row + 1) <= input_board.get_size() - 1) and ((input_col - 2) >= 0):
                if input_board.get_game_square(input_row + 1, input_col - 2).get_occupying_piece() is not None:
                    if (input_board.get_game_square(input_row + 1, input_col - 2).get_occupying_piece()
                            .get_colour() is not input_piece.get_colour()):
                        # need to find out how to capture a piece
                        left_down_square = input_board.get_game_square(input_row + 1, input_col - 2)
                        list_of_candidate_game_squares.append(left_down_square)
                elif input_board.get_game_square(input_row + 1, input_col - 2).get_occupying_piece() is None:
                    left_down_square = input_board.get_game_square(input_row + 1, input_col - 2)
                    list_of_candidate_game_squares.append(left_down_square)

        elif type(input_piece).__name__ == "Rook":
            # The rook can be moved any number of unoccupied squares in a straight line vertically or horizontally

            # check from the piece to a direction: up, down, left, right
            # will stop until sees a peace
            # if piece friendly stop
            # if non friendly add add (row, col) to possible moves but also stops
            # if empty then add it to list and keep going

            # Vertical movements

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
                    list_of_candidate_game_squares.append(input_board.get_game_board()[row_neg][input_col])

            # Horizontal movements

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
                    list_of_candidate_game_squares.append(
                        input_board.get_game_board()[input_row][col_neg])

        elif type(input_piece).__name__ == "Pawn":
            # Normally a pawn moves by advancing a single square,
            #  but the first time a pawn moves, it has the option of advancing two squares. Pawns may not use the
            #  initial two-square advance to jump over an occupied square, or to capture. Any piece immediately 
            #  in front of a pawn, friend or foe, blocks its advance.

            # Normal movements
            # forward 1 step and 2 step
            if input_row > 0:
                # 1 step
                if input_board.get_game_square(input_row - 1, input_col).get_occupying_piece() is None:
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1, input_col))

                # 2 step
                if not input_piece.get_moved_yet_status():
                    if input_board.get_game_square(input_row - 2, input_col).get_occupying_piece() is None:
                        list_of_candidate_game_squares.append(
                            input_board.get_game_square(input_row - 2, input_col))

            # diagonal movements
            # only used when non friendly piece on the front diagonal sides
            # check if inside the board
            # check for edge case for columns 0 and 7
            # if they are just check one diagonal side
            # check if there is a non friendly
            # then add it
            if input_row > 0 and 0 <= input_col <= input_board.get_size() - 1:

                # left most case
                if input_col == 0:
                    if input_board.get_game_square(input_row - 1,
                                                   input_col + 1).get_occupying_piece() is not None:
                        if input_board.get_game_square(input_row - 1, input_col + 1).get_occupying_piece() \
                                .get_colour() is not input_piece.get_colour():
                            list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                              input_col + 1))

                # right most case:
                elif input_col == input_board.get_size() - 1:
                    if input_board.get_game_square(input_row - 1,
                                                   input_col - 1).get_occupying_piece() is not None:
                        if input_board.get_game_square(input_row - 1, input_col - 1).get_occupying_piece() \
                                .get_colour() is not input_piece.get_colour():
                            list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                              input_col - 1))

                # Non edge case
                # checks for both sides of the diagonal front
                # if there is a non friendly add it to the list
                else:
                    # front left
                    if input_board.get_game_square(input_row - 1,
                                                   input_col - 1).get_occupying_piece() is not None:
                        if input_board.get_game_square(input_row - 1, input_col - 1).get_occupying_piece() \
                                .get_colour() is not input_piece.get_colour():
                            list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                              input_col - 1))
                    # front right
                    if input_board.get_game_square(input_row - 1,
                                                   input_col - 1).get_occupying_piece() is not None:
                        if input_board.get_game_square(input_row - 1, input_col - 1).get_occupying_piece() \
                                .get_colour() is not input_piece.get_colour():
                            list_of_candidate_game_squares.append(input_board.get_game_square(input_row - 1,
                                                                                              input_col - 1))

        else:
            # Could not identify the type of piece
            return -1

        return list_of_candidate_game_squares

    else:
        # Game mode is neither "chess" nor "checkers"
        return input_game_type.lower()


def checkers_jump(input_board, input_piece, input_gamesquare, list_moves):
    # Direction Up Left

    # checks if top left is on the board
    if input_gamesquare.get_row() - 1 > 0 and input_gamesquare.get_col() - 1 > 0:
        # check if there is a coin there
        if input_board.get_game_square(input_gamesquare.get_row() - 1,
                                       input_gamesquare.get_col() - 1).get_occupying_piece() is not None:
            # check if its an enemy piece
            if input_board.get_game_square(input_gamesquare.get_row() - 1,
                                           input_gamesquare.get_col() - 1).get_occupying_piece().get_colour() is not \
                    input_piece.get_colour():
                # check if up left of the enemy coin is on the board
                if input_gamesquare.get_row() >= 0 and input_gamesquare.get_col() - 2 >= 0:
                    # check if up left of the enemy coin is empty
                    if input_board.get_game_square(input_gamesquare.get_row() - 2,
                                                   input_gamesquare.get_col() - 2).get_occupying_piece() is None:
                        # can move there
                        list_moves.append(
                            input_board.get_game_square(input_gamesquare.get_row() - 2, input_gamesquare.get_col() - 2))
                        # check if coin can jump more
                        checkers_jump(input_board, input_piece,
                                      input_board.get_game_square(input_gamesquare.get_row() - 2,
                                                                  input_gamesquare.get_col() - 2), list_moves)

                        # look for another enemy to capture

    # checks if top right is on the board
    if input_gamesquare.get_row() - 1 > 0 and input_gamesquare.get_col() + 1 < input_board.get_size() - 1:
        # check if there is a coin there
        if input_board.get_game_square(input_gamesquare.get_row() - 1,
                                       input_gamesquare.get_col() + 1).get_occupying_piece() is not None:
            # check if its an enemy piece
            if input_board.get_game_square(input_gamesquare.get_row() - 1,
                                           input_gamesquare.get_col() + 1).get_occupying_piece().get_colour() is not \
                    input_piece.get_colour():
                # check if up left of the enemy coin is on the board
                if input_gamesquare.get_row() >= 0 and input_gamesquare.get_col() + 2 <= input_board.get_size() - 1:
                    # check if up left of the enemy coin is empty
                    if input_board.get_game_square(input_gamesquare.get_row() - 2,
                                                   input_gamesquare.get_col() + 2).get_occupying_piece() is None:
                        # can move there
                        list_moves.append(
                            input_board.get_game_square(input_gamesquare.get_row() - 2, input_gamesquare.get_col() + 2))
                        # check if coin can jump more
                        checkers_jump(input_board, input_piece,
                                      input_board.get_game_square(input_gamesquare.get_row() - 2,
                                                                  input_gamesquare.get_col() + 2), list_moves)
