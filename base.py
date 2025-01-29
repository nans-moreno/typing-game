import pygame
import random

pygame.init()
FRUIT_IMAGE = pygame.image.load("apple.png")
FRUIT_IMAGE = pygame.transform.scale(FRUIT_IMAGE, (50, 50))  # Redimensionne l'image

class Fruit:
    def __init__(self, x, y, velocity_x, velocity_y, gravity):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = gravity
        self.image = FRUIT_IMAGE

    def update(self):
        """Met à jour la position du fruit avec une trajectoire parabolique."""
        self.x += self.velocity_x
        self.y -= self.velocity_y  # Monte
        self.velocity_y -= self.gravity  # La gravité réduit la vitesse

    def draw(self, screen):
        """Affiche le fruit sur l'écran."""
        screen.blit(self.image, (self.x, self.y))


class RenderGame:
    def __init__(self, screen_width, screen_height, game_name):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        #self.fond = pygame.image.load("background.jpg").convert()
        pygame.display.set_caption(game_name)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)

        self.font = pygame.font.Font(None, 36)
        self.letter_font = pygame.font.Font(None, 28)

class FruitSlicerGame: #Containt game rules and the run
    _game_instance = None  # Design pattern Singleton allows to have one instance of the game if we launch two time the same class

    def __new__(cls, *args, **kwargs):
        if cls._game_instance is None:
            # Create an instance if none is existing
            cls._game_instance = super().__new__(cls)
        return cls._game_instance

    def __init__(self):
        pygame.init()
        self.render_game = RenderGame(800, 600, "Fruit Slicer")       


    def run(self): #Game loop
        clock = pygame.time.Clock()
        running = True
        #listeFruits = []

        num_fruits = random.randint(3, 10)  # Entre 3 et 10 fruits
        fruits = [
            Fruit(
                x=random.randint(200, 600),
                y=600 - 50,
                velocity_x=random.uniform(-3, 3),
                velocity_y=random.uniform(15, 25),  # Augmentation de la vitesse initiale vers le haut
                gravity=0.5
            ) for _ in range(num_fruits)  # Génère 5 fruits
        ]

        while running:
            self.render_game.screen.fill(self.render_game.white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for fruit in fruits:
                fruit.update()
                fruit.draw(self.render_game.screen)

            pygame.display.flip()
            clock.tick(30)  # 30 FPS

        pygame.quit()  

if __name__ == "__main__":
    game = FruitSlicerGame()
    game.run()         