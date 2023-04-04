import chess

class shallowOrange:

    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 300,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }


    def __init__(self, FEN ="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", depth = 1) -> None:
        self.board = chess.Board(FEN)
        self.depth = depth

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
            return self.evaluate()
        if maximizingPlayer:
            value = float('-inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                value = max(value, self.alphabeta(depth - 1, alpha, beta, False))
                self.board.pop()
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                value = min(value, self.alphabeta(depth - 1, alpha, beta, True))
                self.board.pop()
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value
        
    def bestMove(self):
        bestMove = None
        bestValue = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            boardValue = self.alphabeta(self.depth - 1, float('-inf'), float('inf'), self.board.turn)
            self.board.pop()
            if boardValue > bestValue:
                bestMove = move
                bestValue = boardValue
        return bestMove
        
    def gameOver(self):
        return self.board.is_game_over()