import tkinter as tk

import copy


class AliceChess:
    def __init__(self):
        self.boards = {
            "A": self.create_board(),
            "B": self.create_board(empty=True),
        }
        self.current_turn = "white"

    def create_board(self, empty=False):
        if empty:
            return [[None for _ in range(8)] for _ in range(8)]

        # Configuración inicial del ajedrez
        pieces = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        board = []

        # Fila de piezas negras
        board.append([("black", piece) for piece in pieces])
        # Peones negros
        board.append([("black", "P") for _ in range(8)])
        # Filas vacías
        for _ in range(4):
            board.append([None for _ in range(8)])
        # Peones blancos
        board.append([("white", "P") for _ in range(8)])
        # Fila de piezas blancas
        board.append([("white", piece) for piece in pieces])

        return board

    def display_boards(self):
        print("\nBoard A:")
        self.display_board(self.boards["A"])
        print("\nBoard B:")
        self.display_board(self.boards["B"])

    def display_board(self, board):
        for row in board:
            print(" ".join([f"{cell[1][0]}" if cell else "." for cell in row]))

    def get_legal_moves(self, position, start_board, end_board):
        x, y = position
        piece = self.boards[start_board][x][y]

        if not piece:
            return []

        color, piece_type = piece

        if color != self.current_turn:
            return []

        moves = []

        if piece_type == "P":
            moves = self.get_pawn_moves(x, y, start_board, end_board)
        elif piece_type == "N":
            moves = self.get_knight_moves(x, y, start_board, end_board)
        elif piece_type == "B":
            moves = self.get_bishop_moves(x, y, start_board, end_board)
        elif piece_type == "R":
            moves = self.get_rook_moves(x, y, start_board, end_board)
        elif piece_type == "Q":
            moves = self.get_queen_moves(x, y, start_board, end_board)
        elif piece_type == "K":
            moves = self.get_king_moves(x, y, start_board, end_board)

        return moves

    def get_pawn_moves(self, x, y, start_board, end_board):
        moves = []
        direction = -1 if self.current_turn == "white" else 1
        target_board = self.boards[end_board]

        # Movimiento simple hacia adelante
        if 0 <= x + direction < 8 and not target_board[x + direction][y]:
            moves.append((x + direction, y))

        # Captura diagonal
        for dy in [-1, 1]:
            if 0 <= y + dy < 8 and 0 <= x + direction < 8:
                target_piece = target_board[x + direction][y + dy]
                if target_piece and target_piece[0] != self.current_turn:
                    moves.append((x + direction, y + dy))

        return moves

    def get_knight_moves(self, x, y, start_board, end_board):
        moves = []
        target_board = self.boards[end_board]
        knight_jumps = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for dx, dy in knight_jumps:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = target_board[nx][ny]
                if not target_piece or target_piece[0] != self.current_turn:
                    moves.append((nx, ny))

        return moves

    def get_bishop_moves(self, x, y, start_board, end_board):
        return self.get_sliding_moves(x, y, start_board, end_board, directions=[(1, 1), (1, -1), (-1, 1), (-1, -1)])

    def get_rook_moves(self, x, y, start_board, end_board):
        return self.get_sliding_moves(x, y, start_board, end_board, directions=[(1, 0), (0, 1), (-1, 0), (0, -1)])

    def get_queen_moves(self, x, y, start_board, end_board):
        return self.get_sliding_moves(x, y, start_board, end_board, directions=[
            (1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)
        ])

    def get_king_moves(self, x, y, start_board, end_board):
        moves = []
        target_board = self.boards[end_board]
        king_moves = [
            (1, 0), (0, 1), (-1, 0), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for dx, dy in king_moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = target_board[nx][ny]
                if not target_piece or target_piece[0] != self.current_turn:
                    moves.append((nx, ny))

        return moves

    def get_sliding_moves(self, x, y, start_board, end_board, directions):
        moves = []
        target_board = self.boards[end_board]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = target_board[nx][ny]
                if target_piece:
                    if target_piece[0] != self.current_turn:
                        moves.append((nx, ny))
                    break
                moves.append((nx, ny))
                nx += dx
                ny += dy

        return moves

    def move_piece(self, start, end, start_board, end_board):
        sx, sy = start
        ex, ey = end

        piece = self.boards[start_board][sx][sy]

        if not piece:
            return False

        if end not in self.get_legal_moves(start, start_board, end_board):
            return False

        # Realizar movimiento
        self.boards[start_board][sx][sy] = None
        self.boards[end_board][ex][ey] = piece

        # Cambiar turno
        self.current_turn = "black" if self.current_turn == "white" else "white"
        return True

    def is_king_in_check(self, color):
        king_position = None
        king_board = None

        for board_key in ["A", "B"]:
            for x, row in enumerate(self.boards[board_key]):
                for y, cell in enumerate(row):
                    if cell == (color, "K"):
                        king_position = (x, y)
                        king_board = board_key
                        break

        if not king_position:
            return False

        opponent_color = "black" if color == "white" else "white"
        for board_key in ["A", "B"]:
            for x, row in enumerate(self.boards[board_key]):
                for y, cell in enumerate(row):
                    if cell and cell[0] == opponent_color:
                        moves = self.get_legal_moves((x, y), board_key, king_board)
                        if king_position in moves:
                            return True

        return False

    def is_checkmate(self, color):
        for board_key in ["A", "B"]:
            for x in range(8):
                for y in range(8):
                    piece = self.boards[board_key][x][y]
                    if piece and piece[0] == color:
                        for end_board in ["A", "B"]:
                            moves = self.get_legal_moves((x, y), board_key, end_board)
                            for move in moves:
                                cloned_game = self.clone_game()
                                cloned_game.move_piece((x, y), move, board_key, end_board)
                                if not cloned_game.is_king_in_check(color):
                                    return False

        return True

    def clone_game(self):
        import copy
        return copy.deepcopy(self)

    def is_game_over(self):
        if self.is_checkmate("white"):
            print("Black wins by checkmate!")
            return True
        if self.is_checkmate("black"):
            print("White wins by checkmate!")
            return True
        return False



class AliceAI:
    def __init__(self, depth=2):
        self.depth = depth

    def evaluate_board(self, game):
        piece_values = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 1000}
        central_positions = {
            "A": set((x, y) for x in range(3, 5) for y in range(3, 5)),
            "B": set((x, y) for x in range(3, 5) for y in range(3, 5)),
        }

        total_mine = 0
        total_opponent = 0
        center_mine = 0
        center_opponent = 0

        for board_key in game.boards:
            for x, row in enumerate(game.boards[board_key]):
                for y, cell in enumerate(row):
                    if cell:
                        color, piece = cell
                        value = piece_values.get(piece, 0)
                        if color == "white":
                            total_mine += value
                            if (x, y) in central_positions[board_key]:
                                center_mine += value
                        else:
                            total_opponent += value
                            if (x, y) in central_positions[board_key]:
                                center_opponent += value

        return (total_mine - total_opponent) + (center_mine - center_opponent)

    def get_all_moves(self, game, color):
        moves = []
        for board_key in ["A", "B"]:
            for x in range(8):
                for y in range(8):
                    piece = game.boards[board_key][x][y]
                    if piece and piece[0] == color:
                        target_board = "A" if board_key == "B" else "B"
                        legal_moves = game.get_legal_moves((x, y), board_key, target_board)
                        moves.extend([(x, y, move, board_key, target_board) for move in legal_moves])
        return moves

    def minimax(self, game, depth, maximizing_player):
        if depth == 0:
            return self.evaluate_board(game), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_all_moves(game, "white"):
                start_x, start_y, end, start_board, end_board = move
                cloned_game = copy.deepcopy(game)
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
                cloned_game = copy.deepcopy(game)
                cloned_game.move_piece((start_x, start_y), end, start_board, end_board)
                eval, _ = self.minimax(cloned_game, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

class AliceChessGUI:
    def __init__(self, root):
        self.root = root
        self.game = AliceChess()
        self.ai = AliceAI(depth=2)
        self.selected_piece = None
        self.selected_board = None

        self.board_frames = {
            "A": tk.Frame(root),
            "B": tk.Frame(root)
        }

        # Configurar tableros
        for board_key in self.board_frames:
            self.board_frames[board_key].grid(row=0, column=0 if board_key == "A" else 1, padx=10, pady=10)

        self.cells = {
            "A": {},
            "B": {}
        }

        for board_key in self.board_frames:
            for x in range(8):
                for y in range(8):
                    cell = tk.Label(self.board_frames[board_key], width=4, height=2, bg=self.get_cell_color(x, y), relief="raised")
                    cell.grid(row=x, column=y)
                    cell.bind("<Button-1>", lambda e, bx=x, by=y, board=board_key: self.cell_clicked(bx, by, board))
                    self.cells[board_key][(x, y)] = cell

        self.update_board()
        self.create_reset_button()

    def get_cell_color(self, x, y):
        return "#F0D9B5" if (x + y) % 2 == 0 else "#B58863"

    def update_board(self):
        piece_symbols = {
            "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔"
        }

        for board_key, board in self.game.boards.items():
            for x, row in enumerate(board):
                for y, cell in enumerate(row):
                    if cell:
                        color, piece = cell
                        symbol = piece_symbols[piece]
                        self.cells[board_key][(x, y)].config(text=symbol, fg="white" if color == "white" else "black")
                    else:
                        self.cells[board_key][(x, y)].config(text="")

    def show_valid_moves(self, valid_moves, board):
        for x, y in valid_moves:
            self.cells[board][(x, y)].config(bg="#90EE90")  # Verde claro

    def reset_highlights(self):
        for board_key in self.cells:
            for x, y in self.cells[board_key]:
                self.cells[board_key][(x, y)].config(bg=self.get_cell_color(x, y))

    def cell_clicked(self, x, y, board):
        self.reset_highlights()
        cell = self.game.boards[board][x][y]

        if self.selected_piece and (self.selected_board == board):
            # Intenta mover la pieza seleccionada
            target_board = "A" if board == "B" else "B"
            if (x, y) in self.game.get_legal_moves(self.selected_piece, board, target_board):
                self.game.move_piece(self.selected_piece, (x, y), self.selected_board, target_board)
                self.selected_piece = None
                self.selected_board = None
                self.update_board()
                self.check_ai_turn()
                return

        # Si selecciona una pieza
        if cell and cell[0] == self.game.current_turn:
            self.selected_piece = (x, y)
            self.selected_board = board
            valid_moves = self.game.get_legal_moves((x, y), board, "A" if board == "B" else "B")
            self.show_valid_moves(valid_moves, "A" if board == "B" else "B")
            
    def reset_game(self):
            self.game = AliceChess()
            self.selected_piece = None
            self.selected_board = None
            self.update_board()

    def create_reset_button(self):
            reset_button = tk.Button(self.root, text="Reiniciar", command=self.reset_game)
            reset_button.grid(row=3, column=0, columnspan=2, pady=10)

    def check_ai_turn(self):
        if self.game.current_turn == "black":
            self.root.after(500, self.ai_move)

    def ai_move(self):
        _, best_move = self.ai.minimax(self.game, self.ai.depth, maximizing_player=False)
        if best_move:
            start_x, start_y, end, start_board, end_board = best_move
            self.game.move_piece((start_x, start_y), end, start_board, end_board)
            self.update_board()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Alice Chess GUI")
    gui = AliceChessGUI(root)
    root.mainloop()
