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

    def move_piece(self, start, end):
        start_board = "A" if self.current_turn == "white" else "B"
        end_board = "B" if start_board == "A" else "A"

        start_x, start_y = start
        end_x, end_y = end

        if not (self.is_within_bounds(start_x, start_y) and self.is_within_bounds(end_x, end_y)):
            print("Invalid move: Out of bounds.")
            return False

        piece = self.boards[start_board][start_x][start_y]

        # Check the other board if no piece is found on the current board
        if not piece:
            start_board = end_board  # Switch to the other board
            end_board = "A" if start_board == "B" else "B"
            piece = self.boards[start_board][start_x][start_y]

        if not piece or piece[0] != self.current_turn:
            print("Invalid move: No piece or wrong turn.")
            return False

        if self.boards[end_board][end_x][end_y]:
            print("Invalid move: Destination on other board is occupied.")
            return False

        self.boards[start_board][start_x][start_y] = None
        self.boards[end_board][end_x][end_y] = piece
        self.current_turn = "black" if self.current_turn == "white" else "white"
        print(f"Moved {piece[1]} to {end} on board {end_board}.")
        return True

    def get_legal_moves(self, position):
        x, y = position
        moves = []
        piece = self.boards["A"][x][y] or self.boards["B"][x][y]
    
        if not piece:
            return moves
    
        color, piece_type = piece
    
        if piece_type == "P":  # Movimiento de peones
            direction = -1 if color == "white" else 1
            new_x = x + direction
            if self.is_within_bounds(new_x, y) and not self.boards["A"][new_x][y]:
                moves.append((new_x, y))
        # Expandir para otras piezas
        return moves
    