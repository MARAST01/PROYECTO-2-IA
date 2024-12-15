from alice_chess import AliceChess


class AliceAI:
    def __init__(self, depth=2):
        self.depth = depth  # Profundidad del árbol de búsqueda

    def evaluate_board(self, game):
        # Evaluación básica considerando ambos tableros
        piece_values = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 1000}
        evaluation = 0

        for board_key in game.boards:
            for row in game.boards[board_key]:
                for cell in row:
                    if cell:
                        color, piece = cell
                        value = piece_values.get(piece, 0)
                        evaluation += value if color == "white" else -value

        return evaluation

    def get_all_moves(self, game, color):
        moves = []
        for board_key in ["A", "B"]:
            for x in range(8):
                for y in range(8):
                    piece = game.boards[board_key][x][y]
                    if piece and piece[0] == color:
                        target_board = "A" if board_key == "B" else "B"  # Movimiento siempre hacia el otro tablero
                        legal_moves = game.get_legal_moves((x, y), board_key, target_board)
                        moves.extend([(x, y, move, board_key, target_board) for move in legal_moves])
        return moves

    def clone_game(self, game):
        import copy
        return copy.deepcopy(game)

    def minimax(self, game, depth, maximizing_player):
        if depth == 0:
            return self.evaluate_board(game), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_all_moves(game, "white"):
                start_x, start_y, end, start_board, end_board = move
                cloned_game = self.clone_game(game)
                cloned_game.move_piece((start_x, start_y), end, start_board, end_board)
                eval, _ = self.minimax(cloned_game, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.get_all_moves(game, "black"):
                start_x, start_y, end, start_board, end_board = move
                cloned_game = self.clone_game(game)
                cloned_game.move_piece((start_x, start_y), end, start_board, end_board)
                eval, _ = self.minimax(cloned_game, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move


if __name__ == "__main__":
    game = AliceChess()
    ai = AliceAI(depth=2)

    while True:
        game.display_boards()

        # Turno del jugador
        if game.current_turn == "white":
            try:
                start_board = input("Tablero de origen (A/B): ").strip().upper()
                start = tuple(map(int, input("Coordenadas iniciales (x, y): ").split(",")))
                end = tuple(map(int, input("Coordenadas finales (x, y): ").split(",")))
                end_board = "A" if start_board == "B" else "B"  # El tablero de destino es el opuesto

                if not game.move_piece(start, end, start_board, end_board):
                    print("Movimiento inválido. Intenta de nuevo.")
                    continue
            except ValueError:
                print("Entrada inválida. Usa el formato: x,y")
                continue
        else:
            # Turno de la IA
            print("Turno de la IA...")
            all_moves = ai.get_all_moves(game, "black")
            if not all_moves:
                print("La IA no tiene movimientos válidos. Fin del juego.")
                break
            _, best_move = ai.minimax(game, ai.depth, maximizing_player=False)
            if best_move:
                start_x, start_y, end, start_board, end_board = best_move

                # Validación para asegurar que la IA siempre pase al otro tablero
                if start_board == end_board:
                    print("Movimiento inválido de la IA, ajustando...")
                    continue

                game.move_piece((start_x, start_y), end, start_board, end_board)

        # Condición de finalización
        if not ai.get_all_moves(game, "white"):
            print("El jugador no tiene movimientos válidos. Fin del juego.")
            break
        if not ai.get_all_moves(game, "black"):
            print("La IA no tiene movimientos válidos. Fin del juego.")
            break
