# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch


def build_pawn_moves(input_game_square, input_game):
    """
    Build the list of possible moves for a Pawn
    :param input_game_square: GameSquare: The origin game square that you want to build a list of moves for.
    :param input_game: The input game, required to get the game board and game type
    :return list_of_candidate_game_squares: GameSquare[]: List of destination squares the pawn can legally move to
    """

    input_piece = input_game_square.get_occupying_piece()
    input_row = input_game_square.get_row()
    input_col = input_game_square.get_col()
    input_board = input_game.get_board()
    list_of_candidate_game_squares = []

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
                        if type(input_board.get_game_square(input_row, input_col + 1).get_occupying_piece()) \
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
                        if type(input_board.get_game_square(input_row, input_col - 1).get_occupying_piece()) \
                                .__name__ == "Pawn":
                            if input_game.get_light_player().get_colour() == input_piece.get_colour():
                                enemy = input_game.get_dark_player()
                            else:
                                enemy = input_game.get_light_player()
                            if enemy.get_last_move() == ((input_row - 2, input_col - 1),
                                                         (input_row, input_col - 1)):
                                list_of_candidate_game_squares \
                                    .append(input_board.get_game_square(input_row - 1, input_col - 1))
            # anywhere in the middle of the board
            else:
                # check right
                # there need to be an enemy pawn to the right of my pawn
                if input_board.get_game_square(input_row, input_col + 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row,
                                                   input_col + 1).get_occupying_piece().get_colour() is not \
                            input_piece.get_colour():
                        if type(input_board.get_game_square(input_row, input_col + 1).get_occupying_piece()) \
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
                                list_of_candidate_game_squares \
                                    .append(input_board.get_game_square(input_row - 1, input_col + 1))
                # check left
                # there need to be an enemy pawn to the left of my pawn
                if input_board.get_game_square(input_row, input_col - 1).get_occupying_piece() is not None:
                    if input_board.get_game_square(input_row,
                                                   input_col - 1).get_occupying_piece().get_colour() is not \
                            input_piece.get_colour():
                        if type(input_board.get_game_square(input_row, input_col - 1).get_occupying_piece()) \
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
                                list_of_candidate_game_squares \
                                    .append(input_board.get_game_square(input_row - 1, input_col - 1))

    return list_of_candidate_game_squares
