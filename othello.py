#Erika Noma
#CS111 Winter2017 Final Project

import random
import sys

def drawBoard(board):
    Hline = '  +---+---+---+---+---+---+---+---+'
    Vline = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(Hline)
    for y in range(8):
        print(Vline)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(Hline)
        print(Vline)
 
def resetBoard(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    board[3][3] = 'X' #initial four tiles
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def newBoard():
    board = []
    for i in range(8):
        board.append([' ']*8)
    return board

def isLegal(board, tile, xstart, ystart):
    if board[xstart][ystart] != ' ':
        return False
    if not isOnBoard(xstart, ystart):
    	return False

    board[xstart][ystart] = tile 

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    flipTiles = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection 
        y += ydirection 
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    flipTiles.append([x, y])
 
    board[xstart][ystart] = ' ' 
    if len(flipTiles) == 0: 
        return False
    return flipTiles

def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <=7


def BoardWithLegalMoves(board, tile):
    copyBoard = getBoardCopy(board)

    for x, y in getLegalMove(copyBoard, tile):
        copyBoard[x][y] = '.'
    return copyBoard


def getLegalMove(board, tile):
    legalMoves = []
    for x in range(8):
        for y in range(8):
            if isLegal(board, tile, x, y) != False:
                legalMoves.append([x, y])
    return legalMoves


def getScore(board):
    Xscore = 0
    Oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                Xscore += 1
            if board[x][y] == 'O':
                Oscore += 1
    return {'X':Xscore, 'O':Oscore}


def enterPlayerTile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Which do you want to play, X or O? ')
        tile = input().upper()

    if tile == 'X':
        return ['X', 'O']

    else:
        return ['O', 'X']

def firstPlayer():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    print('Do you want to play it again? (yes or no): ')
    return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
    flipTiles = isLegal(board, tile, xstart, ystart)

    if flipTiles == False:
        return False

    board[xstart][ystart] = tile
    for x, y in flipTiles:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    copyBoard = newBoard()

    for x in range(8):
        for y in range(8):
            copyBoard[x][y] = board[x][y]
    return copyBoard

def corner(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getPlayerMove(board, playerTile):
    numbers = ('1 2 3 4 5 6 7 8').split()
    while True:
        print('Enter your move or type "quit" to quit playing.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if len(move) == 2 and move[0] in numbers and move[1] in numbers:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isLegal(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('illegal move!')

    return [x, y]


def getComputerMove(board, computerTile):
    possibleMoves = getLegalMove(board, computerTile)
    random.shuffle(possibleMoves)
    for x, y in possibleMoves:
        if corner(x, y):
            return [x, y]

    bestScore = -1
    for x, y in possibleMoves:
        copyBoard = getBoardCopy(board)
        makeMove(copyBoard, computerTile, x, y)
        score = getScore(copyBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def showPoints(playerTile, computerTile):
    scores = getScore(mainBoard)
    print('You have {0} points. The computer has {1} points.'.format(scores[playerTile], scores[computerTile]))



print('Othello')
gamerunning = True
while gamerunning:
    mainBoard = newBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    turn = firstPlayer()
    print('The ' + turn + ' will go first.')

    while True:
        if turn == 'player':
        	drawBoard(mainBoard)
        	showPoints(playerTile, computerTile)
        	move = getPlayerMove(mainBoard, playerTile)
        	if move == 'quit':
        		print('Thank you for playing')
        		sys.exit()
        	else:
        		makeMove(mainBoard, playerTile, move[0], move[1])
        	if getLegalMove(mainBoard, computerTile) == []:
        		break
        	else:
        		turn = 'computer'

        else:
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            input('Press Enter to see the computer\'s move.')
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y)

            if getLegalMove(mainBoard, playerTile) == []:
                break
            else:
                turn = 'player'

    drawBoard(mainBoard)
    scores = getScore(mainBoard)
    print('X score: {0} points. O score: {1} points.'.format(scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]:
        print('Yay! You won the computer with {} points! '.format(scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost...The computer won with {}more points.'.format(scores[computerTile] - scores[playerTile]))
    

    if not playAgain():
        break


