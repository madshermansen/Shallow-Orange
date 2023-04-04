from chess import IllegalMoveError
from engine import shallowOrange
from chessboard import display
import time

# initialization variables
depth = 3
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
position = True # True is white, False is black

def updateBoard():
    update_fen = engine.board.fen()
    display.update(update_fen, game_board)

def autoPlay():
    while engine.gameOver() == False:
        updateBoard()
        best_move = engine.bestMove()
        engine.board.push(best_move)
        time.sleep(0.1)

    while True:
        display.check_for_quit()

def humanPlay(position):
    tempBoard = engine.board.copy()
    if position:
        move = input("Enter your move: ")
    else:
        engineMove = engine.bestMove()
        engine.board.push(engineMove)
    while engine.gameOver() == False:
        if move == "undo":
            engine.board = tempBoard
            updateBoard()
            move = input("Enter your move: ")
        tempBoard = engine.board.copy()
        try:
            engine.board.push_san(move)
            engineMove = engine.bestMove()
            engine.board.push(engineMove)
            updateBoard()
            move = input("Enter your move: ")
        except:
            print("Illegal move, try again")
            move = input("Enter your move: ")


    while True:
        display.check_for_quit()

if __name__ == "__main__":
    engine = shallowOrange(starting_fen, depth=depth)
    
    # start the display
    game_board = display.start()

    humanPlay(position)

        


