# INST326 – Group 6 - "Save the Penguin!" 

## Project Overview

**Save the Penguin** is a Python game built using the **Pygame** library. The game follows an object-oriented design and is implemented using three main classes: `Penguin`, `Ship`, and `Game`. Each class contains a defined set of methods that work together to manage player movement, enemy behavior, collision detection, health tracking, and overall game flow.

The player controls a penguin character using the arrow keys and must avoid falling ships that decrease the penguin’s health upon collision. The game ends when the penguin’s health reaches zero, at which point the player may restart or quit.

The structure of this project was inspired by the Pokémon battle game developed earlier in the semester.

---

## Class and Method Breakdown

## `Penguin` Class

The `Penguin` class represents the player-controlled character and is responsible for movement, boundary enforcement, and health management.

### Methods

- `__init__(image_path, screen_width, screen_height, start_health=50)`  
  Initializes the penguin’s sprite, movement speed, screen boundaries, and health.

- `handle_input()`  
  Detects arrow key input and updates the penguin’s position accordingly.

- `keep_in_bounds()`  
  Prevents the penguin from moving outside the visible screen area.

- `draw(screen)`  
  Draws the penguin sprite onto the game screen.

- `take_damage(amount)`  
  Reduces the penguin’s health when a collision occurs.

- `is_alive()`  
  Returns `True` if the penguin’s health is greater than zero.

- `reset()`  
  Resets the penguin’s health and position when the game is restarted.

- `update()`  
  Updates the penguin’s state each frame by processing user input.

- `get_rect()`  
  Returns the penguin’s rectangle for collision detection.

---

## `Ship` Class

The `Ship` class represents enemy objects that fall from the top of the screen and damage the penguin upon collision.

### Methods

- `__init__(image_path, screen_width)`  
  Loads the ship sprite, assigns a random speed, and initializes its position.

- `spawn()`  
  Randomly positions the ship along the horizontal axis above the screen.

- `move()`  
  Moves the ship downward at its assigned speed.

- `update()`  
  Updates the ship’s position each frame.

- `draw(screen)`  
  Draws the ship sprite onto the game screen.

- `is_off_screen(screen_height)`  
  Returns `True` if the ship has moved past the bottom of the screen.

- `check_collision(penguin_rect)`  
  Checks for a collision between the ship and the penguin.

- `get_rect()`  
  Returns the ship’s rectangle for collision detection.

---

## `Game` Class

The `Game` class manages the main game loop, asset loading, game state, and player interaction.

### Methods

- `__init__()`  
  Initializes Pygame, loads assets, creates the display window, initializes game objects, and starts background music.

- `spawn_wave()`  
  Spawns a wave of one to three ships.

- `draw_background()`  
  Draws the background image onto the screen.

- `draw_health()`  
  Displays the penguin’s current health in the top-left corner.

- `handle_collisions()`  
  Detects collisions between the penguin and ships and applies damage.

- `update_ships()`  
  Updates ship movement and removes ships that exit the screen.

- `check_game_over()`  
  Determines whether the penguin’s health has reached zero.

- `draw_game_over()`  
  Displays the game-over message and restart/quit instructions.

- `reset_game()`  
  Resets the game state to allow the player to restart.

- `handle_events()`  
  Processes system and keyboard events such as quitting or restarting the game.

- `update()`  
  Updates all game objects and checks game state conditions each frame.

- `draw()`  
  Renders all game elements to the screen.

- `run()`  
  Executes the main game loop until the player quits.

---

## How to Run the Program

### Requirements
- Python 3.x  
- Pygame  

Install Pygame if necessary:
```bash
pip install pygame
```

### Running the Game
1. Clone/Download this Repo
2. Ensure all image files and music.mp3 are in the same directory as the Python file
3. Run the game using

```bash
python SaveThePenguin.py
```

## Controls
-Arrow Keys: Move the Penguin
-R: Restart the Game
-Q: Quit the Game

