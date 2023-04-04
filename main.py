from engine import shallowOrange
from chessboard import display
import time

# initialization variables
depth = 2
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

if __name__ == "__main__":
    engine = shallowOrange(starting_fen, depth=depth)
    
    # start the display
    game_board = display.start()

    while engine.gameOver() == False:
        update_fen = engine.board.fen()
        display.update(update_fen, game_board)
        best_move = engine.bestMove()
        print(best_move)
        engine.board.push(best_move)
        time.sleep(0.5)


