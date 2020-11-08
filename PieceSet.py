# Board Game Simulator
# CMPT 370 Group 4
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import Pieces


class PieceSet:
    """
    A players set of pieces.
        - A checkers piece set consists of 12 identical checkers coins
        - A chess piece set consists of 1 King, 1 Queen, 2 Rooks, 2 Bishops, 2 Knights, and 8 Pawns
    Initially, a piece set will not have castled, and the list of captured pieces will be an empty list.

    Attributes:
        castled: A bool indicating whether or not the piece set has castled.  A piece set can only castle once per game.
        piece_set_type: A string indicating whether the hand is a "Chess" hand or a "Checkers" hand.
                        Has no setter method and therefore can't be changed
        capturedPieces: A list of the pieces that have been captured.  Pieces captured most recently are towards the
                        end of the list.
        livePieces: A list of the live (un-captured) pieces.

    Exceptions:
        Will throw an exception if the piece set type given is not "Chess" or "Checkers"
    """
    def __init__(self, piece_set_type, colour):
        """
        Purpose: Initialize a piece set.
        :param piece_set_type: string: either "Chess" or "Checkers"
        :param colour: string: piece set colour
        """
        self.castled = False
        self.capturedPieces = []
        if piece_set_type == "Checkers" or piece_set_type == "checkers":
            self.pieceSetType = "Checkers"
            self.livePieces = [Pieces.CheckersCoin(colour) for i in range(12)]
        elif piece_set_type == "Chess" or piece_set_type == "chess":
            self.pieceSetType = "Chess"
            self.livePieces = [Pieces.King(colour),
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
        Mark that the piece set has castled
        Castle is a special chess move that can only be done once
        """
        self.castled = True

    def get_castled(self):
        """
        :return: bool: True if this piece set has not castled, false otherwise
        """
        return self.castled

    def capture_piece(self, captured_piece):
        """
        Removes the piece from the list of live peices are appends it to the end of the list of captured pieces
        :param captured_piece: a piece to capture
        :return: bool: True is the piece was successfully captured, False otherwise
        """
        if captured_piece in self.livePieces:
            self.livePieces.remove(captured_piece)
            self.capturedPieces.append(captured_piece)
            return True
        else:
            return False

    def get_captured_pieces(self):
        """
        :return: The list of captured pieces
        """
        return self.capturedPieces

    def get_piece_set_type(self):
        """
        :return: string: The type of game, either "Chess" or "Checkers
        """
        return self.pieceSetType

    def get_live_pieces(self):
        """
        :return: The list of live (non-captured) pieces
        """
        return self.livePieces
