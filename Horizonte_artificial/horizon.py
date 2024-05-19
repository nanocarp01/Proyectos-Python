import pygame

# Definir colores
SKY_BLUE = (135, 206, 235)  # Celeste
BROWN = (139, 69, 19)  # Marrón
BLACK = (0, 0, 0)

def draw_horizon(surface, width, height):
    # Dibujar cielo
    pygame.draw.rect(surface, SKY_BLUE, (0, 0, width, height // 2))
    # Dibujar tierra
    pygame.draw.rect(surface, BROWN, (0, height // 2, width, height // 2))
    # Dibujar línea horizontal del horizonte
    pygame.draw.line(surface, BLACK, (0, height // 2), (width, height // 2), 2)
