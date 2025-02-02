import pygame
import random
from config import KEY_MAPPING

class Fruit:
    def __init__(self, x, y, velocity_x, velocity_y, gravity):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = gravity
        self.image = pygame.image.load("apple.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image_rect = self.image.get_rect(topleft=(self.x, self.y))
        self.letter = random.choice(list(KEY_MAPPING))

    def update(self):
        """Met à jour la position du fruit avec une trajectoire parabolique."""
        self.x += self.velocity_x
        self.y -= self.velocity_y  # Monte
        self.velocity_y -= self.gravity  # La gravité réduit la vitesse
        self.image_rect.topleft = (self.x, self.y)

    def draw_fruits(self, screen):
        screen.blit(self.image, (self.x, self.y))