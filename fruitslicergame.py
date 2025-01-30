import pygame
import random
from fruits import Fruit
from rendergame import RenderGame
from config import KEY_MAPPING

pygame.init()

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

    def handle_input(self, key):
        for fruit in self.fruits:
            if key == KEY_MAPPING.get(fruit.letter):
                print(f"✅ Bon fruit touché ! ({fruit.letter})")
                self.fruits.remove(fruit)
            else:  
                self.life -= 1
                print(f"Vie restante: {self.life}")            

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
                    self.handle_input(event.key)


                    #elif event.key not in [pygame.K_d, pygame.K_f, pygame.K_g]:
                        #self.life -= 1
                        #print(f"Vie restante: {self.life}")

            
            self.spawn_fruit() # Vérifie si un fruit doit apparaître


            self.fruits = [fruit for fruit in self.fruits if fruit.y < self.render_game.screen_height] #Mise à jour et affichage des fruits

            for fruit in self.fruits:
                fruit.update()
                fruit.draw_fruits(self.render_game.screen)
                self.render_game.text_touch(fruit)

            game_status = self.game_status()
            if game_status == "lose":
                self.render_game.draw_text("You don't have any life left.", 230, 280, self.render_game.red)

            pygame.display.flip()
            clock.tick(30)  

        pygame.quit()


if __name__ == "__main__":
    game = FruitSlicerGame()
    game.run()


"""elif event.type == pygame.KEYDOWN:
    if event.key == pygame.K_d:
        print("Touche D pressée !") 
        #EVENEMENT A DEFINIR
    elif event.key == pygame.K_f:
        print("Touche F pressée !")
        #EVENEMENT A DEFINIR
    elif event.key == pygame.K_g:
        print("Touche G pressée !")
        #EVENEMENT A DEFINIR"""