from engine import shallowOrange
from visualizeboard import *
import time

if __name__ == "__main__":
    engine = shallowOrange(depth=4)
    while engine.gameOver() == False:
        startTime = time.time()
        best_move = engine.bestMove()
        print("Time taken: ", time.time() - startTime)
        engine.board.push(best_move)
        print(best_move)


