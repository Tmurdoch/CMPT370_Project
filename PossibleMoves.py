# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

import copy
from GameType import GameType
from build_bishop_moves import build_bishop_moves
from build_knight_moves import build_knight_moves
from build_queen_moves import build_queen_moves
from build_rook_moves import build_rook_moves


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

    if input_game_type == GameType.CHECKERS:
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

        # In the case that the coin is promoted can move backwards as well
        if input_piece.get_promotion_status():
            # Check the square immediately backward and to the left
            if input_row < input_board.get_size() - 1 and input_col > 0:
                if input_board.get_game_square(input_row + 1, input_col - 1).get_occupying_piece() is None:
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 1,
                                                                                      input_col - 1))

            # Check the square immediately backward and to the right
            if input_row < input_board.get_size() - 1 and input_col < input_board.get_size() - 1:
                if input_board.get_game_square(input_row + 1, input_col + 1).get_occupying_piece() is None:
                    list_of_candidate_game_squares.append(input_board.get_game_square(input_row + 1,
                                                                                      input_col + 1))

        # Check for possible jumps moves
        checkers_jump(input_board, input_piece, input_game_square,
                      list_of_candidate_game_squares)

        return list_of_candidate_game_squares

    elif input_game_type == GameType.CHESS:

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
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row + 1, input_col))

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
                                list_of_candidate_game_squares.append(
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
                                list_of_candidate_game_squares.append(
                                    input_board.get_game_square(7, 0))

            # TODO: Review the list of candidate moves, and filter out any that would place the king in check

        elif type(input_piece).__name__ == "Queen":
            list_of_candidate_game_squares = build_queen_moves(input_game_square, input_game)

        elif type(input_piece).__name__ == "Bishop":
            list_of_candidate_game_squares = build_bishop_moves(input_game_square, input_game)

        elif type(input_piece).__name__ == "Knight":
            list_of_candidate_game_squares = build_knight_moves(input_game_square, input_game)

        elif type(input_piece).__name__ == "Rook":
            list_of_candidate_game_squares = build_rook_moves(input_game_square, input_game)

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
                    list_of_candidate_game_squares.append(
                        input_board.get_game_square(input_row - 1, input_col))

                # 2 steps forward (assuming we have not moved yet)
                if not input_piece.get_moved_yet_status():
                    if input_board.get_game_square(input_row - 1, input_col).get_occupying_piece() is None:
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

            # checks if an en passant move can be executed
            # In order for a en passant move to happen following conditions needs to be met
            # - the capturing pawn must be on its fifth rank
            # - the captured pawn must be on an adjacent file and must have just move 2 squares in a single move
            # - the capture can only be made on the move immediately after the enemy pawn makes the double step
            # move; otherwise; the right to capture it en passant is lost
            # 3rd row means 5th rank in this board

            # need row to be in the board
            if 0 <= input_col <= input_board.get_size() - 1:
                # on row 3 is the only row where you can do the en passant move
                if input_row == 3:
                    # edge case left most just check right
                    if input_col == 0:
                        if input_board.get_game_square(input_row, input_col + 1).get_occupying_piece() is not None:
                            if input_board.get_game_square(input_row, input_col + 1) \
                                    .get_occupying_piece().get_colour() is not input_piece.get_colour():
                                # adjacent need to be a Pawn
                                if type(input_board.get_game_square(input_row, input_col + 1).get_occupying_piece())\
                                        .__name__ == "Pawn":
                                    # find out what player to check for the previous move
                                    if input_game.get_light_player().get_colour() == input_piece.get_colour():
                                        enemy = input_game.get_dark_player()
                                    else:
                                        enemy = input_game.get_light_player()
                                    # compare if your adjacent piece is the last move that enemy player did
                                    # get last move returns a tuple of tuples
                                    # ((row orig, col orig), (row dest, col dest))
                                    if enemy.get_last_move() == ((input_row - 2, input_col + 1),
                                                                 (input_row, input_col + 1)):
                                        list_of_candidate_game_squares.append(input_board
                                                                              .get_game_square(input_row - 1,
                                                                                               input_col + 1))
                    # edge case right most just check left
                    elif input_col == input_board.get_size() - 1:
                        if input_board.get_game_square(input_row, input_col - 1).get_occupying_piece() is not None:
                            if input_board.get_game_square(input_row, input_col - 1) \
                                    .get_occupying_piece().get_colour() is not input_piece.get_colour():
                                if type(input_board.get_game_square(input_row, input_col - 1).get_occupying_piece())\
                                        .__name__ == "Pawn":
                                    if input_game.get_light_player().get_colour() == input_piece.get_colour():
                                        enemy = input_game.get_dark_player()
                                    else:
                                        enemy = input_game.get_light_player()
                                    if enemy.get_last_move() == ((input_row - 2, input_col - 1),
                                                                 (input_row, input_col - 1)):
                                        list_of_candidate_game_squares\
                                            .append(input_board.get_game_square(input_row - 1, input_col - 1))
                    # anywhere in the middle of the board
                    else:
                        # check right
                        # there need to be an enemy pawn to the right of my pawn
                        if input_board.get_game_square(input_row, input_col + 1).get_occupying_piece() is not None:
                            if input_board.get_game_square(input_row,
                                                           input_col + 1).get_occupying_piece().get_colour() is not \
                                    input_piece.get_colour():
                                if type(input_board.get_game_square(input_row, input_col + 1).get_occupying_piece())\
                                        .__name__ == "Pawn":
                                    # check the enemy pawn if they did 2 step move last turn
                                    if input_game.get_light_player().get_colour() == input_piece.get_colour():
                                        enemy = input_game.get_dark_player()
                                    else:
                                        enemy = input_game.get_light_player()
                                    # if conditions are met then move 1 diagonal to right and capture the enemy
                                    # adjacent to rigt before the move
                                    if enemy.get_last_move() == (
                                            (input_row - 2, input_col + 1), (input_row, input_col + 1)):
                                        list_of_candidate_game_squares\
                                            .append(input_board.get_game_square(input_row - 1, input_col + 1))
                        # check left
                        # there need to be an enemy pawn to the left of my pawn
                        if input_board.get_game_square(input_row, input_col - 1).get_occupying_piece() is not None:
                            if input_board.get_game_square(input_row,
                                                           input_col - 1).get_occupying_piece().get_colour() is not \
                                    input_piece.get_colour():
                                if type(input_board.get_game_square(input_row, input_col - 1).get_occupying_piece())\
                                        .__name__ == "Pawn":
                                    # check the enemy pawn if they did 2 step move last turn
                                    if input_game.get_light_player().get_colour() == input_piece.get_colour():
                                        enemy = input_game.get_dark_player()
                                    else:
                                        enemy = input_game.get_light_player()
                                    # if conditions are met then move 1 diagonal to left and capture the enemy
                                    # adjacent to left before the move
                                    if enemy.get_last_move() == (
                                            (input_row - 2, input_col - 1), (input_row, input_col - 1)):
                                        list_of_candidate_game_squares\
                                            .append(input_board.get_game_square(input_row - 1, input_col - 1))

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

                    # remove the enemy coin temporarily
                    coin_removed = copy.deepcopy(input_board.get_game_square(
                        input_game_square.get_row() - 1, input_game_square.get_col() - 1).get_occupying_piece())

                    input_board.get_game_square(input_game_square.get_row() - 1,
                                                input_game_square.get_col() - 1).remove_occupying_piece()

                    # Iterate and check if coin can jump more
                    checkers_jump(input_board, input_piece,
                                  input_board.get_game_square(input_game_square.get_row() - 2,
                                                              input_game_square.get_col() - 2), list_moves)

                    # put back the coin removed
                    input_board.get_game_square(input_game_square.get_row() - 1,
                                                input_game_square.get_col() - 1).put_piece_here(coin_removed)

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

                    # remove the enemy coin temporarily
                    coin_removed = copy.deepcopy(input_board.get_game_square(
                        input_game_square.get_row() - 1, input_game_square.get_col() + 1).get_occupying_piece())

                    input_board.get_game_square(input_game_square.get_row() - 1,
                                                input_game_square.get_col() + 1).remove_occupying_piece()

                    # Iterate and check if coin can jump more from there
                    checkers_jump(input_board, input_piece,
                                  input_board.get_game_square(input_game_square.get_row() - 2,
                                                              input_game_square.get_col() + 2), list_moves)
                    # put back the coin removed
                    input_board.get_game_square(input_game_square.get_row() - 1,
                                                input_game_square.get_col() + 1).put_piece_here(coin_removed)

    if input_piece.get_promotion_status():
        # The coin is promoted and can also jump backwards.

        # Check for the jump and down and to the left
        if input_game_square.get_row() + 2 < input_board.get_size() and input_game_square.get_col() - 2 >= 0:
            # The square jump squares are on the board, check if there is a coin there
            if input_board.get_game_square(input_game_square.get_row() + 1,
                                           input_game_square.get_col() - 1).get_occupying_piece() is not None:
                # There is a coin there, check if its an enemy piece
                if input_board.get_game_square(input_game_square.get_row() + 1,
                                               input_game_square.get_col() - 1).get_occupying_piece().get_colour() is not \
                        input_piece.get_colour():
                    # It is an enemy piece, check if the jump spot is clear
                    if input_board.get_game_square(input_game_square.get_row() + 2,
                                                   input_game_square.get_col() - 2).get_occupying_piece() is None:
                        # Legal jump identified, add it to the list
                        list_moves.append(
                            input_board.get_game_square(input_game_square.get_row() + 2,
                                                        input_game_square.get_col() - 2))

                        # remove the enemy coin temporarily
                        coin_removed = copy.deepcopy(input_board.get_game_square(
                            input_game_square.get_row() + 1, input_game_square.get_col() - 1).get_occupying_piece())

                        input_board.get_game_square(input_game_square.get_row() + 1,
                                                    input_game_square.get_col() - 1).remove_occupying_piece()

                        # Iterate and check if coin can jump more
                        checkers_jump(input_board, input_piece,
                                      input_board.get_game_square(input_game_square.get_row() + 2,
                                                                  input_game_square.get_col() - 2), list_moves)

                        # put back the coin removed
                        input_board.get_game_square(input_game_square.get_row() + 1,
                                                    input_game_square.get_col() - 1).put_piece_here(coin_removed)

        # Check for the jump up and to the right
        if input_game_square.get_row() + 2 < input_board.get_size() and input_game_square.get_col() + 2 < input_board.get_size():
            # The square jump squares are on the board, check if there is a coin there
            if input_board.get_game_square(input_game_square.get_row() + 1,
                                           input_game_square.get_col() + 1).get_occupying_piece() is not None:
                # There is a coin there, check if its an enemy piece
                if input_board.get_game_square(input_game_square.get_row() + 1,
                                               input_game_square.get_col() + 1).get_occupying_piece().get_colour() is not \
                        input_piece.get_colour():
                    # It is an enemy piece, check if the jump spot is clear
                    if input_board.get_game_square(input_game_square.get_row() + 2,
                                                   input_game_square.get_col() + 2).get_occupying_piece() is None:
                        # Legal jump identified, add it to the list
                        list_moves.append(
                            input_board.get_game_square(input_game_square.get_row() + 2,
                                                        input_game_square.get_col() + 2))

                        # remove the enemy coin temporarily
                        coin_removed = copy.deepcopy(input_board.get_game_square(
                            input_game_square.get_row() + 1, input_game_square.get_col() + 1).get_occupying_piece())

                        input_board.get_game_square(input_game_square.get_row() + 1,
                                                    input_game_square.get_col() + 1).remove_occupying_piece()

                        # Iterate and check if coin can jump more from there
                        checkers_jump(input_board, input_piece,
                                      input_board.get_game_square(input_game_square.get_row() + 2,
                                                                  input_game_square.get_col() + 2), list_moves)
                        # put back the coin removed
                        input_board.get_game_square(input_game_square.get_row() + 1,
                                                    input_game_square.get_col() + 1).put_piece_here(coin_removed)

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
        previous_destination_piece = copy.deepcopy(
            destination_square.get_occupying_piece())
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
    previous_origin_square.put_piece_here(
        previous_destination_square.get_occupying_piece())
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
    prev_piece_from_destination = temp_move(
        origin_gamesquare, destination_gamesquare)

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
                undo_temp_move(
                    origin_gamesquare, destination_gamesquare, prev_piece_from_destination)
                return True
    else:
        # we have to return everything back before the move
        board.switch_sides()
        undo_temp_move(origin_gamesquare, destination_gamesquare,
                       prev_piece_from_destination)
        raise Exception("Did not find the King")

    # we have to return everything back before the move
    board.switch_sides()
    undo_temp_move(origin_gamesquare, destination_gamesquare,
                   prev_piece_from_destination)
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
