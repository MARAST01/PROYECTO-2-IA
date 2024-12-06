import pygame

class GUI:
    def __init__(self, juego):
        self.juego = juego
        self.pantalla = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Ajedrez Pierde-Gana")

    def iniciar(self):
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
            self.pantalla.fill((255, 255, 255))  # Fondo blanco
            # Dibujar el tablero aquí
            pygame.display.flip()
        pygame.quit()
