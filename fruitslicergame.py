import pygame
import time
import random
import json
from fruits import Fruit,Bomb,Ice
from rendergame import RenderGame
from config import KEY_MAPPING, POINTS_PER_FRUIT

pygame.init()  # Vérif à supprimer si besoin

class FruitSlicerGame:
    _game_instance = None  

    def __new__(cls, *args, **kwargs):
        if cls._game_instance is None:
            cls._game_instance = super().__new__(cls)
        return cls._game_instance

    def __init__(self):
        pygame.init()
        self.render_game = RenderGame(800, 600, "Fruit Slicer",None)
 
        self.state = "menu"
        self.menu_options = [
            {"text": "Play", "rect": pygame.Rect(300, 200, 200, 50), "action": "game"},
            {"text": "Scores", "rect": pygame.Rect(300, 300, 200, 50), "action": "score"},
            {"text": "Quit", "rect": pygame.Rect(300, 400, 200, 50), "action": "quit"}
        ]
        self.player = {}
        self.reset_game()
    
    def reset_game(self):
        print("Resetting game state...")  # Debug
        self.score = 0
        self.life = 3
        self.fruits = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = random.randint(1000, 2000) 
        self.next_fruit_time = pygame.time.get_ticks() + random.randint(1000, 2000)
        self.next_bomb_time = pygame.time.get_ticks() + random.randint(5000, 8000) 
        self.next_ice_time = pygame.time.get_ticks() + random.randint(5000, 8000)

    def spawn_fruit(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            new_fruit = Fruit(
                x = random.randint(200, 600),
                y = 600 - 50,
                velocity_x = random.uniform(-3, 3),
                velocity_y = random.uniform(15, 25),
                gravity = 0.5
            )
            self.fruits.append(new_fruit)
            self.last_spawn_time = current_time
            self.spawn_delay = random.randint(1000, 2000)

    def spawn_bomb(self):
        """Génère une bombe avec un délai."""
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_bomb_time:
            new_bomb = Bomb(
                x=random.randint(200, 600),
                y=550,  
                velocity_x=random.uniform(-3, 3),
                velocity_y=random.uniform(15, 25),
                gravity=0.5
            )
            self.fruits.append(new_bomb)
            self.next_bomb_time = current_time + random.randint(5000, 8000)

    def spawn_ice(self):
        """Génère une bombe avec un délai."""
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_ice_time:
            new_ice = Ice(
                x=random.randint(200, 600),
                y=550,  
                velocity_x=random.uniform(-3, 3),
                velocity_y=random.uniform(15, 25),
                gravity=0.5
            )
            self.fruits.append(new_ice)
            self.next_ice_time = current_time + random.randint(5000, 8000)



    def handle_input(self, key):
        """
        Vérifie si la touche pressée correspond à la lettre d'un fruit non coupé.
        Si oui, on coupe le fruit et on augmente le score.
        """
        for fruit in self.fruits:
            # if not fruit.cut and key == KEY_MAPPING.get(fruit.letter):
            #     fruit.cut_fruit()
            #     self.score += POINTS_PER_FRUIT
            if isinstance(fruit, Fruit):
                fruit.cut_fruit()
                self.score += POINTS_PER_FRUIT
            elif isinstance(fruit, Bomb):  # Si c'est une bombe, on perd une vie
                self.life -= 1
                self.fruits.remove(fruit)  # Supprime la bombe immédiatement
            elif isinstance(fruit, Ice):  # Si c'est une bombe, on perd une vie
                time.sleep(3)
                self.fruits.remove(fruit)

    def handle_menu_click(self, pos):
        for option in self.menu_options:
            if option["rect"].collidepoint(pos):
                print(f"Option du menu sélectionnée: {option['action']}")  # Debug
                if option["action"] == "quit":
                    self.state = "quit"
                else:
                    self.state = option["action"]
                    if option["action"] == "game":
                        self.reset_game()
                return

    def save_score(self):
        """
        Sauvegarde le score du joueur dans scores.txt
        """
        if not self.player.get("name"):
            self.player["name"] = "Player"
        
        current_score = {
            "name": self.player["name"],
            "high_score": max(self.score, self.player.get("high_score", 0))
        }
        
        try:
            with open("scores.txt", "r") as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = {}
        scores[self.player["name"]] = current_score
        
        with open("scores.txt", "w") as f:
            json.dump(scores, f, indent=4)

    def display_score(self):
        """
        Lit le fichier scores.txt et retourne un dictionnaire de scores,
        ou un dictionnaire vide si pas de fichier.
        """
        try:
            with open("scores.txt", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Aucun score trouvé")  # Debug
            return {}

    def game_status(self):
        if self.life <= 0:
            return "lose"
        return "ongoing"

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            if self.state == "menu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_menu_click(event.pos)
                
                self.render_game.draw_menu_screen(self.menu_options)
                pygame.display.flip()
                clock.tick(30)
            
            elif self.state == "score":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                
                scores = self.display_score() 
                self.render_game.draw_score_screen(scores)
                pygame.display.flip()
                clock.tick(30)

            elif self.state == "game":
                self.render_game.screen.blit(self.render_game.background_image, (0, 0))
                
                self.render_game.draw_lives(self.life)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        self.handle_input(event.key)

                # self.spawn_fruit()
                current_time = pygame.time.get_ticks()
                if current_time >= self.next_fruit_time:
                    self.spawn_fruit()
                if current_time >= self.next_bomb_time:
                    self.spawn_bomb()
                if current_time >= self.next_ice_time:
                    self.spawn_ice()

                for fruit in self.fruits:
                    fruit.update(self.render_game.screen_width)
                
                for i in range(len(self.fruits)):
                    for j in range(i + 1, len(self.fruits)):
                        fruit1 = self.fruits[i]
                        fruit2 = self.fruits[j]
                        if not fruit1.cut and not fruit2.cut:
                            if fruit1.image_rect.colliderect(fruit2.image_rect):
                                fruit1.velocity_x, fruit2.velocity_x = -fruit1.velocity_x, -fruit2.velocity_x

                now = pygame.time.get_ticks()
                new_fruits = []

                for fruit in self.fruits:
                    if fruit.cut and fruit.cut_time is not None:
                        if now - fruit.cut_time > 500:
                            continue

                    if fruit.y > self.render_game.screen_height:
                        if not fruit.cut:
                            self.life -= 1
                        continue

                    new_fruits.append(fruit)
                    fruit.draw_fruits(self.render_game.screen)
                    self.render_game.text_touch(fruit)

                self.fruits = new_fruits

                if self.game_status() == "lose":
                    game_over_rect = self.render_game.game_over_image.get_rect()
                    game_over_rect.center = (
                        self.render_game.screen_width // 2,
                        self.render_game.screen_height // 2
                    )
                    self.render_game.screen.blit(self.render_game.game_over_image, game_over_rect)

                    pygame.display.flip()
                    pygame.time.wait(2000)
                    
                    self.save_score()
                    self.state = "menu"

                pygame.display.flip()
                clock.tick(30)

            elif self.state == "quit":
                running = False

        pygame.quit()


if __name__ == "__main__":
    game = FruitSlicerGame()
    game.run()
