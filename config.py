import pygame

# Fichier pour toutes les constantes
KEY_MAPPING = {
    "D": pygame.K_d,
    "F": pygame.K_f,
    "G": pygame.K_g
}

# Constantes d'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Configuration du jeu
INITIAL_LIVES = 3
POINTS_PER_FRUIT = 10
GAME_FPS = 30