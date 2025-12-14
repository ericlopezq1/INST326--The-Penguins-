import pytest
import pygame
import sys
import random
from unittest.mock import MagicMock, patch
from collections import defaultdict
from SaveThePenguin import Penguin, Ship, Game 


#MOCKING PYGAME DEPENDENCIES

@pytest.fixture(autouse=True)
def mock_pygame_init():
    """Mock pygame systems while keeping real Surface/Rect behavior."""
    pygame.display.init()
    pygame.font.init()
    
    pygame.display.set_mode((1, 1))

    background_surface = pygame.Surface((800, 600), pygame.SRCALPHA)

    sprite_surface = pygame.Surface((100, 100), pygame.SRCALPHA)

    fake_font = MagicMock()
    fake_font.render.return_value = pygame.Surface((10, 10), pygame.SRCALPHA)

    def fake_image_load(path):
        if "GameplayBackground" in path:
            return background_surface
        return sprite_surface

    with patch("pygame.init"), \
         patch("pygame.image.load", side_effect=fake_image_load), \
         patch("pygame.transform.scale", side_effect=lambda surf, size: pygame.Surface(size, pygame.SRCALPHA)), \
         patch("pygame.display.set_mode", return_value=background_surface), \
         patch("pygame.display.set_caption"), \
         patch("pygame.font.SysFont", return_value=fake_font), \
         patch("pygame.time.Clock", return_value=MagicMock()), \
         patch("pygame.mixer.music.load"), \
         patch("pygame.mixer.music.set_volume"), \
         patch("pygame.mixer.music.play"):
        yield


@pytest.fixture(autouse=True)
def mock_pygame_mixer():
    """Mock pygame mixer functions for music handling."""
    with patch('pygame.mixer.music.load'), \
         patch('pygame.mixer.music.set_volume'), \
         patch('pygame.mixer.music.play'):
        yield
        

@pytest.fixture(autouse=True)
def block_sys_exit(monkeypatch):
    """Prevent sys.exit from stopping pytest."""
    monkeypatch.setattr(sys, "exit", lambda *_: None)

#Helper for keyboard input tests
def make_keys(*pressed_keys):
    keys = defaultdict(lambda: False)
    for k in pressed_keys:
        keys[k] = True
    return keys


#Fixtures for Class Instances
@pytest.fixture
def penguin():
    """Fixture for a Penguin object with default dimensions."""
    SCREEN_W, SCREEN_H = 800, 600
    return Penguin("PenguinCharacter.PNG", SCREEN_W, SCREEN_H, start_health=50)

@pytest.fixture
def ship():
    """Fixture for a Ship object."""
    SCREEN_W = 800
    with patch("random.randint", side_effect=[3, 400, -80]):
        yield Ship("Ship.PNG", SCREEN_W)

@pytest.fixture
def game(penguin):
    """Fixture for a Game object with mocked dependencies."""
    with patch.object(Game, "spawn_wave", lambda self: None):
        g = Game()

    g.penguin = penguin
    g.ships = []
    return g



#TEST FUNCTIONS

#Penguin Class Tests

def test_penguin_initialization_and_health(penguin):
    """Test initial state (health, speed) and collision rect center."""
    assert penguin.health == 50
    assert penguin.speed == 5
    assert penguin.get_rect().center == (400, 520)
    assert penguin.is_alive() is True

def test_penguin_take_damage_and_death_edge_case(penguin):
    """Test damage logic leading to death state."""
    penguin.take_damage(49)
    assert penguin.health == 1
    assert penguin.is_alive() is True

    penguin.take_damage(1)
    assert penguin.health == 0
    assert penguin.is_alive() is False

def test_penguin_movement_and_boundary_right(penguin):
    """Test movement (right) and boundary clipping (right side)."""
    penguin.rect.right = penguin.screen_width - 2

    with patch("pygame.key.get_pressed", return_value=make_keys(pygame.K_RIGHT)):
        penguin.handle_input()

    assert penguin.get_rect().right == penguin.screen_width

def test_penguin_movement_up_and_reset_position(penguin):
    """Test upward movement and verify position reset."""
    initial_y = penguin.rect.y

    with patch("pygame.key.get_pressed", return_value=make_keys(pygame.K_UP)):
        penguin.handle_input()

    assert penguin.rect.y == initial_y - penguin.speed

    penguin.reset()
    assert penguin.get_rect().bottom == 560

def test_penguin_no_movement_when_no_key_pressed(penguin):
    """Test that position remains static without input."""
    initial_rect = penguin.get_rect().copy()

    with patch("pygame.key.get_pressed", return_value=make_keys()):
        penguin.handle_input()

    assert penguin.get_rect() == initial_rect


#Ship Class Tests

def test_ship_initial_spawn_position(ship):
    """Test ship spawn randomness and initial position."""
    assert ship.get_rect().x == 400
    assert ship.get_rect().y == -80
    assert ship.is_off_screen(600) == False

def test_ship_movement_and_speed(ship):
    """Test ship movement is downward and uses its randomized speed."""
    initial_y = ship.get_rect().y
    ship.update()
    assert ship.get_rect().y == initial_y + ship.speed
    assert 3 <= ship.speed <= 6

def test_ship_collision_check_positive(ship, penguin):
    """Test collision detection when objects overlap."""
    ship.rect.topleft = penguin.rect.topleft
    assert ship.check_collision(penguin.get_rect()) is True

    ship.rect.x += penguin.rect.width + 1
    assert ship.check_collision(penguin.get_rect()) is False


#Game Class Tests

def test_game_handle_collisions_logic(game, penguin):
    """Test that collision causes damage AND a new wave spawn."""
    
    with patch("random.randint", side_effect=[3, 200, -80]):
        test_ship = Ship("Ship.PNG", game.width)

    test_ship.rect.topleft = penguin.rect.topleft
    game.ships = [test_ship]

    initial_health = penguin.health

    def respawn_one_ship():
        with patch("random.randint", side_effect=[3, 250, -80]):
            game.ships = [Ship("Ship.PNG", game.width)]

    game.spawn_wave = respawn_one_ship

    game.handle_collisions()

    assert penguin.health == initial_health - 10
    assert len(game.ships) == 1
    assert game.ships[0] is not test_ship

def test_game_update_ships_wave_management(game):
    """Test wave management when ships leave the screen (off_screen)."""
    off_screen_ship = Ship("Ship.PNG", game.width)
    off_screen_ship.rect.top = game.height + 10
    game.ships = [off_screen_ship]

    game.update_ships()

    assert len(game.ships) >= 1
    for s in game.ships:
        assert not s.is_off_screen(game.height)

def test_game_check_game_over_state_change(game, penguin):
    """Test the complete game over flow."""
    penguin.health = 1
    game.check_game_over()
    assert game.game_over is False

    penguin.take_damage(50)
    game.check_game_over()
    assert game.game_over is True
    

