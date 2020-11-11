# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from abc import ABC, abstractmethod


class Move(ABC):
    """
    The interface for a move
    Common Atrributes:
            __piece: Piece object, denotes the piece wanting to move.
            __ending_square: GameSquare object, denotes ending position on the board wanting to move.
            __move_goodness: double, number denoting how "good" the move will be, instantiated by the AI
            __capture: bool, True if a piece will be capture on move completion
            __castle: bool, True if move is a castling move (restricted to "King" Piece object)
    """
    @abstractmethod
    def __init__(self):
        """
        Initialize a Move object
        """
        pass

    @abstractmethod
    def validate_move(self):
        # TODO: potentially remove this function, moves are guaranteed to be validated because they are possible
        pass

    @abstractmethod
    def execute_move(self):
        pass

    def set_piece(self, piece):
        """
        :param piece: Piece object to be set
        """
        self.__piece = piece

    def get_piece(self):
        """
        :return Piece object for Move
        """
        return self.__piece


class ChessMove(Move):
    def __init__(self):
        pass

    def validate_move(self):
        pass

    def execute_move(self):
        # TODO recognize a castle and call set_castled
        pass

    def set_castled(self):
        """
        return: True on success
                raises exception if failure 
        """
        # TODO: implement this to work with Player class
        """
        if self.__castle:
            raise RuntimeError('Logic error: already castled')
        else:
            return True
        """
        return True


class CheckersMove(Move):

    def __init__(self):
        pass

    def validate_move(self):
        pass

    def execute_move(self):
        pass
