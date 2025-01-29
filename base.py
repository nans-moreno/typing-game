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

    def draw_text(self, text, x, y, color):
        label = self.font.render(text, True, color)
        self.screen.blit(label, (x, y))

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
        self.SPAWN_FRUIT_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_FRUIT_EVENT, random.randint(1000, 2000)) 
        self.fruits = []   
        self.life = 3   

#    def life_player(self, event):
 #       if event.key != pygame.K_d or pygame.K_f or pygame.K_g:
  #          self.life -= 1

    def game_status(self):
        if self.life == 0:
            return "lose"
        if self.life > 0:
            return self.life

    def run(self): #Game loop
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
                        #RAJOUTER EVENEMENT
                    elif event.key == pygame.K_f:
                        print("Touche F pressée !")
                        #RAJOUTER EVENEMENT
                    elif event.key == pygame.K_g:
                        print("Touche G pressée !")
                        #RAJOUTER EVENEMENT
                    elif event.key != pygame.K_d or pygame.K_f or pygame.K_g:
                        self.life -= 1
                        print(self.life)
                
                game_status = self.game_status()
                if game_status == "lose":
                    self.render_game.draw_text(f"You don't have any life left.", 230, 280, self.render_game.red)
                elif event.type == self.SPAWN_FRUIT_EVENT:
                    new_fruit = Fruit(
                        x=random.randint(200, 600),
                        y=600 - 50,
                        velocity_x=random.uniform(-3, 3),
                        velocity_y=random.uniform(15, 25),
                        gravity=0.5
                    )
                    self.fruits.append(new_fruit)
                    # Redémarrer le timer avec un nouvel intervalle aléatoire
                    pygame.time.set_timer(self.SPAWN_FRUIT_EVENT, random.randint(1000, 2000))

                # Mise à jour et affichage des fruits
                self.fruits = [fruit for fruit in self.fruits if fruit.y < self.render_game.screen_height]  # Supprime les fruits hors écran
                for fruit in self.fruits:
                    fruit.update()
                    fruit.draw(self.render_game.screen)

                pygame.display.flip()
                clock.tick(30)  # FPS
            

        pygame.quit()  

if __name__ == "__main__":
    game = FruitSlicerGame()
    game.run()         