from __future__ import annotations
from typing import Final
import arcade
import math
from player import *
import gameview
import monsters
import switches
import map_create.create_world as create_world
from abc import abstractmethod

WEAPON_LEFT_POSTION = -20
WEAPON_RIGHT_POSITION = 20

class Weapon(arcade.Sprite):
    """The class from which inherit the Sword and Bow Sprites
    """
    position_respecting_to_player : int
    """A little shift to the position of the weapon to make it look like it is actually held by the player sprite """

    def __init__(self,path_or_texture : str, scale : float, center_x : float, center_y : float,  angle : float) -> None:
        super().__init__(path_or_texture, scale, center_x, center_y, angle )
        self.position_respecting_to_player = 0

    def adapt_weapon_position(self, angle : float) -> None:
        """Shift the position of the weapon to make it look like it is actually held by the player sprite. Will
         shift it to the left of the player sprite if the cursor is in the left side of the screen and vice-versa for the right
           """
        if abs(math.degrees(angle)) > 90:
            self.position_respecting_to_player = -20
        else: 
            self.position_respecting_to_player = 20

    def weapon_movement(self, gameview : gameview.GameView) -> None:
        """Sets the position of the weapon and gives its orientation according to the cursor position"""
        self.center_x = gameview.world.player_sprite.center_x + self.position_respecting_to_player
        self.center_y = gameview.world.player_sprite.center_y - 10
        self.angle = -math.degrees(gameview.angle) + 45


class Lethal(arcade.Sprite):
    """Any Sprite that can kill monsters"""
    
    hit_sound : Final[arcade.Sound] = arcade.load_sound(":resources:/sounds/hit2.wav")
    """Sound played whenever a monster is killed"""

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
        self.__ARROW_SPEED += min(self.__charge_level, self.__MAXIMAL_CHARGE)


    def behavior_before_release(self, bow : Weapon, angle : float) -> None:
        # Angle de la flèche 
        self.angle = -math.degrees(angle) +45
        # Position statique de la flèche (même centre que l'arc)
        self.center_x = bow.center_x  
        self.center_y = bow.center_y 
        #Flèche de plus en plus chargée au cours du temps
        self.__charge_level *= 1.05

    def check_arrow_hits(self, world : create_world.World) -> None:
        """Actives the switch if the arrow collides with one

        Args:
            world (create_world.World): The class that contains the sprite lists
        """
        # Collision avec les interrupteurs
        hit_switches = arcade.check_for_collision_with_list(self, world.switches_list)
        if hit_switches:
            self.remove_from_sprite_lists()  # Détruit la flèche
            for switch in hit_switches:
                switch.on_hit_by_weapon(world.gates_dict)  # Active l'interrupteur
        
        # Collision avec les portails fermés
        hit_gates = arcade.check_for_collision_with_list(self, world.gates_list)
        if hit_gates:
            for gate in hit_gates:
                if not gate.state:  # Si le portail est fermé
                    self.remove_from_sprite_lists()

    def draw_trajectory(self, bow: Weapon, gameview: gameview.GameView) -> None:
        """Dessine une ligne en pointillé représentant la trajectoire estimée de la flèche"""
        # Calculer la vitesse exactement comme dans charge_level_increases_speed
        if self.__charge_level < self.__MAXIMAL_CHARGE:
            speed = self.__ARROW_SPEED + self.__charge_level
        else:
            speed = self.__ARROW_SPEED + self.__MAXIMAL_CHARGE

        # Calculer les composantes de vitesse initiale
        change_x = speed * math.cos(gameview.angle)
        change_y = speed * math.sin(gameview.angle)

        # Position initiale
        x = bow.center_x
        y = bow.center_y
        
        # Dessiner la trajectoire
        points = []
        current_change_y = change_y
        
        # Continuer jusqu'à ce que la flèche sorte de l'écran ou touche le sol
        while y > 0 and len(points) < 75:  # Limite de sécurité pour éviter une boucle infinie
            points.append((x, y))
            
            # Appliquer exactement la même physique que dans arrows_movement
            current_change_y -= self.__ARROW_GRAVITY
            x += change_x
            y += current_change_y

        # Dessiner une ligne pointillée
        for i in range(0, len(points) - 1, 2):
            start = points[i]
            end = points[i + 1]
            arcade.draw_line(start[0], start[1], end[0], end[1], arcade.color.GRAY, 2)

        # Point d'impact
        if points:
            arcade.draw_circle_filled(points[-1][0], points[-1][1], 4, arcade.color.GRAY)


        
