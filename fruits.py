import pygame
import random
from config import KEY_MAPPING, FRUITS_MAPPING

class Fruit:
    def __init__(self, x, y, velocity_x, velocity_y, gravity):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = gravity
        
        self.fruit_name = random.choice(list(FRUITS_MAPPING.keys()))
        self.fruit_type_render = FRUITS_MAPPING[self.fruit_name]

        self.image = pygame.image.load(self.fruit_type_render.get("image"))
        self.image_rect = self.image.get_rect(topleft=(self.x, self.y))

        self.cut = False
        self.cut_time = None
        self.image_left = pygame.image.load(self.fruit_type_render.get("image-left"))
        self.image_right = pygame.image.load(self.fruit_type_render.get("image-right"))

        self.letter = random.choice(list(KEY_MAPPING))

    def update(self, screen_width):
        if self.cut:
            self.left_rect.x -= self.velocity_x 
            self.right_rect.x += self.velocity_x 
            
            self.left_rect.y += self.velocity_y
            self.right_rect.y += self.velocity_y
            
            self.velocity_y += self.gravity

            if self.left_rect.left < 0:
                self.left_rect.left = 0
                self.velocity_x = -self.velocity_x
            elif self.left_rect.right > screen_width:
                self.left_rect.right = screen_width
                self.velocity_x = -self.velocity_x

            if self.right_rect.left < 0:
                self.right_rect.left = 0
                self.velocity_x = -self.velocity_x
            elif self.right_rect.right > screen_width:
                self.right_rect.right = screen_width
                self.velocity_x = -self.velocity_x

        else:
            # Trajectoire parabolique
            self.x += self.velocity_x
            self.y -= self.velocity_y
            self.velocity_y -= self.gravity
            self.image_rect.topleft = (self.x, self.y)

            if self.image_rect.left < 0:
                self.image_rect.left = 0
                self.velocity_x = -self.velocity_x
            elif self.image_rect.right > screen_width:
                self.image_rect.right = screen_width
                self.velocity_x = -self.velocity_x

    def draw_fruits(self, screen):
        if self.cut:
            screen.blit(self.image_left, self.left_rect)
            screen.blit(self.image_right, self.right_rect)
        else: screen.blit(self.image, self.image_rect)


    def cut_fruit(self):
        if not self.cut:
            self.cut = True
            self.cut_time = pygame.time.get_ticks()

        self.velocity_x = 2
        self.velocity_y = 0
        self.gravity = 0.5

        self.left_rect = self.image_left.get_rect(topleft=(self.x - 10, self.y))
        self.right_rect = self.image_right.get_rect(topleft=(self.x + 10, self.y))
