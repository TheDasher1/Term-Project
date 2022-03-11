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
    GeneratePieceMoves = None

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
        self.GeneratePieceMoves = {'P': self.GeneratePawnMoves, 'R': self.GenerateRookMoves,
                                   'N': self.GenerateKnightMoves, 'B': self.GenerateBishopMoves,
                                   'Q': self.GenerateQueenMoves, 'K': self.GenerateKingMoves}

    def movePiece(self, fromSquare, toSquare):
        if self.board[fromSquare[0]][fromSquare[1]] == '-':
            return

        validMoveSet = []

        self.fromX, self.fromY = fromSquare[0], fromSquare[1]
        self.toX, self.toY = toSquare[0], toSquare[1]

        self.pieceToMove = self.board[self.fromX][self.fromY]
        #self.pieceToReplace = self.board[self.toX][self.toY]

        # might need to move this beneth the if statement below this, other wise it runs when ever each piece is clicked on
        # validMoveSet = self.generateValidMoveSet(self.pieceToMove, self.fromX, self.fromY)

        # if self.board[self.fromX][self.fromY] != '-' and self.board[self.fromX][self.fromY][0] == self.CurrentTurn:
        if self.board[self.fromX][self.fromY][0] == self.CurrentTurn:
            
            # only generates the valid moves for a given piece if it is the right players turn
            validMoveSet = self.generateValidMoveSet(self.pieceToMove, self.fromX, self.fromY)
            
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
        # return self.GeneratePieceMoves(piece, row, col)
        print(piece)
        return self.GeneratePieceMoves[piece[1]](piece, row, col)
    
    def GeneratePawnMoves(self, piece, row, col):
        validMoves = []

        # if piece is white, this moveset is used
        if piece[0] == 'w':
            # if the spot in front if the given pawn is empty, it is added to the list of possible moves
            if self.board[row - 1][col] == '-':
                validMoves.append((row - 1, col))

                # if the 2nd spot in front of the given pawn is empty, it is also added to the list of possible moves
                if row == 6 and self.board[row - 2][col] == '-':
                    validMoves.append((row - 2, col))
            
            # if moving to the left column (diagonal to attack) would put it below 0, which would put it off the board
            if (col - 1) >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    validMoves.append((row - 1, col - 1))
            
            # if moving to the right column (diagonal to attack) would put it below 0, which would put it off the board
            if (col + 1) <= 7:
                if self.board[row - 1][col + 1][0] == 'b':
                    validMoves.append((row - 1, col + 1))
        
        # if the piece is a black piece, this moveset is used
        else:
            # if the spot in front if the given pawn is empty, it is added to the list of possible moves
            if self.board[row + 1][col] == '-':
                validMoves.append((row + 1, col))

                # if the 2nd spot in front of the given pawn is empty, it is also added to the list of possible moves
                if row == 1 and self.board[row + 2][col] == '-':
                    validMoves.append((row + 2, col))
            
            # if moving to the left column (diagonal to attack) would put it below 0, which would put it off the board
            if (col - 1) >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    validMoves.append((row + 1, col - 1))
            
            # if moving to the right column (diagonal to attack) would put it below 0, which would put it off the board
            if (col + 1) <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    validMoves.append((row + 1, col + 1))
        
        return validMoves

    def GenerateRookMoves(self, piece, row, col):
        validMoves = []

        if piece[0] == 'w':
            # Start at where the current piece is (row), stop at the length of the board's row - the row is is on, move by -1 to go up
            for r in range(row, len(self.board) - row, - 1):

                # this loop checks all possible spots going right
                # start at the given column, stop at the edge of the column in this row - 1 for indexing, increase by + 1 (goes right)
                for rCr in range(col, len(self.board[r]) - 1, + 1):
                    # checks in the columns of the current row if there are any open spots sideways or if there are any pieces it can kill
                    if self.board[r][rCr + 1] == '-':# or self.board[r][rC + 1][0] == 'b':
                        validMoves.append((r, rCr + 1))
                    
                    if self.board[r][rCr + 1][0] == 'b':
                        validMoves.append((r, rCr + 1))
                        break
                    
                    # if there are no more open spots, break
                    else:
                        break
                
                # start at the given column, stop at the 0th column (index 0), decrease by - 1 (goes left)
                for rCl in range(col, 0, - 1):
                    if self.board[r][rCl - 1] == '-':# or self.board[r][rC - 1][0] == 'b':
                        validMoves.append((r, rCl - 1))
                    
                    if self.board[r][rCl - 1][0] == 'b':
                        validMoves.append((r, rCl - 1))
                        break

                    # if there are no more open spots, break
                    else:
                        break

                if self.board[r - 1][col] == '-':
                    validMoves.append((r - 1, col))
                
                elif self.board[r - 1][col][0] == 'b': # above method and this one can be merged (maybe)
                    validMoves.append((row - 1, col))
                    break
                
                else: # its reached a piece that it can't go past (friendly)
                    break
        
        return validMoves
    
    def GenerateKnightMoves(self, piece, row, col):
        pass

    def GenerateBishopMoves(self, piece, row, col):
        pass
    
    def GenerateQueenMoves(self, piece, row, col):
        pass

    def GenerateKingMoves(self, piece, row, col):
        pass

    def swapPlayers(self):
        # self.CurrentTurn = 'b' if self.CurrentTurn == 'w' else 'b'

        if self.CurrentTurn == 'w':
            self.CurrentTurn = 'b'
        
        elif self.CurrentTurn == 'b':
            self.CurrentTurn = 'w'


