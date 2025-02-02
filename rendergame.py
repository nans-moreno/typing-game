import pygame
import random
from fruits import Fruit
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, BLUE

class RenderGame:
    def __init__(self, game_name):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(game_name)
        self.white = WHITE
        self.black = BLACK
        self.red = RED
        self.blue = BLUE
        self.font = pygame.font.Font(None, 36)
        self.letter_font = pygame.font.Font(None, 28)

    def draw_text(self, text, x, y, color):
        label = self.font.render(text, True, color)
        self.screen.blit(label, (x, y))

    def text_touch(self, fruit):
        image_rect = fruit.image_rect
        text_x = image_rect.centerx
        text_y = image_rect.bottom + 10 
        self.draw_text(fruit.letter, text_x, text_y, self.red)

    def draw_menu_screen(self, menu_options):
        self.screen.fill(self.white)
        for option in menu_options:
            pygame.draw.rect(self.screen, self.black, option["rect"])
            text_surface = self.font.render(option["text"], True, self.white)
            text_rect = text_surface.get_rect(center=option["rect"].center)
            self.screen.blit(text_surface, text_rect)

    def draw_score_screen(self, scores):
        self.screen.fill(self.white)
        self.draw_text("High Scores", 300, 50, self.black)
        y_offset = 150
        for player, data in scores.items():
            score_text = f"{data['name']}: Score: {data.get('high_score', 0)}"
            self.draw_text(score_text, 200, y_offset, self.black)
            y_offset += 40
        self.draw_text("Press ESC to return to menu", 200, 500, self.blue)

    def draw_game_screen(self, score, life, fruits):
        self.screen.fill(self.white)
        self.draw_text(f"Score: {score}", 20, 20, self.black)
        self.draw_text(f"Lives: {life}", 20, 50, self.black)
        
        for fruit in fruits:
            fruit.draw_fruits(self.screen)
            self.text_touch(fruit)

    def draw_game_over(self, score):
        self.draw_text("Game Over!", 300, 250, self.red)
        self.draw_text(f"Final Score: {score}", 300, 300, self.black)