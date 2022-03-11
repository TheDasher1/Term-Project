import pygame as py
import glob
import ChessGameLogic as CGL

# Please modify the file path as needed
PATH = "Term Project\\images\\*.png" # change the file path as needed
WIDTH, HEIGHT = 600, 600
NumOfSquares = 8 # the number of rows and columns in a chess board
DimensionsOfSquares = HEIGHT / NumOfSquares # 600 / 8 = 75 pixels by 75 pixels of height and width for the square blocks and the chess pieces size
ChessPieces = {} # the dictionary that will hold the chess pieces, given a piece identifiers (bK, bP, wR, wB, etc..) it will return the accociated image of that piece
COLORS = [py.Color(243,217,180,255), py.Color(185,139,97,255)] # the 2 colors that will be used to represent the players

def main():
    fileNames = glob.glob(PATH) # the file path that will use checked to load the game pieces

    for p in fileNames:
        pieceNameTemp = p.split('Term Project\\images\\') # seperates the image names to be used in the board
        pieceNameTemp = pieceNameTemp[1].split('.png')
        
        # adjust the image size to fit the board
        ChessPieces[pieceNameTemp[0]] = py.transform.scale(py.image.load(p), (DimensionsOfSquares, DimensionsOfSquares))

    VSHuman = False
    depth = 0

    # gets the information for who the game is against, if AI is selected, also asks for the depth
    while True:
        try:
            VSHuman = int(input('Enter 1 to play against human or 0 to play against AI: '))

            if VSHuman == 0 or VSHuman == 1:
                VSHuman = bool(VSHuman)
                
                if VSHuman == 0:
                    while True:
                            try:
                                depth = int(input('Enter the depth: '))

                                if depth > 0:
                                    break
                            
                            except ValueError as err:
                                print(f'Invalid input. {err}')

                break
        
        except ValueError as err:
            print(f'Invalid input. {err}')

    py.init() # initialises the game window

    window = py.display.set_mode((WIDTH, HEIGHT))
    window.fill(py.Color('white'))

    gameLogic = CGL.ChessGameLogic() # the Chess Game logic class

    running = True

    FromSquare = (0, 0) # the location that the player will click on to select pieces
    playerClicks = [] # keep track of where the player has clicked on
    
    gameLogic.setVsHuman(VSHuman, depth) # sets up who the game will be against

    while running:
        for event in py.event.get():
            if event.type == py.QUIT: # quits the game
                running = False

            if event.type == py.MOUSEBUTTONDOWN: # gets the location of where the player clicks on the window
                location = py.mouse.get_pos()
                y = int(location[0] // DimensionsOfSquares) # divide the pixel location on the window by the square size to get int numbers that are used to represent where on the board a player has clicked
                x = int(location[1] // DimensionsOfSquares)

                if FromSquare == (x, y):
                    FromSquare = ()
                    playerClicks = []
                
                else: # adds the second click of the player to the list
                    FromSquare = (x, y)
                    playerClicks.append(FromSquare)

                    # ------------ part of color possible squares ---------------
                    # colorMoveAbleSpots(window, gameLogic, gameLogic.generateValidMoveSet(gameLogic.board[x][y], x, y), FromSquare)
                    # colorMoveAbleSpots(window, gameLogic, gameLogic.board[x][y])
                    # colorMoveAbleSpots(window, gameLogic, FromSquare)
                    
                    # Color the game board of the available moves given a selected piece
                    # gameBoard = gameLogic.board
                    # generateMoveAbleSpotsToColor = gameLogic.generateValidMoveSet(gameLogic.board[x, y], x, y)
                    # colorMoveAbleSpots(window, gameBoard, generateMoveAbleSpotsToColor)
                    # ------------ part of color possible squares ---------------
                
                if len(playerClicks) == 2: # if there are 2 seperate clicks on the board, check if they can be considered piece movements, if so perform the movement
                    status = gameLogic.movePiece(playerClicks[0], playerClicks[1])

                    if status[0] == 1: # if the move was sucessful
                        print('\nMove worked.\n')
                    
                    elif status[0] == 2: # if the resulting move was a pawn reaching the end, the pawn is promoted to selected piece
                        while True:
                            typeOfPieceToPromote = input("\nPawn has reached the end. Enter the type of piece to promote it to (queen, bishop, rook, night(knight)): ")

                            typeOfPieceToPromote = str.lower(typeOfPieceToPromote)

                            if typeOfPieceToPromote == 'queen' or typeOfPieceToPromote == 'bishop' or typeOfPieceToPromote == 'rook' or typeOfPieceToPromote == 'night':
                                firstLetter = typeOfPieceToPromote[0].upper()

                                if status[1][0] == 7:
                                    color = 'b'
                                elif status[1][0] == 0:
                                    color = 'w'

                                newPiece = color + firstLetter
                                
                                gameLogic.upgradePawn(status[1][0], status[1][1], newPiece)

                                break

                    elif status[0] == -1: # if the movement faild
                        print('\nInvalid pieces chosen.\n')
                        FromSquare = ()
                        playerClicks = []

                    FromSquare = ()
                    playerClicks = []
        
        # redraws the board based on most current board state
        updateBoard(window, gameLogic)#, FromSquare)
        # colorMoveAbleSpots(window, gameLogic, validMoveSet, FromSquare)

        py.display.flip()

    # window = py.Window

# this method will be used to color in possible square that a clicked on piece can move to ----------- doesn't work for some reason - try fixing it later --------------------
def colorMoveAbleSpots(window, gameLogic, PieceToMove):
    validMoves = []

    if PieceToMove != ():# or PieceToMove != None:
        pieceMoved = gameLogic.board[PieceToMove[0]][PieceToMove[1]]
        row, col = PieceToMove[0], PieceToMove[1]

        if gameLogic.board[row][col][0] == ('w' if gameLogic.CurrentTurn else 'b'):
            surf = py.Surface((DimensionsOfSquares, DimensionsOfSquares))
            surf.set_alpha(100)
            surf.fill(py.Color("green"))

            # LocationOfSquares = py.Rect(col * DimensionsOfSquares, row * DimensionsOfSquares, DimensionsOfSquares, DimensionsOfSquares)
            
            surf.blit(window, (row * DimensionsOfSquares, col * DimensionsOfSquares))

            surf.fill(py.Color('yellow'))

            validMoves = gameLogic.GeneratePieceMoves[pieceMoved[1]](pieceMoved, row, col)

            for move in validMoves:
                # if move.fromX == row and move.fromY == col:
                # surf.blit(window, (move[0] * DimensionsOfSquares, move[1] * DimensionsOfSquares))
                LocationOfSquares = py.Rect(move[0] * DimensionsOfSquares, move[1] * DimensionsOfSquares, DimensionsOfSquares, DimensionsOfSquares)
            
                surf.blit(surf, LocationOfSquares)

# draws the board
def updateBoard(window, GL):#, PieceToMove):
    colorIndex = 0

    for row in range(NumOfSquares):
        for col in range(NumOfSquares):
            colorIndex = 1 - colorIndex # swaps between 1 and 0 to choose which color will be displayed
            # if colorIndex is currently 0, it will be equal to 1 (1 - 0 = 1)
            # if colorIndex is currently 1, it will be equal to 0 (1 - 1 = 0)

            LocationOfSquares = py.Rect(col * DimensionsOfSquares, row * DimensionsOfSquares, DimensionsOfSquares, DimensionsOfSquares)
            
            py.draw.rect(window, COLORS[colorIndex], LocationOfSquares)

            if GL.board[row][col] != '--': # if the current spot in the board/array is not empty ('-' represents empty spot) then draw the given piece from the dictionary
                window.blit(ChessPieces[GL.board[row][col]], LocationOfSquares)

        colorIndex = 1 - colorIndex # flips again to start with the other color in the next row, causes all rows and coloumns to look the same otherwise

    # colorMoveAbleSpots(window, GL, PieceToMove)

if __name__ == '__main__':
    main()