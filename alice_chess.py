class AliceChess:
    def __init__(self):
        self.boards = {
            "A": self.create_board(),
            "B": self.create_board()
        }
        self.place_pieces()
        self.current_turn = "white"

    @staticmethod
    def create_board():
        return [[None for _ in range(8)] for _ in range(8)]

    @staticmethod
    def get_initial_positions():
        return {
            "white": {
                "P": [(6, i) for i in range(8)],  # Pawns
                "R": [(7, 0), (7, 7)],  # Rooks
                "N": [(7, 1), (7, 6)],  # Knights
                "B": [(7, 2), (7, 5)],  # Bishops
                "Q": [(7, 3)],          # Queen
                "K": [(7, 4)]           # King
            },
            "black": {
                "P": [(1, i) for i in range(8)],
                "R": [(0, 0), (0, 7)],
                "N": [(0, 1), (0, 6)],
                "B": [(0, 2), (0, 5)],
                "Q": [(0, 3)],
                "K": [(0, 4)]
            }
        }

    def place_pieces(self):
        positions = self.get_initial_positions()
        for color, pieces in positions.items():
            for piece, coords in pieces.items():
                for x, y in coords:
                    self.boards["A"][x][y] = (color, piece)

    @staticmethod
    def display_board(board):
        for row in board:
            print(" ".join([f"{piece[1]}({piece[0][0]})" if piece else "--" for piece in row]))
        print("\n")

    def display_boards(self):
        print("Board A:")
        self.display_board(self.boards["A"])
        print("Board B:")
        self.display_board(self.boards["B"])

    @staticmethod
    def is_within_bounds(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def move_piece(self, start, end, start_board, end_board):
        start_x, start_y = start
        end_x, end_y = end

        if not (self.is_within_bounds(start_x, start_y) and self.is_within_bounds(end_x, end_y)):
            print("Movimiento inválido: Fuera de los límites.")
            return False

        piece = self.boards[start_board][start_x][start_y]

        if not piece or piece[0] != self.current_turn:
            print("Movimiento inválido: No hay pieza o turno incorrecto.")
            return False

        # Captura en el mismo tablero
        if start_board == "B" and self.boards[start_board][end_x][end_y]:
            target_piece = self.boards[start_board][end_x][end_y]
            if target_piece[0] != self.current_turn:
                print(f"Capturada {target_piece[1]} en {end} del tablero {start_board}.")
                self.boards[start_board][end_x][end_y] = None

                # Teletransportar la pieza capturadora al tablero A
                self.boards[start_board][start_x][start_y] = None
                self.boards["A"][end_x][end_y] = piece
                self.current_turn = "black" if self.current_turn == "white" else "white"
                print(f"Teletransportado {piece[1]} a {end} en el tablero A.")
                return True
            else:
                print("Movimiento inválido: No puedes capturar tus propias piezas.")
                return False

        # Verificar si el destino está ocupado en el tablero opuesto
        if start_board != end_board and self.boards[end_board][end_x][end_y]:
            print("Movimiento inválido: El destino está ocupado en el tablero opuesto.")
            return False

        # Realizar el movimiento sin captura
        self.boards[start_board][start_x][start_y] = None
        self.boards[end_board][end_x][end_y] = piece
        self.current_turn = "black" if self.current_turn == "white" else "white"
        print(f"Movido {piece[1]} a {end} en el tablero {end_board}.")
        return True

    def get_legal_moves(self, position, start_board, end_board):
        x, y = position
        moves = []
        piece = self.boards[start_board][x][y]

        if not piece:
            return moves

        color, piece_type = piece

        # Generar movimientos según el tipo de pieza
        if piece_type == "P":  # Peón
            direction = -1 if color == "white" else 1
            new_x = x + direction
            if self.is_within_bounds(new_x, y) and not self.boards[end_board][new_x][y]:
                moves.append((new_x, y))
            # Captura diagonal
            for dx in [-1, 1]:
                nx, ny = x + direction, y + dx
                if self.is_within_bounds(nx, ny):
                    target_piece = self.boards[start_board][nx][ny]
                    if target_piece and target_piece[0] != color:
                        moves.append((nx, ny))
        elif piece_type == "R":  # Torre
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                for i in range(1, 8):
                    nx, ny = x + dx * i, y + dy * i
                    if not self.is_within_bounds(nx, ny):
                        break
                    if self.boards[start_board][nx][ny]:
                        if self.boards[start_board][nx][ny][0] != color:
                            moves.append((nx, ny))
                        break
                    moves.append((nx, ny))
        # Agregar lógica para otras piezas
        return moves
