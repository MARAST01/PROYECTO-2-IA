# Representación del tablero inicial de ajedrez estándar
# Las filas están enumeradas de 1 a 8 (de abajo hacia arriba, como se hace en notación estándar).
# Las columnas están etiquetadas de 'a' a 'h' (de izquierda a derecha).
# Un tablero vacío adyacente estará representado por ' ' en cada celda.

Tablero = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 8
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 7
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 6
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 5
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 4
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 3
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 2
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']   # 1
]

# Leyenda:
# r, n, b, q, k: piezas negras (rook, knight, bishop, queen, king)
# R, N, B, Q, K: piezas blancas
# p: peón negro, P: peón blanco
# ' ': casilla vacía

PIECE_VALUES = {
    'p': 1, 'P': 1,
    'n': 3, 'N': 3,
    'b': 3, 'B': 3,
    'r': 5, 'R': 5,
    'q': 9, 'Q': 9,
    'k': 0, 'K': 0
}

CENTER_SQUARES = {(3, 3), (3, 4), (4, 3), (4, 4)}


def heuristic(board, taken_pieces):
    """Calcula la heurística del tablero."""
    my_total = 0
    op_total = 0
    my_center = 0
    op_center = 0

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell in PIECE_VALUES:
                value = PIECE_VALUES[cell]
                if cell.isupper():  # Mis piezas (mayúsculas)
                    my_total += value
                    if (i, j) in CENTER_SQUARES:
                        my_center += value
                else:  # Piezas del oponente (minúsculas)
                    op_total += value
                    if (i, j) in CENTER_SQUARES:
                        op_center += value

    return my_total - op_total + my_center - op_center


def generate_moves(board, is_maximizing):
    """Genera todos los movimientos posibles para el jugador dado."""
    moves = []

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if (is_maximizing and cell.isupper()) or (not is_maximizing and cell.islower()):
                # Ejemplo: simular que cada pieza puede moverse a una casilla adyacente vacía
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 8 and 0 <= nj < 8 and board[ni][nj] == ' ':
                        moves.append(((i, j), (ni, nj)))

    return moves


def apply_move(board, move, taken_pieces):
    """Aplica un movimiento al tablero y actualiza las piezas tomadas si es necesario."""
    (from_i, from_j), (to_i, to_j) = move
    new_board = [row[:] for row in board]  # Copia profunda del tablero
    piece = new_board[from_i][from_j]
    new_board[from_i][from_j] = ' '

    # Si se toma una pieza, agregarla a la lista de fichas tomadas
    if new_board[to_i][to_j] != ' ':
        taken_pieces.append(new_board[to_i][to_j])

    new_board[to_i][to_j] = piece
    return new_board, taken_pieces


def minimax(board, depth, alpha, beta, is_maximizing, taken_pieces):
    """Implementa el algoritmo minimax con poda alfa-beta."""
    if depth == 0 or is_terminal(board):
        return heuristic(board, taken_pieces), board

    if is_maximizing:
        max_eval = float('-inf')
        best_board = None
        for move in generate_moves(board, is_maximizing):
            new_board, new_taken = apply_move(board, move, taken_pieces[:])
            eval, _ = minimax(new_board, depth - 1, alpha, beta, False, new_taken)
            if eval > max_eval:
                max_eval = eval
                best_board = new_board
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_board
    else:
        min_eval = float('inf')
        best_board = None
        for move in generate_moves(board, is_maximizing):
            new_board, new_taken = apply_move(board, move, taken_pieces[:])
            eval, _ = minimax(new_board, depth - 1, alpha, beta, True, new_taken)
            if eval < min_eval:
                min_eval = eval
                best_board = new_board
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_board


def imperfect_decision(board, taken_pieces, depth):
    """Toma una decisión imperfecta basada en el algoritmo minimax con una profundidad limitada."""
    _, best_board = minimax(board, depth, float('-inf'), float('inf'), True, taken_pieces)
    return best_board


def is_terminal(board):
    """Determina si el tablero está en un estado terminal."""
    # Un estado terminal es cuando uno de los reyes ha sido capturado
    has_white_king = any('K' in row for row in board)
    has_black_king = any('k' in row for row in board)
    return not (has_white_king and has_black_king)


def print_board(board):
    """Imprime el tablero en una representación visual para facilitar la lectura."""
    for row in board:
        print(' '.join(row))

# Ejemplo de uso
print("Tablero inicial:")
print_board(Tablero)

taken = []
Tablero = imperfect_decision(Tablero, taken, 2)  # Profundidad de 2 niveles
print("\nTablero después de un movimiento minimax:")
print_board(Tablero)
