import random
import numpy as np

class ChessGameLogic:

    # initial variables
    #whiteGoesFirst = True
    CurrentTurn = 'w' # since white goes first, default value is set to 'w'
    DEPTH = 0
    pawnMovedFromColumns = []
    HumanVSHuman = True
    WhiteKingPosition = (7, 4) # the default of the white king's position
    BlackKingPosition = (0, 4) # the default of the black king's position
    IsCheck = False
    ListOfEnpassentAblePawns = []
    CPURunning = False
    board = None#np.array([
                        # ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                        # ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                        # ['-', '-', '-', '-', '-', '-', '-', '-'],
                        # ['-', '-', '-', '-', '-', '-', '-', '-'],
                        # ['-', '-', '-', '-', '-', '-', '-', '-'],
                        # ['-', '-', '-', '-', '-', '-', '-', '-'],
                        # ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                        # ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
                        # ]) # This array will represent the chess board with 8 rows and 8 columns, spaces are represented with '--'
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
    #                     ]) # This array will represent the chess board with 8 rows and 8 columns, spaces are represented with '--'

    def __init__(self):
        # initialise the board
        self.board = np.array([ # '--' is used to represent empty spots since every other character identifier is also 2 character so checking for '-'[1] would cause index error since its only 1 char long string
                              ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                              ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                              ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                              ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
                              ]) # This array will represent the chess board with 8 rows and 8 columns, spaces are represented with '--'
        self.GeneratePieceMoves = {'P': self.GeneratePawnMoves, 'R': self.GenerateRookMoves,
                                   'N': self.GenerateKnightMoves, 'B': self.GenerateBishopMoves,
                                   'Q': self.GenerateQueenMoves, 'K': self.GenerateKingMoves}

    def movePiece(self, board, fromSquare, toSquare):
        if self.board[fromSquare[0]][fromSquare[1]] == '--':# or self.board[fromSquare[0]][fromSquare[1]][0] != self.CurrentTurn:
            print('\nEmpty spot.')# or not right piece chosen.')
            return -1, None
        
        elif self.board[fromSquare[0]][fromSquare[1]][0] != self.CurrentTurn:
            print(f'\nNot this colors turn, it is currently {self.CurrentTurn}s turn.')
            return - 1, None

        validMoveSet = []
        SetOfKingInCheckMoves = []
        KingIncheck = False
    
        self.fromX, self.fromY = fromSquare[0], fromSquare[1]
        self.toX, self.toY = toSquare[0], toSquare[1]

        self.pieceToMove = self.board[self.fromX][self.fromY]
        self.pieceToReplace = self.board[self.toX][self.toY]

        if self.board[self.fromX][self.fromY][0] == self.CurrentTurn:
            
            # only generates the valid moves for a given piece if it is the right players turn
            validMoveSet = self.generateValidMoveSet(self.board, self.pieceToMove, self.fromX, self.fromY)
            
            # if self.board[self.toX][self.toY] in validMoveSet: # performs the move if it is within the valid move sets generated for the piece
            if toSquare in validMoveSet:
                self.board[self.fromX][self.fromY] = '--'
                self.board[self.toX][self.toY] = self.pieceToMove

                # if the piece moved is one of the kings, update that king's position ----------------------
                if self.board[self.toX][self.toY] == 'wK':
                    self.WhiteKingPosition = (self.toX, self.toY)
                
                # update the black king's position if the piece moved is the black king
                elif self.board[self.toX][self.toY] == 'bK':
                    self.BlackKingPosition = (self.toX, self.toY)

                # if the move resulted in the current players king reciving a check
                isKingInCheck = self.checkForChecksAndPins(self.board, self.pieceToMove)

                if isKingInCheck[0]:
                    print("\nThis move resulted in a check occuring. Select a different move.\n")
                    self.board[self.toX][self.toY] = self.pieceToReplace#self.pieceToMove
                    self.board[self.fromX][self.fromY] = self.pieceToMove#self.pieceToReplace
                    # KingIncheck = True

                    # # if king is in check, also generate its moves and activate a flag
                    # SetOfKingInCheckMoves = self.GenerateKingMoves(self.pieceToMove, self.fromX, self.fromY)

                    return -1, None
                
                else: # if the move didn't cause a check on the current player's king, it was a sucessfull move                
                    # self.swapPlayers()
                    print(f'\nSucessful move, {self.CurrentTurn}\'s turn.')

                    # this handles the pawn promotion ------------------------------
                    if (self.pieceToMove == 'wP' and self.toX == 0) or (self.pieceToMove == 'bP' and self.toX == 7):
                        
                        return 2, (self.toX, self.toY)

                    # This handles the pawns enpassent Motion --- EN PASSANT ------------------
                    if (self.pieceToMove == 'bP'): # if the piece moved is a pawn
                        distance = self.fromX + self.toX # check distance between the new pawns square and the old pawn square

                        if (distance == 4): # if the black piece's square moved to is 4, then it gets added to list of enpassent
                        #if (self.toX == 3): # if the pawn is moved to 3
                            self.ListOfEnpassentAblePawns.append((self.pieceToMove, self.toX, self.toY))
                            print(f"\n{self.pieceToMove} has moved 2 squares.\tList of enpassentable pawns: {self.ListOfEnpassentAblePawns}")

                        # if the pawn that is moved is in the list of enpassentable pawns, then it is removed as it is not longer considered enpessatable
                        if (self.pieceToMove, self.fromX, self.fromY) in self.ListOfEnpassentAblePawns:
                            self.ListOfEnpassentAblePawns.remove((self.pieceToMove, self.fromX, self.fromY))
                            print(f"\n{self.pieceToMove} was enpassantable, but this move clears it. Current list: {self.ListOfEnpassentAblePawns}")
                    
                        # ----------------------------------------------------------------------
                        for i in self.ListOfEnpassentAblePawns:
                            # if the spot im going to is behind this pawn which is in the list of enpassantable pawns, delete this pawn
                            # behindPawn = i[1] - 1
                            
                            # if i[0] == 'bP' and behindPawn == i[1] - 1 and self.toY == i[2]:
                            if i[0] == 'wP' and self.toX == i[1] + 1 and self.toY == i[2]:
                                self.board[i[1]][i[2]] = '--'
                                self.ListOfEnpassentAblePawns.remove(i) # removes that pawn from list of enpassantable pawns
                        # ----------------------------------------------------------------------

                    elif (self.pieceToMove == 'wP'): # if the piece moved is a white pawn
                        distance = self.fromX - self.toX
                        pieceToLeft = self.board[self.fromX][self.fromY]

                        if (distance == 2):
                        # if (self.toX == 4): # if the pawn has moved from row 6 to row 4, then it has moved 2 squares
                            self.ListOfEnpassentAblePawns.append((self.pieceToMove, self.toX, self.toY))
                            print(f"\n{self.pieceToMove} has moved 2 squares.\tList of enpassentable pawns: {self.ListOfEnpassentAblePawns}")

                        # if the pawn that is moved is in the list of enpassentable pawns, then it is removed as it is not longer considered enpessatable
                        if (self.pieceToMove, self.fromX, self.fromY) in self.ListOfEnpassentAblePawns:
                            self.ListOfEnpassentAblePawns.remove((self.pieceToMove, self.fromX, self.fromY))
                            print(f"\n{self.pieceToMove} was enpassantable, but this move clears it. Current list: {self.ListOfEnpassentAblePawns}")
                    
                        # if the piece to the left of this pawn is the same spawn
                        # if ((pieceToLeft, self.toX, self.toY) in self.ListOfEnpassentAblePawns):
                        for i in self.ListOfEnpassentAblePawns:
                            # if the spot im going to is behind this pawn which is in the list of enpassantable pawns, delete this pawn
                            # behindPawn = i[1] - 1
                            
                            # if i[0] == 'bP' and behindPawn == i[1] - 1 and self.toY == i[2]:
                            if i[0] == 'bP' and self.toX == i[1] - 1 and self.toY == i[2]:
                                self.board[i[1]][i[2]] = '--'
                                self.ListOfEnpassentAblePawns.remove(i) # removes that pawn from list of enpassantable pawns

                    # ------------------- EN PASSANT LIST UPDATER ---------------------------------

                    

                    # swaps to the other user, CPU or human
                    self.swapPlayers()

            else:
                print(f'\nInvalid move, {self.CurrentTurn} moves again.\n')
                validMoveSet = []
                
                return -1, None

        return 1, None
    
    def checkForChecksAndPins(self, board, piece):
        checks = [] # a list of checks and a tuple of where a piece that is blocking a check is located
        self.IsCheck = False
        
        if piece[0] == 'w':
            kingX, kingY = self.WhiteKingPosition[0], self.WhiteKingPosition[1]
            enemyKingName = 'wK'
        
        elif piece[0] == 'b':
            kingX, kingY = self.BlackKingPosition[0], self.BlackKingPosition[1]
            enemyKingName = 'bK'
        
        KingDirections = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        for j in range(len(KingDirections)):
            d = KingDirections[j]

            possibleBlocker = ()

            for i in range(1, 8):
                endRow = kingX + d[0] * i
                endCol = kingY + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    # endPiece = self.board[endRow][endCol]
                    endPiece = board[endRow][endCol]

                    # if the spot is empty, it doesn't bother checking for anything in the spot
                    if endPiece != '--':
                        # if the end piece is an ally piece
                        if endPiece[0] == enemyKingName[0]: # ending piece is not the same color as the enemy king (use the opposing king to check that)
                            if possibleBlocker == ():
                                # stores the location of the piece that maybe able to be used as a defensive pin and its direction
                                possibleBlocker = ((endRow, endCol, d[0], d[1]))
                        
                            else:
                                break

                        elif endPiece[0] != enemyKingName[0]: # the ending piece is an enemy piece
                            typeOfPiece = endPiece[1]

                            # j represents the direction and i represents the distance the piece is from the king, the lower is is the closer it is to the king
                            if (0 <= j <= 3 and typeOfPiece == 'R' and i > 1) or \
                                (4 <= j <= 7 and typeOfPiece == 'B' and i > 1) or \
                                (i == 1 and typeOfPiece == 'P' and ((endPiece[0] == 'w' and 6 <= j <= 7) or (endPiece[0] == 'b' and 4 <= j <= 5))) or \
                                (typeOfPiece == 'Q' and i > 1) or (i == 1 and typeOfPiece == 'K'):

                                if possibleBlocker == (): # if this is empty, there there is a check presented to the king
                                    self.IsCheck = True

                                    print(f"Check Presented from square {endRow + 1}, {endCol + 1}, from direction: {d}")

                                    checks.append((endRow, endCol, d[0], d[1]))
                                    break
                            
                            else:
                                break
                
                else:
                    break
        
        # all the possible locations a knight could be from the king
        PossibleKnightLocations = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

        for move in PossibleKnightLocations:
            endRow = kingX + move[0]
            endCol = kingY + move[1]

            if 0 <= endRow < 8 and 0 <= endRow < 8:
                # endPiece = self.board[endRow][endCol]
                endPiece = board[endRow][endCol]

                # if the spot is not empty, check for what kind of piece it is
                if endPiece != '--':
                    # if the knight piece there is not the same color, then it presents a check
                    if endPiece[0] != enemyKingName[0] and endPiece[1] == 'N':
                        self.IsCheck = True
                        
                        print(f"Check Presented from square {endRow + 1}, {endCol + 1}, from direction: {move}")
                        
                        checks.append((endRow, endCol, move[0], move[1]))

        return self.IsCheck, checks

    def generateValidMoveSet(self, board, piece, row, col):
        validMoves = []

        self.IsCheck, self.checks = self.checkForChecksAndPins(board, piece)

        if piece[0] == 'w':
            KingPos = self.WhiteKingPosition
            kingX, kingY = self.WhiteKingPosition[0], self.WhiteKingPosition[1]
            enemyKingName = 'bK'
        
        elif piece[0] == 'b':
            KingPos = self.BlackKingPosition
            kingX, kingY = self.BlackKingPosition[0], self.BlackKingPosition[1]
            enemyKingName = 'wK'

        if self.IsCheck:
            if len(self.checks) == 1: # only 1 check
                availMoves = self.GeneratePieceMoves[piece[1]](board, piece, row, col)

                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]

                pieceChecking = board[checkRow][checkCol]

                validSquares = []

                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                
                else:
                    for i in range(1, 8):
                        validSquare = (kingX + check[2] * i, kingY + check[3] * i)
                        validSquares.append(validSquare)

                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                
                for i in range(len(availMoves) - 1, - 1, -1):
                    # if the first input parameter (the piece) is not the king
                    temp = availMoves[i]
                    # pieceBeingMoved = self.board[self.fromX][self.fromY]
                    pieceBeingMoved = board[self.fromX][self.fromY]

                    # if tempPiece != '--':
                    if pieceBeingMoved[1] != 'K': # if the king is the one not being moved
                        tempMove = availMoves[i]

                        # if not (tempMove[0], tempMove[1]) in validSquares:
                        if not ((self.toX, self.toY) in validSquares):
                            availMoves.remove(availMoves[i])
                
                validMoves = availMoves.copy()
                
                # # if there is a check and the piece being moved is the king, generate all possible king moves and return them
                # if (self.IsCheck and self.board[self.fromX][self.fromY][1] == 'K'):
                #     validMoves = self.GenerateKingMoves(self.board[self.fromX][self.fromY], self.toX, self.toY)
                
                
            
            else:
                validMoves = self.GenerateKingMoves(board, piece, row, col)

        else:
            validMoves = self.GeneratePieceMoves[piece[1]](board, piece, row, col)

        return validMoves
    
    # this method generates the -------------- PAWN'S ----------- move set
    def GeneratePawnMoves(self, board, piece, row, col):
        validMoves = []

        if piece[0] == 'w':
            # if the spot in front if the given pawn is empty, it is added to the list of possible moves
            if board[row - 1][col] == '--': # 1 square only move check, only check if the spot infront of the pawn is empty
                validMoves.append((row - 1, col))

                # if the 2nd spot in front of the given pawn is empty, it is also added to the list of possible moves
                if row == 6 and board[row - 2][col] == '--':
                    validMoves.append((row - 2, col))
            
            # if moving to the left column (diagonal to attack) would put it below 0, which would put it off the board
            if (col - 1) >= 0:
                if board[row - 1][col - 1][0] == 'b':
                    validMoves.append((row - 1, col - 1))
            
            # if moving to the right column (diagonal to attack) would put it below 0, which would put it off the board
            if (col + 1) <= 7:
                if board[row - 1][col + 1][0] == 'b': 
                    validMoves.append((row - 1, col + 1))

            # check if there are any enemy pawns to the left or right
            # if there are any black pawns to the left
            if (0 <= col - 1 <= 7):
                pieceToLeft = board[row][col - 1]

                # if the piece to the left of this pawn is a black pawn and it is in the list of enpassantable pawns
                if pieceToLeft == 'bP' and ((pieceToLeft, row, col - 1) in self.ListOfEnpassentAblePawns):
                    print(f'Pawn to the left was enpassantable.')
                    validMoves.append((row - 1, col - 1))
            
            # if there are any squares to is right
            if (0 <= col + 1 <= 7):
                pieceToLeft = board[row][col + 1]

                # if the piece to the left of this pawn is a black pawn and it is in the list of enpassantable pawns
                if pieceToLeft == 'bP' and ((pieceToLeft, row, col + 1) in self.ListOfEnpassentAblePawns):
                    print(f'Pawn to the right was enpassantable.')
                    validMoves.append((row - 1, col + 1))

        
        # if the piece is a black piece, this moveset is used
        else:
            # if the spot in front if the given pawn is empty, it is added to the list of possible moves
            if board[row + 1][col] == '--':
                validMoves.append((row + 1, col))

                # if the 2nd spot in front of the given pawn is empty, it is also added to the list of possible moves
                if row == 1 and board[row + 2][col] == '--':
                    validMoves.append((row + 2, col))
            
            # if moving to the left column (diagonal to attack) would put it below 0, which would put it off the board
            if (col - 1) >= 0:
                if board[row + 1][col - 1][0] == 'w':
                    validMoves.append((row + 1, col - 1))
            
            # if moving to the right column (diagonal to attack) would put it below 0, which would put it off the board
            if (col + 1) <= 7:
                if board[row + 1][col + 1][0] == 'w':
                    validMoves.append((row + 1, col + 1))


            # -----------------------------------------------------------------------------------------
            # check if there are any enemy pawns to the left or right
            # if there are any black pawns to the left
            if (0 <= col - 1 <= 7):
                pieceToLeft = board[row][col - 1]

                # if the piece to the left of this pawn is a black pawn and it is in the list of enpassantable pawns
                if pieceToLeft == 'wP' and ((pieceToLeft, row, col - 1) in self.ListOfEnpassentAblePawns):
                    print(f'Pawn to the left was enpassantable.')
                    validMoves.append((row + 1, col - 1))
            
            # if there are any squares to is right
            if (0 <= col + 1 <= 7):
                pieceToLeft = board[row][col + 1]

                # if the piece to the left of this pawn is a black pawn and it is in the list of enpassantable pawns
                if pieceToLeft == 'wP' and ((pieceToLeft, row, col + 1) in self.ListOfEnpassentAblePawns):
                    print(f'Pawn to the right was enpassantable.')
                    validMoves.append((row + 1, col + 1))
            # -----------------------------------------------------------------------------------------
        
        return validMoves

    def upgradePawn(self, row, col, newPiece):
        
        self.board[row][col] = newPiece

    # this method generates the -------------- ROOK ----------- move set
    def GenerateRookMoves(self, board, piece, row, col):
        validMoves = []

        # -------------------------------- WHITE ROOKS -----------------------------------------
        if piece[0] == 'w':
            # ------------------ FORWARD/UP -------------------------------
            # Start at where the current piece is (row), stop at the length of the board's row - the row is is on, move by -1 to go up
            # stops at the 0th row
            for r in range(row, 0, - 1):

                if board[r - 1][col][0] == 'b': # above method and this one can be merged (maybe)
                    validMoves.append((r - 1, col))
                    break
                
                elif board[r - 1][col] == '--':
                    validMoves.append((r - 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break
            
            # ----------------- BACKWARDS/DOWN ---------------------------
            for r in range(row, len(board[row]) - 1, + 1):

                if board[r + 1][col][0] == 'b': # above method and this one can be merged (maybe)
                    validMoves.append((r + 1, col))
                    break
                
                elif board[r + 1][col] == '--':
                    validMoves.append((r + 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break

            # ------------------- RIGHT -----------------------------------
            # this loop checks all possible spots going right
            # start at the given column, stop at the edge of the column in this row - 1 for indexing, increase by + 1 (goes right)
            for rCr in range(col, len(board[row]) - 1, + 1):
                # checks in the columns of the current row if there are any open spots sideways or if there are any pieces it can kill
                if board[row][rCr + 1][0] == 'b':
                    validMoves.append((row, rCr + 1))
                    break
                
                elif board[row][rCr + 1] == '--':
                    validMoves.append((row, rCr + 1))
                
                # if there are no more open spots, break
                else:
                    break
            
            # ------------------- LEFT -------------------------------------
            # start at the given column, stop at the 0th column (index 0), decrease by - 1 (goes left)
            for rCl in range(col, 0, - 1):
                if board[row][rCl - 1][0] == 'b':
                    validMoves.append((row, rCl - 1))
                    break
                
                elif board[row][rCl - 1] == '--':
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

                if board[r - 1][col][0] == 'w': # above method and this one can be merged (maybe)
                    validMoves.append((r - 1, col))
                    break
                
                elif board[r - 1][col] == '--':
                    validMoves.append((r - 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break
            
            # ----------------- BACKWARDS/DOWN ---------------------------
            for r in range(row, len(board) - 1, + 1):
                if board[r + 1][col][0] == 'w': # above method and this one can be merged (maybe)
                    validMoves.append((r + 1, col))
                    break
                
                elif board[r + 1][col] == '--':
                    validMoves.append((r + 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break

            # ------------------- RIGHT -----------------------------------
            # this loop checks all possible spots going right
            # start at the given column, stop at the edge of the column in this row - 1 for indexing, increase by + 1 (goes right)
            for rCr in range(col, len(board[row]) - 1, + 1):
                # checks in the columns of the current row if there are any open spots sideways or if there are any pieces it can kill
                if board[row][rCr + 1][0] == 'w':
                    validMoves.append((row, rCr + 1))
                    break
                
                elif board[row][rCr + 1] == '--':
                    validMoves.append((row, rCr + 1))
                
                # if there are no more open spots, break
                else:
                    break
            
            # ------------------- LEFT -------------------------------------
            # start at the given column, stop at the 0th column (index 0), decrease by - 1 (goes left)
            for rCl in range(col, 0, - 1):
                if board[row][rCl - 1][0] == 'w':
                    validMoves.append((row, rCl - 1))
                    break
                
                elif board[row][rCl - 1] == '--':
                    validMoves.append((row, rCl - 1))

                # if there are no more open spots, break
                else:
                    break

        return validMoves # returns the list of valid moves
    
    def GenerateKnightMoves(self, board, piece, row, col):
        validMoves = []
        alliedPiece = None
        
        if piece[0] == 'w':
            alliedPiece = 'w'
        
        elif piece[0] == 'b':
            alliedPiece = 'b'

        # -------------------- FORWARD/UP ----------------------
        # generates all the valid moves for the knight going up
        # row - 2 since we're going up and it is greater than or equal to 0 (row = 7 - 2 (going up) = 5, row = 2 - 2 (going up) = 0, row = 1 - 2 = - 1 !>= 0)
        if row - 2 >= 0:
            # check is left is not off the board
            if col - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
                if board[row - 2][col - 1][0] != alliedPiece:
                    validMoves.append((row - 2, col - 1))
            
            # check if right is not off the board
            if col + 1 <= 7:
                # if this spot on the board is not an allied piece, move there
                if board[row - 2][col + 1][0] != alliedPiece:
                    validMoves.append((row - 2, col + 1))
        
        # -------------------- BACKWARD/DOWN ----------------------
        # generates all the valid moves for the knight going down
        if row + 2 <= 7:
            # check if left is not off the board
            if col - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
                if board[row + 2][col - 1][0] != alliedPiece:
                    validMoves.append((row + 2, col - 1))
            
            # check if right is not off the board
            if col + 1 <= 7:
                # if this spot on the board is not an allied piece, move there
                if board[row + 2][col + 1][0] != alliedPiece:
                    validMoves.append((row + 2, col + 1))

        # -------------------- LEFT ----------------------
        # generates all the valid moves for the knight going left
        if col - 2 >= 0:
            # check if turning left is not off the board
            if row - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
                if board[row - 1][col - 2][0] != alliedPiece:
                    validMoves.append((row - 1, col - 2))
            
            # check if turning right is not off the board
            if row + 1 <= 7:
                # if this spot on the board is not an allied piece, move there
                if board[row + 1][col - 2][0] != alliedPiece:
                    validMoves.append((row + 1, col - 2))
        
        # -------------------- RIGHT ----------------------
        # generates all the valid moves for the knight going right
        if col + 2 <= 7:
            # check if turning left is not off the board
            if row - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
                if board[row - 1][col + 2][0] != alliedPiece:
                    validMoves.append((row - 1, col + 2))
            
            # check if turning right is not off the board
            if row + 1 <= 7:
                # if this spot on the board is not an allied piece, move there
                if board[row + 1][col + 2][0] != alliedPiece:
                    validMoves.append((row + 1, col + 2))
        
        return validMoves

    def GenerateBishopMoves(self, board, piece, row, col):
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
        for r, c in zip(range(row, len(board[row]) - 1, 1), range(col, len(board[row]) - 1, 1)):
            if board[r + 1][c + 1][0] == enemyPiece:
                validMoves.append((r + 1, c + 1))
                break
            
            # if spot diagonaly right below is empty, appends it to the list of valid moves
            elif board[r + 1][c + 1] == '--':
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
                if board[r + 1][c - 1][0] == enemyPiece:
                    validMoves.append((r + 1, c - 1))
                    r += 1 # might not need these 2 lines
                    c -= 1
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif board[r + 1][c - 1] == '--':
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
                if board[r - 1][c + 1][0] == enemyPiece:
                    validMoves.append((r - 1, c + 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif board[r - 1][c + 1] == '--':
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
                if board[r - 1][c - 1][0] == enemyPiece:
                    validMoves.append((r - 1, c - 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif board[r - 1][c - 1] == '--':
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
    
    def GenerateQueenMoves(self, board, piece, row, col):
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
            if board[r - 1][col][0] == enemyPiece: # above method and this one can be merged (maybe)
                validMoves.append((r - 1, col))
                break
            
            elif board[r - 1][col] == '--':
                validMoves.append((r - 1, col))

            else: # its reached a piece that it can't go past (friendly)
                break
        
        # ----------------- BACKWARDS/DOWN ---------------------------
        for r in range(row, len(board[row]) - 1, + 1):
            if board[r + 1][col][0] == enemyPiece: # above method and this one can be merged (maybe)
                validMoves.append((r + 1, col))
                break
            
            elif board[r + 1][col] == '--':
                validMoves.append((r + 1, col))

            else: # its reached a piece that it can't go past (friendly)
                break

        # ------------------- RIGHT -----------------------------------
        # this loop checks all possible spots going right
        # start at the given column, stop at the edge of the column in this row - 1 for indexing, increase by + 1 (goes right)
        for rCr in range(col, len(board[row]) - 1, + 1):
            # checks in the columns of the current row if there are any open spots sideways or if there are any pieces it can kill
            if board[row][rCr + 1][0] == enemyPiece:
                validMoves.append((row, rCr + 1))
                break
            
            elif board[row][rCr + 1] == '--':
                validMoves.append((row, rCr + 1))
            
            # if there are no more open spots, break
            else:
                break
        
        # ------------------- LEFT -------------------------------------
        # start at the given column, stop at the 0th column (index 0), decrease by - 1 (goes left)
        for rCl in range(col, 0, - 1):
            if board[row][rCl - 1][0] == enemyPiece:
                validMoves.append((row, rCl - 1))
                break
            
            elif board[row][rCl - 1] == '--':
                validMoves.append((row, rCl - 1))

            # if there are no more open spots, break
            else:
                break
        
        # ------------------- DIAGONALY DOWN RIGHT --------------------------
        # performs the check going diagonaly down right
        for r, c in zip(range(row, len(board[row]) - 1, 1), range(col, len(board[row]) - 1, 1)):
            if board[r + 1][c + 1][0] == enemyPiece:
                validMoves.append((r + 1, c + 1))
                break
            
            # if spot diagonaly right below is empty, appends it to the list of valid moves
            elif board[r + 1][c + 1] == '--':
                validMoves.append((r + 1, c + 1))
                
            # if there are no more spots remaining, break
            else:
                break
        
        # ------------------- DIAGONALY DOWN LEFT --------------------------
        # performs the check going diagonaly down left
        r, c = row, col
        while True:
            # check if the next movement is out of bounds or not
            if r + 1 <= 7 and c - 1 >= 0:
                if board[r + 1][c - 1][0] == enemyPiece:
                    validMoves.append((r + 1, c - 1))
                    r += 1 # might not need these 2 lines
                    c -= 1
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif board[r + 1][c - 1] == '--':
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
                if board[r - 1][c + 1][0] == enemyPiece:
                    validMoves.append((r - 1, c + 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif board[r - 1][c + 1] == '--':
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
                if board[r - 1][c - 1][0] == enemyPiece:
                    validMoves.append((r - 1, c - 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif board[r - 1][c - 1] == '--':
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

    def GenerateKingMoves(self, board, piece, row, col):
        validMoves = []
        enemyPiece = 'b' if piece[0] == 'w' else 'w'
        
        if piece[0] == 'w':
            enemyPiece = 'b'
        
        elif piece[0] == 'b':
            enemyPiece = 'w'

        r = row
        c = col

        # --------------------- MOVE UP ------------------------
        if r - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if board[r - 1][c] == enemyPiece or board[r - 1][c] == '--':
                validMoves.append((r - 1, c))
        
        # --------------------- MOVE DOWN ------------------------
        if r + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if board[r + 1][c] == enemyPiece or board[r + 1][c] == '--':
                validMoves.append((r + 1, c))
        
        # --------------------- MOVE LEFT ------------------------
        if c - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if board[r][c - 1] == enemyPiece or board[r][c - 1] == '--':
                validMoves.append((r, c - 1))

        # --------------------- MOVE RIGHT ------------------------
        if c + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if board[r][c + 1] == enemyPiece or board[r][c + 1] == '--':
                validMoves.append((r, c + 1))

        # --------------------- MOVE DIAGONAL UP RIGHT ------------------------
        if r - 1 >= 0 and c + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if board[r - 1][c + 1] == enemyPiece or board[r - 1][c + 1] == '--':
                validMoves.append((r - 1, c + 1))

        # --------------------- MOVE DIAGONAL UP LEFT ------------------------
        if r - 1 >= 0 and c - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if board[r - 1][c - 1] == enemyPiece or board[r - 1][c - 1] == '--':
                validMoves.append((r - 1, c - 1))

        # --------------------- MOVE DIAGONAL DOWN RIGHT ------------------------
        if r + 1 <= 7 and c + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if board[r + 1][c + 1] == enemyPiece or board[r + 1][c + 1] == '--':
                validMoves.append((r + 1, c + 1))

        # --------------------- MOVE DIAGONAL DOWN LEFT ------------------------
        if r + 1 <= 7 and c - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if board[r + 1][c - 1] == enemyPiece or board[r + 1][c - 1] == '--':
                validMoves.append((r + 1, c - 1))
        
        return validMoves

    def swapPlayers(self):
        # self.CurrentTurn = 'b' if self.CurrentTurn == 'w' else 'b'

        if self.CurrentTurn == 'w':
            self.CurrentTurn = 'b'

            if not self.HumanVSHuman:
                self.CPUTurn()
        
        elif self.CurrentTurn == 'b':# and self.CPURunning == False:
            self.CurrentTurn = 'w'

    def CPUTurn(self):
        # MaxScore = -100000000000
        # moveSet = self.GenerateAllValidMovesForGivenColor()
        # random.shuffle(moveSet)
        # bestMove = None
        # OriginalBoard = self.board.copy()
        # OriginalListOfEnPassant = self.ListOfEnpassentAblePawns.copy()
        # self.CPURunning = True

        tempGameLogic = ChessGameLogic()

        tempGameLogic.board = self.board.copy()

        GameBoard = self.board.copy()

        chosenMove = self.MinMaxStart(GameBoard, self.DEPTH, True)

    def MinMaxStart(self, board, depth, IsMaximizingPlayer):
        
        self.MinMaxAlphaBeta(board, depth, -100000, 100000, True)

    def MinMaxAlphaBeta(self, board, depth, alpha, beta, MaximizingPlayer):
        if depth == 0:
            return -self.ScoreBoard()

        bestMove = None
        OriginalBoard = board.copy()

        if MaximizingPlayer: # if the current player's score is supposed to be maximized, goes here (black's turn)
            possibleMovablePieces = self.GenerateAllValidMovesForGivenColor('b')
            bestScore = -1000000000

            for piece in possibleMovablePieces:
                for move in piece[2]:
                    result = self.movePiece(piece[1], move)

                    if result[0] == 2:
                        bestScore = max(bestScore, self.MinMaxAlphaBeta(board, depth - 1))
        

        return bestMove

    def ScoreBoard(self, board):
        PieceValues = {'K' : 900, 'Q' : 90, 'R' : 50, 'B' : 30, 'N' : 30, 'P' : 10} # scoring dictionary, given type of piece, it returns how many points the piece is worth
        score = 0 # total of the score

        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col][0] == 'w':
                    score -= PieceValues[board[row][col][1]]
                
                elif board[row][col][0] == 'b':
                    score += PieceValues[board[row][col][1]]

        return score
    
    def GenerateAllValidMovesForGivenColor(self, color, board):
        allPiecesFound = self.findAllBlackPieces(board) if color == 'b' else self.findAllWhitePieces(board)
        allPossibleMoves = []

        for piece in allPiecesFound:
            moveSet = self.GeneratePieceMoves[piece[0][1]](board, piece, piece[1], piece[2])
            
            # only adds pieces that are moveable (not blocked in someway)
            if len(moveSet) > 0:#moveSet != None or moveSet != () or len(moveSet) > 0:
                # appends the type of piece, the row and column as a tuple it is in, and the possible squares it can move to
                allPossibleMoves.append((piece, (piece[1], piece[2]), moveSet)) 
    
        return allPossibleMoves

    def findAllBlackPieces(self, board):
        listOfLocations = []

        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c][0] == 'b':
                    listOfLocations.append((board[r][c], r, c)) # appends what piece it is and where it is
            
            # if found max number of black pieces that can be on the board early, break the loop as there is not point looking for more
            if len(listOfLocations) == 16:
                break

        return listOfLocations # a list of tuples, each tuple contains 3 elements: the type of piece, its row and its column

    def findAllWhitePieces(self, board):
        listOfLocations = []

        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c][0] == 'w':
                    listOfLocations.append((board[r][c], r, c)) # appends what piece it is and where it is
            
            # if found max number of black pieces that can be on the board early, break the loop as there is not point looking for more
            if len(listOfLocations) == 16:
                break

        return listOfLocations # a list of tuples, each tuple contains 3 elements: the type of piece, its row and its column


    def setVsHuman(self, Val, depth):
        # print(f"{self.HumanVSHuman}\t{Val}")
        self.HumanVSHuman = Val
        self.DEPTH = depth
        # print(f"{self.HumanVSHuman}\t{Val}")

