# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import Pieces


class PieceSet:
    """
    A players set of pieces.
        - A checkers piece set consists of 12 identical checkers coins
        - A chess piece set consists of 1 King, 1 Queen, 2 Rooks, 2 Bishops, 2 Knights, and 8 Pawns
    Initially, a piece set will not have castled, and the list of captured pieces will be an empty list.

    Attributes:
        __castled: A bool indicating whether or not the piece set has castled.  A piece set can only castle once per game.
        __pieceSetType: A string indicating whether the hand is a "Chess" hand or a "Checkers" hand.
                        Has no setter method and therefore can't be changed
        __capturedPieces: A list of the pieces that have been captured.  Pieces captured most recently are towards the
                        end of the list.
        __livePieces: A list of the live (un-captured) pieces.

    Exceptions:
        Will throw an exception if the piece set type given is not "Chess" or "Checkers"
    """
    def __init__(self, piece_set_type, colour):
        """
        Purpose: Initialize a piece set.
        :param piece_set_type: string: either "Chess" or "Checkers"
        :param colour: string: piece set __colour
        """
        self.__castled = False
        self.__capturedPieces = []
        if piece_set_type == "Checkers" or piece_set_type == "checkers":
            self.__pieceSetType = "Checkers"
            self.__livePieces = [Pieces.CheckersCoin(colour) for i in range(12)]
        elif piece_set_type == "Chess" or piece_set_type == "chess":
            self.__pieceSetType = "Chess"
            self.__livePieces = [Pieces.King(colour),
                                 Pieces.Queen(colour),
                                 Pieces.Rook(colour), Pieces.Rook(colour),
                                 Pieces.Bishop(colour), Pieces.Bishop(colour),
                                 Pieces.Knight(colour), Pieces.Knight(colour),
                                 Pieces.Pawn(colour), Pieces.Pawn(colour), Pieces.Pawn(colour), Pieces.Pawn(colour),
                                 Pieces.Pawn(colour), Pieces.Pawn(colour), Pieces.Pawn(colour), Pieces.Pawn(colour)]
        else:
            raise Exception("piece_set_type can only be Chess or Checkers")

    def castle(self):
        """
        Mark that the piece set has __castled
        Castle is a special chess move that can only be done once
        """
        self.__castled = True

    def get_castled(self):
        """
        :return: bool: True if this piece set has not __castled, false otherwise
        """
        return self.__castled

    def capture_piece(self, captured_piece):
        """
        Removes the piece from the list of live peices are appends it to the end of the list of captured pieces
        :param captured_piece: a piece to capture
        :return: bool: True is the piece was successfully captured, False otherwise
        """
        if captured_piece in self.__livePieces:
            self.__livePieces.remove(captured_piece)
            self.__capturedPieces.append(captured_piece)
            return True
        else:
            return False

    def get_captured_pieces(self):
        """
        :return: The list of captured pieces
        """
        return self.__capturedPieces

    def get_piece_set_type(self):
        """
        :return: string: The type of game, either "Chess" or "Checkers
        """
        return self.__pieceSetType

    def get_live_pieces(self):
        """
        :return: The list of live (non-captured) pieces
        """
        return self.__livePieces

    def get_number_of_live_pieces(self):
        """
        :return: The number of live (non-captured) pieces
        """
        return len(self.__livePieces)

    def get_number_of_captured_pieces(self):
        """
        :return: The number captured pieces
        """
        return len(self.__capturedPieces)

    def get_colour(self):
        """
        :return: The colour of the piece set
        """
        # All pieces will be the same colour, so just look at one
        if len(self.__livePieces) >= 0:
            return self.__livePieces[0].get_colour()
        else:
            return self.__capturedPieces[0].get_colour()
