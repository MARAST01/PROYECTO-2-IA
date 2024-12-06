class Tablero:
    def __init__(self):
        # Inicializar los dos tableros como matrices 8x8
        self.tablero1 = [
            ["Tn", "Cn", "An", "Qn", "Kn", "An", "Cn", "Tn"],
            ["Pn", "Pn", "Pn", "Pn", "Pn", "Pn", "Pn", "Pn"],
            ["z", "z", "z", "z", "z", "z", "z", "z"],
            ["z", "z", "z", "z", "z", "z", "z", "z"],
            ["z", "z", "z", "z", "z", "z", "z", "z"],
            ["z", "z", "z", "z", "z", "z", "z", "z"],
            ["Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb"],
            ["Tb", "Cb", "Ab", "Qb", "Kb", "Ab", "Cb", "Tb"]
        ]

        self.tablero2 = [
            ["Tn", "Cn", "An", "Qn", "Kn", "An", "Cn", "Tn"],
            ["Pn", "Pn", "Pn", "Pn", "Pn", "Pn", "Pn", "Pn"],
            ["z", "z", "z", "z", "z", "z", "z", "z"],
            ["z", "z", "z", "z", "z", "z", "z", "z"],
            ["z", "z", "z", "z", "z", "z", "z", "z"],
            ["z", "z", "z", "z", "z", "z", "z", "z"],
            ["Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb"],
            ["Tb", "Cb", "Ab", "Qb", "Kb", "Ab", "Cb", "Tb"]
        ]

        # Lista para fichas tomadas de ambos equipos
        self.fichas_tomadas = []

    def mostrar_tableros(self):
        """Muestra ambos tableros en consola."""
        print("Tablero 1:")
        for fila in self.tablero1:
            print(" ".join(fila))
        print("\nTablero 2:")
        for fila in self.tablero2:
            print(" ".join(fila))
            

# Ejemplo de uso
if __name__ == "__main__":
    tablero = Tablero()
    tablero.mostrar_tableros()
    tablero.tomar_ficha("An")  # Simula tomar un alfil negro
    tablero.mostrar_fichas_tomadas()
