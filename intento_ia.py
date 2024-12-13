import copy
import math

def evaluar_tablero(tablero_activo, tablero_pasivo):
    """Evalúa el tablero para la heurística."""
    valores_piezas = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000,
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1000
    }
    puntuacion = 0
    for fila in tablero_activo:
        for pieza in fila:
            puntuacion += valores_piezas.get(pieza, 0)
    for fila in tablero_pasivo:
        for pieza in fila:
            puntuacion += valores_piezas.get(pieza, 0) / 2  # Menor peso para piezas en tablero pasivo
    return puntuacion

def generar_movimientos(tablero, tablero_otro):
    """Genera todos los movimientos legales para el tablero actual."""
    movimientos = []
    for fila in range(8):
        for col in range(8):
            pieza = tablero[fila][col]
            if pieza != ' ':  # Solo consideramos casillas ocupadas
                movimientos += generar_movimientos_pieza(tablero, tablero_otro, fila, col, pieza)
    return movimientos


def generar_movimientos_pieza(tablero, tablero_otro, fila, col, pieza):
    """Genera movimientos legales para una pieza específica, evitando duplicados en tableros."""
    movimientos = []
    direcciones = {
        'P': [(1, 0), (1, 1), (1, -1)],  # Peón blanco: avance y captura
        'p': [(-1, 0), (-1, 1), (-1, -1)],  # Peón negro: avance y captura
        'N': [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)],  # Caballo
        'B': [(1, 1), (1, -1), (-1, 1), (-1, -1)],  # Alfil
        'R': [(0, 1), (0, -1), (1, 0), (-1, 0)],  # Torre
        'Q': [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)],  # Dama
        'K': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Rey
    }

    if pieza.upper() in direcciones:
        for d in direcciones[pieza.upper()]:
            nuevo_fila, nuevo_col = fila, col

            while True:
                nuevo_fila += d[0]
                nuevo_col += d[1]

                if not (0 <= nuevo_fila < 8 and 0 <= nuevo_col < 8):
                    break  # Salimos si nos salimos del tablero

                casilla_destino = tablero[nuevo_fila][nuevo_col]

                if pieza.upper() in ['N', 'K'] or pieza.lower() == 'p':
                    # Caballo, rey y peones no se mueven en líneas largas
                    if casilla_destino == ' ' or casilla_destino.islower() if pieza.isupper() else casilla_destino.isupper():
                        generar_estado_movimientos(movimientos, tablero, tablero_otro, fila, col, nuevo_fila, nuevo_col, pieza)
                    break

                if casilla_destino == ' ':
                    # Movimiento válido para piezas de rango largo
                    generar_estado_movimientos(movimientos, tablero, tablero_otro, fila, col, nuevo_fila, nuevo_col, pieza)
                elif casilla_destino.islower() if pieza.isupper() else casilla_destino.isupper():
                    # Captura
                    generar_estado_movimientos(movimientos, tablero, tablero_otro, fila, col, nuevo_fila, nuevo_col, pieza)
                    break
                else:
                    break
    return movimientos

def generar_estado_movimientos(movimientos, tablero, tablero_otro, fila, col, nuevo_fila, nuevo_col, pieza):
    """Genera un nuevo estado con teletransportación."""
    # Mover en el tablero activo
    nuevo_tablero = copy.deepcopy(tablero)
    nuevo_tablero_otro = copy.deepcopy(tablero_otro)

    # Actualizar posición en el tablero activo
    nuevo_tablero[fila][col] = ' '
    nuevo_tablero[nuevo_fila][nuevo_col] = pieza

    # Teletransportar al tablero pasivo
    if tablero_otro[nuevo_fila][nuevo_col] == ' ':
        # Limpiar la casilla de origen en el tablero pasivo
        nuevo_tablero_otro[fila][col] = ' '
        # Colocar la pieza en la casilla correspondiente
        nuevo_tablero_otro[nuevo_fila][nuevo_col] = pieza

    # Añadir el estado resultante a los movimientos posibles
    movimientos.append((nuevo_tablero, nuevo_tablero_otro))


def poda_alfa_beta(tablero_activo, tablero_pasivo, profundidad, alfa, beta, maximizando):
    """Algoritmo de decisión con poda alfa-beta."""
    if profundidad == 0:
        return evaluar_tablero(tablero_activo, tablero_pasivo), None

    movimientos = generar_movimientos(tablero_activo, tablero_pasivo)
    mejor_movimiento = None

    if maximizando:
        max_eval = -math.inf
        for nuevo_tablero_activo, nuevo_tablero_pasivo in movimientos:
            evaluacion, _ = poda_alfa_beta(nuevo_tablero_activo, nuevo_tablero_pasivo, profundidad - 1, alfa, beta, False)
            if evaluacion > max_eval:
                max_eval = evaluacion
                mejor_movimiento = (nuevo_tablero_activo, nuevo_tablero_pasivo)
            alfa = max(alfa, evaluacion)
            if beta <= alfa:
                break
        return max_eval, mejor_movimiento
    else:
        min_eval = math.inf
        for nuevo_tablero_activo, nuevo_tablero_pasivo in movimientos:
            evaluacion, _ = poda_alfa_beta(nuevo_tablero_activo, nuevo_tablero_pasivo, profundidad - 1, alfa, beta, True)
            if evaluacion < min_eval:
                min_eval = evaluacion
                mejor_movimiento = (nuevo_tablero_activo, nuevo_tablero_pasivo)
            beta = min(beta, evaluacion)
            if beta <= alfa:
                break
        return min_eval, mejor_movimiento

def decidir_movimiento(tablero_activo, tablero_pasivo, profundidad):
    """Decide el mejor movimiento basado en poda alfa-beta."""
    _, mejor_movimiento = poda_alfa_beta(tablero_activo, tablero_pasivo, profundidad, -math.inf, math.inf, True)
    return mejor_movimiento

def imprimir_tableros(tablero_activo, tablero_pasivo):
    """Imprime los tableros activo y pasivo."""
    print("Tablero Activo:")
    for fila in tablero_activo:
        print(' '.join(fila))
    print("\nTablero Pasivo:")
    for fila in tablero_pasivo:
        print(' '.join(fila))

# Ejemplo de uso
Tablero_activo = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

Tablero_pasivo = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
]

profundidad = 3
nuevo_tablero_activo, nuevo_tablero_pasivo = decidir_movimiento(Tablero_activo, Tablero_pasivo, profundidad)

# Imprimir los tableros resultantes
imprimir_tableros(nuevo_tablero_activo, nuevo_tablero_pasivo)
