# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import random


def select_best(candidate_game_squares):
    """
    Chooses and returns the best game square to move to from a list of candidate squares.
    Note: Right now it is just returning a random candidate.
    :param: GameSquare[[origin_square][destSquare], [][], ...]: List of GameSquares to choose from.
    :return: GameSquare[][]: [origin_square][square_moving_to]. Returns None if there are no moves for that square.
    """
    if len(candidate_game_squares) == 0:
        # List of moves is empty
        print("Can't select best, the AI has no moves available")
        return None
    elif len(candidate_game_squares) == 1:
        # The is only one move, it has to be the best
        return [candidate_game_squares[0][0], candidate_game_squares[0][1]]
    else:
        # TODO: Develop some AI code to evaluate the list of moves to choose the best one, in the mean time we are just
        #  returning a random candidate
        random_move = random.randrange(0, len(candidate_game_squares), 1)
        return [candidate_game_squares[random_move][0], candidate_game_squares[random_move][1]]
