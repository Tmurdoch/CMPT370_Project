# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from abc import ABC, abstractmethod


class PieceInterface(ABC):
    """
    The interface for a game piece.
    Common Attributes:
        __colour: string: Piece colour.
        __id: int: A unique value used to identify the pieces.
    """
    @abstractmethod
    def __init__(self, colour, piece_id):
        """
        Initialize a piece
        :param colour: string: Piece colour.
        :param piece_id: int: A unique value used to identify the pieces.
        """
        self.__colour = colour
        self.__id = piece_id
        pass

    @abstractmethod
    def set_colour(self, colour):
        """
        :param colour: Piece colour as a string.
        """
        pass

    @abstractmethod
    def get_colour(self):
        """
        :return: Piece colour as a string.
        """
        pass

    @abstractmethod
    def get_piece_id(self):
        """
        :return: int: The pieces unique identifier.
        """
        pass


class King(PieceInterface):
    """
    Implements PieceInterface. Represents a King chess piece.
    """

    def __init__(self, colour, piece_id):
        super().__init__(colour, piece_id)
        self.__colour = colour
        self.__id = piece_id
        self.__movedYet = False

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour

    def get_piece_id(self):
        return self.__id

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


class Queen(PieceInterface):
    """
    Implements PieceInterface. Represents a Queen chess piece.
    """

    def __init__(self, colour, piece_id):
        super().__init__(colour, piece_id)
        self.__colour = colour
        self.__id = piece_id

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour

    def get_piece_id(self):
        return self.__id


class Knight(PieceInterface):
    """
    Implements PieceInterface. Represents a Knight chess piece.
    """

    def __init__(self, colour, piece_id):
        super().__init__(colour, piece_id)
        self.__colour = colour
        self.__id = piece_id

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour

    def get_piece_id(self):
        return self.__id


class Bishop(PieceInterface):
    """
    Implements PieceInterface. Represents a Bishop chess piece.
    """

    def __init__(self, colour, piece_id):
        super().__init__(colour, piece_id)
        self.__colour = colour
        self.__id = piece_id

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour

    def get_piece_id(self):
        return self.__id


class Rook(PieceInterface):
    """
    Implements PieceInterface. Represents a Rook chess piece.
    """

    def __init__(self, colour, piece_id):
        super().__init__(colour, piece_id)
        self.__colour = colour
        self.__id = piece_id
        self.__movedYet = False

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour

    def get_piece_id(self):
        return self.__id

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


class Pawn(PieceInterface):
    """
    Implements PieceInterface. Represents a Pawn chess piece.
    Initially the pawn has not moved and has not been promoted.

    Pawn Specific Attributes:
        __movedYet: A bool indicating if the pawn has moved yet, True if it has
                (Pawns can move twice only on their first move)
    """

    def __init__(self, colour, piece_id):
        super().__init__(colour, piece_id)
        self.__colour = colour
        self.__id = piece_id
        self.__movedYet = False

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour

    def get_piece_id(self):
        return self.__id

    def promote(self, class_promoted_to):
        """
        Promote a pawn to a different type of chess piece.
        MAKE SURE TO CATCH AND USE THE NEW PIECE!
        Pawns can only be promoted once because afterwards you should discard the pawn.
        :param class_promoted_to: String: The type of piece you would like to promote to -
            Options are "queen", "knight", "bishop", and "rook"
        :return: If the promotion was successful: A new piece object with the same id
                 If the promotion was unsuccessful: None
        """
        if class_promoted_to.lower() == "queen":
            return Queen(self.__colour, self.__id)
        elif class_promoted_to.lower() == "knight":
            return Knight(self.__colour, self.__id)
        elif class_promoted_to.lower() == "bishop":
            return Bishop(self.__colour, self.__id)
        elif class_promoted_to.lower() == "rook":
            return Rook(self.__colour, self.__id)
        else:
            return None

    def move(self):
        """
        Indicate that the pawn has moved, the pawn will no longer be able to move 2 spaces forward.
        """
        self.__movedYet = True

    def get_moved_yet_status(self):
        """
        :return: Move status, True if the pawn has already made its first move, False otherwise.
        """
        return self.__movedYet


class CheckersCoin(PieceInterface):
    """
    Implements PieceInterface. Represents a checkers coin game piece.
    Initially the checkers coin has not been promoted.

    Checkers coin Specific Attributes:
        __promoted: A bool representing promotion status, True if the checkers coin has been promoted.
    """

    def __init__(self, colour, piece_id):
        super().__init__(colour, piece_id)
        self.__colour = colour
        self.__id = piece_id
        self.__promoted = False

    def set_colour(self, colour):
        self.__colour = colour

    def get_colour(self):
        return self.__colour

    def get_piece_id(self):
        return self.__id

    def promote(self):
        """
        Promote a checkers coin.
        """
        self.__promoted = True

    def is_promoted(self):
        """
        :return: Promotion status, True if the coin has been promoted, False otherwise.
        """
        return self.__promoted
