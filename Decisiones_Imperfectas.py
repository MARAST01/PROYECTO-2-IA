#Importaciones 
import tkinter as tk
import copy

class AliceChess:
    def __init__(self):
        self.boards = {
            "A": self.create_board(), #Tablero A
            "B": self.create_board(empty=True), #Tablero B
        }
        self.current_turn = "white" #Turno de las blancas (HUMANO)

    def create_board(self, empty=False):
        if empty:
            return [[None for _ in range(8)] for _ in range(8)] #Tablero 8x8

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
        self.display_board(self.boards["A"]) # imprime el tablero A
        print("\nBoard B:")
        self.display_board(self.boards["B"]) # imprime el tablero B

    def display_board(self, board):
        for row in board:
            print(" ".join([f"{cell[1][0]}" if cell else "." for cell in row])) # mostrar tablero en texto

    def get_legal_moves(self, position, start_board, end_board):
        x, y = position
        piece = self.boards[start_board][x][y]

        if not piece:
            return []

        color, piece_type = piece

        if color != self.current_turn:
            return []

        moves = []

        # 
        if piece_type == "P": # Peón
            moves = self.get_pawn_moves(x, y, start_board, end_board)
        elif piece_type == "N": # Caballo
            moves = self.get_knight_moves(x, y, start_board, end_board)
        elif piece_type == "B": # Alfil
            moves = self.get_bishop_moves(x, y, start_board, end_board)
        elif piece_type == "R": # Torre
            moves = self.get_rook_moves(x, y, start_board, end_board)
        elif piece_type == "Q": # Reina
            moves = self.get_queen_moves(x, y, start_board, end_board)
        elif piece_type == "K": # Rey
            moves = self.get_king_moves(x, y, start_board, end_board)

        return moves

    def get_pawn_moves(self, x, y, start_board, end_board):
        # Movimientos posibles del peón
        moves = []
        direction = -1 if self.current_turn == "white" else 1 # Dirección del peón (hacia adelante)
        target_board = self.boards[end_board] # Tablero objetivo 

        # Movimiento simple hacia adelante
        if 0 <= x + direction < 8 and not target_board[x + direction][y]: # Si no hay pieza en la casilla y que este dentro del limite del tablero (x)
            moves.append((x + direction, y)) # Se agrega la casilla a los movimientos posibles

        # Captura diagonal
        for dy in [-1, 1]:
            if 0 <= y + dy < 8 and 0 <= x + direction < 8: # Si no hay pieza en la casilla y que este dentro del limite del tablero (y)
                target_piece = target_board[x + direction][y + dy] # Se toma la pieza en la casilla diagonal objetivo.
                if target_piece and target_piece[0] != self.current_turn: # Si hay una pieza y no es del mismo color
                    moves.append((x + direction, y + dy)) # Se agrega la casilla a los movimientos posibles

        return moves

    def get_knight_moves(self, x, y, start_board, end_board):
        # Movimientos posibles del caballo
        moves = []
        target_board = self.boards[end_board] # Tablero objetivo
        knight_jumps = [
            (2, 1), (2, -1), (-2, 1), (-2, -1), # Movimientos en L
            (1, 2), (1, -2), (-1, 2), (-1, -2) # Movimientos en L
        ] 

        for dx, dy in knight_jumps: # Se recorren los saltos del caballo
            nx, ny = x + dx, y + dy # Se calcula la nueva posición
            if 0 <= nx < 8 and 0 <= ny < 8: # Si la nueva posición esta dentro del limite del tablero
                target_piece = target_board[nx][ny] # Se toma la pieza en la nueva posición
                if not target_piece or target_piece[0] != self.current_turn: # Si no hay pieza o la pieza no es del mismo color
                    moves.append((nx, ny)) # Se agrega la casilla a los movimientos posibles

        return moves

    def get_bishop_moves(self, x, y, start_board, end_board): # Alfil
        return self.get_sliding_moves(x, y, start_board, end_board, directions=[(1, 1), (1, -1), (-1, 1), (-1, -1)]) # Se obtienen los movimientos posibles

    def get_rook_moves(self, x, y, start_board, end_board): # Torre
        return self.get_sliding_moves(x, y, start_board, end_board, directions=[(1, 0), (0, 1), (-1, 0), (0, -1)]) # Se obtienen los movimientos posibles

    def get_queen_moves(self, x, y, start_board, end_board): # Reina
        return self.get_sliding_moves(x, y, start_board, end_board, directions=[
            (1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1) # Se obtienen los movimientos posibles
        ])

    def get_king_moves(self, x, y, start_board, end_board): # Rey
        moves = []
        target_board = self.boards[end_board] # Tablero objetivo
        king_moves = [
            (1, 0), (0, 1), (-1, 0), (0, -1), # Movimientos en cruz
            (1, 1), (1, -1), (-1, 1), (-1, -1) # Movimientos en diagonal
        ]

        for dx, dy in king_moves: # Se recorren los movimientos del rey
            nx, ny = x + dx, y + dy # Se calcula la nueva posición
            if 0 <= nx < 8 and 0 <= ny < 8: # Si la nueva posición esta dentro del limite del tablero
                target_piece = target_board[nx][ny] # Se toma la pieza en la nueva posición
                if not target_piece or target_piece[0] != self.current_turn: # Si no hay pieza o la pieza no es del mismo color
                    moves.append((nx, ny)) # Se agrega la casilla a los movimientos posibles

        return moves # Se retornan los movimientos posibles

    def get_sliding_moves(self, x, y, start_board, end_board, directions): # Movimientos deslizantes
        moves = [] # Lista de movimientos
        target_board = self.boards[end_board] # Tablero objetivo

        for dx, dy in directions: # Se recorren las direcciones
            nx, ny = x + dx, y + dy # Se calcula la nueva posición
            while 0 <= nx < 8 and 0 <= ny < 8: # Mientras la nueva posición este dentro del limite del tablero
                target_piece = target_board[nx][ny] # Se toma la pieza en la nueva posición
                if target_piece: # Si hay una pieza
                    if target_piece[0] != self.current_turn: # Si la pieza no es del mismo color
                        moves.append((nx, ny)) # Se agrega la casilla a los movimientos posibles
                    break # Se rompe el ciclo
                moves.append((nx, ny)) # Se agrega la casilla a los movimientos posibles
                nx += dx # Se actualiza la posición en x
                ny += dy # Se actualiza la posición en y

        return moves

    def move_piece(self, start, end, start_board, end_board): # Mover pieza
        sx, sy = start # Posición inicial
        ex, ey = end # Posición final

        piece = self.boards[start_board][sx][sy] # Se obtiene la pieza

        if not piece: # Si no hay pieza
            return False # Se retorna falso

        if end not in self.get_legal_moves(start, start_board, end_board): # Si la casilla final no esta en los movimientos posibles
            return False # Se retorna falso

        # Realizar movimiento
        self.boards[start_board][sx][sy] = None # Se limpia la casilla inicial
        self.boards[end_board][ex][ey] = piece # Se coloca la pieza en la casilla final

        # Cambiar turno
        self.current_turn = "black" if self.current_turn == "white" else "white" # Se cambia el turno
        return True # Se retorna verdadero

    def is_king_in_check(self, color): # ¿El rey esta en jaque?
        king_position = None # Posición del rey
        king_board = None # Tablero del rey

        for board_key in ["A", "B"]: # Se recorren los tableros
            for x, row in enumerate(self.boards[board_key]): # Se recorren las filas
                for y, cell in enumerate(row): # Se recorren las columnas
                    if cell == (color, "K"): # Si la pieza es el rey
                        king_position = (x, y) # Se guarda la posición del rey
                        king_board = board_key # Se guarda el tablero del rey
                        break # Se rompe el ciclo

        if not king_position: # Si no se encontro el rey
            return False # Se retorna falso

        opponent_color = "black" if color == "white" else "white" # Se obtiene el color del oponente
        for board_key in ["A", "B"]: # Se recorren los tableros y el board_key es el tablero 
            for x, row in enumerate(self.boards[board_key]): # Se recorren las filas
                for y, cell in enumerate(row): # Se recorren las columnas
                    if cell and cell[0] == opponent_color: # Si hay una pieza y es del oponente
                        moves = self.get_legal_moves((x, y), board_key, king_board) # Se obtienen los movimientos posibles
                        if king_position in moves: # Si la posición del rey esta en los movimientos posibles
                            return True # Se retorna verdadero

        return False

    def is_checkmate(self, color): # ¿Jaque mate?
        for board_key in ["A", "B"]: # Se recorren los tableros
            for x in range(8): # Se recorren las filas
                for y in range(8): # Se recorren las columnas
                    piece = self.boards[board_key][x][y] # Se obtiene la pieza
                    if piece and piece[0] == color: # Si hay una pieza y es del color
                        for end_board in ["A", "B"]: # Se recorren los tableros
                            moves = self.get_legal_moves((x, y), board_key, end_board) # Se obtienen los movimientos posibles
                            for move in moves: # Se recorren los movimientos posibles
                                cloned_game = self.clone_game() # Se clona el juego
                                cloned_game.move_piece((x, y), move, board_key, end_board) # Se realiza el movimiento
                                if not cloned_game.is_king_in_check(color): # Si el rey no esta en jaque
                                    return False # Se retorna falso

        return True # Se retorna verdadero

    def clone_game(self): # Clonar juego
        import copy # Se importa la libreria copy
        return copy.deepcopy(self) # Se clona el juego

    def is_game_over(self): # ¿Juego terminado?
        if self.is_checkmate("white"): # Si las blancas estan en jaque mate
            print("Black wins by checkmate!") # Se imprime que las negras ganan por jaque mate
            return True
        if self.is_checkmate("black"): # Si las negras estan en jaque mate
            print("White wins by checkmate!") # Se imprime que las blancas ganan por jaque mate
            return True
        return False



