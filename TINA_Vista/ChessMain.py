import pygame as p  # Importamos la librería pygame como p
import ChessMotor as CM  # Importamos la clase ChessMotor del archivo ChessMotor.py

WIDTH = HEIGHT = 512  # Ancho y alto de cada tablero
DIMENSION = 8  # Dimensión del tablero 8x8
SQ_SIZE = HEIGHT // DIMENSION  # Tamaño de la casilla
MAX_FPS = 15  # Para animaciones
IMAGES = {}  # Diccionario para cargar imágenes
MARGIN = 50  # Margen entre los tableros
TOTAL_WIDTH = WIDTH * 2 + MARGIN  # Ancho total con margen

# Inicializamos un diccionario global de imágenes. Esto se llamará exactamente una vez en el main.
def cargarImagenes():
    piezas = ['Peon_N', 'Torre_N', 'Caballo_N', 'Alfil_N', 'Reina_N', 'Rey_N',
              'Peon_B', 'Torre_B', 'Caballo_B', 'Alfil_B', 'Reina_B', 'Rey_B']
    for pieza in piezas:
        IMAGES[pieza] = p.transform.scale(
            p.image.load("Ajedrez/images/" + pieza + ".png"), (SQ_SIZE, SQ_SIZE))  # Cargamos las imágenes de las piezas

# El main será responsable de manejar la entrada del usuario y actualizar la interfaz
def main():
    p.init()  # Inicializamos pygame
    Pantalla = p.display.set_mode((TOTAL_WIDTH, HEIGHT))  # Creamos la pantalla con espacio para dos tableros
    reloj = p.time.Clock()  # Creamos un reloj
    Pantalla.fill(p.Color("white"))  # Llenamos la pantalla de blanco
    EstadoJuegoA = CM.estadoJuego()  # Tablero A
    EstadoJuegoB = estado_vacio()  # Tablero B vacío
    cargarImagenes()  # Cargamos las imágenes solo una vez después del while loop
    corriendo = True
    seleccionado = None  # Piezas seleccionadas
    tablero_actual = "A"  # Empezamos con el tablero A

    while corriendo:
        for e in p.event.get():
            if e.type == p.QUIT:
                corriendo = False
            elif e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                if pos[0] < WIDTH:
                    tablero_actual = "A"
                    manejar_click(pos, EstadoJuegoA, seleccionado)
                elif pos[0] > WIDTH + MARGIN:
                    tablero_actual = "B"
                    manejar_click((pos[0] - WIDTH - MARGIN, pos[1]), EstadoJuegoB, seleccionado)
        
        DibujarEstadoJuego(Pantalla, EstadoJuegoA, EstadoJuegoB)
        reloj.tick(MAX_FPS)
        p.display.flip()

def estado_vacio():
    """Crea un tablero vacío sin piezas."""
    class EstadoJuegoVacio:
        def __init__(self):
            self.tablero = [["--" for _ in range(DIMENSION)] for _ in range(DIMENSION)]
    return EstadoJuegoVacio()

def manejar_click(pos, EstadoJuego, seleccionado):
    fila = pos[1] // SQ_SIZE
    columna = pos[0] // SQ_SIZE
    if seleccionado is None:
        seleccionado = (fila, columna)
    else:
        mover_pieza(EstadoJuego, seleccionado, (fila, columna))
        seleccionado = None

def mover_pieza(EstadoJuego, origen, destino):
    # Movimiento simplificado: actualiza el tablero y "salta" la pieza al otro tablero
    pieza = EstadoJuego.tablero[origen[0]][origen[1]]
    EstadoJuego.tablero[origen[0]][origen[1]] = "--"
    EstadoJuego.tablero[destino[0]][destino[1]] = pieza

def DibujarEstadoJuego(Pantalla, EstadoJuegoA, EstadoJuegoB):
    # Dibujamos ambos tableros
    DibujarTablero(Pantalla, 0, EstadoJuegoA)  # Tablero A
    DibujarTablero(Pantalla, WIDTH + MARGIN, EstadoJuegoB)  # Tablero B

def DibujarTablero(Pantalla, offset, EstadoJuego):
    colores = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colores[((r + c) % 2)]
            p.draw.rect(Pantalla, color, p.Rect(c * SQ_SIZE + offset, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            pieza = EstadoJuego.tablero[r][c]
            if pieza != "--":
                Pantalla.blit(IMAGES[pieza], p.Rect(c * SQ_SIZE + offset, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()  # Llamamos al main