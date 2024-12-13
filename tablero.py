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

def print_board(board):
    """Imprime el tablero en una representación visual para facilitar la lectura."""
    for row in board:
        print(' '.join(row))

# Imprimir el estado inicial del tablero con el tablero vacío
print_board(Tablero)