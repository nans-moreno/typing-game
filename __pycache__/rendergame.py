import pygame
import random
from fruits import Fruit

class RenderGame:
    def __init__(self, screen_width, screen_height, game_name):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(game_name)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.font = pygame.font.Font(None, 36)
        self.letter_font = pygame.font.Font(None, 28)
        self.fruit_class = Fruit(
            x=random.randint(200, 600),
            y=600 - 50,
            velocity_x=random.uniform(-3, 3),
            velocity_y=random.uniform(15, 25),
            gravity=0.5
        )

    def draw_text(self, text, x, y, color):
        label = self.font.render(text, True, color)
        self.screen.blit(label, (x, y))

    def text_touch(self, fruit):
        print(f"Affichage du texte sous le fruit à {fruit.image_rect.topleft}")
        image_rect = fruit.image_rect
        text_x = image_rect.centerx
        text_y = image_rect.bottom + 10 
        self.draw_text(fruit.letter, text_x, text_y, (255, 0, 0))
