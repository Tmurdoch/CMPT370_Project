# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import Pieces
from GameType import GameType


class PieceSet:
    """
    A players set of pieces.
        - A checkers piece set consists of 12 identical checkers coins
        - A chess piece set consists of 1 King, 1 Queen, 2 Rooks, 2 Bishops, 2 Knights, and 8 Pawns
    Initially, a piece set will not have castled, and the list of captured pieces will be an empty list.

    Attributes:
        __pieceSetType: A string indicating whether the Game type for the set is a "Chess" type or a "Checkers" type.
                        Has no setter method and therefore can't be changed
        __capturedPieces: A list of the pieces that have been captured.  Pieces captured most recently are towards the
                        end of the list.
        __livePieces: A list of the live (un-captured) pieces.

    Exceptions:
        Will throw an exception if the piece set type given is not "Chess" or "Checkers"
    """

    def __init__(self, piece_set_type, colour):
        """
        Purpose: Initialize a piece set
        :param piece_set_type: integer: either "1" for chess or "0" for Checkers
        :param colour: string: piece set __colour
        """
        self.__capturedPieces = []
        self.__pieceSetType = piece_set_type
        if piece_set_type == GameType.CHECKERS:
            self.__livePieces = [Pieces.CheckersCoin(colour, 1), Pieces.CheckersCoin(colour, 2),
                                 Pieces.CheckersCoin(colour, 3), Pieces.CheckersCoin(colour, 4),
                                 Pieces.CheckersCoin(colour, 5), Pieces.CheckersCoin(colour, 6),
                                 Pieces.CheckersCoin(colour, 7), Pieces.CheckersCoin(colour, 8),
                                 Pieces.CheckersCoin(colour, 9), Pieces.CheckersCoin(colour, 10),
                                 Pieces.CheckersCoin(colour, 11), Pieces.CheckersCoin(colour, 12)]
            self.__all = []
            x = 0
            while x != len(self.__livePieces):
                self.__all.append(self.__livePieces[x])
                x += 1
        elif piece_set_type == GameType.CHESS:
            self.__livePieces = [Pieces.King(colour, 1),
                                 Pieces.Queen(colour, 2),
                                 Pieces.Rook(colour, 3), Pieces.Rook(colour, 4),
                                 Pieces.Bishop(colour, 5), Pieces.Bishop(colour, 6),
                                 Pieces.Knight(colour, 7), Pieces.Knight(colour, 8),
                                 Pieces.Pawn(colour, 9), Pieces.Pawn(colour, 10),
                                 Pieces.Pawn(colour, 11), Pieces.Pawn(colour, 12),
                                 Pieces.Pawn(colour, 13), Pieces.Pawn(colour, 14),
                                 Pieces.Pawn(colour, 15), Pieces.Pawn(colour, 16)]
            self.__all = []
            x = 0
            while x != len(self.__livePieces):
                self.__all.append(self.__livePieces[x])
                x += 1
        else:
            raise Exception("piece_set_type can only be Chess or Checkers")

    def capture_piece(self, captured_piece):
        """
        Removes the piece from the list of live pieces and appends it to the end of the list of captured pieces
        :param captured_piece: a piece to capture
        :return: bool: If the piece was successfully captured, return True, False otherwise
        """
        print("capture_piece() was called on piece id " + str(captured_piece.get_piece_id()))

        live_ids = self.get_live_piece_ids()

        print("Here is the list of all the live ids: ")
        print(live_ids)

        for piece_id_index, piece_id in enumerate(live_ids):
            if captured_piece.get_piece_id() == piece_id:
                self.__livePieces.pop(piece_id_index)
                self.__capturedPieces.append(captured_piece)
                print("Capture successful, now here is the list of all the live ids: ")
                print(self.get_live_piece_ids())
                return True

        print("The piece you are trying to capture has id: " + str(captured_piece.get_piece_id()) +
              ", but that was not found in the list of ids :(")
        return False

    def get_captured_pieces(self):
        """ :return: Piece[]: The list of captured pieces """
        return self.__capturedPieces

    def get_piece_set_type(self):
        """ :return: string: The type of game, either "Chess" or "Checkers
        """
        return self.__pieceSetType

    def get_live_pieces(self):
        """ :return: Piece[]: The list of live (non-captured) pieces """
        return self.__livePieces

    def get_all_pieces(self):
        return self.__all

    def get_live_piece_ids(self):
        """
        :return: int[]: A list containing all the list piece ids
        Note: Live piece ids will be in the same order as the corresponding pieces are in __live_pieces
        """
        live_ids = []
        for piece in self.__livePieces:
            live_ids.append(piece.get_piece_id())
        return live_ids

    def get_number_of_live_pieces(self):
        """ :return: The number of live (non-captured) pieces """
        return len(self.__livePieces)

    def get_number_of_captured_pieces(self):
        """ :return: The number of captured pieces """
        return len(self.__capturedPieces)

    def get_colour(self):
        """ :return: The colour of the piece set """
        # All pieces will be the same colour, so just look at one
        if len(self.__livePieces) >= 0:
            return self.__livePieces[0].get_colour()
        else:
            return self.__capturedPieces[0].get_colour()
