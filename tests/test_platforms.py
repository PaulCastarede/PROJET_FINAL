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
    
    def test_invalid_platform(self) -> None:
        try:
            create_world.readmap(self.world, "test_invalid_platform.txt")
            assert False
        except create_world.InvalidMapFormat:
            assert True

    def test_valid_platform(self) -> None:
        create_world.readmap(self.world, "test_valid_platform.txt")
        assert True
        for platform in self.world.moving_platforms_list:
            assert platform.change_x != 0
            assert platform.change_y != 0
            if platform.boundary_left is not None and platform.boundary_right is not None and \
               platform.boundary_top is not None and platform.boundary_bottom is not None:
                assert platform.center_x <=platform.boundary_right
                assert platform.center_x >= platform.boundary_left
                assert platform.center_y <= platform.boundary_top
                assert platform.center_y >= platform.boundary_bottom
            else:
                assert False
