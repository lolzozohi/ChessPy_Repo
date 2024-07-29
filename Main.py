import chess
import chess.engine

class SimpleChessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.max_depth = 1  # Set a default search depth

    def evaluate(self, board):
        # Simple evaluation: material count
        material = sum(piece.piece_type for piece in board.piece_map().values())
        return material if board.turn else -material

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board), None

        best_move = None
        if is_maximizing:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def best_move(self):
        _, move = self.minimax(self.board, self.max_depth, float('-inf'), float('inf'), True)
        return move

    def uci_loop(self):
        while True:
            command = input()
            if command == 'uci':
                print('id name SimpleChessEngine')
                print('id author Ayan Zakaria')  
                print('uciok')
            elif command.startswith('position'):
                self.position(command)
            elif command.startswith('go'):
                self.go()
            elif command == 'quit':
                break

    def position(self, command):
        parts = command.split()
        if 'startpos' in command:
            self.board.set_fen(chess.STARTING_FEN)
        else:
            fen_index = parts.index('fen')
            fen = ' '.join(parts[fen_index + 1:fen_index + 7])
            self.board.set_fen(fen)
        if 'moves' in command:
            moves_index = parts.index('moves')
            moves = parts[moves_index + 1:]
            for move in moves:
                self.board.push_uci(move)

    def go(self):
        move = self.best_move()
        if move:
            print(f'bestmove {move.uci()}')

if __name__ == '__main__':
    engine = SimpleChessEngine()
    engine.uci_loop()