class AliceAI:
    def __init__(self, depth=2): # Profundidad de busqueda
        self.depth = depth # Profundidad de busqueda (2)

    def evaluate_board(self, game): # Evaluar tablero
        piece_values = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 1000} # Valor de las piezas
        central_positions = {
            "A": set((x, y) for x in range(3, 5) for y in range(3, 5)), # se setean las posiciones centrales del tablero A para las piezas
            "B": set((x, y) for x in range(3, 5) for y in range(3, 5)), # se setean las posiciones centrales del tablero B para las piezas
        }

        total_mine = 0 # Total de piezas del jugador
        total_opponent = 0 # Total de piezas del oponente
        center_mine = 0 # Total de piezas centrales del jugador
        center_opponent = 0 # Total de piezas centrales del oponente

        for board_key in game.boards: # Se recorren los tableros del juego 
            for x, row in enumerate(game.boards[board_key]): # Accede a la matriz que representa el tablero actual.
                for y, cell in enumerate(row):  # Si contiene una pieza, será algo como ("white", "Knight"); si está vacía, será None
                    if cell:
                        color, piece = cell
                        value = piece_values.get(piece, 0)
                        
                        if color == "white":
                            total_mine += value # Suma el valor de las piezas propias.
                            if (x, y) in central_positions[board_key]: # Si la pieza esta en una posición central
                                center_mine += value # Suma el valor de las piezas centrales.
                        else:
                            total_opponent += value # Suma el valor de las piezas del oponente.
                            if (x, y) in central_positions[board_key]: # Si la pieza esta en una posición central
                                center_opponent += value # Suma el valor de las piezas centrales.

        return (total_mine - total_opponent) + (center_mine - center_opponent) # Retorna la diferencia de las piezas propias y las del oponente (Heurística)

    def get_all_moves(self, game, color): # Obtener todos los movimientos posibles
        moves = []
        for board_key in ["A", "B"]: # Se recorren los tableros
            for x in range(8): # Se recorren las filas en el limite del tablero
                for y in range(8): # Se recorren las columnas en el limite del tablero
                    piece = game.boards[board_key][x][y] # Se obtiene la pieza en la posición actual y se tiene en cuenta el tablero
                    if piece and piece[0] == color: # Si hay una pieza y es del color
                        target_board = "A" if board_key == "B" else "B" # Se obtiene el tablero objetivo
                        legal_moves = game.get_legal_moves((x, y), board_key, target_board) # Se obtienen los movimientos posibles
                        moves.extend([(x, y, move, board_key, target_board) for move in legal_moves]) # Se agregan los movimientos posibles
        return moves # Se retornan los movimientos posibles

    def minimax(self, game, depth, maximizing_player): # Algoritmo Minimax
        if depth == 0: # Si la profundidad es 0
            return self.evaluate_board(game), None # Se retorna la evaluación del tablero y ningun movimiento

        best_move = None # Mejor movimiento (ninguno)
        if maximizing_player: # Si es el jugador que maximiza
            max_eval = float('-inf') # Valor de evaluación máximo (-infinito)
            for move in self.get_all_moves(game, "white"): # Se recorren los movimientos posibles de las blancas
                start_x, start_y, end, start_board, end_board = move # Se obtienen los datos del movimiento (posición inicial, posición final, tablero A, tablero B)
                cloned_game = copy.deepcopy(game) # Se clona el juego
                cloned_game.move_piece((start_x, start_y), end, start_board, end_board) # Se realiza el movimiento en el juego clonado
                eval, _ = self.minimax(cloned_game, depth - 1, False) # Se obtiene la evaluación del tablero y se le resta 1 a la profundidad
                if eval > max_eval: # Si la evaluación es mayor al valor máximo
                    max_eval = eval # Se actualiza el valor máximo
                    best_move = move # Se actualiza el mejor movimiento
            return max_eval, best_move # Se retorna el valor máximo y el mejor movimiento
        else: # Si es el jugador que minimiza
            min_eval = float('inf') # Valor de evaluación mínimo (infinito)
            for move in self.get_all_moves(game, "black"): # Se recorren los movimientos posibles de las negras
                start_x, start_y, end, start_board, end_board = move # Se obtienen los datos del movimiento (posición inicial, posición final, tablero A, tablero B)
                cloned_game = copy.deepcopy(game) # Se clona el juego
                cloned_game.move_piece((start_x, start_y), end, start_board, end_board) # Se realiza el movimiento en el juego clonado
                eval, _ = self.minimax(cloned_game, depth - 1, True) # Se obtiene la evaluación del tablero  y se le resta 1 a la profundidad
                if eval < min_eval: # Si la evaluación es menor al valor mínimo
                    min_eval = eval # Se actualiza el valor mínimo
                    best_move = move # Se actualiza el mejor movimiento
            return min_eval, best_move # Se retorna el valor mínimo y el mejor movimiento

