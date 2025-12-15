"""
Shared pytest fixtures and helpers for SaveThePenguin tests

This file centralizes pygame mocking, system exit blocking,
and keyboard input helpers so individual test files remain clean
and focused on behavior rather than setup
"""

import pytest
import pygame
import sys
from unittest.mock import MagicMock, patch
from collections import defaultdict


def make_keys(*pressed_keys):
    """
    Create a dictionary-like object that simulates pygame.key.get_pressed().

    Any key not explicitly passed in defaults to False.

    Args:
        *pressed_keys: pygame key constants to simulate as pressed.

    Returns:
        defaultdict: mapping of key constants to boolean pressed states.
    """
    keys = defaultdict(lambda: False)
    for key in pressed_keys:
        keys[key] = True
    return keys


@pytest.fixture(autouse=True)
def mock_pygame():
    """
    Automatically mock pygame dependencies for all tests.

    outcome:
    Initializes pygame display and font modules
    Sets a minimal video mode so convert_alpha() works
    Mocks image loading, scaling, fonts, clocks, and music
    prevents file I/O and audio playback during testing
    """
    pygame.display.init()
    pygame.font.init()

    # Required for convert_alpha()
    pygame.display.set_mode((1, 1))

    background_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
    sprite_surface = pygame.Surface((100, 100), pygame.SRCALPHA)

    fake_font = MagicMock()
    fake_font.render.return_value = pygame.Surface((10, 10), pygame.SRCALPHA)

    def fake_image_load(path):
        """Return appropriate dummy surfaces based on asset type."""
        if "GameplayBackground" in path:
            return background_surface
        return sprite_surface

    with patch("pygame.init"), \
         patch("pygame.image.load", side_effect=fake_image_load), \
         patch("pygame.transform.scale",
               side_effect=lambda surf, size: pygame.Surface(size, pygame.SRCALPHA)), \
         patch("pygame.display.set_caption"), \
         patch("pygame.font.SysFont", return_value=fake_font), \
         patch("pygame.time.Clock", return_value=MagicMock()), \
         patch("pygame.mixer.music.load"), \
         patch("pygame.mixer.music.set_volume"), \
         patch("pygame.mixer.music.play"):
        yield


@pytest.fixture(autouse=True)
def block_sys_exit(monkeypatch):
    """
    Prevent sys.exit() from terminating pytest during Game tests.
    """
    monkeypatch.setattr(sys, "exit", lambda *_: None)
