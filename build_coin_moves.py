# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

import copy


def build_coin_moves(input_game_square, input_game):
    """
    Build the list of possible moves for a Checkers coin
    :param input_game_square: GameSquare: The origin game square that you want to build a list of moves for.
    :param input_game: The input game, required to get the game board and game type
    :return list_of_candidate_game_squares: GameSquare[]: List of destination squares the coin can legally move to
    """

    input_piece = input_game_square.get_occupying_piece()
    input_row = input_game_square.get_row()
    input_col = input_game_square.get_col()
    input_board = input_game.get_board()
    list_of_candidate_game_squares = []

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
    if input_piece.is_promoted():
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
    checkers_jump_helper(input_board, input_piece, input_game_square, list_of_candidate_game_squares)
    print("Here is the list of destination game squares that build_coin_moves() has come up with:")
    for square in list_of_candidate_game_squares:
        print(square.get_row_and_column())

    return list_of_candidate_game_squares


def checkers_jump_helper(input_board, input_piece, input_game_square, list_moves):
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
                    checkers_jump_helper(input_board, input_piece,
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
                    checkers_jump_helper(input_board, input_piece,
                                         input_board.get_game_square(input_game_square.get_row() - 2,
                                                                     input_game_square.get_col() + 2), list_moves)
                    # put back the coin removed
                    input_board.get_game_square(input_game_square.get_row() - 1,
                                                input_game_square.get_col() + 1).put_piece_here(coin_removed)

    if input_piece.is_promoted():
        # The coin is promoted and can also jump backwards.

        # Check for the jump and down and to the left
        if input_game_square.get_row() + 2 < input_board.get_size() and input_game_square.get_col() - 2 >= 0:
            # The square jump squares are on the board, check if there is a coin there
            if input_board.get_game_square(input_game_square.get_row() + 1,
                                           input_game_square.get_col() - 1).get_occupying_piece() is not None:
                # There is a coin there, check if its an enemy piece
                if input_board.get_game_square(input_game_square.get_row() + 1,
                                               input_game_square.get_col() - 1).get_occupying_piece().get_colour() \
                        is not input_piece.get_colour():
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
                        checkers_jump_helper(input_board, input_piece,
                                             input_board.get_game_square(input_game_square.get_row() + 2,
                                                                         input_game_square.get_col() - 2), list_moves)

                        # put back the coin removed
                        input_board.get_game_square(input_game_square.get_row() + 1,
                                                    input_game_square.get_col() - 1).put_piece_here(coin_removed)

        # Check for the jump up and to the right
        if input_game_square.get_row() + 2 < input_board.get_size() \
                and input_game_square.get_col() + 2 < input_board.get_size():
            # The square jump squares are on the board, check if there is a coin there
            if input_board.get_game_square(input_game_square.get_row() + 1,
                                           input_game_square.get_col() + 1).get_occupying_piece() is not None:
                # There is a coin there, check if its an enemy piece
                if input_board.get_game_square(input_game_square.get_row() + 1,
                                               input_game_square.get_col() + 1).get_occupying_piece().get_colour() \
                        is not input_piece.get_colour():
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
                        checkers_jump_helper(input_board, input_piece,
                                             input_board.get_game_square(input_game_square.get_row() + 2,
                                                                         input_game_square.get_col() + 2), list_moves)
                        # put back the coin removed
                        input_board.get_game_square(input_game_square.get_row() + 1,
                                                    input_game_square.get_col() + 1).put_piece_here(coin_removed)
    return
