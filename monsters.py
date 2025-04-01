import arcade
import math
from typing import Final
import dataclasses
import random
from abc import abstractmethod

BAT_SPEED = 2
"""Speed of the bats, in pixels per frame"""

SLIMES_SPEED = 1
"""Speed of the slimes, in pixels per frame"""


slime_textures = []
#On ajoute le sprite du slime qui regarde à gauche
texture = arcade.load_texture(":resources:/images/enemies/slimeBlue.png")    
slime_textures.append(texture)   
#Et celui du slime regardant a droite                                    
texture = arcade.load_texture("assets/slimeBlue.png",)
slime_textures.append(texture)

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1



class Monster(arcade.Sprite):

    @abstractmethod
    def movement(self) -> None:
        ...
    



class Bat(Monster): 
    x_spawn : Final[float]
    y_spawn : Final[float]
    time_travel : int
    theta : float
    range : int

    def __init__(self, path_or_texture : str, center_x : float, center_y : float, scale : float) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y )
        self.x_spawn = self.center_x
        self.y_spawn = self.center_y
        self.time_travel = 0
        self.theta = 0
        self.range = 200
    
    #Calcul de la distance entre la position de la bat et son point d'apparition
    def distance_from_spawn(self) -> float: 
        return math.sqrt((self.center_x - self.x_spawn)**2 + (self.center_y - self.y_spawn)**2) 
    
    #DEPLACEMENT DES BATS
    def movement(self) -> None:
        #Modifie leur position en fonction de leur vitesse
        self.center_x += self.change_x
        self.center_y += self.change_y
        #vitesse selon x et selon y en fonction de l'angle de leur direction
        self.change_x = BAT_SPEED*math.cos(self.theta)
        self.change_y = BAT_SPEED*math.sin(self.theta)
        self.time_travel += 1       
        #Si la chauve-souris dépasse sa sphère d'action...
        if  self.distance_from_spawn() > self.range and self.time_travel > 30:
            self.theta += math.pi   #... elle fait demi-tour
            self.time_travel = 0
        if self.time_travel%15 == 0:
            self.theta = random.normalvariate(self.theta, math.pi/10)




class Slime(Monster):
    front : arcade.Sprite
    below : arcade.Sprite
    wall_list : arcade.SpriteList[arcade.Sprite]

    def __init__(self, path_or_texture : str, center_x : float, center_y : float, scale : float) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y )
        self.change_x = SLIMES_SPEED
        self.front = arcade.Sprite(scale = 0.005, center_x= self.center_x + self.change_x * 22 , center_y = self.center_y - 15 )
        self.below = arcade.Sprite(center_x = self.center_x + self.change_x * 85, center_y = self.center_y - 30 )

    def movement(self) -> None:
        self.center_x += self.change_x 
        self.below = arcade.Sprite(center_x = self.center_x + self.change_x * 85, center_y = self.center_y - 30 )
        below_collision = arcade.check_for_collision_with_list(self.below, self.wall_list)                                             #Check s'il y a un wall en dessous de l'endroit ou le slime se dirige                   
        self.front = arcade.Sprite(scale = 0.005, center_x= self.center_x + self.change_x * 22 , center_y = self.center_y - 15 )
        front_collision = arcade.check_for_collision_with_list(self.front, self.wall_list)                                             #Check s'il y a un obstacle en face du slime
        if not below_collision or front_collision:
            #S'il y a un obstacle, le slime fait demi-tour
            self.change_x *= -1  
        
        #On adapte le sprite du slime en fonction de sa direction
        if self.change_x < 0:
            self.texture = slime_textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = slime_textures[TEXTURE_RIGHT]
