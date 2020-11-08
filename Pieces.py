# Board Game Simulator
# CMPT 370 Group 4
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from abc import ABC, abstractmethod


class PieceInterface(ABC):
    """
    The interface for a game piece.
    Common Attributes:
        colour: A sting representing the piece set colour.  Starts with a capital letter (e.g. "White").
    """
    @abstractmethod
    def __init__(self, colour):
        """
        Initialize a piece
        :param colour: Piece colour as a string with the first letter capitalized (e.g. "White").
        """
        self.colour = colour

    @abstractmethod
    def set_colour(self, colour):
        """
        :param colour: Piece colour as a string with the first letter capitalized (e.g. "White").
        """
        pass

    @abstractmethod
    def get_colour(self):
        """
        :return: colour: Piece colour as a string (e.g. "White").
        """
        pass


class King(PieceInterface):
    """
    Implements PieceInterface. Represents a King chess piece.
    """
    def __init__(self, colour):
        super().__init__(colour)

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour


class Queen(PieceInterface):
    """
    Implements PieceInterface. Represents a Queen chess piece.
    """
    def __init__(self, colour):
        super().__init__(colour)

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour


class Knight(PieceInterface):
    """
    Implements PieceInterface. Represents a Knight chess piece.
    """
    def __init__(self, colour):
        super().__init__(colour)

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour


class Bishop(PieceInterface):
    """
    Implements PieceInterface. Represents a Bishop chess piece.
    """
    def __init__(self, colour):
        super().__init__(colour)

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour


class Rook(PieceInterface):
    """
    Implements PieceInterface. Represents a Rook chess piece.
    """
    def __init__(self, colour):
        super().__init__(colour)

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour


class Pawn(PieceInterface):
    """
    Implements PieceInterface. Represents a Pawn chess piece.
    Initially the pawn has not moved and has not been promoted

    Pawn Specific Attributes:
        promoted: A bool representing promotion status, True if the pawn has been promoted
        promotedTo: The piece that the pawn has been promoted to
        movedYet: A bool indicating if the pawn has moved yet, True if it has
                (Pawns can move twice only on their first move)
    """
    def __init__(self, colour):
        super().__init__(colour)
        self.promoted = False
        self.promotedTo = None
        self.movedYet = False

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour

    def promote(self, class_promoted_to):
        """
        Promote a pawn to a different type of chess piece
        :param class_promoted_to: String: The type of piece you would like to promote to, first letter capitalized
            (e.g. "King").
        :return: True is the piece was successfully promoted, false otherwise
        """
        if class_promoted_to == "King":
            self.promotedTo = King(self.colour)
            self.promoted = True
            return True
        elif class_promoted_to == "Queen":
            self.promotedTo = Queen(self.colour)
            self.promoted = True
            return True
        elif class_promoted_to == "Knight":
            self.promotedTo = Queen(self.colour)
            self.promoted = True
            return True
        elif class_promoted_to == "Bishop":
            self.promotedTo = Bishop(self.colour)
            self.promoted = True
            return True
        elif class_promoted_to == "Rook":
            self.promotedTo = Rook(self.colour)
            self.promoted = True
            return True
        else:
            return False

    def get_promotion_status(self):
        """
        :return: Promotion statues, True if the pawn has been promoted, False otherwise
        """
        return self.promoted

    def move(self):
        """
        Indicate that the pawn has moved, the pawn will no longer be able to move 2 spaces forward
        """
        self.movedYet = True

    def get_moved_yet_status(self):
        """
        :return: Move status, True if the pawn has already made its first move, False otherwise
        """
        return self.movedYet


class CheckersCoin(PieceInterface):
    """
    Implements PieceInterface. Represents a checkers coin game piece.
    Initially the checkers coin has not been promoted

    Checkers coin Specific Attributes:
        promoted: A bool representing promotion status, True if the checkers coin has been promoted
    """
    def __init__(self, colour):
        super().__init__(colour)
        self.promoted = False

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour

    def promote(self):
        """
        Promote a checkers coin
        """
        self.promoted = True

    def get_promotion_status(self):
        """
        :return: Promotion status, True if the coin has been promoted, False otherwise
        """
        return self.promoted
