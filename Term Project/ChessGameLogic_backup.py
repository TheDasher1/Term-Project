import numpy as np

class ChessGameLogic:

    # initial variables
    #whiteGoesFirst = True
    CurrentTurn = 'w' # since white goes first, default value is set to 'w'
    pawnMovedFromColumns = []
    board = None#np.array([
                        # ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                        # ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                        # ['-', '-', '-', '-', '-', '-', '-', '-'],
                        # ['-', '-', '-', '-', '-', '-', '-', '-'],
                        # ['-', '-', '-', '-', '-', '-', '-', '-'],
                        # ['-', '-', '-', '-', '-', '-', '-', '-'],
                        # ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                        # ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
                        # ]) # This array will represent the chess board with 8 rows and 8 columns, spaces are represented with '-'
    
    # board = np.array([
    #                     ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'], # Uppercase represents black pieces
    #                     ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    #                     ['-', '-', '-', '-', '-', '-', '-', '-'],
    #                     ['-', '-', '-', '-', '-', '-', '-', '-'],# empty spaces are represented by '-'
    #                     ['-', '-', '-', '-', '-', '-', '-', '-'],
    #                     ['-', '-', '-', '-', '-', '-', '-', '-'],
    #                     ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], # Lowercase represents white pieces
    #                     ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    #                     ]) # This array will represent the chess board with 8 rows and 8 columns, spaces are represented with '-'

    def __init__(self):
        # initialise the board
        self.board = np.array([
                              ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                              ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                              ['-', '-', '-', '-', '-', '-', '-', '-'],
                              ['-', '-', '-', '-', '-', '-', '-', '-'],
                              ['-', '-', '-', '-', '-', '-', '-', '-'],
                              ['-', '-', '-', '-', '-', '-', '-', '-'],
                              ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                              ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
                              ]) # This array will represent the chess board with 8 rows and 8 columns, spaces are represented with '-'

    def movePiece(self, fromSquare, toSquare):
        if self.board[fromSquare[0]][fromSquare[1]] == '-':
            return

        validMoveSet = []

        self.fromX, self.fromY = fromSquare[0], fromSquare[1]
        self.toX, self.toY = toSquare[0], toSquare[1]

        self.pieceToMove = self.board[self.fromX][self.fromY]
        #self.pieceToReplace = self.board[self.toX][self.toY]

        validMoveSet = self.generateValidMoveSet(self.pieceToMove, self.fromX, self.fromY)

        if self.board[self.fromX][self.fromY] != '-' and self.board[self.fromX][self.fromY][0] == self.CurrentTurn:
            # if self.board[self.toX][self.toY] in validMoveSet: # performs the move if it is within the valid move sets generated for the piece
            if toSquare in validMoveSet:
                self.board[self.fromX][self.fromY] = '-'
                self.board[self.toX][self.toY] = self.pieceToMove

                self.swapPlayers()
                

        # self.pieceToMove = self.board[fromSquare[0]][fromSquare[1]]
        # self.pieceToReplace = self.board[toSquare[0]][toSquare[1]]

        # if self.board[fromSquare[0]][fromSquare[0]] != '-':
        #     self.board[fromSquare[0]][fromSquare[1]] = '-'
        #     self.board[toSquare[0]][toSquare[1]] = self.pieceToMove

    def generateValidMoveSet(self, piece, row, col):
        generatedMoves = []
        r = 0
        c = 0

        if piece == 'wP':
            if self.pawnInStartPosition(piece, row, col):
                r = row - 2
                c = col
                generatedMoves.append((r, c))
                r = row - 1
                c = col
                generatedMoves.append((r, c))
            else:
                r = row - 1
                c = col
                generatedMoves.append((r, c))
        
        elif piece == 'bP':
            if self.pawnInStartPosition(piece, row, col):
                r = row + 2
                c = col
                generatedMoves.append((r, c))
                r = row + 1
                c = col
                generatedMoves.append((r, c))
            else:
                r = row + 1
                c = col
                generatedMoves.append((r, c))

        return generatedMoves

    def pawnInStartPosition(self, piece, row, col):
        # if piece == 'bP' and piece in self.board[1] and col not in self.pawnMovedFromColumns:
        if piece == 'bP' and (row, col) not in self.pawnMovedFromColumns:
            self.pawnMovedFromColumns.append((row, col))
            return True
        # elif piece == 'wP' and piece in self.board[6] and col not in self.pawnMovedFromColumns:
        if piece == 'wP' and (row, col) not in self.pawnMovedFromColumns:
            self.pawnMovedFromColumns.append((row, col))
            return True
        
        return False

    def swapPlayers(self):
        # self.CurrentTurn = 'b' if self.CurrentTurn == 'w' else 'b'

        if self.CurrentTurn == 'w':
            self.CurrentTurn = 'b'
        
        elif self.CurrentTurn == 'b':
            self.CurrentTurn = 'w'


