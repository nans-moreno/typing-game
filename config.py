import pygame

#Fichier pour toutes les constantes

KEY_MAPPING = {
        "D": pygame.K_d,
        "F": pygame.K_f,
        "G": pygame.K_g
    }

FRUITS_MAPPING = {
    "apple": { "image": "assets/apple.png",
              "image-left": "assets/apple-1.png",
              "image-right": "assets/apple-2.png"},
    "peach": {"image": "assets/peach.png",
              "image-left": "assets/peach-1.png",
              "image-right": "assets/peach-2.png"},
    "strawberry": {"image": "assets/strawberry.png",
              "image-left": "assets/strawberry-1.png",
              "image-right": "assets/strawberry-2.png"},                       
}

POINTS_PER_FRUIT = 10

INITIAL_LIVES = 3  # Nombre initial de vies

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
