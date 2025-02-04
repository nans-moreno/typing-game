import pygame
import random
from fruits import Entity,Fruit,Bomb,Ice

class RenderGame:
    def __init__(self, screen_width, screen_height, game_name,entity_name):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(game_name)
        self.background_image = pygame.image.load("assets/background.jpg").convert()
        self.background_image = pygame.transform.scale(
            self.background_image, 
            (self.screen_width, self.screen_height)
        )
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.font = pygame.font.Font(None, 36)
        self.letter_font = pygame.font.Font(None, 28)
        self.heart_image = pygame.image.load("assets/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (84, 84))
        self.game_over_image = pygame.image.load("assets/game-over.png").convert_alpha()

        if entity_name=="fruit":
            self.fruit_class = Fruit(
                x=random.randint(200, 600),
                y=600 - 50,
                velocity_x=random.uniform(-3, 3),
                velocity_y=random.uniform(15, 25),
                gravity=0.5
            )
        elif entity_name=="bomb":
             self.fruit_class = Bomb(
                x=random.randint(200, 600),
                y=600 - 50,
                velocity_x=random.uniform(-3, 3),
                velocity_y=random.uniform(15, 25),
                gravity=0.5
            )
        elif entity_name == "ice":
            self.fruit_class = Ice(
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
        if not fruit.cut:
            image_rect = fruit.image_rect
            text_x = image_rect.centerx
            text_y = image_rect.bottom + 10 
            self.draw_text(fruit.letter, text_x, text_y, (255, 0, 0))

    
    def draw_lives(self, life):
        for i in range(life):
            x = 10 + i * 40
            y = 10
            self.screen.blit(self.heart_image, (x, y))

    def draw_menu_screen(self, menu_options):
        self.screen.fill(self.white)
        for option in menu_options:
            pygame.draw.rect(self.screen, self.black, option["rect"])
            text_surface = self.font.render(option["text"], True, self.white)
            text_rect = text_surface.get_rect(center=option["rect"].center)
            self.screen.blit(text_surface, text_rect)

    def draw_enter_name_screen(self, current_name):
        self.screen.fill(self.white)
        self.draw_text("Enter your name", 300, 50, self.black)
        self.draw_text(f"Current name : {current_name}", 200, 200, self.blue)
        self.draw_text("Press Enter to validate", 200, 400, self.red)


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
