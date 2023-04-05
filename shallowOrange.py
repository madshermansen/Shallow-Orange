import random
import chess
import chess.polyglot
import time

class shallowOrange:

    # values for evaluation
    PIECE_VALUES = {
        chess.PAWN: 1000,
        chess.KNIGHT: 3005,
        chess.BISHOP: 3330,
        chess.ROOK: 5630,
        chess.QUEEN: 9500,
        chess.KING: 30000
    }

    POSITIONAL_VALUES_BLACK = {
        chess.PAWN: [
        [0, 0, 0, 0, 0, 0, 0, 0,],
        [-100, -50, 50, 100, 100, 50, -50, -100,],
        [-100, -50, 50, 150, 150, 50, -50, -100,],
        [-100, -50, 200, 100, 100, 200, -50, -100,],
        [-30, 30, 170, 270, 270, 170, 30, -30,],
        [60, 120, 250, 140, 140, 250, 120, 60,],
        [250, 400, 400, 250, 250, 400, 400, 250,],
        [0, 0, 0, 0, 0, 0, 0, 0,],
        ],
        chess.KNIGHT: [
        [-500, -400, -300, -300, -300, -300, -400, -500],
        [-400, -200, 0, 50, 50, 0, -200, -400],
        [-300, 500, 100, 150, 150, 100, 50, -300],
        [-300, 0, 150, 200, 200, 150, 0, -300],
        [-300,  500,  150, 200, 200, 150, 500, -300],
        [-300,  0, 100, 150, 150, 100, 0, -300],
        [-400, -200, 0, 0, 0, 0, -200, -400],
        [-500, -400, -300, -300, -300, -300, -400, -500]
        ],
        chess.BISHOP: [
        [-200, -100, -100, -100, -100, -100, -100, -200],
        [-100, 50, 0, 0, 0, 0, 50, -100],
        [-100, 100, 100, 100, 100, 100, 100, -100],
        [-100, 0, 100, 100, 100, 100, 0, -100],
        [-100, 50, 50, 100, 100, 50, 50, -100],
        [-100, 0, 50, 100, 100, 50, 0, -100],
        [-100, 0, 0, 0, 0, 0, 0, -100],
        [-200, -100, -100, -100, -100, -100, -100, -200],
        ],
        chess.ROOK: [     
        [0, 0, 0, 50, 50, 0, 0, 0,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [0, 0, 0, 50, 50, 0, 0, 0,],
        ],
        chess.QUEEN: [
        [-200, -100, -100, -50, -50, -100, -100, -200],
        [-100, 0, 0, 0, 0, 0, 0, -100],
        [-100, 0, 50, 50, 50, 50, 0, -100],
        [-50, 0, 50, 50, 50, 50, 0, -50],
        [0, 0, 50, 50, 50, 50, 0, -50],
        [-100, 50, 50, 50, 50, 50, 0, -100],
        [-100, 0, 50, 0, 0, 0, 0, -100],
        [-200, -100, -100, -50, -50, -100, -100, -200],
        ],
        chess.KING: [
        [200, 300, 100, 0, 0, 100, 300, 200],
        [200, 200, 0, 0, 0, 0, 200, 200],
        [-100, -200, -200, -200, -200, -200, -200, -100],
        [-200, -300, -300, -400, -400, -300, -300, -200],
        [-300, -400, -400, -500, -500, -400, -400, -300],
        [-300, -400, -400, -500, -500, -400, -400, -300],
        [-300, -400, -400, -500, -500, -400, -400, -300],
        [-300, -400, -400, -500, -500, -400, -400, -300]
        ]
    }

    POSITIONAL_VALUES_WHITE = {
        chess.PAWN: [
        [0, 0, 0, 0, 0, 0, 0, 0,],
        [250, 400, 400, 250, 250, 400, 400, 250,],
        [60, 120, 250, 140, 140, 250, 120, 60,],
        [-30, 30, 170, 270, 270, 170, 30, -30,],
        [-100, -50, 200, 100, 100, 200, -50, -100],
        [-100, -50, 50, 150, 150, 50, -50, -100,],
        [-100, -50, 50, 100, 100, 50, -50, -100,],
        [0, 0, 0, 0, 0, 0, 0, 0,],
        ],
        chess.KNIGHT: [ 
        [-500, -400, -300, -300, -300, -300, -400, -500],
        [-400, -200, 0, 50, 50, 0, -200, -400],
        [-300, 500, 100, 150, 150, 100, 50, -300],
        [-300, 0, 150, 200, 200, 150, 0, -300],
        [-300,  500,  150, 200, 200, 150, 500, -300],
        [-300,  0, 100, 150, 150, 100, 0, -300],
        [-400, -200, 0, 0, 0, 0, -200, -400],
        [-500, -400, -300, -300, -300, -300, -400, -500],
        ],
        chess.BISHOP: [
        [-200, -100, -100, -100, -100, -100, -100, -200],
        [-100, 50, 0, 0, 0, 0, 50, -100],
        [-100, 100, 100, 100, 100, 100, 100, -100],
        [-100, 0, 100, 100, 100, 100, 0, -100],
        [-100, 50, 50, 100, 100, 50, 50, -100],
        [-100, 0, 50, 100, 100, 50, 0, -100],
        [-100, 0, 0, 0, 0, 0, 0, -100],
        [-200, -100, -100, -100, -100, -100, -100, -200],
        ],
        chess.ROOK: [
        [0, 0, 0, 50, 50, 0, 0, 0,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [-50, 0, 0, 0, 0, 0, 0, -50,],
        [0, 0, 0, 50, 50, 0, 0, 0,],
        ],
        chess.QUEEN: [
        [-200, -100, -100, -50, -50, -100, -100, -200],
        [-100, 0, 0, 0, 0, 0, 0, -100],
        [-100, 0, 50, 50, 50, 50, 0, -100],
        [-50, 0, 50, 50, 50, 50, 0, -50],
        [0, 0, 50, 50, 50, 50, 0, -50],
        [-100, 50, 50, 50, 50, 50, 0, -100],
        [-100, 0, 50, 0, 0, 0, 0, -100],
        [-200, -100, -100, -50, -50, -100, -100, -200],
        ],
        chess.KING: [
        [-300, -400, -400, -500, -500, -400, -400, -300],
        [-300, -400, -400, -500, -500, -400, -400, -300],
        [-300, -400, -400, -500, -500, -400, -400, -300],
        [-300, -400, -400, -500, -500, -400, -400, -300],
        [-200, -300, -300, -400, -400, -300, -300, -200],
        [-100, -200, -200, -200, -200, -200, -200, -100],
        [200, 200, 0, 0, 0, 0, 200, 200],
        [200, 300, 100, 0, 0, 100, 300, 200],
        ]
    }

    def __init__(self, FEN ="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", depth = 1, book="polyglot/Human.bin") -> None:
        self.board = chess.Board(FEN)
        self.depth = depth
        self.book = book
        self.early_game = True
        self.zobrist_table = self.init_zobrist_table()
        self.transposition_table = {}

    def init_zobrist_table(self):
        table = {}
        for square in chess.SQUARES:
            table[square] = {}
            for piece in range(1, 7):
                table[square][piece] = {}
                for color in [chess.WHITE, chess.BLACK]:
                    table[square][piece][color] = random.getrandbits(64)
        return table

    def hash_board(self):
        h = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                h ^= self.zobrist_table[square][piece.piece_type][piece.color]
        return h


    def evaluate(self):
        if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_seventyfive_moves() or self.board.is_fivefold_repetition():
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
                # material advantage
                if piece.color == chess.WHITE:
                    evaluation += self.PIECE_VALUES[piece.piece_type]
                else:
                    evaluation -= self.PIECE_VALUES[piece.piece_type]
                # positional advantage
                if piece.color == chess.WHITE:
                    evaluation += self.POSITIONAL_VALUES_WHITE[piece.piece_type][chess.square_rank(square)][chess.square_file(square)]
                else:
                    evaluation -= self.POSITIONAL_VALUES_BLACK[piece.piece_type][chess.square_rank(square)][chess.square_file(square)]
        return evaluation

    def alphabeta(self, depth, alpha, beta, maximizingPlayer):
        zobrist_hash = self.hash_board()
        if zobrist_hash in self.transposition_table:
            stored_depth, stored_eval, stored_move = self.transposition_table[zobrist_hash]
            
            if stored_depth >= depth:
                return stored_eval, stored_move
        else:
            stored_depth = -1

        if depth == 0:
            return self.evaluate(), None

        if maximizingPlayer:
            maxEval = float('-inf')
            bestMove = None
            for move in self.board.legal_moves:
                self.board.push(move)
                evaluation, _ = self.alphabeta(depth - 1, alpha, beta, False)
                self.board.pop()
                if evaluation > maxEval:
                    maxEval = evaluation
                    bestMove = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

            # Store the result in the transposition table
            self.transposition_table[zobrist_hash] = (depth, maxEval, bestMove)
            return maxEval, bestMove
        else:
            minEval = float('inf')
            bestMove = None
            for move in self.board.legal_moves:
                self.board.push(move)
                evaluation, _ = self.alphabeta(depth - 1, alpha, beta, True)
                self.board.pop()
                if evaluation < minEval:
                    minEval = evaluation
                    bestMove = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            self.transposition_table[zobrist_hash] = (depth, minEval, bestMove)
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
        startTime = time.time()
        evaluation, bestMove = self.alphabeta(self.depth - 1, float('-inf'), float('inf'), self.board.turn)
        print(f"Time taken: {time.time() - startTime}")
        return bestMove

    def gameOver(self):
        return self.board.is_game_over() or self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_seventyfive_moves() or self.board.is_fivefold_repetition()