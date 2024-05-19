import pygame

class MouseTracker:
    def __init__(self):
        self.x, self.y = 0, 0

    def start_tracking(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    self.x, self.y = event.pos

    def get_coordinates(self):
        return self.x, self.y
