from __future__ import annotations
import arcade
import pytest
from typing import Final
import create_world
import platforming

class TestPlatformsValidation:
    window: arcade.Window
    world: create_world.World

    def setup_method(self) -> None:
        self.window = arcade.Window(1280, 720, "Test Window")
        self.world = create_world.World()

    def test_duplicated_platforms(self) -> None:
        try:
            create_world.readmap(self.world, "test_duplicated_platforms.txt")
            assert False
        except create_world.InvalidMapFormat:
            assert True
        
    