import tkinter as tk

# Definición de las piezas
PIECES = {
    'T': '♖',  # Torre blanca
    'C': '♘',  # Caballo blanco
    'A': '♗',  # Alfil blanco
    'RE': '♕',  # Reina blanca
    'R': '♔',  # Rey blanco
    'P': '♙',  # Peón blanco
    't': '♜',  # Torre negra
    'c': '♞',  # Caballo negro
    'a': '♟',  # Alfil negro
    're': '♛',  # Reina negra
    'r': '♚',  # Rey negro
    'p': '♟',  # Peón negro
}

class ChessGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Ajedrez de Alicia")
        self.board1 = self.create_board()
        self.board2 = self.create_board()  # Tablero paralelo vacío
        self.current_turn = 'white'  # Turno inicial
        self.selected_piece = None
        self.selected_position = None

        self.initialize_board()
        self.create_gui()

    def create_board(self):
        # Crear un tablero vacío
        return [['' for _ in range(8)] for _ in range(8)]

    def initialize_board(self):
        # Inicializar las posiciones de las piezas en el tablero
        self.board1[0] = ['T', 'C', 'A', 'RE', 'R', 'A', 'C', 'T']  # Piezas blancas
        self.board1[1] = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']  # Peones blancos
        self.board1[6] = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']  # Peones negros
        self.board1[7] = ['t', 'c', 'a', 're', 'r', 'a', 'c', 't']  # Piezas negras

    def create_gui(self):
        # Crear la interfaz gráfica
        self.canvas1 = tk.Canvas(self.master, width=400, height=400)
        self.canvas1.pack(side=tk.LEFT)
        self.canvas2 = tk.Canvas(self.master, width=400, height=400)
        self.canvas2.pack(side=tk.RIGHT)

        self.turn_label = tk.Label(self.master, text=f"Turno: {self.current_turn.capitalize()}", font=("Arial", 16))
        self.turn_label.pack()

        self.draw_board(self.canvas1, self.board1)
        self.draw_board(self.canvas2, self.board2)

        self.canvas1.bind("<Button-1>", lambda event: self.on_click(event, self.board1, self.canvas1))
        self.canvas2.bind("<Button-1>", lambda event: self.on_click(event, self.board2, self.canvas2))

    def draw_board(self, canvas, board):
        # Dibujar el tablero
        canvas.delete("all")  # Limpiar el canvas antes de dibujar
        for row in range(8):
            for col in range(8):
                color = 'white' if (row + col) % 2 == 0 else 'gray'
                canvas.create_rectangle(col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color)
                piece = board[row][col]
                if piece:
                    canvas.create_text(col * 50 + 25, row * 50 + 25, text=PIECES.get(piece, ''), font=("Arial", 24))

    def on_click(self, event, board, canvas):
        col = event.x // 50
        row = event.y // 50

        if self.selected_piece:
            # Intentar mover la pieza seleccionada
            if self.is_valid_move(self.selected_piece, self.selected_position, (row, col), board):
                self.move_piece(self.selected_position, (row, col), board)
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                self.turn_label.config(text=f"Turno: {self .current_turn.capitalize()}")
                if self.current_turn == 'black':
                    self.ai_move()
            self.selected_piece = None
            self.selected_position = None
        else:
            # Seleccionar una pieza
            piece = board[row][col]
            if (self.current_turn == 'white' and piece.isupper()) or (self.current_turn == 'black' and piece.islower()):
                self.selected_piece = piece
                self.selected_position = (row, col)

        self.draw_board(canvas, board)

    def is_valid_move(self, piece, start, end, board):
        # Implementar la lógica de movimiento de las piezas
        start_row, start_col = start
        end_row, end_col = end

        # Ejemplo de lógica simple para el movimiento de las piezas
        if piece.upper() == 'P':  # Peón blanco
            if start_row == 1 and end_row == 3 and start_col == end_col and board[end_row][end_col] == '':
                return True  # Movimiento de dos espacios
            if end_row == start_row + 1 and start_col == end_col and board[end_row][end_col] == '':
                return True  # Movimiento de un espacio
            if end_row == start_row + 1 and abs(start_col - end_col) == 1 and board[end_row][end_col].islower():
                return True  # Captura

        if piece.lower() == 'p':  # Peón negro
            if start_row == 6 and end_row == 4 and start_col == end_col and board[end_row][end_col] == '':
                return True  # Movimiento de dos espacios
            if end_row == start_row - 1 and start_col == end_col and board[end_row][end_col] == '':
                return True  # Movimiento de un espacio
            if end_row == start_row - 1 and abs(start_col - end_col) == 1 and board[end_row][end_col].isupper():
                return True  # Captura

        # Lógica para otras piezas
        if piece.upper() == 'T':  # Torre
            if start_row == end_row or start_col == end_col:
                return self.is_path_clear(start, end, board)

        if piece.upper() == 'C':  # Caballo
            if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
                return True

        if piece.upper() == 'A':  # Alfil
            if abs(start_row - end_row) == abs(start_col - end_col):
                return self.is_path_clear(start, end, board)

        if piece.upper() == 'RE':  # Reina
            if (start_row == end_row or start_col == end_col) or (abs(start_row - end_row) == abs(start_col - end_col)):
                return self.is_path_clear(start, end, board)

        if piece.upper() == 'R':  # Rey
            if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
                return True

        return False

    def is_path_clear(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        row_step = (end_row - start_row) // max(1, abs(end_row - start_row)) if start_row != end_row else 0
        col_step = (end_col - start_col) // max(1, abs(end_col - start_col)) if start_col != end_col else 0

        current_row, current_col = start_row + row_step, start_col + col_step
        while (current_row, current_col) != (end_row, end_col):
            if board[current_row][current_col] != '':
                return False
            current_row += row_step
            current_col += col_step
        return True

    def move_piece(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        piece = board[start_row][start_col]
        board[end_row][end_col] = piece
        board[start_row][start_col] = ''
        # Actualizar el tablero paralelo solo si es un movimiento de la IA
        if self.current_turn == 'black':
            self.update_parallel_board(piece, end_row, end_col)  # Solo mover la pieza en el tablero paralelo
        self.draw_board(self.canvas1, self.board1)

    def update_parallel_board(self, piece, row, col):
        self.board2[row][col] = piece  # Mover la pieza en el tablero paralelo
        self.draw_board(self.canvas2, self.board2)

    def ai_move(self):
        best_move = self.minimax(self.board1, 3, True)
        if best_move:
            start, end = best_move
            self.move_piece(start, end, self.board1)  # Mover en el tablero principal
            self.current_turn = 'white'
            self.turn_label.config(text=f"Turno: {self.current_turn.capitalize()}")

    def minimax(self, board, depth, is_maximizing):
        if depth == 0 or self.is_game_over(board):
            return self.evaluate_board(board)

        if is_maximizing:
            best_value = float('-inf')
            best_move = None
            for row in range(8):
                for col in range(8):
                    piece = board[row][col]
                    if piece.islower():  # Solo considerar piezas negras
                        for r in range(8):
                            for c in range(8):
                                if self.is_valid_move(piece, (row, col), (r, c), board):
                                    # Realizar el movimiento
                                    original_piece = board[r][c]
                                    board[r][c] = piece
                                    board[row][col] = ''
                                    move_value = self.minimax(board, depth - 1, False)
                                    board[row][col] = piece
                                    board[r][c] = original_piece
                                    if move_value > best_value:
                                        best_value = move_value
                                        best_move = ((row, col), (r, c))
            return best_move if depth == 3 else best_value
        else:
            best_value = float('inf')
            for row in range(8):
                for col in range(8):
                    piece = board[row][col]
                    if piece.isupper():  # Solo considerar piezas blancas
                        for r in range(8):
                            for c in range(8):
                                if self.is_valid_move(piece, (row, col), (r, c), board):
                                    # Realizar el movimiento
                                    original_piece = board[r][c]
                                    board[r][c] = piece
                                    board[row][col] = ''
                                    move_value = self.minimax(board, depth - 1, True)
                                    board[row][col] = piece
                                    board[r][c] = original_piece
                                    best_value = min(best_value, move_value)
            return best_value

    def evaluate_board(self, board):
        # Implementar una heurística simple para evaluar el tablero
        value = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece.isupper():  # Piezas blancas
                    value += self.get_piece_value(piece)
                elif piece.islower():  # Piezas negras
                    value -= self.get_piece_value(piece.lower())
        return value

    def get_piece_value(self, piece):
        # Asignar valores a las piezas
        values = {
            'p': 1,  # Peón
            'c': 3,  # Caballo
            'a': 3,  # Alfil
            't': 5,  # Torre
            're': 9,  # Reina
            'r': 1000,  # Rey (valor alto para protegerlo)
        }
        return values.get(piece, 0)

    def is_game_over(self, board):
        # Implementar lógica para determinar si el juego ha terminado
        return False  # Placeholder, implementar lógica real

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()