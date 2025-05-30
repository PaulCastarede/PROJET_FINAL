from __future__ import annotations
import arcade
import pytest
from typing import Final
import create_world

class TestMapValidation:
    window: arcade.Window
    world: create_world.World

    def setup_method(self) -> None:
        self.window = arcade.Window(1280, 720, "Test Window")
        self.world = create_world.World()

    def test_invalid_dimensions(self) -> None:
        try:
            create_world.readmap(self.world, "test_invalid_dimensions.txt")
            assert False
        except create_world.InvalidMapFormat:
            assert True 

    def test_invalid_end(self) -> None:
        try:
            create_world.readmap(self.world, "test_invalid_end.txt")
            assert False
        except create_world.InvalidMapFormat:
            assert True

    def test_invalid_config(self) -> None:
        try:
            create_world.readmap(self.world, "test_invalid_config.txt")
            assert False
        except create_world.InvalidMapFormat:
            assert True

    def test_invalid_character(self) -> None:
        try:
            create_world.readmap(self.world, "test_invalid_characters.txt")
            assert False
        except create_world.InvalidMapFormat:
            assert True

    def test_valid_map(self) -> None:
        create_world.readmap(self.world, "map1.txt")
        assert True

    def teardown_method(self) -> None:
        self.window.close()