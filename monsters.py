import arcade
import math
from typing import Final
import random
from abc import abstractmethod


slime_textures = []
#On ajoute le sprite du slime qui regarde à gauche
texture = arcade.load_texture(":resources:/images/enemies/slimeBlue.png")    
slime_textures.append(texture)   
#Et celui du slime regardant a droite                                    
texture = arcade.load_texture("assets/slimeBlue.png")
slime_textures.append(texture)

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1



class Monster(arcade.Sprite):

    @abstractmethod
    def movement(self) -> None:
        ...
    


class Bat(Monster): 
    BAT_SPEED : Final[float] = 2
    """Speed of the bats, in pixels per frame"""
    __range : Final[int] = 200
    """maximal distance between the bat and its spawn point"""
    __x_spawn : Final[float]
    __y_spawn : Final[float]
    __time_travel : int
    __theta : float
    

    def __init__(self, path_or_texture : str = "assets/kenney-extended-enemies-png/bat.png", center_x : float = 0, center_y : float = 0, scale : float = 0.5) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y )
        self.__x_spawn = self.center_x
        self.__y_spawn = self.center_y
        self.__time_travel = 0
        self.__theta = 0
    
    #Calcul de la distance entre la position de la bat et son point d'apparition
    @property
    def distance_from_spawn(self) -> float: 
        return math.sqrt((self.center_x - self.__x_spawn)**2 + (self.center_y - self.__y_spawn)**2) 
    
    #DEPLACEMENT DES BATS
    def movement(self) -> None:
        #Modifie leur position en fonction de leur vitesse
        self.center_x += self.change_x
        self.center_y += self.change_y
        #vitesse selon x et selon y en fonction de l'angle de leur direction
        self.change_x = self.BAT_SPEED*math.cos(self.__theta)
        self.change_y = self.BAT_SPEED*math.sin(self.__theta)
        self.__time_travel += 1       
        #Si la chauve-souris dépasse sa sphère d'action...
        if  self.distance_from_spawn > self.__range and self.__time_travel > 30:
            self.__theta += math.pi   #... elle fait demi-tour
            self.__time_travel = 0
        if self.__time_travel%15 == 0:
            self.__theta = random.normalvariate(self.__theta, math.pi/10)



class Slime(Monster):
    SLIMES_SPEED : Final[int] = 1
    """Speed of the slimes, in pixels per frame"""  
    __front : arcade.Sprite
    __below : arcade.Sprite
    __wall_list : Final[arcade.SpriteList[arcade.Sprite]]

    def __init__(self,  wall_list : arcade.SpriteList[arcade.Sprite], path_or_texture : str = "assets/slimeBlue.png", center_x : float = 0, center_y : float = 0, scale : float = 0.5) -> None:
        super().__init__(path_or_texture, scale, center_x, center_y)
        self.__wall_list = wall_list
        self.change_x = self.SLIMES_SPEED
        self.__front = arcade.Sprite(scale = 0.005, center_x= self.center_x + self.change_x * 22 , center_y = self.center_y - 15 )
        self.__below = arcade.Sprite(center_x = self.center_x + self.change_x * 85, center_y = self.center_y - 30 )

    def movement(self) -> None:
        self.center_x += self.change_x 
        #Checker s'il y a un wall en dessous de l'endroit ou le slime se dirige    
        self.__below = arcade.Sprite(center_x = self.center_x + self.change_x * 85, center_y = self.bottom)
        below_collision = arcade.check_for_collision_with_list(self.__below, self.__wall_list)       
        #Checker s'il y a un obstacle en face du slime                                                    
        self.__front = arcade.Sprite(scale = 0.005, center_x= self.center_x + self.change_x * 22 , center_y = self.center_y - 15 )
        front_collision = arcade.check_for_collision_with_list(self.__front, self.__wall_list)                                             
        if not below_collision or front_collision:
            #S'il y a un obstacle, le slime fait demi-tour
            self.change_x *= -1  
        
        #On adapte le sprite du slime en fonction de sa direction
        if self.change_x < 0:
            self.texture = slime_textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = slime_textures[TEXTURE_RIGHT]
