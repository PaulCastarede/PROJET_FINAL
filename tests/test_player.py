from __future__ import annotations
import arcade
from typing import Final
from player import Player
import gameview
from world_sprites_types.coins import Coin
from monsters import Bat, Slime
from gameview import GameView

class TestPlayer:
    window: arcade.Window
    player: Player
    gameview: GameView

    def setup_method(self) -> None:
        self.window = arcade.Window(1280, 720, "Test Window")
        original_ambient_music = GameView.ambient_music
        self.gameview = GameView()
        if self.gameview.music_playback:
            arcade.stop_sound(self.gameview.music_playback)
            self.gameview.music_playback = None # type: ignore
        # Nous avons été obligés de faire cela car autrement le son ne peut pas être arrêté    
        self.player = Player(respawn_map="map1.txt", center_x=100, center_y=100)
        self.gameview.world.player_sprite = self.player
        self.gameview.world.player_sprite_list.append(self.player)
        
        self.gameview.world.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.gameview.world.wall_list,
            gravity_constant=1.0
        )
        
        
    def test_player_movement(self) -> None:
        # Test du mouvement vers la droite
        initial_x: float = self.player.center_x
        self.gameview.right_pressed = True
        
        for _ in range(5):  
            self.player.movement(self.gameview)
            self.gameview.world.physics_engine.update()  # Important : mettre à jour le moteur physique
        
        assert self.player.change_x > 0  
        assert self.player.center_x > initial_x  
        
        # Test du mouvement vers la gauche
        initial_x = self.player.center_x
        self.gameview.right_pressed = False
        self.gameview.left_pressed = True
        
        for _ in range(5):
            self.player.movement(self.gameview)
            self.gameview.world.physics_engine.update()
        
        assert self.player.change_x < 0
        assert self.player.center_x < initial_x 
        
    def test_player_jump(self) -> None:
        initial_change_y: float = self.player.change_y
        self.player.jump()
        assert self.player.change_y > initial_change_y
        assert self.player.change_y == self.player.PLAYER_JUMP_SPEED
        
    def test_player_collect_coins(self) -> None:
        self.gameview.world.coins_list.clear()
        coin: Coin = Coin(center_x=self.player.center_x, center_y=self.player.center_y)
        self.gameview.world.coins_list.append(coin)
        initial_coins: int = self.player.coins_possessed
        
        self.player.collect_coins(self.gameview)
        assert self.player.coins_possessed > initial_coins
        assert len(self.gameview.world.coins_list) == 0
        
    def test_player_dies_from_monster(self) -> None:
        monster: Bat = Bat(
            path_or_texture="Assets/kenney-extended-enemies-png/bat.png",
            center_x=self.player.center_x,
            center_y=self.player.center_y,
            scale=0.5
        )
        self.gameview.world.monsters_list.append(monster)
        initial_lives: int = self.player.lives
        
        self.player.dies(self.gameview)
        assert self.player.lives < initial_lives
        
    def test_player_respawn(self) -> None:
        initial_x: float = self.player.center_x
        initial_y: float = self.player.center_y
        self.player.respawn_point = (200, 200)
        
        self.player.respawn(self.gameview)
        assert self.player.center_x == 200
        assert self.player.center_y == 200
        
    def test_player_lives_from_coins(self) -> None:
        self.player.coins_possessed = 9
        coin: Coin = Coin(center_x=self.player.center_x, center_y=self.player.center_y)
        self.gameview.world.coins_list.append(coin)
        initial_lives: int = self.player.lives
        
        self.player.collect_coins(self.gameview)
        assert self.player.lives > initial_lives
        assert self.player.coins_possessed == 0

    def teardown_method(self) -> None:
        self.window.close()