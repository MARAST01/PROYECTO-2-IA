from tablero1 import Tablero

def main():
    tablero = Tablero()
    tablero.mostrar_tablero()
    print("\nMover peón blanco de (6, 4) a (4, 4):")
    tablero.mover_pieza((6, 4), (4, 4))
    tablero.mostrar_tablero()

if __name__ == "__main__":
    main()