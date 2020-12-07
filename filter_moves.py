# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import build_list_of_moves
import copy


def temp_move(origin_square, destination_square):
    """
    mimics a movement of a piece in the board.
    once used should use undo temp to undo the move
    :param origin_square: GameSquare: where the piece is coming from
    :param destination_square: GameSquare: where the piece is going
    return: piece or None from the destination_square
    """
    previous_destination_piece = None
    # Make a copy of the piece on destination if there is one
    if destination_square.get_occupying_piece() is not None:
        previous_destination_piece = copy.deepcopy(
            destination_square.get_occupying_piece())
    destination_square.put_piece_here(origin_square.get_occupying_piece())
    origin_square.remove_occupying_piece()
    return previous_destination_piece


def undo_temp_move(previous_origin_square, previous_destination_square, previous_destination_piece):
    """
    Undo the move that temp_move did
    :param previous_destination_piece: None or a piece previously on the destination_square
    :param previous_origin_square: GameSquare: what you had for origin_square from temp_move
    :param previous_destination_square: GameSquare: what you had for destination_square from temp_move
    """
    previous_origin_square.put_piece_here(previous_destination_square.get_occupying_piece())
    previous_destination_square.put_piece_here(previous_destination_piece)


def make_move_and_check(origin_game_square, destination_game_square, game):
    """
    This mimics moving the a piece from an origin to a destination
    :param game: Game: The current game object
    :param origin_game_square: GameSquare: where the piece is coming from
    :param destination_game_square: GameSquare: where the piece is going
    :return: Bool: True if the move cause a check and False if it does not
    """
    board = game.get_board()

    prev_piece_from_destination = temp_move(origin_game_square, destination_game_square)  # Make the temp move
    board.switch_sides()   # Board switches as if you have actually made that move

    my_king = None  # My king location

    # enemy moves currently at the bottom of the board get all their moves also look for where my king is
    enemy_moves = []
    for row in board.get_game_board():
        for game_square in row:
            if game_square.get_occupying_piece() is not None:
                # get moves of enemy pieces
                if game_square.get_occupying_piece().get_colour() \
                        is not destination_game_square.get_occupying_piece().get_colour():
                    enemy_moves += build_list_of_moves.build_list_of_moves(game_square, game)
                # find my king
                if game_square.get_occupying_piece().get_colour() \
                        is destination_game_square.get_occupying_piece().get_colour():
                    if type(game_square.get_occupying_piece()).__name__ == "King":
                        my_king = game_square

    # Make sure you find your king
    if my_king is not None:
        for an_enemy_move in enemy_moves:
            if (my_king.get_row(), my_king.get_col()) == (an_enemy_move.get_row(), an_enemy_move.get_col()):
                # We now have to return everything back to the way it was before we made this temp move
                board.switch_sides()
                undo_temp_move(origin_game_square, destination_game_square, prev_piece_from_destination)
                return True
    else:
        # We now have to return everything back to the way it was before we made this temp move
        board.switch_sides()
        undo_temp_move(origin_game_square, destination_game_square, prev_piece_from_destination)
        raise Exception("Did not find the King")

    # We now have to return everything back to the way it was before we made this temp move
    board.switch_sides()
    undo_temp_move(origin_game_square, destination_game_square, prev_piece_from_destination)
    return False


def filter_check_moves(my_game_square, game, list_of_moves_to_be_filtered):
    """
    This creates a filtered list of GameSquares from list_of_moves_to_be_filtered that filter
    all the moves that cause a check
    :param my_game_square: GameSquare: where the piece is moving from
    :param game: The current chess game
    :param list_of_moves_to_be_filtered: GameSquares[]: list of GameSquares that is from build_list_of_moves()
    :returns: GameSquares[]: A list of filtered moves
    """
    filtered_moves = []

    # Check every move to see if moves places the king in check
    for my_move in list_of_moves_to_be_filtered:
        if not make_move_and_check(my_game_square, my_move, game):
            filtered_moves.append(my_move)

    return filtered_moves


def build_enemy_list_of_moves(game_square, game):
    """
    - This function is just for testing -
    :param game_square: GameSquare: The square you want to build a list of moves for
    :param game: Game: Current chess game
    :return: GameSquare[]: The list of enemy moves
    """
    # all of enemy list of moves
    enemy_moves = []
    tmp_game = copy.deepcopy(game)
    tmp_gamesquare = copy.deepcopy(game_square)
    board = tmp_game.get_board()

    board.switch_sides()  # switch board to identify enemy moves

    # Check every game piece in the switched board for every moves that the enemy can make
    for row in board.get_game_board():
        for col in row:
            if col.get_occupying_piece() is not None:
                if col.get_occupying_piece().get_colour() is not tmp_gamesquare.get_occupying_piece().get_colour():
                    # add the game square one by one to the enemy moves
                    enemy_moves += build_list_of_moves.build_list_of_moves(col, tmp_game)
    board.switch_sides()   # Switch board back to normal

    return enemy_moves


def is_king_checked(your_king_game_square, game):
    """
    - This function is just for testing -
    :param your_king_game_square: GameSquare: The game square with the king
    :param game: Game: Current chess game
    :return: Bool: Whether or not the king is checked
    """
    # Get all enemy moves, compare enemy moves to king position, all of enemy list of moves
    enemy_moves = []
    board = game.get_board()

    board.switch_sides()   # switch board to identify enemy moves

    # Checks every game piece in the switched board for every moves that the enemy can make
    for row in board.get_game_board():
        for game_square in row:
            if game_square.get_occupying_piece() is not None:
                if game_square.get_occupying_piece().get_colour() \
                        is not your_king_game_square.get_occupying_piece().get_colour():
                    # Add the game square one by one to the enemy moves
                    enemy_moves += build_list_of_moves.build_list_of_moves(game_square, game)

    # check if one of the enemy moves is equal to your kings game square
    for move in enemy_moves:
        if (move.get_row(), move.get_col()) == (your_king_game_square.get_row(), your_king_game_square.get_col()):
            board.switch_sides()
            return True

    board.switch_sides()
    return False
