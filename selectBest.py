# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import random


def select_best(candidate_game_squares):
    """
    Chooses and returns the best game square to move to from a list of candidate squares.
    :param: GameSquare[[game_sq][possible_moves_for_it], [][], ...]: List of GameSquares to choose from.
    :return: GameSquare[][]: [origin_square][square_moving_to]. Returns None if there are no moves for that square.
    """
    random_move = random.choice(candidate_game_squares)
    if not random_move:
        # List of moves is empty
        return None
    elif len(random_move[1]) == 1:
        # The is only one move, it has to be the best
        return [random_move[0], random_move[1]]
    else:
        # TODO: Some AI code to evaluate the list of moves to choose the best one, in the mean time we are just
        #  returning the first one in the list
        # Right now we will just return a random candidate
        random_index = (random.randrange(0, len(random_move[1]), 1))
        return [random_move[0], random_move[1][random_index]]
