import pygame
import random
import json
from fruits import Fruit
from rendergame import RenderGame
from config import (
    KEY_MAPPING, SCREEN_WIDTH, SCREEN_HEIGHT, INITIAL_LIVES,
    POINTS_PER_FRUIT, GAME_FPS
)

class FruitSlicerGame:
    _game_instance = None

    def __new__(cls, *args, **kwargs):
        if cls._game_instance is None:
            cls._game_instance = super().__new__(cls)
        return cls._game_instance

    def __init__(self):
        print("Initializing game...") # Debug
        pygame.init()
        self.state = "menu"
        self.render_game = RenderGame("Fruit Slicer")
        self.reset_game()
        self.player = {}
        
        # Configuration du menu
        self.menu_options = [
            {"text": "Play", "rect": pygame.Rect(300, 200, 200, 50), "action": "game"},
            {"text": "Scores", "rect": pygame.Rect(300, 300, 200, 50), "action": "score"},
            {"text": "Quit", "rect": pygame.Rect(300, 400, 200, 50), "action": "quit"}
        ]
        print("Game initialized successfully") # Debug

    def reset_game(self):
        print("Resetting game state...") # Debug
        self.life = INITIAL_LIVES
        self.fruits = []
        self.score = 0
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = random.randint(1000, 2000)

    def handle_input(self, key):
        for fruit in self.fruits:
            if key == KEY_MAPPING.get(fruit.letter):
                print(f"✅ Bon fruit touché ! ({fruit.letter})")
                self.fruits.remove(fruit)
                self.score += POINTS_PER_FRUIT
            else:
                self.life -= 1
                print(f"Vie perdue! Vie restante: {self.life}")

    def spawn_fruit(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            new_fruit = Fruit(
                x=random.randint(200, 600),
                y=SCREEN_HEIGHT - 50,
                velocity_x=random.uniform(-3, 3),
                velocity_y=random.uniform(15, 25),
                gravity=0.5
            )
            self.fruits.append(new_fruit)
            print(f"Nouveau fruit créé à ({new_fruit.x}, {new_fruit.y})") # Debug
            self.last_spawn_time = current_time
            self.spawn_delay = random.randint(1000, 2000)

    def handle_menu_click(self, pos):
        for option in self.menu_options:
            if option["rect"].collidepoint(pos):
                print(f"Option du menu sélectionnée: {option['action']}") # Debug
                if option["action"] == "quit":
                    return False
                self.state = option["action"]
                if option["action"] == "game":
                    self.reset_game()
                return True
        return True

    def save_score(self):
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
        print(f"Score sauvegardé pour {self.player['name']}: {current_score['high_score']}") # Debug

    def display_score(self):
        try:
            with open("scores.txt", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Aucun score trouvé") # Debug
            return {}

    def update_game_state(self):
        # Keep only fruits that are still on screen
        self.fruits = [fruit for fruit in self.fruits if fruit.y < SCREEN_HEIGHT]
        for fruit in self.fruits:
            fruit.update()

    def run(self):
        print("Démarrage du jeu") # Debug
        clock = pygame.time.Clock()
        running = True

        while running:
            if self.state == "menu":
                self.render_game.draw_menu_screen(self.menu_options)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        running = self.handle_menu_click(event.pos)

            elif self.state == "score":
                scores = self.display_score()
                self.render_game.draw_score_screen(scores)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "menu"

            elif self.state == "game":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                        else:
                            self.handle_input(event.key)

                self.spawn_fruit()
                self.update_game_state()
                self.render_game.draw_game_screen(self.score, self.life, self.fruits)

                if self.life <= 0:
                    print("Game Over!") # Debug
                    self.render_game.draw_game_over(self.score)
                    self.save_score()
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    self.state = "menu"

            pygame.display.flip()
            clock.tick(GAME_FPS)

        pygame.quit()
        print("Jeu terminé") # Debug

if __name__ == "__main__":
    game = FruitSlicerGame()
    game.run()