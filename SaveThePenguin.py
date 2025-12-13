import pygame
import random
import sys

pygame.mixer.init()

class Penguin:
    """
    Represents the penguin controlled by the player using arrow keys.
    """

    def __init__(self, image_path, screen_width, screen_height, start_health=50):
        """Initialize penguin attributes."""
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (50, 50))

        self.rect = self.image.get_rect(
            center=(screen_width // 2, screen_height - 80)
        )

        self.health = start_health
        self.speed = 5
        self.screen_width = screen_width
        self.screen_height = screen_height

    def handle_input(self):
        """Handle keyboard input."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.keep_in_bounds()

    def keep_in_bounds(self):
        """Keep penguin within screen limits."""
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self.screen_width, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(self.screen_height, self.rect.bottom)

    def draw(self, screen):
        """Draw penguin."""
        screen.blit(self.image, self.rect)

    def take_damage(self, amount):
        """Reduce health."""
        self.health -= amount

    def is_alive(self):
        """Check health state."""
        return self.health > 0

    def reset(self):
        """Reset penguin state."""
        self.health = 50
        self.rect.centerx = self.screen_width // 2
        self.rect.bottom = self.screen_height - 40

    def update(self):
        """Update penguin movement."""
        self.handle_input()

    def get_rect(self):
        """Return collision rect."""
        return self.rect


class Ship:
    """
    Represents enemy ships that fall from top to bottom.
    """

    def __init__(self, image_path, screen_width):
        """Initialize ship."""
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (40, 40))

        self.rect = self.image.get_rect()
        self.speed = random.randint(3, 6)
        self.screen_width = screen_width
        self.spawn()

    def spawn(self):
        """Spawn ship within horizontal screen limits."""
        self.rect.x = random.randint(
            0, self.screen_width - self.rect.width
        )
        self.rect.y = random.randint(-120, -40)

    def move(self):
        """Move ship downward."""
        self.rect.y += self.speed

    def update(self):
        """Update ship movement."""
        self.move()

    def draw(self, screen):
        """Draw ship."""
        screen.blit(self.image, self.rect)

    def is_off_screen(self, screen_height):
        """Check if ship left screen."""
        return self.rect.top > screen_height

    def check_collision(self, penguin_rect):
        """Check collision with penguin."""
        return self.rect.colliderect(penguin_rect)

    def get_rect(self):
        """Return collision rect."""
        return self.rect


class Game:
    """
    Controls game setup, loop, and logic.
    """

    def __init__(self):
        """Initialize game."""
        pygame.init()

    # Load background first (no conversion yet)
        raw_background = pygame.image.load("GameplayBackground.PNG")

    # Set screen size to background size
        self.width = raw_background.get_width()
        self.height = raw_background.get_height()

    # Create the display window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Save the Penguin")

    # Now convert background safely
        self.background = raw_background.convert()

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

        self.font = pygame.font.SysFont(None, 36)

        self.penguin = Penguin(
        "PenguinCharacter.PNG", self.width, self.height
        )

        self.ships = []
        self.spawn_wave()


        self.ships = []
        self.spawn_wave()

        #Add music in a cont. loop
        try:
            pygame.mixer.music.load("music.mp3")
            pygame.mixer.music.set_volume(0.5)  # optional: adjust volume
            pygame.mixer.music.play(loops=-1, fade_ms=2000)
        except pygame.error as e:
            print(f"Music file not found or could not play: {e}")


    def spawn_wave(self):
        """Spawn a wave of 1–3 ships."""
        self.ships.clear()
        for _ in range(random.randint(1, 3)):
            self.ships.append(Ship("Ship.PNG", self.width))

    def draw_background(self):
        """Draw background."""
        self.screen.blit(self.background, (0, 0))

    def draw_health(self):
        """Draw health text."""
        if self.penguin.health <= 20:
            color = (255, 0, 0)   # red
        else:
            color = (255, 255, 255)  # white
        
        text = self.font.render(
            f"Health: {self.penguin.health}", True, color
        )
        self.screen.blit(text, (10, 10))

    def handle_collisions(self):
        """Handle collisions."""
        for ship in self.ships:
            if ship.check_collision(self.penguin.get_rect()):
                self.penguin.take_damage(10)
                self.spawn_wave()
                break

    def update_ships(self):
        """Update ships and waves."""
        for ship in self.ships:
            ship.update()

        self.ships = [
            ship for ship in self.ships
            if not ship.is_off_screen(self.height)
        ]

        if not self.ships:
            self.spawn_wave()

    def check_game_over(self):
        """Check game over."""
        if not self.penguin.is_alive():
            self.game_over = True

    def draw_game_over(self):
        """Draw game over screen."""
        line1 = self.font.render("Game Over!", True, (255, 255, 255))
        line2 = self.font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

        spacing = 10  

        line1_rect = line1.get_rect(center=(self.width // 2, self.height // 2 - (line1.get_height() // 2 + spacing)))
        line2_rect = line2.get_rect(center=(self.width // 2, self.height // 2 + (line2.get_height() // 2)))

        self.screen.blit(line1, line1_rect)
        self.screen.blit(line2, line2_rect)


    def reset_game(self):
        """Reset game."""
        self.penguin.reset()
        self.spawn_wave()
        self.game_over = False

    def handle_events(self):
        """Handle events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    self.running = False

    def update(self):
        """Update game state."""
        if not self.game_over:
            self.penguin.update()
            self.update_ships()
            self.handle_collisions()
            self.check_game_over()

    def draw(self):
        """Draw everything."""
        self.draw_background()
        self.penguin.draw(self.screen)

        for ship in self.ships:
            ship.draw(self.screen)

        self.draw_health()

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        """Run game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
