import pygame

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
        running = True

        while running:
            self.render_game.screen.fill(self.render_game.white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
        pygame.quit()  

if __name__ == "__main__":
    game = FruitSlicerGame()
    game.run()         