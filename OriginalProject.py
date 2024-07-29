import chess
#re-name as main.py when you run it.

# Piece values
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0  # The king's value is set to 0 as its capture ends the game
}

def evaluate_board(board):
    """
    Evaluate the board position from the perspective of the player to move.

    Positive score means the position is favorable for white.
    Negative score means the position is favorable for black.
    """
    
    score = 0
    for piece_type, value in piece_values.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value
    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth):
    best_move = None
    best_value = -float('inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, -float('inf'), float('inf'), False)
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_move = move
    return best_move

def play_game():
    global difficulty
    print("Enter difficulty level (1-10): ")
    difficulty = int(input("Lower = faster but poorer moves. Higher = better yet slower." ))
    board = chess.Board()
    while not board.is_game_over():
        print("  ")
        print(board)
        print(evaluate_board(board))
        if board.turn == chess.WHITE:
            move = input("Enter your move (Ex:e2e4)")
            if move in [str(m) for m in board.legal_moves]:
                board.push_san(move)
            else:
                print("Invalid move. Try again.")
        else:
            print("AI is thinking...")
            best_move = find_best_move(board, difficulty)  # Depth of 3 for simplicity
            if best_move is not None:
                board.push(best_move)
                print(f"AI played: {best_move}")

    print("Game over!")
    print(board.result())

if __name__ == "__main__":
    play_game()
