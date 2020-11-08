# Board Game Simulator
# CMPT 370 Group 4
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from abc import ABC, abstractmethod


class PieceInterface(ABC):
    """
    Purpose:

    """
    @abstractmethod
    def __init__(self, colour):
        self.colour = colour

    @abstractmethod
    def set_colour(self, colour): pass

    @abstractmethod
    def get_colour(self): pass


class King(PieceInterface):
    def __init__(self, colour):
        super().__init__(colour)

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour


class Queen(PieceInterface):
    def __init__(self, colour):
        super().__init__(colour)

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour


class Knight(PieceInterface):
    def __init__(self, colour):
        super().__init__(colour)

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour


class Bishop(PieceInterface):
    def __init__(self, colour):
        super().__init__(colour)

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour


class Rook(PieceInterface):
    def __init__(self, colour):
        super().__init__(colour)

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour


class Pawn(PieceInterface):
    """

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

    def promote_pawn(self, class_promoted_to):
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
        return self.promoted

    def move(self):
        self.movedYet = True

    def get_moved_yet_status(self):
        return self.movedYet


class CheckersCoin(PieceInterface):
    def __init__(self, colour):
        super().__init__(colour)
        self.promoted = False

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour

    def promote(self):
        self.promoted = True

    def get_promotion_status(self):
        return self.promoted
