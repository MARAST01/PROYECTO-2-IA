"""
esta clase es responsable para brindar toda la info sobre el estado actual del juego, determinar los movimientos validos del estado actual y también mantendrá un registro de movimientos.
"""
#estructura: Lista de listas
class estadoJuego():
    def __init__(self):
        #tablero es una lista de 8 listas, cada uno de los elementos de la lista tiene 2 characteres
        #el primer caracter representa el color de la pieza (b o w)
        #el segundo caracter representa el tipo de la pieza (R, N, B, Q, K o P)
        #"--" representa un espacio vacio en el tablero
        self.tablero = [
            ["Torre_N", "Caballo_N", "Alfil_N", "Reina_N", "Rey_N", "Alfil_N", "Caballo_N", "Torre_N"],
            ["Peon_N", "Peon_N", "Peon_N", "Peon_N", "Peon_N", "Peon_N", "Peon_N", "Peon_N"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["Peon_B", "Peon_B", "Peon_B", "Peon_B", "Peon_B", "Peon_B", "Peon_B", "Peon_B"],
            ["Torre_B", "Caballo_B", "Alfil_B", "Reina_B", "Rey_B", "Alfil_B", "Caballo_B", "Torre_B"],
        ]
        self.BlancoMueve = True
        self.MovimientosLog = []