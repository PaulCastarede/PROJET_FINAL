from __future__ import annotations
from typing import Final
import arcade
import math
from player import *
import gameview
import monsters
from abc import abstractmethod

WEAPON_LEFT_POSTION = -20
WEAPON_RIGHT_POSITION = 20

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

    def weapon_movement(self, gameview : gameview.GameView) -> None:
        self.center_x = gameview.world.player_sprite.center_x + self.position_respecting_to_player
        self.center_y = gameview.world.player_sprite.center_y - 10
        self.angle = -math.degrees(gameview.angle) + 45


class Lethal(arcade.Sprite):
    hit_sound : Final[arcade.Sound] = arcade.load_sound(":resources:/sounds/hit2.wav")

    def kills_monsters(self, monsters_list : arcade.SpriteList[monsters.Monster]) -> None:
        # Vérifier les collisions avec les monstres
        for monster in arcade.check_for_collision_with_list(self, monsters_list):
            monster.remove_from_sprite_lists()
            arcade.play_sound(self.hit_sound)
            if type(self) is Arrow:
                self.remove_from_sprite_lists()


class Bow(Weapon):
    ...

 

class Sword(Weapon, Lethal):
    ...
    


class Arrow(Lethal):
    __ARROW_SPEED : float = 5
    """Speed of the arrows, in pixels per frame"""
    __ARROW_GRAVITY : Final[float] = 0.25
    """Lateral speed of the arrows, in pixels per frame"""
    __charge_level : float
    __MAXIMAL_CHARGE : Final[float] = 12
    released : bool

    def __init__(self, path_or_texture : str = "assets/kenney-voxel-items-png/arrow.png", center_x : float = 0, center_y : float = 0, scale : float = 0.4, angle : float = 0) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y, angle)
        self.__charge_level = 1
        self.released = False

    @property 
    def speed(self) -> float :
        return self.__ARROW_SPEED

    def arrows_movement(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> None:
        if self.released:
            # Appliquer la physique
            self.change_y -= self.__ARROW_GRAVITY
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
            if (self.center_y < -250):
                self.remove_from_sprite_lists()


    def charge_level_increases_speed(self) -> None:
        """Fait en sorte que plus l'arc est bandé (plus on a gardé le clic gauche appuyé longtemps), plus la flèche est chargée et plus elle part vite
        """
        if self.__charge_level < self.__MAXIMAL_CHARGE:
            self.__ARROW_SPEED += self.__charge_level 
        else:
            self.__ARROW_SPEED += self.__MAXIMAL_CHARGE


    def behavior_before_release(self, bow : Weapon) -> None:
        # Angle de la flèche 
        self.angle = bow.angle + 80
        # Position statique de la flèche (même centre que l'arc)
        self.center_x = bow.center_x  
        self.center_y = bow.center_y 
        #Flèche de plus en plus chargée au cours du temps
        self.__charge_level *= 1.05



        
