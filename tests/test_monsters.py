from __future__ import annotations
import arcade
from typing import Final
import pytest

from monsters import Bat, Slime, Monster
from weapons import Arrow, Weapon, Sword
from gameview import GameView as GameView
import create_world
from world_sprites_types.coins import Coin

class TestMonsters:
    window: arcade.Window
    gameview: GameView

    def setup_method(self) -> None:
        self.window = arcade.Window(1280, 720, "Test Window")
        original_ambient_music = GameView.ambient_music
        self.gameview = GameView()
        if self.gameview.music_playback:
            arcade.stop_sound(self.gameview.music_playback)
            self.gameview.music_playback = None # type: ignore
        # Nous avons été obligés de faire cela car autrement le son ne peut pas être arrêté
   
    def test_slime_wall_collision(self) -> None:
        wall = arcade.Sprite(
            ":resources:images/tiles/grassMid.png",
            scale=0.5,
            center_x=100,
            center_y=100
        )
        self.gameview.world.wall_list.append(wall)
        
        slime = Slime(
            wall_list=self.gameview.world.wall_list,
            path_or_texture="assets/slimeBlue.png",
            center_x=97,
            center_y=100)
        self.gameview.world.monsters_list.append(slime)
        initial_direction = slime.change_x
        slime.movement()
        assert slime.change_x == -initial_direction

    def test_arrow_kills_slime(self) -> None:
        slime = Slime(
            wall_list=self.gameview.world.wall_list,
            path_or_texture="assets/slimeBlue.png",
            center_x=100,
            center_y=100
        )
        self.gameview.world.monsters_list.append(slime)
        
        arrow = Arrow(
            path_or_texture="assets/kenney-voxel-items-png/arrow.png",
            center_x=100,
            center_y=100
        )
        arrow_list: arcade.SpriteList[Arrow] = arcade.SpriteList()
        arrow_list.append(arrow)
        
        initial_monsters = len(self.gameview.world.monsters_list)
        arrow.kills_monsters(self.gameview.world.monsters_list, self.gameview.world.coins_list)
        
        assert len(self.gameview.world.monsters_list) < initial_monsters
        assert arrow not in arrow_list

    def test_arrow_kills_bat(self) -> None:
        bat = Bat(
            path_or_texture="assets/kenney-extended-enemies-png/bat.png",
            center_x=100,
            center_y=100
        )
        self.gameview.world.monsters_list.append(bat)
        
        arrow = Arrow(
            path_or_texture="assets/kenney-voxel-items-png/arrow.png",
            center_x=100,
            center_y=100
        )
        arrow_list: arcade.SpriteList[Arrow] = arcade.SpriteList()
        arrow_list.append(arrow)
        
        initial_monsters = len(self.gameview.world.monsters_list)
        arrow.kills_monsters(self.gameview.world.monsters_list, self.gameview.world.coins_list)
        
        assert len(self.gameview.world.monsters_list) < initial_monsters
        assert arrow not in arrow_list

    def test_sword_kills_monsters(self) -> None:
        slime = Slime(
            wall_list=self.gameview.world.wall_list,
            path_or_texture="assets/slimeBlue.png",
            center_x=100,
            center_y=100
        )
        bat = Bat(
            path_or_texture="assets/kenney-extended-enemies-png/bat.png",
            center_x=100,
            center_y=100
        )
        self.gameview.world.monsters_list.clear()

        self.gameview.world.monsters_list.append(slime)
        self.gameview.world.monsters_list.append(bat)
        
        sword = Sword(
            path_or_texture="assets/kenney-voxel-items-png/sword_silver.png",
            scale=0.5,
            center_x=100,
            center_y=100,
            angle=0
        )
        
        initial_monsters = len(self.gameview.world.monsters_list)
        assert initial_monsters == 2  

        sword.kills_monsters(self.gameview.world.monsters_list, self.gameview.world.coins_list)
        
        assert len(self.gameview.world.monsters_list) < initial_monsters
        assert len(self.gameview.world.monsters_list) == 0

    
    def teardown_method(self) -> None:
        self.window.close()
