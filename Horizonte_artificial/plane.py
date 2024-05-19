import pygame


#color rojo
RED = (255,0,0)

def draw_plane(surface, width, height,x,y):
    #dibujar el avion der
    pygame.draw.line(surface, RED, (width // 2 + 50,  y), (width - 150, y ), 4)
    #dibujar el avion izq
    pygame.draw.line(surface, RED, (width // 2 - 50, y), (width - 650,  y  ), 4)
    #dibujar un punto en el centro
    pygame.draw.circle(surface, RED, (width // 2, y), 5, 0)