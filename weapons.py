from __future__ import annotations
import arcade
import math
from player import *
import gameview
import create_world
from abc import abstractmethod

SWORD_LEFT_POSTION = -20
SWORD_RIGHT_POSITION = 20

ARROW_SPEED = 15
"""Speed of the arrows, in pixels per frame"""

ARROW_GRAVITY = 0.3
"""Lateral speed of the arrows, in pixels per frame"""

class Weapon(arcade.Sprite):
    position_respecting_to_player : int

    def __init__(self,path_or_texture : str, scale : float, center_x : float, center_y : float,  angle : float) -> None:
        super().__init__(path_or_texture, scale, center_x, center_y, angle )
        self.position_respecting_to_player = 0

    def adapt_weapon_position(self, angle : float) -> None:
        if abs(math.degrees(angle)) > 90:
            self.position_respecting_to_player = -20
        else: 
            self.position_respecting_to_player = 20

    def manage(self, gameview : gameview.GameView) -> None:
        self.center_x = gameview.world.player_sprite.center_x + self.position_respecting_to_player
        self.center_y = gameview.world.player_sprite.center_y - 10
        self.angle = -math.degrees(gameview.angle) + 45


class Lethal(arcade.Sprite):
    
    @abstractmethod
    def kills(self, gameview : gameview.GameView) -> None:
        ...


class Bow(Weapon):

    def __init__(self,path_or_texture : str, center_x : float, center_y : float, scale : float, angle : float ) -> None:
        super().__init__(path_or_texture, center_x, center_y, scale, angle)
        self.position_respecting_to_player = 0

 

class Sword(Weapon, Lethal):

    def __init__(self,path_or_texture : str, center_x : float, center_y : float, scale : float, angle : float) -> None:
        super().__init__(path_or_texture, center_x, center_y, scale, angle )
        self.position_respecting_to_player = 0

    def kills(self, gameview : gameview.GameView) -> None:
        # Vérifier les collisions avec les monstres
        touched_monsters = arcade.check_for_collision_with_list(self, gameview.world.monsters_list)
        for monster in touched_monsters:
            monster.remove_from_sprite_lists()
            gameview.score += 1
            arcade.play_sound(gameview.coin_sound)


    

    


class Arrow(Lethal):
    charge_level : float
    released : bool

    def __init__(self,path_or_texture : str, center_x : float, center_y : float, scale : float, angle : float) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y, angle )
        self.charge_level = 0
        self.released = False


    def kills(self, gameview : gameview.GameView) -> None:
        # Vérifier les collisions avec les monstres
        touched_monsters = arcade.check_for_collision_with_list(self, gameview.world.monsters_list)
        for monster in touched_monsters:
            monster.remove_from_sprite_lists()
            self.remove_from_sprite_lists()
            gameview.score += 1
            arcade.play_sound(gameview.coin_sound)


    def arrows_movement(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> None:
        if self.released:
            # Appliquer la physique
            self.change_y -= ARROW_GRAVITY
            self.center_x += self.change_x
            self.center_y += self.change_y
            # Orienter la flèche en fonction de sa direction
            if self.change_x >0 :
                self.angle = math.degrees(math.acos(self.change_y/(math.sqrt((self.change_x)**2 +(self.change_y)**2)))) -45
            elif self.change_x < 0:
                self.angle = math.degrees(math.asin(self.change_y/(math.sqrt((self.change_x)**2 +(self.change_y)**2)))) +225
            # Vérifier les collisions avec les murs
            if arcade.check_for_collision_with_list(self, wall_list):
                self.remove_from_sprite_lists()


    def charge_level_increases_speed(self) -> None:
        if self.charge_level < 15:
            self.change_x+= self.charge_level
            self.change_y += self.charge_level
        else:
            self.change_x+= 15
            self.change_y += 15
        
