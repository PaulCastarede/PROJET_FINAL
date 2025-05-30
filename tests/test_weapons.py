from __future__ import annotations
import arcade
import math
from typing import Final
from weapons import Bow, Arrow, Sword
from world_sprites_types.switches import Switch
import world_sprites_types.gates as gates
import platforming.platforms 
import platforming.block_detecting
import create_world

class TestWeapons:
    window: arcade.Window
    player: arcade.Sprite
    bow: Bow
    sword: Sword

    def setup_method(self) -> None:
        self.window = arcade.Window(1280, 720, "Test Window")
        self.player = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", 0.5)
        self.player.center_x = 100
        self.player.center_y = 100
        
        self.bow = Bow("Assets/kenney-voxel-items-png/bow.png", 0.5, self.player.center_x, self.player.center_y, 0)
        self.sword = Sword("Assets/kenney-voxel-items-png/sword_iron.png", 0.5, self.player.center_x, self.player.center_y, 0)
        
    def test_arrow_gravity(self) -> None:
        arrow: Arrow = Arrow(center_x=100, center_y=100)
        initial_y: float = arrow.center_y
        arrow.released = True
        arrow.arrows_movement()
        assert arrow.center_y != initial_y
        
    def test_arrow_charge_level(self) -> None:
        arrow: Arrow = Arrow()
        initial_speed: float = arrow.speed
        arrow.charge_level_increases_speed()
        assert arrow.speed > initial_speed
            
    def test_arrow_collision_wall_platform(self) -> None:
        world: create_world.World = create_world.World()

        arrow: Arrow = Arrow(center_x=101, center_y=100)
        arrow.released = True
        arrow_list: arcade.SpriteList[Arrow] = arcade.SpriteList()
        arrow_list.append(arrow)

        trajectory: platforming.platforms.Trajectory = platforming.platforms.Trajectory()
        trajectory.right_movement = 2.0
        crate: platforming.platforms.Collidable_Platform = platforming.platforms.Collidable_Platform(
            path_or_texture=":resources:images/tiles/boxCrate_double.png",
            scale=0.5,
            center_x=100,
            center_y=100,
            angle=0,
            platform_trajectory=trajectory)
        
        world.moving_platforms_list.append(crate)
        assert arrow in arrow_list
        crate.define_boundaries()
        initial_x: float = crate.center_x
        crate.movement()
        arrow.check_arrow_hits(world)
        assert crate.center_x != initial_x
        assert arrow not in arrow_list


    def test_arrow_trajectory(self) -> None:
        arrow: Arrow = Arrow(center_x=100, center_y=100)
        arrow.released = True
        arrow.change_x = 5
        arrow.change_y = 10
        
        initial_x: float = arrow.center_x
        initial_y: float = arrow.center_y
        
        for _ in range(5):
            arrow.arrows_movement()
            
        assert arrow.center_x > initial_x
        assert arrow.center_y != initial_y
        assert arrow.change_y < 10

    def test_arrow_out_of_screen(self) -> None:
        arrow: Arrow = Arrow(center_x=100, center_y=-300)
        arrow.released = True
        arrow_list: arcade.SpriteList[Arrow] = arcade.SpriteList()
        arrow_list.append(arrow)
        assert arrow in arrow_list
        arrow.arrows_movement()
        assert arrow not in arrow_list

        
  
        
    