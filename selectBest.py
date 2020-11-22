# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import random


def select_best(candidate_game_squares):
    """
    Chooses and return the best game square to move to from a list of candidate squares
    :param: List of GameSquares to choose from
    :return: GameSquare, the best game square to move to. Returns None if there are no moves for that square
    """
    if not candidate_game_squares:
        # List of moves is empty
        return None
    elif len(candidate_game_squares) == 1:
        # The is only one move, it has to be the best
        return candidate_game_squares[0]
    else:
        # TODO: Some AI code to evaluate the list of moves to choose the best one, in the mean time we are jsut
        #  returning the first one in the list
        # Right now we will just return a random candidate
        random_index = (random.randrange(0, len(candidate_game_squares), 1))
        return candidate_game_squares[random_index]
