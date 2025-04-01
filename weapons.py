import arcade
import math
from player import *

ARROW_SPEED = 15
"""Speed of the arrows, in pixels per frame"""

ARROW_GRAVITY = 0.3
"""Lateral speed of the arrows, in pixels per frame"""



class Arrow(arcade.Sprite):
    charge_level : int

    def __init__(self,path_or_texture : str, center_x : float, center_y : float, scale : float, angle : float) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y, angle )
        self.charge_level = 0

    #def increase_speed_according_to_charge(self) -> None:
        #if 
        #self.change_x += self
        


#from gameview import GameView


#def weapons_management(self : GameView, weapon : arcade.Sprite) -> None:



#def arrows_management(self : GameView, arrow : Arrow) -> None:
