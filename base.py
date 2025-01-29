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
        pygame.display.set_caption(game_name)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)

        self.font = pygame.font.Font(None, 36)
        self.letter_font = pygame.font.Font(None, 28)

    def draw_text(self, text, x, y, color):
        label = self.font.render(text, True, color)
        self.screen.blit(label, (x, y))


class FruitSlicerGame:
    _game_instance = None  

    def __new__(cls, *args, **kwargs):
        if cls._game_instance is None:
            cls._game_instance = super().__new__(cls)
        return cls._game_instance

    def __init__(self):
        pygame.init()
        self.render_game = RenderGame(800, 600, "Fruit Slicer")
        self.life = 3  
        self.fruits = [] 
        self.last_spawn_time = pygame.time.get_ticks()  
        self.spawn_delay = random.randint(1000, 2000) 

    def spawn_fruit(self):
        """Fait apparaître un fruit à un intervalle aléatoire."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            new_fruit = Fruit(
                x=random.randint(200, 600),
                y=600 - 50,
                velocity_x=random.uniform(-3, 3),
                velocity_y=random.uniform(15, 25),
                gravity=0.5
            )
            self.fruits.append(new_fruit)
            self.last_spawn_time = current_time
            self.spawn_delay = random.randint(1000, 2000)

    def game_status(self):
        if self.life <= 0:
            return "lose"
        return self.life

    def run(self):  
        clock = pygame.time.Clock()
        running = True

        while running:
            self.render_game.screen.fill(self.render_game.white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        print("Touche D pressée !")
                        for fruit in self.fruits:
                            fruit.x += 10  # Déplace tous les fruits vers la droite
                    elif event.key == pygame.K_f:
                        print("Touche F pressée !")
                        for fruit in self.fruits:
                            fruit.y -= 10  # Déplace tous les fruits vers le haut
                    elif event.key == pygame.K_g:
                        print("Touche G pressée !")
                        for fruit in self.fruits:
                            fruit.velocity_y += 1  # Accélère la chute des fruits
                    elif event.key not in [pygame.K_d, pygame.K_f, pygame.K_g]:
                        self.life -= 1
                        print(f"Vie restante: {self.life}")

            # Vérifie si un fruit doit apparaître
            self.spawn_fruit()

            # Mise à jour et affichage des fruits
            self.fruits = [fruit for fruit in self.fruits if fruit.y < self.render_game.screen_height]  
            for fruit in self.fruits:
                fruit.update()
                fruit.draw(self.render_game.screen)

            # Affichage du statut du jeu
            game_status = self.game_status()
            if game_status == "lose":
                self.render_game.draw_text("You don't have any life left.", 230, 280, self.render_game.red)

            pygame.display.flip()
            clock.tick(30)  

        pygame.quit()


if __name__ == "__main__":
    game = FruitSlicerGame()
    game.run()