#INTERFAZ GRÁFICA
class AliceChessGUI:  # Se define la clase para la interfaz gráfica del ajedrez de Alicia
    def __init__(self, root):  # Constructor de la clase, se pasa el objeto root de Tkinter
        self.root = root  # Asigna la ventana principal de la interfaz
        self.game = AliceChess()  # Crea una instancia del juego de ajedrez
        self.ai = AliceAI(depth=2)  # Crea una instancia de la IA con una profundidad de búsqueda de 2
        self.selected_piece = None  # Inicializa la pieza seleccionada
        self.selected_board = None  # Inicializa el tablero seleccionado

        # Diccionario que contiene los frames de los tableros A y B
        self.board_frames = {
            "A": tk.Frame(root),
            "B": tk.Frame(root)
        }

        # Configurar tableros
        for board_key in self.board_frames:  # Recorre los tableros A y B
            self.board_frames[board_key].grid(row=0, column=0 if board_key == "A" else 1, padx=10, pady=10)  
            # Asigna los tableros en la misma fila pero en columnas diferentes (A en 0, B en 1)

        # Diccionario para almacenar las celdas de cada tablero
        self.cells = {
            "A": {},
            "B": {}
        }

        # Crear las celdas de cada tablero (8x8)
        for board_key in self.board_frames:
            for x in range(8):  # Recorre las filas
                for y in range(8):  # Recorre las columnas
                    cell = tk.Label(self.board_frames[board_key], width=4, height=2, bg=self.get_cell_color(x, y), relief="raised")  
                    # Crea una celda con color dependiendo de la posición
                    cell.grid(row=x, column=y)  # Coloca la celda en la cuadrícula
                    cell.bind("<Button-1>", lambda e, bx=x, by=y, board=board_key: self.cell_clicked(bx, by, board))  
                    # Asocia un evento para hacer clic en la celda
                    self.cells[board_key][(x, y)] = cell  # Almacena la celda en el diccionario

        self.update_board()  # Actualiza la visualización del tablero

    def get_cell_color(self, x, y):  # Determina el color de la celda
        return "#F0D9B5" if (x + y) % 2 == 0 else "#B58863"  # Si la suma de las coordenadas es par, es blanco, sino es marrón

    def update_board(self):  # Actualiza el tablero visualmente
        piece_symbols = {
            "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔"  # Diccionario con los símbolos de las piezas
        }

        for board_key, board in self.game.boards.items():  # Recorre los tableros del juego
            for x, row in enumerate(board):  # Recorre las filas del tablero
                for y, cell in enumerate(row):  # Recorre las columnas
                    if cell:  # Si hay una pieza en la celda
                        color, piece = cell  # Obtiene el color y tipo de pieza
                        symbol = piece_symbols[piece]  # Obtiene el símbolo de la pieza
                        self.cells[board_key][(x, y)].config(text=symbol, fg="white" if color == "white" else "black")  # Actualiza la celda
                    else:  # Si no hay una pieza
                        self.cells[board_key][(x, y)].config(text="")  # Limpia la celda

    def show_valid_moves(self, valid_moves, board):  # Muestra los movimientos válidos en el tablero
        for x, y in valid_moves:  # Recorre las posiciones de los movimientos válidos
            self.cells[board][(x, y)].config(bg="#90EE90")  # Cambia el color de la celda a verde claro

    def reset_highlights(self):  # Restablece los resaltados de las celdas
        for board_key in self.cells:  # Recorre ambos tableros
            for x, y in self.cells[board_key]:  # Recorre todas las celdas
                self.cells[board_key][(x, y)].config(bg=self.get_cell_color(x, y))  # Restaura el color original de la celda

    def cell_clicked(self, x, y, board):  # Función que se llama al hacer clic en una celda
        self.reset_highlights()  # Restaura el color original de las celdas
        cell = self.game.boards[board][x][y]  # Obtiene la pieza en la celda seleccionada

        if self.selected_piece and (self.selected_board == board):  # Si ya hay una pieza seleccionada en el tablero actual
            # Intenta mover la pieza seleccionada
            target_board = "A" if board == "B" else "B"  # Determina el tablero objetivo (opuesto al actual)
            if (x, y) in self.game.get_legal_moves(self.selected_piece, board, target_board):  
                # Si el movimiento es válido
                self.game.move_piece(self.selected_piece, (x, y), self.selected_board, target_board)  # Mueve la pieza
                self.selected_piece = None  # Resetea la pieza seleccionada
                self.selected_board = None  # Resetea el tablero seleccionado
                self.update_board()  # Actualiza el tablero
                self.check_ai_turn()  # Verifica si es el turno de la IA
                return

        # Si se selecciona una pieza propia
        if cell and cell[0] == self.game.current_turn:  
            self.selected_piece = (x, y)  # Establece la pieza seleccionada
            self.selected_board = board  # Establece el tablero seleccionado
            valid_moves = self.game.get_legal_moves((x, y), board, "A" if board == "B" else "B")  # Obtiene los movimientos válidos
            self.show_valid_moves(valid_moves, "A" if board == "B" else "B")  # Muestra los movimientos válidos

    def check_ai_turn(self):  # Verifica si es el turno de la IA
        if self.game.current_turn == "black":  # Si es el turno de la IA (negras)
            self.root.after(500, self.ai_move)  # Espera 500ms y luego realiza el movimiento de la IA

    def ai_move(self):  # Realiza el movimiento de la IA
        _, best_move = self.ai.minimax(self.game, self.ai.depth, maximizing_player=False)  # Obtiene el mejor movimiento de la IA
        if best_move:  # Si hay un movimiento válido
            start_x, start_y, end, start_board, end_board = best_move  # Descompone el movimiento
            self.game.move_piece((start_x, start_y), end, start_board, end_board)  # Mueve la pieza de la IA
            self.update_board()  # Actualiza el tablero

if __name__ == "__main__":  # Ejecuta el siguiente bloque solo si este archivo es ejecutado directamente
    root = tk.Tk()  # Crea la ventana principal de Tkinter
    root.title("Alice Chess GUI")  # Establece el título de la ventana
    gui = AliceChessGUI(root)  # Crea la instancia de la interfaz gráfica
    root.mainloop()  # Inicia el bucle principal de Tkinter
