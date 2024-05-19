import pygame
import sys
from horizon import draw_horizon
from angle_lines import draw_angle_lines
from plane import draw_plane
import threading
from trackMouse import MouseTracker

# Inicializar pygame
pygame.init()

# Definir dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)

# Definir colores
SKY_BLUE = (135, 206, 235)  # Celeste

# Inicializar la ventana
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Horizonte Artificial")

# Crear una instancia de MouseTracker
tracker = MouseTracker()

# Iniciar el seguimiento del mouse en un hilo separado
tracking_thread = threading.Thread(target=tracker.start_tracking)
tracking_thread.start()


# Ángulo de inclinación inicial
angulo10 = 40
angulo15 = 20
angulo20 = 80

# Loop principal del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener las coordenadas actuales del mouse
    x, y = tracker.get_coordinates()

    # Dibujar
    screen.fill(SKY_BLUE)
    draw_horizon(screen, WIDTH, HEIGHT)
    draw_angle_lines(screen, WIDTH, HEIGHT, angulo10, angulo15, angulo20)
    draw_plane(screen, WIDTH, HEIGHT, x,y)
    pygame.display.flip()

# Cerrar la ventana
pygame.quit()
sys.exit()
