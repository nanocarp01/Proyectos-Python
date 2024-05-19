import pygame

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_angle_lines(surface, width, height, angulo10, angulo15, angulo20):
    font = pygame.font.SysFont(None, 24)

    #líneas de ángulo y números 5°
    pygame.draw.line(surface, BLACK, (width // 2 + angulo15, height // 2 - 20), (width // 2 - angulo15, height // 2 - 20), 2)
    pygame.draw.line(surface, WHITE, (width // 2 + angulo15, height // 2 + 20), (width // 2 - angulo15, height // 2 + 20), 2)
    
    # Líneas y números 10°
    pygame.draw.line(surface, BLACK, (width // 2 + angulo10, height // 2 - 40), (width // 2 - angulo10, height // 2 - 40), 2)
    pygame.draw.line(surface, WHITE, (width // 2 + angulo10, height // 2 + 40), (width // 2 - angulo10, height // 2 + 40), 2)
    draw_angle_text(surface, font, "10", BLACK, width // 2 + 55, height // 2 - 40)
    draw_angle_text(surface, font, "10", BLACK, width // 2 - 55, height // 2 - 40)
    draw_angle_text(surface, font, "10", WHITE, width // 2 - 55, height // 2 + 40)
    draw_angle_text(surface, font, "10", WHITE, width // 2 + 55, height // 2 + 40)
    
    # Líneas y números 15°
    pygame.draw.line(surface, BLACK, (width // 2 + angulo15, height // 2 - 60), (width // 2 - angulo15, height // 2 - 60), 2)
    pygame.draw.line(surface, WHITE, (width // 2 + angulo15, height // 2 + 60), (width // 2 - angulo15, height // 2 + 60), 2)
    
    # Líneas y números 20°
    pygame.draw.line(surface, BLACK, (width // 2 + angulo20, height // 2 - 80), (width // 2 - angulo20, height // 2 - 80), 2)
    pygame.draw.line(surface, WHITE, (width // 2 + angulo20, height // 2 + 80), (width // 2 - angulo20, height // 2 + 80), 2)
    draw_angle_text(surface, font, "20", BLACK, width // 2 + 95, height // 2 - 80)
    draw_angle_text(surface, font, "20", BLACK, width // 2 - 95, height // 2 - 80)
    draw_angle_text(surface, font, "20", WHITE, width // 2 + 95, height // 2 + 80)
    draw_angle_text(surface, font, "20", WHITE, width // 2 - 95, height // 2 + 80)

def draw_angle_text(surface, font, text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)
