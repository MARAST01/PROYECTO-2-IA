class Tablero:
    def __init__(self):
        """Inicializa el tablero con la configuración estándar."""
        self.tablero = self.crear_tablero_inicial()
        self.dimension = 8  # Dimensiones del tablero (8x8)

    def crear_tablero_inicial(self):
        """Crea la configuración inicial de un tablero de ajedrez."""
        tablero = [
            ["t", "c", "a", "d", "r", "a", "c", "t"],  # Fila 0: piezas negras
            ["p", "p", "p", "p", "p", "p", "p", "p"],  # Fila 1: peones negros
            [None] * 8,                               # Filas 2 a 5: vacías
            [None] * 8,
            [None] * 8,
            [None] * 8,
            ["P", "P", "P", "P", "P", "P", "P", "P"],  # Fila 6: peones blancos
            ["T", "C", "A", "D", "R", "A", "C", "T"],  # Fila 7: piezas blancas
        ]
        return tablero

    def mostrar_tablero(self):
        """Imprime el tablero en formato legible para depuración."""
        for fila in self.tablero:
            print(["--" if casilla is None else casilla for casilla in fila])

    def mover_pieza(self, origen, destino):
        """Mueve una pieza de una posición de origen a una posición de destino."""
        pieza = self.tablero[origen[0]][origen[1]]
        if pieza is None:
            raise ValueError("No hay pieza en la posición de origen.")
        if not self.es_movimiento_valido(origen, destino):
            raise ValueError("El movimiento no es válido.")
        self.tablero[origen[0]][origen[1]] = None
        self.tablero[destino[0]][destino[1]] = pieza

    def es_movimiento_valido(self, origen, destino):
        """Comprueba si un movimiento es válido según las reglas básicas del ajedrez."""
        pieza = self.tablero[origen[0]][origen[1]]
        if pieza is None:
            return False
        # Lógica específica para cada tipo de pieza.
        tipo_pieza = pieza.lower()  # Normalizamos para piezas blancas/negras
        if tipo_pieza == "p":
            return self._es_movimiento_peon(origen, destino, pieza)
        elif tipo_pieza == "t":
            return self._es_movimiento_torre(origen, destino)
        elif tipo_pieza == "c":
            return self._es_movimiento_caballo(origen, destino)
        elif tipo_pieza == "a":
            return self._es_movimiento_alfil(origen, destino)
        elif tipo_pieza == "d":
            return self._es_movimiento_dama(origen, destino)
        elif tipo_pieza == "r":
            return self._es_movimiento_rey(origen, destino)
        return False

    def _es_movimiento_peon(self, origen, destino, pieza):
        """Valida movimientos de un peón."""
        direccion = -1 if pieza.isupper() else 1
        fila_origen, columna_origen = origen
        fila_destino, columna_destino = destino

        # Movimiento hacia adelante
        if columna_origen == columna_destino:
            if fila_destino == fila_origen + direccion and self.tablero[fila_destino][columna_destino] is None:
                return True
            if fila_destino == fila_origen + 2 * direccion and fila_origen in (1, 6) and self.tablero[fila_destino][columna_destino] is None:
                return True

        # Movimiento de captura
        if abs(columna_origen - columna_destino) == 1 and fila_destino == fila_origen + direccion:
            return self.tablero[fila_destino][columna_destino] is not None

        return False

    def _es_movimiento_torre(self, origen, destino):
        """Valida movimientos de una torre."""
        fila_origen, columna_origen = origen
        fila_destino, columna_destino = destino

        # Movimiento en línea recta (horizontal o vertical)
        if fila_origen == fila_destino or columna_origen == columna_destino:
            return self._camino_libre(origen, destino)
        return False

    def _es_movimiento_caballo(self, origen, destino):
        """Valida movimientos de un caballo."""
        fila_origen, columna_origen = origen
        fila_destino, columna_destino = destino

        # Movimiento en forma de L
        return (abs(fila_origen - fila_destino), abs(columna_origen - columna_destino)) in [(2, 1), (1, 2)]

    def _es_movimiento_alfil(self, origen, destino):
        """Valida movimientos de un alfil."""
        fila_origen, columna_origen = origen
        fila_destino, columna_destino = destino

        # Movimiento en diagonal
        if abs(fila_origen - fila_destino) == abs(columna_origen - columna_destino):
            return self._camino_libre(origen, destino)
        return False

    def _es_movimiento_dama(self, origen, destino):
        """Valida movimientos de una dama."""
        # Combina movimientos de torre y alfil
        return self._es_movimiento_torre(origen, destino) or self._es_movimiento_alfil(origen, destino)

    def _es_movimiento_rey(self, origen, destino):
        """Valida movimientos de un rey."""
        fila_origen, columna_origen = origen
        fila_destino, columna_destino = destino

        # Movimiento de una casilla en cualquier dirección
        return max(abs(fila_origen - fila_destino), abs(columna_origen - columna_destino)) == 1

    def _camino_libre(self, origen, destino):
        """Comprueba si no hay piezas bloqueando el camino entre dos posiciones."""
        fila_origen, columna_origen = origen
        fila_destino, columna_destino = destino

        # Movimiento horizontal
        if fila_origen == fila_destino:
            paso = 1 if columna_origen < columna_destino else -1
            for columna in range(columna_origen + paso, columna_destino, paso):
                if self.tablero[fila_origen][columna] is not None:
                    return False

        # Movimiento vertical
        elif columna_origen == columna_destino:
            paso = 1 if fila_origen < fila_destino else -1
            for fila in range(fila_origen + paso, fila_destino, paso):
                if self.tablero[fila][columna_origen] is not None:
                    return False

        # Movimiento diagonal
        else:
            paso_fila = 1 if fila_origen < fila_destino else -1
            paso_columna = 1 if columna_origen < columna_destino else -1
            for i in range(1, abs(fila_origen - fila_destino)):
                if self.tablero[fila_origen + i * paso_fila][columna_origen + i * paso_columna] is not None:
                    return False

        return True
