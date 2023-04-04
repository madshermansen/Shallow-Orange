import chess
import chess.polyglot

class shallowOrange:

    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 300,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }


    def __init__(self, FEN ="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", depth = 1, book="polyglot/baron30.bin") -> None:
        self.board = chess.Board(FEN)
        self.depth = depth
        self.book = book
        self.early_game = True

    def evaluate(self):
        if self.board.is_stalemate():
            return 0
        if self.board.is_checkmate():
            if self.board.turn:
                return float('inf')
            else:
                return float('-inf')

        evaluation = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece != None:
                if piece.color == chess.WHITE:
                    evaluation += self.PIECE_VALUES[piece.piece_type]
                else:
                    evaluation -= self.PIECE_VALUES[piece.piece_type]
        return evaluation
        

    def alphabeta(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            return self.evaluate(), None
        if maximizingPlayer:
            maxEval = float('-inf')
            bestMove = None
            for move in self.board.legal_moves:
                self.board.push(move)
                evaluation = self.alphabeta(depth - 1, alpha, beta, False)[0]
                self.board.pop()
                if evaluation > maxEval:
                    maxEval = evaluation
                    bestMove = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return maxEval, bestMove
        else:
            minEval = float('inf')
            bestMove = None
            for move in self.board.legal_moves:
                self.board.push(move)
                evaluation = self.alphabeta(depth - 1, alpha, beta, True)[0]
                self.board.pop()
                if evaluation < minEval:
                    minEval = evaluation
                    bestMove = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return minEval, bestMove
    
    def handleBookMoves(self):
        with chess.polyglot.open_reader(self.book) as reader:
            # find best book move
            try:
                entry = reader.weighted_choice(self.board)
                return entry.move
            except IndexError:
                self.early_game = False
        return self.bestMove()

    def bestMove(self):
        if self.early_game:
            return self.handleBookMoves()
        evaluation, bestMove = self.alphabeta(self.depth - 1, float('-inf'), float('inf'), self.board.turn)
        return bestMove
            

    def gameOver(self):
        return self.board.is_game_over()