from itertools import count
import random
import numpy as np

class ChessGameLogic:

    # initial variables
    CurrentTurn = 'w' # since white goes first, default value is set to 'w'
    DEPTH = 0 # the depth the MinMax tree will span
    HumanVSHuman = True # this will determine if the game is against a human or CPU
    WhiteKingPosition = (7, 4) # the default of the white king's position
    BlackKingPosition = (0, 4) # the default of the black king's position
    IsCheck = False # is there a check represented the current player's king
    ListOfEnpassentAblePawns = [] # a list of pawns that can En-Passant
    CPURunning = False # is the MinMax algorithm running
    board = None # the board array
    GeneratePieceMoves = None # the dictionary that will link all the pieces to their correct move generator method

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
        # initialise the board and the dictionary that will be used to look up piece moves
        self.board = np.array([ # '--' is used to represent empty spots since every other character identifier is also 2 character so checking for '-'[1] would cause index error since its only 1 char long string
                              ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'], # black pieces are represented with 'b' in front of the capital letter that shows what piece it is
                              ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                              ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                              ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],# white pieces are represented with 'w' in front of the capital letter that shows what piece it is
                              ]) # This array will represent the chess board with 8 rows and 8 columns, spaces are represented with '--'
        
        # the dictonary that is used to find the right move generator, given a piece type (P = pawn, R = Rook, B = Bishop ...)
        self.GeneratePieceMoves = {'P': self.GeneratePawnMoves, 'R': self.GenerateRookMoves,
                                   'N': self.GenerateKnightMoves, 'B': self.GenerateBishopMoves,
                                   'Q': self.GenerateQueenMoves, 'K': self.GenerateKingMoves}

    # this method handles the movement of a piece from one square to another
    # it takes the origin square and the destinaion square as parameters
    def movePiece(self, fromSquare, toSquare):
        # if the origin square is empty, the movement is not possible
        if self.board[fromSquare[0]][fromSquare[1]] == '--':
            # print('\nEmpty spot.')# or not right piece chosen.')
            return -1, None
        
        # if the piece selected is not the same color as the players (white's turn but a black piece is selected or reverse)
        elif self.board[fromSquare[0]][fromSquare[1]][0] != self.CurrentTurn:
            # print(f'\nNot this colors turn, it is currently {self.CurrentTurn}s turn.')
            return - 1, None

        validMoveSet = [] # the list of valid moved available to the given piece
        
        self.fromX, self.fromY = fromSquare[0], fromSquare[1] # seperates the origin square's row and col to make easier to use
        self.toX, self.toY = toSquare[0], toSquare[1] # seperates the destination square's row and col to make easier to use

        self.pieceToMove = self.board[self.fromX][self.fromY] # finds the piece that is being moved
        self.pieceToReplace = self.board[self.toX][self.toY] # finds the piece that will be replaced (empty spot or an enemy piece)

        # if the piece selected is actually a piece of the current player
        if self.board[self.fromX][self.fromY][0] == self.CurrentTurn:
            
            # only generates the valid moves for a given piece if it is the right players turn
            validMoveSet = self.generateValidMoveSet(self.pieceToMove, self.fromX, self.fromY)
            
            # performs the move if it is within the valid move sets generated for the piece
            if toSquare in validMoveSet:
                self.board[self.fromX][self.fromY] = '--'
                self.board[self.toX][self.toY] = self.pieceToMove

                # if the piece moved is one of the kings, update that king's position ----------------------
                if self.board[self.toX][self.toY] == 'wK':
                    self.WhiteKingPosition = (self.toX, self.toY)
                
                # update the black king's position if the piece moved is the black king
                elif self.board[self.toX][self.toY] == 'bK':
                    self.BlackKingPosition = (self.toX, self.toY)

                # check if the move resulted in the current players king reciving a check
                isKingInCheck = self.checkForChecksAndBlocks(self.pieceToMove)
                
                # if the above method resulted in a check on that players king, undoes the move
                if isKingInCheck[0]:
                    # print("\nThis move resulted in a check occuring. Select a different move.\n")
                    self.board[self.toX][self.toY] = self.pieceToReplace
                    self.board[self.fromX][self.fromY] = self.pieceToMove
                    
                    return -1, None
                
                else: # if the move didn't cause a check on the current player's king, it was a sucessfull move                
                    
                    # this handles the pawn promotion for the players ------------------------------
                    if (self.pieceToMove == 'wP' and self.toX == 0) or (self.pieceToMove == 'bP' and self.toX == 7 and self.HumanVSHuman):
                        
                        return 2, (self.toX, self.toY)

                    # this is the pawn promotion for the AI
                    if (self.pieceToMove == 'bp' and self.toX == 7 and self.HumanVSHuman == False):
                        # selects a random piece to upgrade to, the number of occurences is based on how powerful the piece is
                        randomPieceToUpgradeTo = random.choice('bQ', 'bQ', 'bQ', 'bQ', 'bQ', 'bR', 'bR', 'bR', 'bB', 'bB', 'bN', 'bN')

                        # upgrades the piece
                        self.upgradePawn(self.toX, self.toY, randomPieceToUpgradeTo)

                    # This handles the pawns enpassent Motion --- EN PASSANT ------------------
                    if (self.pieceToMove == 'bP'): # if the piece moved is a black pawn
                        distance = self.fromX + self.toX # check distance between the new pawns square and the old pawn square

                        if (distance == 4): # if the black piece's square moved to is 4, then it gets added to list of enpassent
                            self.ListOfEnpassentAblePawns.append((self.pieceToMove, self.toX, self.toY))
                            # print(f"\n{self.pieceToMove} has moved 2 squares.\tList of enpassentable pawns: {self.ListOfEnpassentAblePawns}")

                        # if the pawn that is moved is in the list of enpassentable pawns, then it is removed as it is not longer considered enpessatable
                        if (self.pieceToMove, self.fromX, self.fromY) in self.ListOfEnpassentAblePawns:
                            self.ListOfEnpassentAblePawns.remove((self.pieceToMove, self.fromX, self.fromY))
                            # print(f"\n{self.pieceToMove} was enpassantable, but this move clears it. Current list: {self.ListOfEnpassentAblePawns}")
                    
                        # ----------------------------------------------------------------------
                        for i in self.ListOfEnpassentAblePawns:
                            # if the spot the pawn is going to is behind this pawn which is in the list of enpassantable pawns, delete this pawn
                            if i[0] == 'wP' and self.toX == i[1] + 1 and self.toY == i[2]:
                                self.board[i[1]][i[2]] = '--'
                                self.ListOfEnpassentAblePawns.remove(i) # removes that pawn from list of enpassantable pawns
                        # ----------------------------------------------------------------------

                    elif (self.pieceToMove == 'wP'): # if the piece moved is a white pawn
                        distance = self.fromX - self.toX
                        
                        # make sure the distance traveled and from where is enough to be considered an En-Passant move
                        if (distance == 2):
                        # if the pawn has moved from row 6 to row 4, then it has moved 2 squares
                            self.ListOfEnpassentAblePawns.append((self.pieceToMove, self.toX, self.toY))
                            # print(f"\n{self.pieceToMove} has moved 2 squares.\tList of enpassentable pawns: {self.ListOfEnpassentAblePawns}")

                        # if the pawn that is moved is in the list of enpassentable pawns, then it is removed as it is not longer considered enpessatable
                        if (self.pieceToMove, self.fromX, self.fromY) in self.ListOfEnpassentAblePawns:
                            self.ListOfEnpassentAblePawns.remove((self.pieceToMove, self.fromX, self.fromY))
                            # print(f"\n{self.pieceToMove} was enpassantable, but this move clears it. Current list: {self.ListOfEnpassentAblePawns}")
                    
                        # if the piece to the left of this pawn is the same pawn
                        for i in self.ListOfEnpassentAblePawns:
                            # if the spot the pawn is going to is behind this pawn which is in the list of enpassantable pawns, delete this pawn
                            if i[0] == 'bP' and self.toX == i[1] - 1 and self.toY == i[2]:
                                self.board[i[1]][i[2]] = '--'
                                self.ListOfEnpassentAblePawns.remove(i) # removes that pawn from list of enpassantable pawns

                    # ------------------- EN PASSANT LIST UPDATER ---------------------------------

                    
                    if not self.CPURunning:
                        # swaps to the other user, CPU or human
                        self.swapPlayers()

            else: # if the move failed, resets the list of valid moves and returns
                # print(f'\nInvalid move, {self.CurrentTurn} moves again.\n')
                validMoveSet = []
                
                return -1, None
    
        return 1, None
    
    # this method checks for checks on the current player's king
    def checkForChecksAndBlocks(self, piece):
        checks = [] # a list of checks and a tuple of where a piece that is blocking a check is located
        self.IsCheck = False

        kingX, kingY, ThisKingName = (self.WhiteKingPosition[0], self.WhiteKingPosition[1], 'wK') if piece[0] == 'w' else (self.BlackKingPosition[0], self.BlackKingPosition[1], 'bK')
        
        # if piece[0] == 'w':
        #     kingX, kingY = self.WhiteKingPosition[0], self.WhiteKingPosition[1]
        #     enemyKingName = 'wK'
        
        # elif piece[0] == 'b':
        #     kingX, kingY = self.BlackKingPosition[0], self.BlackKingPosition[1]
        #     enemyKingName = 'bK'
        
        # the 8 directions that the king can recieve a check from
        KingDirections = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        # itterate each of the 8 directions
        for j in range(len(KingDirections)):
            d = KingDirections[j]

            possibleBlocker = ()

            # goes out 8 blocks away from the king in the current direction
            for i in range(1, 8):
                endRow = kingX + d[0] * i
                endCol = kingY + d[1] * i

                # if the square is not out of bounds
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]

                    # if the spot is empty, it doesn't bother checking for anything in the spot
                    if endPiece != '--':
                        # if the end piece is an ally piece
                        if endPiece[0] == ThisKingName[0]: # ending piece is not the same color as the enemy king (use the opposing king to check that)
                            if possibleBlocker == ():
                                # stores the location of the piece that maybe able to be used as a defensive pin and its direction
                                possibleBlocker = ((endRow, endCol, d[0], d[1]))
                        
                            else: # if there is a friendly piece in one of the directions, break
                                break

                        elif endPiece[0] != ThisKingName[0]: # the ending piece is an enemy piece
                            typeOfPiece = endPiece[1] # gets the type of piece it is

                            # 'j' represents the direction and 'i' represents the distance the piece is from the king, the lower 'i' is the closer it is to the king
                            # if the piece presenting check is a Rook and is more than '1' square away (used to make sure king can't fight back if it is close enough)
                            if (0 <= j <= 3 and typeOfPiece == 'R' and i > 1):

                                if possibleBlocker == (): # if this is empty, there there is a check presented to the king
                                    self.IsCheck = True

                                    # print(f"Check Presented from square {endRow + 1}, {endCol + 1}, from direction: {d}")

                                    checks.append((endRow, endCol, d[0], d[1]))
                                    break
                            
                            # if the piece presenting check is a Bishop and is more than '1' square away
                            elif (4 <= j <= 7 and typeOfPiece == 'B' and i > 1):
                                if possibleBlocker == (): # if this is empty, there there is a check presented to the king
                                    self.IsCheck = True

                                    # print(f"Check Presented from square {endRow + 1}, {endCol + 1}, from direction: {d}")

                                    checks.append((endRow, endCol, d[0], d[1]))
                                    break
                            
                            # if the piece presenting check is a Pawn and is in the right bracket to present a check to the king
                            elif (i == 1 and typeOfPiece == 'P' and ((endPiece[0] == 'w' and 6 <= j <= 7) or (endPiece[0] == 'b' and 4 <= j <= 5))):
                                if possibleBlocker == (): # if this is empty, there there is a check presented to the king
                                    self.IsCheck = True

                                    # print(f"Check Presented from square {endRow + 1}, {endCol + 1}, from direction: {d}")

                                    checks.append((endRow, endCol, d[0], d[1]))
                                    break
                            
                            # if the piece presenting check is a Queen and is more than '1' square away or is the King and is only '1' square away
                            elif (typeOfPiece == 'Q' and i > 1) or (i == 1 and typeOfPiece == 'K'):
                                if possibleBlocker == (): # if this is empty, there there is a check presented to the king
                                    self.IsCheck = True

                                    # print(f"Check Presented from square {endRow + 1}, {endCol + 1}, from direction: {d}")

                                    checks.append((endRow, endCol, d[0], d[1]))
                                    break

                            else:
                                break
                
                else:
                    break
        
        # all the possible locations a knight could be from the king
        PossibleKnightLocations = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

        for move in PossibleKnightLocations:
            endRow = kingX + move[0] # moves to the relative square row away from the king a horse would be
            endCol = kingY + move[1] # moves to the relative square column away from the king a horse would be

            # if the square is on the board
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol] # check what type of piece is on the square

                # if the spot is not empty, check for what kind of piece it is
                if endPiece != '--':
                    # if the knight piece there is not the same color, then it presents a check
                    if endPiece[0] != ThisKingName[0] and endPiece[1] == 'N':
                        self.IsCheck = True
                        
                        # print(f"Check Presented from square {endRow + 1}, {endCol + 1}, from direction: {move}")
                        
                        checks.append((endRow, endCol, move[0], move[1])) # appends the spot as a square a check being presented from by a horse

        return self.IsCheck, checks # returns a flag if king is in check or not and a list of where the check(s) are from

    # generates the valid moveset taking into account if there is a check on the king
    def generateValidMoveSet(self, piece, row, col):
        validMoves = []

        self.IsCheck, self.checks = self.checkForChecksAndBlocks(piece) # sends the currently moving piece to check if there is a check presented on the current player's king
        
        # stores the location of the current player's king
        kingX, kingY = (self.WhiteKingPosition[0], self.WhiteKingPosition[1]) if piece[0] == 'w' else (self.BlackKingPosition[0], self.BlackKingPosition[1])

        # if piece[0] == 'w':
        #     kingX, kingY = self.WhiteKingPosition[0], self.WhiteKingPosition[1]
            
        # elif piece[0] == 'b':
        #     kingX, kingY = self.BlackKingPosition[0], self.BlackKingPosition[1]
            
        if self.IsCheck: # if there is a check being presented, generate moves based on where and from what
            if len(self.checks) == 1: # if there is only 1 piece checking the king
                availMoves = self.GeneratePieceMoves[piece[1]](piece, row, col) # send 2nd letter of the piece being moved to generate it's possible moves, irrelevent if the king is in check

                check = self.checks[0] 
                checkRow = check[0] # the row of the piece
                checkCol = check[1] # the column of the piece

                pieceChecking = self.board[checkRow][checkCol] # what piece is presenting the check

                validSquares = []

                if pieceChecking[1] == 'N': # if the piece presenting check is a knight, one of the only possible moves is to kill the knight
                    validSquares = [(checkRow, checkCol)]
                
                else: # if it is not a knight, check around the king for any open square to move to
                    for i in range(1, 8):
                        validSquare = (kingX + check[2] * i, kingY + check[3] * i)
                        validSquares.append(validSquare)

                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                
                for i in range(len(availMoves) - 1, - 1, -1):
                    # if the first input parameter (the piece) is not the king
                    pieceBeingMoved = self.board[self.fromX][self.fromY]

                    if pieceBeingMoved[1] != 'K': # if the king is the one not being moved
                        if not ((self.toX, self.toY) in validSquares): # if the move is not in the list of possible(available) moves, remove it
                            availMoves.remove(availMoves[i])
                
                validMoves = availMoves.copy()
                
            else: # if there is multiple checks, move the king
                validMoves = self.GenerateKingMoves(piece, row, col)

        else: # if there is not checks, just generate the possible moves for the given piece
            validMoves = self.GeneratePieceMoves[piece[1]](piece, row, col)

        return validMoves # return the list of possible moves
    
    # this method generates the -------------- PAWN'S ----------- move set
    def GeneratePawnMoves(self, piece, row, col):
        validMoves = []

        if piece[0] == 'w':
            if row - 1 >= 0:
                # if the spot in front if the given pawn is empty, it is added to the list of possible moves
                if self.board[row - 1][col] == '--': # 1 square only move check, only check if the spot infront of the pawn is empty
                    validMoves.append((row - 1, col))

                    # if the 2nd spot in front of the given pawn is empty, it is also added to the list of possible moves
                    if row == 6 and self.board[row - 2][col] == '--':
                        validMoves.append((row - 2, col))
                
                # if moving to the left column (diagonal to attack) would put it below 0, which would put it off the board
                if (col - 1) >= 0:
                    if self.board[row - 1][col - 1][0] == 'b':
                        validMoves.append((row - 1, col - 1))
                
                # if moving to the right column (diagonal to attack) would put it below 0, which would put it off the board
                if (col + 1) <= 7:
                    if self.board[row - 1][col + 1][0] == 'b': 
                        validMoves.append((row - 1, col + 1))

            # check if there are any enemy pawns to the left or right
            # if there are any black pawns to the left
            if (0 <= col - 1 <= 7):
                pieceToLeft = self.board[row][col - 1]

                # if the piece to the left of this pawn is a black pawn and it is in the list of enpassantable pawns
                if pieceToLeft == 'bP' and ((pieceToLeft, row, col - 1) in self.ListOfEnpassentAblePawns):
                    # print(f'Pawn to the left was enpassantable.')
                    validMoves.append((row - 1, col - 1))
            
            # if there are any squares to is right
            if (0 <= col + 1 <= 7):
                pieceToLeft = self.board[row][col + 1]

                # if the piece to the left of this pawn is a black pawn and it is in the list of enpassantable pawns
                if pieceToLeft == 'bP' and ((pieceToLeft, row, col + 1) in self.ListOfEnpassentAblePawns):
                    # print(f'Pawn to the right was enpassantable.')
                    validMoves.append((row - 1, col + 1))

        
        # if the piece is a black piece, this moveset is used
        elif piece[0] == 'b':
            # make sure the movement is on the board
            if row + 1 < 8:
                # if the spot in front if the given pawn is empty, it is added to the list of possible moves
                if self.board[row + 1][col] == '--':
                    validMoves.append((row + 1, col))

                    # if the 2nd spot in front of the given pawn is empty, it is also added to the list of possible moves
                    if row == 1 and self.board[row + 2][col] == '--':
                        validMoves.append((row + 2, col))
                
                # if moving to the left column (diagonal to attack) would put it below 0, which would put it off the board
                if (col - 1) >= 0:
                    if self.board[row + 1][col - 1][0] == 'w':
                        validMoves.append((row + 1, col - 1))
                
                # if moving to the right column (diagonal to attack) would put it below 0, which would put it off the board
                if (col + 1) <= 7:
                    if self.board[row + 1][col + 1][0] == 'w':
                        validMoves.append((row + 1, col + 1))


            # -----------------------------------------------------------------------------------------
            # check if there are any enemy pawns to the left or right
            # if there are any black pawns to the left
            if (0 <= col - 1 <= 7):
                pieceToLeft = self.board[row][col - 1]

                # if the piece to the left of this pawn is a black pawn and it is in the list of enpassantable pawns
                if pieceToLeft == 'wP' and ((pieceToLeft, row, col - 1) in self.ListOfEnpassentAblePawns):
                    # print(f'Pawn to the left was enpassantable.')
                    validMoves.append((row + 1, col - 1))
            
            # if there are any squares to is right
            if (0 <= col + 1 <= 7):
                pieceToLeft = self.board[row][col + 1]

                # if the piece to the left of this pawn is a black pawn and it is in the list of enpassantable pawns
                if pieceToLeft == 'wP' and ((pieceToLeft, row, col + 1) in self.ListOfEnpassentAblePawns):
                    # print(f'Pawn to the right was enpassantable.')
                    validMoves.append((row + 1, col + 1))
            # -----------------------------------------------------------------------------------------
        
        return validMoves

    # this method upgrades the pawn in this row and column to the new piece given
    def upgradePawn(self, row, col, newPiece):
        
        self.board[row][col] = newPiece

    # this method generates the -------------- ROOK ----------- move set
    def GenerateRookMoves(self, piece, row, col):
        validMoves = []

        # -------------------------------- WHITE ROOKS -----------------------------------------
        if piece[0] == 'w':
            # ------------------ FORWARD/UP -------------------------------
            # Start at where the current piece is (row), stop at the length of the board's row - the row is is on, move by -1 to go up
            # stops at the 0th row
            for r in range(row, 0, - 1):
                if self.board[r - 1][col][0] == 'b': # if there is an enemy piece, append that square to movable squares and stop searching
                    validMoves.append((r - 1, col))
                    break
                
                elif self.board[r - 1][col] == '--': # if the square is empty, append it as a moveable square
                    validMoves.append((r - 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break
            
            # ----------------- BACKWARDS/DOWN ---------------------------
            for r in range(row, len(self.board[row]) - 1, + 1):
                # if there is an enemy piece, append that square to movable squares and stop searching
                if self.board[r + 1][col][0] == 'b':
                    validMoves.append((r + 1, col))
                    break
                
                # if the square is empty, append it as a moveable square
                elif self.board[r + 1][col] == '--':
                    validMoves.append((r + 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break

            # ------------------- RIGHT -----------------------------------
            # this loop checks all possible spots going right
            # start at the given column, stop at the edge of the column in this row - 1 for indexing, increase by + 1 (goes right)
            for rCr in range(col, len(self.board[row]) - 1, + 1):
                # checks in the columns of the current row if there are any open spots sideways or if there are any pieces it can kill
                if self.board[row][rCr + 1][0] == 'b':
                    validMoves.append((row, rCr + 1))
                    break
                
                elif self.board[row][rCr + 1] == '--': # if the square is empty, append it as a moveable square
                    validMoves.append((row, rCr + 1))
                
                # if there are no more open spots, break
                else:
                    break
            
            # ------------------- LEFT -------------------------------------
            # start at the given column, stop at the 0th column (index 0), decrease by - 1 (goes left)
            for rCl in range(col, 0, - 1):
                if self.board[row][rCl - 1][0] == 'b': # if there is an enemy piece, append that square to movable squares and stop searching
                    validMoves.append((row, rCl - 1))
                    break
                
                elif self.board[row][rCl - 1] == '--': # if the square is empty, append it as a moveable square
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

                if self.board[r - 1][col][0] == 'w': # if there is an enemy piece, append that square to movable squares and stop searching
                    validMoves.append((r - 1, col))
                    break
                
                elif self.board[r - 1][col] == '--': # if the square is empty, append it as a moveable square
                    validMoves.append((r - 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break
            
            # ----------------- BACKWARDS/DOWN ---------------------------
            for r in range(row, len(self.board) - 1, + 1):
                if self.board[r + 1][col][0] == 'w': # if there is an enemy piece, append that square to movable squares and stop searching
                    validMoves.append((r + 1, col))
                    break
                
                elif self.board[r + 1][col] == '--': # if the square is empty, append it as a moveable square
                    validMoves.append((r + 1, col))

                else: # its reached a piece that it can't go past (friendly)
                    break

            # ------------------- RIGHT -----------------------------------
            # this loop checks all possible spots going right
            # start at the given column, stop at the edge of the column in this row - 1 for indexing, increase by + 1 (goes right)
            for rCr in range(col, len(self.board[row]) - 1, + 1):
                # checks in the columns of the current row if there are any open spots sideways or if there are any pieces it can kill
                if self.board[row][rCr + 1][0] == 'w': # if there is an enemy piece, append that square to movable squares and stop searching
                    validMoves.append((row, rCr + 1))
                    break
                
                elif self.board[row][rCr + 1] == '--': # if the square is empty, append it as a moveable square
                    validMoves.append((row, rCr + 1))
                
                # if there are no more open spots, break
                else:
                    break
            
            # ------------------- LEFT -------------------------------------
            # start at the given column, stop at the 0th column (index 0), decrease by - 1 (goes left)
            for rCl in range(col, 0, - 1):
                if self.board[row][rCl - 1][0] == 'w': # if there is an enemy piece, append that square to movable squares and stop searching
                    validMoves.append((row, rCl - 1))
                    break
                
                elif self.board[row][rCl - 1] == '--': # if the square is empty, append it as a moveable square
                    validMoves.append((row, rCl - 1))

                # if there are no more open spots, break
                else:
                    break

        return validMoves # returns the list of valid moves
    
    def GenerateKnightMoves(self, piece, row, col):
        validMoves = []
        alliedPiece = 'w' if piece[0] == 'w' else 'b'

        # -------------------- FORWARD/UP ----------------------
        # generates all the valid moves for the knight going up
        # row - 2 since we're going up and it is greater than or equal to 0 (row = 7 - 2 (going up) = 5, row = 2 - 2 (going up) = 0, row = 1 - 2 = - 1 !>= 0)
        if row - 2 >= 0:
            # check if square is not off the board
            if col - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
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
            # check if square is not off the board
            if col - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
                if self.board[row + 2][col - 1][0] != alliedPiece:
                    validMoves.append((row + 2, col - 1))
            
            # check if square is not off the board
            if col + 1 <= 7:
                # if this spot on the board is not an allied piece, move there
                if self.board[row + 2][col + 1][0] != alliedPiece:
                    validMoves.append((row + 2, col + 1))

        # -------------------- LEFT ----------------------
        # generates all the valid moves for the knight going left
        if col - 2 >= 0:
            # check if square is not off the board
            if row - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
                if self.board[row - 1][col - 2][0] != alliedPiece:
                    validMoves.append((row - 1, col - 2))
            
            # check if square is not off the board
            if row + 1 <= 7:
                # if this spot on the board is not an allied piece, move there
                if self.board[row + 1][col - 2][0] != alliedPiece:
                    validMoves.append((row + 1, col - 2))
        
        # -------------------- RIGHT ----------------------
        # generates all the valid moves for the knight going right
        if col + 2 <= 7:
            # check if square is not off the board
            if row - 1 >= 0:
                # if this spot on the board is not an allied piece, move there
                if self.board[row - 1][col + 2][0] != alliedPiece:
                    validMoves.append((row - 1, col + 2))
            
            # check if square is not off the board
            if row + 1 <= 7:
                # if this spot on the board is not an allied piece, move there
                if self.board[row + 1][col + 2][0] != alliedPiece:
                    validMoves.append((row + 1, col + 2))
        
        return validMoves

    def GenerateBishopMoves(self, piece, row, col):
        validMoves = []
        enemyPiece = 'b' if piece[0] == 'w' else 'w'

        # ------------------- DIAGONALY DOWN RIGHT --------------------------
        # performs the check going diagonaly down right
        for r, c in zip(range(row, len(self.board[row]) - 1, 1), range(col, len(self.board[row]) - 1, 1)):
            # if the square contains an enemy piece
            if self.board[r + 1][c + 1][0] == enemyPiece:
                validMoves.append((r + 1, c + 1))
                break
            
            # if spot diagonaly right below is empty, appends it to the list of valid moves
            elif self.board[r + 1][c + 1] == '--':
                validMoves.append((r + 1, c + 1))
                
            # if there are no more spots remaining, break
            else:
                break
        
        # ------------------- DIAGONALY DOWN LEFT --------------------------
        # performs the check going diagonaly down left
        # zip() method stopped working correctly so I had to use this while loop from here
        r, c = row, col
        while True:
            # check if the next movement is out of bounds or not
            if r + 1 <= 7 and c - 1 >= 0:
                # if the square contains an enemy piece
                if self.board[r + 1][c - 1][0] == enemyPiece:
                    validMoves.append((r + 1, c - 1))
                    r += 1
                    c -= 1
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r + 1][c - 1] == '--':
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
                # if the square contains an enemy piece
                if self.board[r - 1][c + 1][0] == enemyPiece:
                    validMoves.append((r - 1, c + 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r - 1][c + 1] == '--':
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
                if self.board[r - 1][c - 1][0] == enemyPiece: # if the square contains an enemy piece
                    validMoves.append((r - 1, c - 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r - 1][c - 1] == '--':
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
        enemyPiece = 'b' if piece[0] == 'w' else 'w'

        # ------------------ FORWARD/UP -------------------------------
        # Start at where the current piece is (row), stop at the length of the board's row - the row is is on, move by -1 to go up
        # stops at the 0th row
        for r in range(row, 0, - 1):
            if self.board[r - 1][col][0] == enemyPiece: # if the square contains an enemy piece
                validMoves.append((r - 1, col))
                break
            
            elif self.board[r - 1][col] == '--': # if the square contains an empty spot
                validMoves.append((r - 1, col))

            else: # its reached a piece that it can't go past (friendly)
                break
        
        # ----------------- BACKWARDS/DOWN ---------------------------
        for r in range(row, len(self.board[row]) - 1, + 1): 
            if self.board[r + 1][col][0] == enemyPiece: # if the square contains an enemy piece
                validMoves.append((r + 1, col))
                break
            
            elif self.board[r + 1][col] == '--': # if the square contains an empty spot
                validMoves.append((r + 1, col))

            else: # its reached a piece that it can't go past (friendly)
                break

        # ------------------- RIGHT -----------------------------------
        # this loop checks all possible spots going right
        # start at the given column, stop at the edge of the column in this row - 1 for indexing, increase by + 1 (goes right)
        for rCr in range(col, len(self.board[row]) - 1, + 1):
            # checks in the columns of the current row if there are any open spots sideways or if there are any pieces it can kill
            if self.board[row][rCr + 1][0] == enemyPiece:
                validMoves.append((row, rCr + 1))
                break
            
            elif self.board[row][rCr + 1] == '--':
                validMoves.append((row, rCr + 1))
            
            # if there are no more open spots, break
            else:
                break
        
        # ------------------- LEFT -------------------------------------
        # start at the given column, stop at the 0th column (index 0), decrease by - 1 (goes left)
        for rCl in range(col, 0, - 1):
            if self.board[row][rCl - 1][0] == enemyPiece: # if the square contains an enemy piece
                validMoves.append((row, rCl - 1))
                break
            
            elif self.board[row][rCl - 1] == '--': # if the square contains an empty spots
                validMoves.append((row, rCl - 1))

            # if there are no more open spots, break
            else:
                break
        
        # ------------------- DIAGONALY DOWN RIGHT --------------------------
        # performs the check going diagonaly down right
        for r, c in zip(range(row, len(self.board[row]) - 1, 1), range(col, len(self.board[row]) - 1, 1)):
            if self.board[r + 1][c + 1][0] == enemyPiece: # if the square contains an enemy piece
                validMoves.append((r + 1, c + 1))
                break
            
            # if spot diagonaly right below is empty, appends it to the list of valid moves
            elif self.board[r + 1][c + 1] == '--':
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
                if self.board[r + 1][c - 1][0] == enemyPiece: # if the square contains an enemy piece
                    validMoves.append((r + 1, c - 1))
                    r += 1
                    c -= 1
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r + 1][c - 1] == '--':
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
                if self.board[r - 1][c + 1][0] == enemyPiece: # if the square contains an enemy piece
                    validMoves.append((r - 1, c + 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r - 1][c + 1] == '--':
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
                if self.board[r - 1][c - 1][0] == enemyPiece: # if the square contains an enemy piece
                    validMoves.append((r - 1, c - 1))
                    break
                
                # if spot diagonaly right below is empty, appends it to the list of valid moves
                elif self.board[r - 1][c - 1] == '--':
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
        enemyPiece = 'b' if piece[0] == 'w' else 'w'
        
        # --------------------- MOVE UP ------------------------
        if row - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[row - 1][col][0] == enemyPiece or self.board[row - 1][col] == '--':
                validMoves.append((row - 1, col))
        
        # --------------------- MOVE DOWN ------------------------
        if row + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[row + 1][col][0] == enemyPiece or self.board[row + 1][col] == '--':
                validMoves.append((row + 1, col))
        
        # --------------------- MOVE LEFT ------------------------
        if col - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[row][col - 1][0] == enemyPiece or self.board[row][col - 1] == '--':
                validMoves.append((row, col - 1))

        # --------------------- MOVE RIGHT ------------------------
        if col + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[row][col + 1][0] == enemyPiece or self.board[row][col + 1] == '--':
                validMoves.append((row, col + 1))

        # --------------------- MOVE DIAGONAL UP RIGHT ------------------------
        if row - 1 >= 0 and col + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[row - 1][col + 1][0] == enemyPiece or self.board[row - 1][col + 1] == '--':
                validMoves.append((row - 1, col + 1))

        # --------------------- MOVE DIAGONAL UP LEFT ------------------------
        if row - 1 >= 0 and col - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[row - 1][col - 1][0] == enemyPiece or self.board[row - 1][col - 1] == '--':
                validMoves.append((row - 1, col - 1))

        # --------------------- MOVE DIAGONAL DOWN RIGHT ------------------------
        if row + 1 <= 7 and col + 1 <= 7:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[row + 1][col + 1][0] == enemyPiece or self.board[row + 1][col + 1] == '--':
                validMoves.append((row + 1, col + 1))

        # --------------------- MOVE DIAGONAL DOWN LEFT ------------------------
        if row + 1 <= 7 and col - 1 >= 0:
            # if the spot is empty, or there is an enemy piece there, add the spot as a possible move
            if self.board[row + 1][col - 1][0] == enemyPiece or self.board[row + 1][col - 1] == '--':
                validMoves.append((row + 1, col - 1))
        
        return validMoves

    # this method swaps the players and also starts the MinMax algorithm if VS CPU is selected
    def swapPlayers(self):
        if self.CurrentTurn == 'w':
            self.CurrentTurn = 'b'

            if not self.HumanVSHuman: # if VS CPU is selected, runs the MinMax algorithm with Alpha-Beta Prunning to select a move for black
                self.CPUTurn()
        
        elif self.CurrentTurn == 'b':
            self.CurrentTurn = 'w'

    def CPUTurn(self):
        # used to UNDO any move made by just copy and pasting the board 
        GameBoard = self.board.copy() # copies the current version of the board
        OriginalListOfEnPassant = self.ListOfEnpassentAblePawns.copy() # copies the current list of enpassent pawns

        self.CPURunning = True # sets a flag that is used to prevent player switching while MinMax is running

        chosenMove = self.MinMaxStart(self.board, self.ListOfEnpassentAblePawns, self.DEPTH, True) # runs the MinMax algorithm to get the best move

        # undo the move done
        self.board = GameBoard.copy()
        self.ListOfEnpassentAblePawns = OriginalListOfEnPassant.copy()

        print(f'ChosenMove: From: {chosenMove[0]} - To: {chosenMove[1]}')
        
        self.CurrentTurn = 'b' # sets the current turn to be black
        self.CPURunning = False # turns off the flag that prevents the player to swap

        self.movePiece(chosenMove[0], chosenMove[1]) # performs the move chosen

    def MinMaxStart(self, board, EnPassList, depth, IsMaximizingPlayer):
        possibleMovablePieces = self.GenerateAllValidMovesForGivenColor('b' if IsMaximizingPlayer else 'w') # gets the list of all possible moves for given color
        random.shuffle(possibleMovablePieces) # shuffles them in random order
        bestMove = -9999 # inits the lowest score to compare future scores to
        bestMoveFinal = None
        OriginalBoard = board.copy() # copy of the current board state is stored which will be used to 'undo' all the moves the MinMax will do
        OriginalListOfEnPassant = EnPassList.copy() # copy of the En-Passant list that serves the same purpose as above

        # runs the min max for every possible move for black (CPU)
        for piece in possibleMovablePieces:
            for move in piece[2]:
                self.CurrentTurn = 'b' # sets the current player turn to be black to allow movement or pieces

                self.movePiece(piece[1], move) # moves the piece

                # calculates the value for all possible player's moves
                value = max(bestMove, self.MinMaxAlphaBeta(self.board, self.ListOfEnpassentAblePawns, depth - 1, -10000, 10000, not IsMaximizingPlayer))

                self.board = OriginalBoard.copy() # undo the move
                self.ListOfEnpassentAblePawns = OriginalListOfEnPassant.copy()

                # if value is greater than bestMove, stores this move as the best possible move
                if value > bestMove:
                    print("Best score: " ,str(bestMove))
                    print("Best move: ", str(bestMoveFinal))
                    bestMove = value # updates the current best score
                    bestMoveFinal = (piece[1], move) # stores the best possible move
        
        return bestMoveFinal # returns the best move that was chosen

    # the MinMax Algorithm with Alpha-Beta prunning
    # it takes the board state, the En-Passant list, then depth, alpha, beta and the player to Maximize the score for as parameters
    def MinMaxAlphaBeta(self, board, EnPassList, depth, alpha, beta, MaximizingPlayer):
        # if the lowest depth is reached, returns the current score of the board based on which pieces are sill on it
        if depth == 0 or self.isCheckMate('w' if MaximizingPlayer else 'b'): # or if there is a terminal node(checkmate)
            return self.ScoreBoard() # should return less than -900(maybe positive if I have my numbers backwards) points since the king is worth a lot and there is a check mate in place

        bestMove = None
        # stores the current state of the board and the En-Passant list which will be used to undo moves made
        OriginalBoard = board.copy()
        OriginalListOfEnPassant = EnPassList.copy()

        if MaximizingPlayer: # if the current player's score is supposed to be maximized, goes here (black's turn)
            self.CurrentTurn = 'b' # sets it as blacks turn
            possibleMovablePieces = self.GenerateAllValidMovesForGivenColor('b') # generates all possible moves for all it's pieces
            bestMove = -1000000000 # best move to compare against (maximize this)
            
            # moves each piece for all its possible moves
            for piece in possibleMovablePieces:
                for move in piece[2]:
                    self.movePiece(piece[1], move) # performs the move

                    # recursively calls it's self and
                    bestMove = max(bestMove, self.MinMaxAlphaBeta(self.board, self.ListOfEnpassentAblePawns, depth - 1, alpha, beta, not MaximizingPlayer))

                    self.board = OriginalBoard.copy() # undo the move
                    self.ListOfEnpassentAblePawns = OriginalListOfEnPassant.copy()

                    alpha = max(alpha, bestMove) # takes the best between alpha and the best move made, if alpha is worse than beta, don't go further down this tree

                    if beta <= alpha: # compares alpha to beta, if less than beta, return (no point in going down this tree)
                        return bestMove
                
            return bestMove
        
        else:
            self.CurrentTurn = 'w' # sets it as white's turn to allow piece movement
            possibleMovablePieces = self.GenerateAllValidMovesForGivenColor('w') # gets all possible moves
            bestMove = 1000000000 # (minimize this) score to compare against

            for piece in possibleMovablePieces: # goes to every piece that is moveable
                for move in piece[2]:
                    self.movePiece(piece[1], move) # performs every move this piece is capable

                    # takes the minimum between self's best score and what this move's future move will cause
                    bestMove = min(bestMove, self.MinMaxAlphaBeta(self.board, self.ListOfEnpassentAblePawns, depth - 1, alpha, beta, not MaximizingPlayer))

                    self.board = OriginalBoard.copy() # undo the move
                    self.ListOfEnpassentAblePawns = OriginalListOfEnPassant.copy()

                    beta = min(beta, bestMove) # takes the minimum between beta(move that cause this move) and the move done here
                    
                    if(beta <= alpha): # if beta is less than current alpha, set this as a 'good' move
                        return bestMove
            
            return bestMove

    def isCheckMate(self, currentPlayer):
        # checks all around the king for open spots, makes the move, then if there is still a check on the king for all open moves, then it is considered check mate
        KingX, kingY, = (self.WhiteKingPosition[0], self.WhiteKingPosition[1]) if currentPlayer[0] == 'w' else (self.BlackKingPosition[0], self.BlackKingPosition[1])
        counter = 0
        OriginalBoard = self.board.copy()

        KingMoves = self.GenerateKingMoves(currentPlayer, KingX, kingY)

        # compare number of available moves to how many cause no check, if there is atleast 1 spot that doesn't cause check, then game is not over
        for move in KingMoves:
            self.movePiece((KingX, kingY), move)
            
            if not self.IsCheck: # if there is one spot that hasn't cause a check then the game is not over (not checkmate)
                counter += 1
            
            # undo the move
            self.board = OriginalBoard.copy()
        
        if counter >= 1: # if one spot doesn't cause check, return false to indicate game is not over
            return False
        
        elif counter == 0 and self.IsCheck: # if there are no open spots and king is in check, then there is a checkmate
            return True


    # this method returns a score based on how many pieces of a given color there are on the board
    def ScoreBoard(self):
        PieceValues = {'K' : 900, 'Q' : 90, 'R' : 50, 'B' : 30, 'N' : 30, 'P' : 10} # scoring dictionary, given type of piece, it returns how many points the piece is worth
        score = 0 # total of the score

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col][0] == 'w': # if there is white piece here, decrease the score by how much that piece is worth (keep this as high as possible (or maybe it was lower and I have my numbers backwards))
                    score -= PieceValues[self.board[row][col][1]]
                
                elif self.board[row][col][0] == 'b': # if there is black piece here, increase the score by how much that piece is worth (keep this as low as possible)
                    score += PieceValues[self.board[row][col][1]]

        return score # returns the score
    
    # for a given color as a parameter, finds all the pieces and generates all possible moves for the piece and returns them
    def GenerateAllValidMovesForGivenColor(self, color):
        allPiecesFound = self.findAllBlackPieces() if color == 'b' else self.findAllWhitePieces()
        allPossibleMoves = []

        for piece in allPiecesFound:
            moveSet = self.GeneratePieceMoves[piece[0][1]](piece[0], piece[1], piece[2])
            
            # only adds pieces that are moveable (not blocked in someway)
            if len(moveSet) > 0:#moveSet != None or moveSet != () or len(moveSet) > 0:
                # appends the type of piece, the row and column as a tuple it is in, and the possible squares it can move to
                allPossibleMoves.append((piece, (piece[1], piece[2]), moveSet)) 
    
        return allPossibleMoves

    # finds all black pieces
    def findAllBlackPieces(self):
        listOfLocations = []

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c][0] == 'b':
                    listOfLocations.append((self.board[r][c], r, c)) # appends what piece it is and where it is
            
            # if found max number of black pieces that can be on the board early, break the loop as there is not point looking for more
            if len(listOfLocations) == 16:
                break

        return listOfLocations # a list of tuples, each tuple contains 3 elements: the type of piece, its row and its column

    # finds all white pieces on the board
    def findAllWhitePieces(self):
        listOfLocations = []

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c][0] == 'w':
                    listOfLocations.append((self.board[r][c], r, c)) # appends what piece it is and where it is
            
            # if found max number of black pieces that can be on the board early, break the loop as there is not point looking for more
            if len(listOfLocations) == 16:
                break

        return listOfLocations # a list of tuples, each tuple contains 3 elements: the type of piece, its row and its column

    # if VS CPU is selected, sets the flag and the correct depth
    def setVsHuman(self, Val, depth):
        # print(f"{self.HumanVSHuman}\t{Val}")
        self.HumanVSHuman = Val
        self.DEPTH = depth
        # print(f"{self.HumanVSHuman}\t{Val}")

