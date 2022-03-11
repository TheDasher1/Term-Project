import random
import numpy as np

class ChessGameLogic:

    # initial variables
    #whiteGoesFirst = True
    CurrentTurn = 'w' # since white goes first, default value is set to 'w'
    pawnMovedFromColumns = []
    HumanVSHuman = True
    WhiteKingPosition = (7, 4) # the default of the white king's position
    BlackKingPosition = (0, 4) # the default of the black king's position
    CurrentKingInCheckPos = None
    CurrentKingInCheckName = None
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
        if self.board[fromSquare[0]][fromSquare[1]] == '-' or self.board[fromSquare[0]][fromSquare[1]][0] != self.CurrentTurn:
            print('Empty spot or not right piece chosen.')
            return -1

        validMoveSet = []
        self.InCheck = False

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
            
            # if the king is in check, remove the check
            # 1) Check around the king for open spots, append any to the list of valid moves
            # 2) Check all allied pieces to see if they can be moved to block the check, append any found to the list of valid moves
            # 3) set that list to this list of validMoveSet
            if self.InCheck[0]:
                self.CheckForOpenSpotsNextToKing()
            
            # if self.board[self.toX][self.toY] in validMoveSet: # performs the move if it is within the valid move sets generated for the piece
            if toSquare in validMoveSet:
                self.board[self.fromX][self.fromY] = '-'
                self.board[self.toX][self.toY] = self.pieceToMove
                
                self.swapPlayers()
                print(f'Sucessful move, {self.CurrentTurn}\'s turn.')

                # if the piece moved is one of the kings, update that king's position
                # update the white king's position if the piece moved is the white king
                if self.board[self.toX][self.toY] == 'wK':
                    self.WhiteKingPosition = (self.toX, self.toY)
                
                # update the black king's position if the piece moved is the black king
                elif self.board[self.toX][self.toY] == 'bK':
                    self.BlackKingPosition = (self.toX, self.toY)

                # # check if after this move, the opposing king is in check
                # InCheck = self.checkIfKingIsInCheck(self.pieceToMove, self.toX, self.toY)

                # if InCheck[0]:
                #     pass

            else:
                print(f'Invalid move, {self.CurrentTurn} moves again.')
                validMoveSet = []
            
            # check if after this move, the opposing king is in check
            self.InCheck = self.checkIfKingIsInCheck(self.pieceToMove, self.toX, self.toY)

            # if self.InCheck[0]:
            #     pass

        return 1
        # self.pieceToMove = self.board[fromSquare[0]][fromSquare[1]]
        # self.pieceToReplace = self.board[toSquare[0]][toSquare[1]]

        # if self.board[fromSquare[0]][fromSquare[0]] != '-':
        #     self.board[fromSquare[0]][fromSquare[1]] = '-'
        #     self.board[toSquare[0]][toSquare[1]] = self.pieceToMove

    def CheckForOpenSpotsNextToKing(self, king, kingPos):
        validMoves = []

        validMoves = self.GenerateKingMoves(king, kingPos[0], kingPos[1])

        return validMoves

    # checks all 8 directions of the given king piece to see if there is an opposing piece there that can attack
    def checkIfGivenKingIsInCheck(self, KingPiece, KingPieceRow, KingPieceCol):
        enemyPiece = None
        isInCheck = False

        if KingPiece[0] == 'w':
            enemyPiece = 'b'
        elif KingPiece[0] == 'b':
            enemyPiece = 'w'
        
        # ------------------ FORWARD/UP -------------------------------
        # Start at where the current piece is (row), stop at the length of the board's row - the row is is on, move by -1 to go up
        # stops at the 0th row
        for r in range(KingPieceRow, 0, - 1):
            if self.board[r - 1][KingPieceCol][0] == enemyPiece: # above method and this one can be merged (maybe)
                isInCheck = True
                break
        
        # ----------------- BACKWARDS/DOWN ---------------------------
        for r in range(KingPieceRow, len(self.board[KingPieceRow]) - 1, + 1):
            if self.board[r + 1][KingPieceCol][0] == enemyPiece: # above method and this one can be merged (maybe)
                isInCheck = True
                break

        # ------------------- RIGHT -----------------------------------
        # this loop checks all possible spots going right
        # start at the given column, stop at the edge of the column in this row - 1 for indexing, increase by + 1 (goes right)
        for rCr in range(KingPieceCol, len(self.board[KingPieceRow]) - 1, + 1):
            # checks in the columns of the current row if there are any open spots sideways or if there are any pieces it can kill
            if self.board[KingPieceRow][rCr + 1][0] == enemyPiece:
                isInCheck = True
                break
        
        # ------------------- LEFT -------------------------------------
        # start at the given column, stop at the 0th column (index 0), decrease by - 1 (goes left)
        for rCl in range(KingPieceCol, 0, - 1):
            if self.board[KingPieceRow][rCl - 1][0] == enemyPiece:
                isInCheck = True
                break
        
        # ------------------- DIAGONALY DOWN RIGHT --------------------------
        # performs the check going diagonaly down right
        for r, c in zip(range(KingPieceRow, len(self.board[KingPieceRow]) - 1, 1), range(KingPieceCol, len(self.board[KingPieceRow]) - 1, 1)):
            if self.board[r + 1][c + 1][0] == enemyPiece:
                isInCheck = True
                break
        
        # ------------------- DIAGONALY DOWN LEFT --------------------------
        # performs the check going diagonaly down left
        r, c = KingPieceRow, KingPieceCol
        while True:
            # check if the next movement is out of bounds or not
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == enemyPiece:
                    isInCheck = True
                    break
                
            r += 1 # might not need these 2 lines
            c -= 1
                
            # breaks if the bottom row is reached or if the 0th column is reached
            if r >= 7 or c <= 0:
                break
        
        # ------------------- DIAGONALY UP RIGHT --------------------------
        # performs the check going diagonaly up right
        r, c = KingPieceRow, KingPieceCol
        while True:
            # check if the next movement is out of bounds or not
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == enemyPiece:
                    isInCheck = True
                    break
                
            r -= 1
            c += 1

            # breaks if the bottom row is reached or if the 0th column is reached
            if r <= 0 or c >= 7:
                break

        # ------------------- DIAGONALY UP LEFT --------------------------
        # performs the check going diagonaly up left
        r, c = KingPieceRow, KingPieceCol
        while True:
            # check if the next movement is out of bounds or not
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == enemyPiece:
                    isInCheck = True
                    break
            r -= 1
            c -= 1

            # breaks if the bottom row is reached or if the 0th column is reached
            if r <= 0 or c <= 0:
                break

    def checkIfKingIsInCheck(self, piece, r, c):
        if piece[0] == 'w':
            enemyKingPos = self.BlackKingPosition
            enemyKingName = 'bK'
        
        elif piece[0] == 'b':
            enemyKingPos = self.WhiteKingPosition
            enemyKingName = 'wK'

        # the list of possible moves for this piece
        PhantomMoveSet = self.generateValidMoveSet(piece, r, c)

        if enemyKingPos in PhantomMoveSet:
            print(f'{enemyKingName} is in check.')
            
            # location will be store in global variable
            self.CurrentKingInCheckPos = enemyKingPos
            self.CurrentKingInCheckName = enemyKingName
            
            return True, enemyKingName
        
        else:
            return False, None

    def generateValidMoveSet(self, piece, row, col):
        # return self.GeneratePieceMoves(piece, row, col)
        # print(piece)
        return self.GeneratePieceMoves[piece[1]](piece, row, col)
    
    # this method generates the -------------- PAWN'S ----------- move set
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

    # this method generates the -------------- ROOK'S ----------- move set
    def GenerateRookMoves(self, piece, row, col):
        validMoves = []

        # -------------------------------- WHITE ROOKS -----------------------------------------
        if piece[0] == 'w':
            # ------------------ FORWARD/UP -------------------------------
            # Start at where the current piece is (row), stop at the length of the board's row - the row is is on, move by -1 to go up
            # stops at the 0th row
            for r in range(row, 0, - 1):

                # if self.board[r - 1][col] == '-':
                #     validMoves.append((r - 1, col))
                
                if self.board[r - 1][col][0] == 'b': # above method and this one can be merged (maybe)
                    validMoves.append((r - 1, col))
                    break
                
                elif self.board[r - 1][col] == '-':
                    validMoves.append((r - 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break
            
            # ----------------- BACKWARDS/DOWN ---------------------------
            for r in range(row, len(self.board[row]) - 1, + 1):

                # if self.board[r - 1][col] == '-':
                #     validMoves.append((r - 1, col))
                
                if self.board[r + 1][col][0] == 'b': # above method and this one can be merged (maybe)
                    validMoves.append((r + 1, col))
                    break
                
                elif self.board[r + 1][col] == '-':
                    validMoves.append((r + 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break

            # ------------------- RIGHT -----------------------------------
            # this loop checks all possible spots going right
            # start at the given column, stop at the edge of the column in this row - 1 for indexing, increase by + 1 (goes right)
            for rCr in range(col, len(self.board[row]) - 1, + 1):
                # checks in the columns of the current row if there are any open spots sideways or if there are any pieces it can kill
                # if self.board[r][rCr + 1] == '-':# or self.board[r][rC + 1][0] == 'b':
                #     validMoves.append((r, rCr + 1))
                
                if self.board[row][rCr + 1][0] == 'b':
                    validMoves.append((row, rCr + 1))
                    break
                
                elif self.board[row][rCr + 1] == '-':
                    validMoves.append((row, rCr + 1))
                
                # if there are no more open spots, break
                else:
                    break
            
            # ------------------- LEFT -------------------------------------
            # start at the given column, stop at the 0th column (index 0), decrease by - 1 (goes left)
            for rCl in range(col, 0, - 1):
                # if self.board[row][rCl - 1] == '-':# or self.board[r][rC - 1][0] == 'b':
                #     validMoves.append((r, rCl - 1))
                
                if self.board[row][rCl - 1][0] == 'b':
                    validMoves.append((row, rCl - 1))
                    break
                
                elif self.board[row][rCl - 1] == '-':
                    validMoves.append((row, rCl - 1))

                # if there are no more open spots, break
                else:
                    break
        
        # -------------------------------- BLACK ROOKS -----------------------------------------
        # if the piece is a black piece, use these moveset, these are just a mirror of the above for loops
        else:
            # ------------------ FORWARD/UP -------------------------------
            # Start at where the current piece is (row), stop at the length of the board's row - the row is is on, move by -1 to go up
            # stops at the 0th row
            for r in range(row, 0, - 1):

                # if self.board[r - 1][col] == '-':
                #     validMoves.append((r - 1, col))
                
                if self.board[r - 1][col][0] == 'w': # above method and this one can be merged (maybe)
                    validMoves.append((r - 1, col))
                    break
                
                elif self.board[r - 1][col] == '-':
                    validMoves.append((r - 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break
            
            # ----------------- BACKWARDS/DOWN ---------------------------
            for r in range(row, len(self.board) - 1, + 1):

                # if self.board[r - 1][col] == '-':
                #     validMoves.append((r - 1, col))
                
                if self.board[r + 1][col][0] == 'w': # above method and this one can be merged (maybe)
                    validMoves.append((r + 1, col))
                    break
                
                elif self.board[r + 1][col] == '-':
                    validMoves.append((r + 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break

            # ------------------- RIGHT -----------------------------------
            # this loop checks all possible spots going right
            # start at the given column, stop at the edge of the column in this row - 1 for indexing, increase by + 1 (goes right)
            for rCr in range(col, len(self.board[row]) - 1, + 1):
                # checks in the columns of the current row if there are any open spots sideways or if there are any pieces it can kill
                # if self.board[r][rCr + 1] == '-':# or self.board[r][rC + 1][0] == 'b':
                #     validMoves.append((r, rCr + 1))
                
                if self.board[row][rCr + 1][0] == 'w':
                    validMoves.append((row, rCr + 1))
                    break
                
                elif self.board[row][rCr + 1] == '-':
                    validMoves.append((row, rCr + 1))
                
                # if there are no more open spots, break
                else:
                    break
            
            # ------------------- LEFT -------------------------------------
            # start at the given column, stop at the 0th column (index 0), decrease by - 1 (goes left)
            for rCl in range(col, 0, - 1):
                # if self.board[row][rCl - 1] == '-':# or self.board[r][rC - 1][0] == 'b':
                #     validMoves.append((r, rCl - 1))
                
                if self.board[row][rCl - 1][0] == 'w':
                    validMoves.append((row, rCl - 1))
                    break
                
                elif self.board[row][rCl - 1] == '-':
                    validMoves.append((row, rCl - 1))

                # if there are no more open spots, break
                else:
                    break

        return validMoves # returns the list of valid moves
    
    def GenerateKnightMoves(self, piece, row, col):
        validMoves = []
        alliedPiece = None
        
        if piece[0] == 'w':
            alliedPiece = 'w'
        
        elif piece[0] == 'b':
            alliedPiece = 'b'

        # if piece[0] == 'w':
        # -------------------- FORWARD/UP ----------------------
        # generates all the valid moves for the knight going up
        # row - 2 since we're going up and it is greater than or equal to 0 (row = 7 - 2 (going up) = 5, row = 2 - 2 (going up) = 0, row = 1 - 2 = - 1 !>= 0)
        if row - 2 >= 0:
            # check is left is not off the board
            if col - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
                # if self.board[row - 2][col - 1][0] != 'w':
                if self.board[row - 2][col - 1][0] != alliedPiece:
                    validMoves.append((row - 2, col - 1))
            
            # check if right is not off the board
            if col + 1 <= 7:
                # if this spot on the board is not an allied piece, move there
                if self.board[row - 2][col + 1][0] != alliedPiece:
                    validMoves.append((row - 2, col + 1))
        
        # -------------------- BACKWARD/DOWN ----------------------
        # generates all the valid moves for the knight going down
        if row + 2 <= 7:
            # check if left is not off the board
            if col - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
                if self.board[row + 2][col - 1][0] != alliedPiece:
                    validMoves.append((row + 2, col - 1))
            
            # check if right is not off the board
            if col + 1 <= 7:
                # if this spot on the board is not an allied piece, move there
                if self.board[row + 2][col + 1][0] != alliedPiece:
                    validMoves.append((row + 2, col + 1))

        # -------------------- LEFT ----------------------
        # generates all the valid moves for the knight going left
        if col - 2 >= 0:
            # check if turning left is not off the board
            if row - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
                if self.board[row - 1][col - 2][0] != alliedPiece:
                    validMoves.append((row - 1, col - 2))
            
            # check if turning right is not off the board
            if row + 1 <= 7:
                # if this spot on the board is not an allied piece, move there
                if self.board[row + 1][col - 2][0] != alliedPiece:
                    validMoves.append((row + 1, col - 2))
        
        # -------------------- RIGHT ----------------------
        # generates all the valid moves for the knight going right
        if col + 2 <= 7:
            # check if turning left is not off the board
            if row - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
                if self.board[row - 1][col + 2][0] != alliedPiece:
                    validMoves.append((row - 1, col + 2))
            
            # check if turning right is not off the board
            if row + 1 <= 7:
                # if this spot on the board is not an allied piece, move there
                if self.board[row + 1][col + 2][0] != alliedPiece:
                    validMoves.append((row + 1, col + 2))
        
        return validMoves

    def GenerateBishopMoves(self, piece, row, col):
        validMoves = []

        alliedPiece = None
        enemyPiece = None
        
        if piece[0] == 'w':
            alliedPiece = 'w'
            enemyPiece = 'b'
        
        elif piece[0] == 'b':
            alliedPiece = 'b'
            enemyPiece = 'w'
        

        # ------------------- DIAGONALY DOWN RIGHT --------------------------
        # performs the check going diagonaly down right
        # for r in range(row, len(self.board[row]) - 1, 1):
        #     for c in range(col, len(self.board[r]) - 1, 1):
        #         # check is the spot diagonal right below is an opposing piece, if not, add the spot to valid moves list
        #         if self.board[r + 1][c + 1][0] == enemyPiece:
        #             validMoves.append((r + 1, c + 1))
        #             r += 1
        #             break
                
        #         # if spot diagonaly right below is empty, appends it to the list of valid moves
        #         elif self.board[r + 1][c + 1] == '-':
        #             validMoves.append((r + 1, c + 1))
        #             r += 1
                
        #         # if there are no more spots remaining, break
        #         else:
        #             break
        for r, c in zip(range(row, len(self.board[row]) - 1, 1), range(col, len(self.board[row]) - 1, 1)):
            if self.board[r + 1][c + 1][0] == enemyPiece:
                validMoves.append((r + 1, c + 1))
                break
            
            # if spot diagonaly right below is empty, appends it to the list of valid moves
            elif self.board[r + 1][c + 1] == '-':
                validMoves.append((r + 1, c + 1))
                
            # if there are no more spots remaining, break
            else:
                break
        
        # ------------------- DIAGONALY DOWN LEFT --------------------------
        # performs the check going diagonaly down left
        # for rCl, cCl in zip(range(row, len(self.board[row]) - 1, 1), range(col, len(self.board[row]) - 1, -1)):
        r, c = row, col
        while True:
            # check if the next movement is out of bounds or not
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == enemyPiece:
                    validMoves.append((r + 1, c - 1))
                    r += 1 # might not need these 2 lines
                    c -= 1
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r + 1][c - 1] == '-':
                    validMoves.append((r + 1, c - 1))
                    r += 1
                    c -= 1

                    # breaks if the bottom row is reached or if the 0th column is reached
                    if r == 7 or c == 0:
                        break
                    
                # if there are no more spots remaining, break
                else:
                    break
            
            else: # if next movement is outofbounds, break loop
                break
        
        # ------------------- DIAGONALY UP RIGHT --------------------------
        # performs the check going diagonaly up right
        r, c = row, col
        while True:
            # check if the next movement is out of bounds or not
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == enemyPiece:
                    validMoves.append((r - 1, c + 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r - 1][c + 1] == '-':
                    validMoves.append((r - 1, c + 1))
                    r -= 1
                    c += 1

                    # breaks if the bottom row is reached or if the 0th column is reached
                    if r == 0 or c == 7:
                        break
                    
                # if there are no more spots remaining, break
                else:
                    break
            
            else: # if next movement is outofbounds, break loop
                break

        # ------------------- DIAGONALY UP LEFT --------------------------
        # performs the check going diagonaly up left
        r, c = row, col
        while True:
            # check if the next movement is out of bounds or not
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == enemyPiece:
                    validMoves.append((r - 1, c - 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r - 1][c - 1] == '-':
                    validMoves.append((r - 1, c - 1))
                    r -= 1
                    c -= 1

                    # breaks if the bottom row is reached or if the 0th column is reached
                    if r == 0 or c == 0:
                        break
                    
                # if there are no more spots remaining, break
                else:
                    break
            
            else: # if next movement is outofbounds, break loop
                break
        
        return validMoves
    
    def GenerateQueenMoves(self, piece, row, col):
        validMoves = []
        alliedPiece = None
        enemyPiece = None
        
        if piece[0] == 'w':
            alliedPiece = 'w'
            enemyPiece = 'b'
        
        elif piece[0] == 'b':
            alliedPiece = 'b'
            enemyPiece = 'w'

        # ------------------ FORWARD/UP -------------------------------
        # Start at where the current piece is (row), stop at the length of the board's row - the row is is on, move by -1 to go up
        # stops at the 0th row
        for r in range(row, 0, - 1):

            # if self.board[r - 1][col] == '-':
            #     validMoves.append((r - 1, col))
            
            if self.board[r - 1][col][0] == enemyPiece: # above method and this one can be merged (maybe)
                validMoves.append((r - 1, col))
                break
            
            elif self.board[r - 1][col] == '-':
                validMoves.append((r - 1, col))

            else: # its reached a piece that it can't go past (friendly)
                break
        
        # ----------------- BACKWARDS/DOWN ---------------------------
        for r in range(row, len(self.board[row]) - 1, + 1):

            # if self.board[r - 1][col] == '-':
            #     validMoves.append((r - 1, col))
            
            if self.board[r + 1][col][0] == enemyPiece: # above method and this one can be merged (maybe)
                validMoves.append((r + 1, col))
                break
            
            elif self.board[r + 1][col] == '-':
                validMoves.append((r + 1, col))

            else: # its reached a piece that it can't go past (friendly)
                break

        # ------------------- RIGHT -----------------------------------
        # this loop checks all possible spots going right
        # start at the given column, stop at the edge of the column in this row - 1 for indexing, increase by + 1 (goes right)
        for rCr in range(col, len(self.board[row]) - 1, + 1):
            # checks in the columns of the current row if there are any open spots sideways or if there are any pieces it can kill
            # if self.board[r][rCr + 1] == '-':# or self.board[r][rC + 1][0] == 'b':
            #     validMoves.append((r, rCr + 1))
            
            if self.board[row][rCr + 1][0] == enemyPiece:
                validMoves.append((row, rCr + 1))
                break
            
            elif self.board[row][rCr + 1] == '-':
                validMoves.append((row, rCr + 1))
            
            # if there are no more open spots, break
            else:
                break
        
        # ------------------- LEFT -------------------------------------
        # start at the given column, stop at the 0th column (index 0), decrease by - 1 (goes left)
        for rCl in range(col, 0, - 1):
            # if self.board[row][rCl - 1] == '-':# or self.board[r][rC - 1][0] == 'b':
            #     validMoves.append((r, rCl - 1))
            
            if self.board[row][rCl - 1][0] == enemyPiece:
                validMoves.append((row, rCl - 1))
                break
            
            elif self.board[row][rCl - 1] == '-':
                validMoves.append((row, rCl - 1))

            # if there are no more open spots, break
            else:
                break
        
        # ------------------- DIAGONALY DOWN RIGHT --------------------------
        # performs the check going diagonaly down right
        for r, c in zip(range(row, len(self.board[row]) - 1, 1), range(col, len(self.board[row]) - 1, 1)):
            if self.board[r + 1][c + 1][0] == enemyPiece:
                validMoves.append((r + 1, c + 1))
                break
            
            # if spot diagonaly right below is empty, appends it to the list of valid moves
            elif self.board[r + 1][c + 1] == '-':
                validMoves.append((r + 1, c + 1))
                
            # if there are no more spots remaining, break
            else:
                break
        
        # ------------------- DIAGONALY DOWN LEFT --------------------------
        # performs the check going diagonaly down left
        # for rCl, cCl in zip(range(row, len(self.board[row]) - 1, 1), range(col, len(self.board[row]) - 1, -1)):
        r, c = row, col
        while True:
            # check if the next movement is out of bounds or not
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == enemyPiece:
                    validMoves.append((r + 1, c - 1))
                    r += 1 # might not need these 2 lines
                    c -= 1
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r + 1][c - 1] == '-':
                    validMoves.append((r + 1, c - 1))
                    r += 1
                    c -= 1

                    # breaks if the bottom row is reached or if the 0th column is reached
                    if r == 7 or c == 0:
                        break
                    
                # if there are no more spots remaining, break
                else:
                    break
            
            else: # if next movement is outofbounds, break loop
                break
        
        # ------------------- DIAGONALY UP RIGHT --------------------------
        # performs the check going diagonaly up right
        r, c = row, col
        while True:
            # check if the next movement is out of bounds or not
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == enemyPiece:
                    validMoves.append((r - 1, c + 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r - 1][c + 1] == '-':
                    validMoves.append((r - 1, c + 1))
                    r -= 1
                    c += 1

                    # breaks if the bottom row is reached or if the 0th column is reached
                    if r == 0 or c == 7:
                        break
                    
                # if there are no more spots remaining, break
                else:
                    break
            
            else: # if next movement is outofbounds, break loop
                break

        # ------------------- DIAGONALY UP LEFT --------------------------
        # performs the check going diagonaly up left
        r, c = row, col
        while True:
            # check if the next movement is out of bounds or not
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == enemyPiece:
                    validMoves.append((r - 1, c - 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r - 1][c - 1] == '-':
                    validMoves.append((r - 1, c - 1))
                    r -= 1
                    c -= 1

                    # breaks if the bottom row is reached or if the 0th column is reached
                    if r == 0 or c == 0:
                        break
                    
                # if there are no more spots remaining, break
                else:
                    break
            
            else: # if next movement is outofbounds, break loop
                break
        
        return validMoves

    def GenerateKingMoves(self, piece, row, col):
        validMoves = []
        alliedPiece = None
        enemyPiece = None
        
        if piece[0] == 'w':
            alliedPiece = 'w'
            enemyPiece = 'b'
        
        elif piece[0] == 'b':
            alliedPiece = 'b'
            enemyPiece = 'w'

        r = row
        c = col

        # --------------------- MOVE UP ------------------------
        if r - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[r - 1][c] == enemyPiece or self.board[r - 1][c] == '-':
                validMoves.append((r - 1, c))
        
        # --------------------- MOVE DOWN ------------------------
        if r + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[r + 1][c] == enemyPiece or self.board[r + 1][c] == '-':
                validMoves.append((r + 1, c))
        
        # --------------------- MOVE LEFT ------------------------
        if c - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[r][c - 1] == enemyPiece or self.board[r][c - 1] == '-':
                validMoves.append((r, c - 1))

        # --------------------- MOVE RIGHT ------------------------
        if c + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[r][c + 1] == enemyPiece or self.board[r][c + 1] == '-':
                validMoves.append((r, c + 1))

        # --------------------- MOVE DIAGONAL UP RIGHT ------------------------
        if r - 1 >= 0 and c + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[r - 1][c + 1] == enemyPiece or self.board[r - 1][c + 1] == '-':
                validMoves.append((r - 1, c + 1))

        # --------------------- MOVE DIAGONAL UP LEFT ------------------------
        if r - 1 >= 0 and c - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[r - 1][c - 1] == enemyPiece or self.board[r - 1][c - 1] == '-':
                validMoves.append((r - 1, c - 1))

        # --------------------- MOVE DIAGONAL DOWN RIGHT ------------------------
        if r + 1 <= 7 and c + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[r + 1][c + 1] == enemyPiece or self.board[r + 1][c + 1] == '-':
                validMoves.append((r + 1, c + 1))

        # --------------------- MOVE DIAGONAL DOWN LEFT ------------------------
        if r + 1 <= 7 and c - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[r + 1][c - 1] == enemyPiece or self.board[r + 1][c - 1] == '-':
                validMoves.append((r + 1, c - 1))
        
        return validMoves

    def swapPlayers(self):
        # self.CurrentTurn = 'b' if self.CurrentTurn == 'w' else 'b'

        if self.CurrentTurn == 'w':
            self.CurrentTurn = 'b'

            if not self.HumanVSHuman:
                self.CPUTurn()
        
        elif self.CurrentTurn == 'b':
            self.CurrentTurn = 'w'

    def CPUTurn(self):
        # select a random black piece
        # check it for valid moves
        # if there are valid moves, select some random move
        rand = random.Random()
        
        availableMoves = []

        randomPiecesList = self.findAllBlackPieces()

        while len(availableMoves) <= 0:
        #     x = np.random.random_integers(0, 1)
        #     y = np.random.random_integers(0, 7)
            
            # randomPiecesList = self.findAllBlackPieces()#self.board[x][y]
            # print(f"Random piece chosen: {randomPiece}")
            randIndex = np.random.random_integers(0, len(randomPiecesList) - 1)
            
            randomPiece = randomPiecesList[randIndex]

            # availableMoves = np.asarray(self.generateValidMoveSet(randomPiece, x, y))
            availableMoves = self.generateValidMoveSet(randomPiece[0], randomPiece[1], randomPiece[2])

            # if the number of available moves is zero, remove the piece because it must mean the piece is blocked in some way
            if len(availableMoves) == 0:
                randomPiecesList.pop(randIndex)

        print(f'Available moves: {availableMoves}')

        # chosenMove = np.random.choice(len(availableMoves), 1)
        chosenMove = rand.choice(availableMoves)

        print(chosenMove)

        self.movePiece((randomPiece[1], randomPiece[2]), chosenMove)
    
    def findAllBlackPieces(self):
        listOfLocations = []

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c][0] == 'b':
                    listOfLocations.append((self.board[r][c], r, c))
            
            # if found max number of black pieces that can be on the board early, break the loop as there is not point looking for more
            if len(listOfLocations) == 16:
                break

        return listOfLocations

    def setVsHuman(self, Val):
        # print(f"{self.HumanVSHuman}\t{Val}")
        self.HumanVSHuman = Val
        # print(f"{self.HumanVSHuman}\t{Val}")

