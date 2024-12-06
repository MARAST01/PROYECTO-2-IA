from tablero1 import Tablero

class Juego:
    def __init__(self):
        self.tableros = [Tablero(), Tablero()]  # Dos tableros paralelos
        self.turno_actual = "Jugador"

    def cambiar_turno(self):
        self.turno_actual = "IA" if self.turno_actual == "Jugador" else "Jugador"

    def realizar_movimiento(self, origen, destino, tablero_id):
        tablero = self.tableros[tablero_id]
        tablero.mover_pieza(origen, destino)
        self.cambiar_turno()
