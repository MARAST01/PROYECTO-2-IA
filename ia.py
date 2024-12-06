class IA:
    def __init__(self, profundidad):
        self.profundidad = profundidad

    def mejor_movimiento(self, tablero):
        # Utiliza Minimax con poda alfa-beta.
        pass

    def minimax(self, tablero, profundidad, alfa, beta, maximizando):
        if profundidad == 0 or self.es_terminado(tablero):
            return self.evaluar_tablero(tablero)
        # Resto de la implementación aquí.
