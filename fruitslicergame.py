import pygame
import random
import json
from fruits import Fruit
from rendergame import RenderGame
from config import KEY_MAPPING, POINTS_PER_FRUIT, INITIAL_LIVES, SCREEN_WIDTH, SCREEN_HEIGHT


pygame.init()  # Vérif à supprimer si besoin
pygame.mixer.init()

pygame.mixer.music.load("sound/Soundtrack.mp3")  
pygame.mixer.music.play(-1)  
pygame.mixer.music.set_volume(0.5)  

class FruitSlicerGame:
    _game_instance = None  

    def __new__(cls, *args, **kwargs):
        if cls._game_instance is None:
            cls._game_instance = super().__new__(cls)
        return cls._game_instance

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.render_game = RenderGame(SCREEN_WIDTH, SCREEN_HEIGHT, "Fruit Slicer")
        
        try:
            self.slice_sound = pygame.mixer.Sound("sound/Impact.wav")
        except pygame.error as e:
            print(f"Erreur chargement son: {e}")
            self.slice_sound = None
 
        self.state = "menu"
        self.menu_options = [
            {"text": "Play", "rect": pygame.Rect(300, 200, 200, 50), "action": "game"},
            {"text": "Scores", "rect": pygame.Rect(300, 300, 200, 50), "action": "score"},
            {"text": "Quit", "rect": pygame.Rect(300, 400, 200, 50), "action": "quit"}
        ]
        self.player = {}
        self.current_name = ""  # For "enter_name" state
        self.reset_game()
    
    def reset_game(self):
        print("Resetting game state...")  # Debug
        self.score = 0
        self.life = INITIAL_LIVES

        self.fruits = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = random.randint(1000, 2000) 

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

    def handle_input(self, key):
        
        """
        Vérifie si la touche pressée correspond à la lettre d'un fruit non coupé.
        Si oui, on coupe le fruit et on augmente le score.
        """
        for fruit in self.fruits:
            if not fruit.cut and key == KEY_MAPPING.get(fruit.letter):
                fruit.cut_fruit()
                self.score += POINTS_PER_FRUIT
            else: self.life -= 1  # Perd une vie si la touche ne correspond à aucun fruit
            self.slice_sound.play()
            


    def handle_menu_click(self, pos):
        for option in self.menu_options:
            if option["rect"].collidepoint(pos):
                print(f"Option du menu sélectionnée: {option['action']}")  # Debug
                if option["action"] == "quit":
                    self.state = "quit"
                else:
                    # If "Play" is selected, require name entry if not set.
                    if option["action"] == "game":
                        if not self.player.get("name"):
                            self.state = "enter_name"
                        else:
                            self.state = "game"
                            self.reset_game()
                    else:
                        self.state = option["action"]
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

            elif self.state == "enter_name":
                # Allow the player to enter his name
                self.render_game.draw_enter_name_screen(self.current_name)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.current_name.strip():
                                self.player["name"] = self.current_name.strip()
                                self.current_name = ""
                                self.state = "game"  # Proceed to game after name entry
                                self.reset_game()
                        elif event.key == pygame.K_BACKSPACE:
                            self.current_name = self.current_name[:-1]
                        elif event.unicode.isalpha():
                            self.current_name += event.unicode

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

                self.spawn_fruit()

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
