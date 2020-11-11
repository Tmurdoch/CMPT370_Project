# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from abc import ABC, abstractmethod


class PieceInterface(ABC):
    """
    The interface for a game piece.
    Common Attributes:
        __colour: A sting representing the piece set __colour.  Starts with a capital letter (e.g. "White").
    """
    @abstractmethod
    def __init__(self, colour):
        """
        Initialize a piece
        :param colour: Piece __colour as a string with the first letter capitalized (e.g. "White").
        """
        pass

    @abstractmethod
    def set_colour(self, colour):
        """
        :param colour: Piece colour as a string with the first letter capitalized (e.g. "White").
        """
        pass

    @abstractmethod
    def get_colour(self):
        """
        :return: Piece colour as a string (e.g. "White").
        """
        pass


class King(PieceInterface):
    """
    Implements PieceInterface. Represents a King chess piece.
    """
    def __init__(self, colour):
        super().__init__(colour)
        self.__colour = colour

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour


class Queen(PieceInterface):
    """
    Implements PieceInterface. Represents a Queen chess piece.
    """
    def __init__(self, colour):
        super().__init__(colour)
        self.__colour = colour

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour


class Knight(PieceInterface):
    """
    Implements PieceInterface. Represents a Knight chess piece.
    """
    def __init__(self, colour):
        super().__init__(colour)
        self.__colour = colour

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour


class Bishop(PieceInterface):
    """
    Implements PieceInterface. Represents a Bishop chess piece.
    """
    def __init__(self, colour):
        super().__init__(colour)
        self.__colour = colour

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour


class Rook(PieceInterface):
    """
    Implements PieceInterface. Represents a Rook chess piece.
    """
    def __init__(self, colour):
        super().__init__(colour)
        self.__colour = colour

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour


class Pawn(PieceInterface):
    """
    Implements PieceInterface. Represents a Pawn chess piece.
    Initially the pawn has not moved and has not been promoted

    Pawn Specific Attributes:
        __promoted: A bool representing promotion status, True if the pawn has been promoted
        __promotedTo: The piece that the pawn has been promoted to
        movedYet: A bool indicating if the pawn has moved yet, True if it has
                (Pawns can move twice only on their first move)
    """
    def __init__(self, colour):
        super().__init__(colour)
        self.__colour = colour
        self.__promoted = False
        self.__promotedTo = None
        self.__movedYet = False

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour

    def promote(self, class_promoted_to):
        """
        Promote a pawn to a different type of chess piece
        Pawns can only be promoted once
        :param class_promoted_to: String: The type of piece you would like to promote to, first letter capitalized
            Options are "Queen", "Knight", "Bishop", and "Rook"
        :return: True is the piece was successfully promoted, false otherwise
        """
        # TODO: actually make the piece the type of the new object
        if not self.__promoted and class_promoted_to == "Queen":
            self.__promotedTo = Queen(self.__colour)
            self.__promoted = True
            return True
        elif class_promoted_to == "Knight":
            self.__promotedTo = Knight(self.__colour)
            self.__promoted = True
            return True
        elif class_promoted_to == "Bishop":
            self.__promotedTo = Bishop(self.__colour)
            self.__promoted = True
            return True
        elif class_promoted_to == "Rook":
            self.__promotedTo = Rook(self.__colour)
            self.__promoted = True
            return True
        else:
            return False

    def get_promotion_status(self):
        """
        :return: Promotion statues, True if the pawn has been promoted, False otherwise
        """
        return self.__promoted

    def get_promoted_to(self):
        """
        :return: The piece the pawn has been promoted to
        """
        return self.__promotedTo

    def move(self):
        """
        Indicate that the pawn has moved, the pawn will no longer be able to move 2 spaces forward
        """
        self.__movedYet = True

    def get_moved_yet_status(self):
        """
        :return: Move status, True if the pawn has already made its first move, False otherwise
        """
        return self.__movedYet


class CheckersCoin(PieceInterface):
    """
    Implements PieceInterface. Represents a checkers coin game piece.
    Initially the checkers coin has not been promoted

    Checkers coin Specific Attributes:
        __promoted: A bool representing promotion status, True if the checkers coin has been promoted
    """
    def __init__(self, colour):
        super().__init__(colour)
        self.__colour = colour
        self.__promoted = False

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour

    def promote(self):
        """
        Promote a checkers coin
        """
        self.__promoted = True

    def get_promotion_status(self):
        """
        :return: Promotion status, True if the coin has been promoted, False otherwise
        """
        return self.__promoted
