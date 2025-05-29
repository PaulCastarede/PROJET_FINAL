from __future__ import annotations
from typing import Final
import arcade
from dataclasses import dataclass
from create_world import TILE_SIZE





class Platform(arcade.Sprite):
    """
    A moving, yet inanimate Sprite 

    """
    PLATFORM_SPEED : Final[float] = 1.5
    PLATFORM_ARCADE_GAP : Final[int] = 32
    """Looks like there is gap between where the boundary of the platform is and where it really is. Fixing it with this constant"""    
    __x_spawn : Final[float]
    __y_spawn : Final[float]
    platform_trajectory : Trajectory

    def __init__(self,path_or_texture : str, scale : float, center_x : float, center_y : float,  angle : float, platform_trajectory : Trajectory ) -> None:
        super().__init__(path_or_texture, scale, center_x, center_y, angle )
        self.platform_trajectory = platform_trajectory
        self.__x_spawn = self.center_x
        self.__y_spawn = self.center_y
        

    def define_boundaries(self) -> None:
        """Set to which point in the world the platform should go before changing direction"""
        self.change_x = self.PLATFORM_SPEED
        self.change_y = self.PLATFORM_SPEED

        if (self.platform_trajectory.right_movement == 0) and (self.platform_trajectory.left_movement == 0):
            #If the platform has no horizontal movement, has no horizontal speed and no left-right boundaries
            self.change_x = 0.0
            self.boundary_left = None
            self.boundary_right = None

        if (self.platform_trajectory.up_movement == 0) and (self.platform_trajectory.down_movement == 0):
            #If the platform has no vertical movement, has no vertical speed and no up-down boundaries"""
            self.change_y = 0.0
            self.boundary_bottom = None
            self.boundary_top = None

        #Define boundaries according to trajectory attribute
        self.boundary_left = self.__x_spawn - self.platform_trajectory.left_movement*TILE_SIZE - self.PLATFORM_ARCADE_GAP    
        self.boundary_right = self.__x_spawn + self.platform_trajectory.right_movement*TILE_SIZE + self.PLATFORM_ARCADE_GAP
        self.boundary_bottom = self.__y_spawn - self.platform_trajectory.down_movement*TILE_SIZE - self.PLATFORM_ARCADE_GAP  
        self.boundary_top = self.__y_spawn + self.platform_trajectory.up_movement*TILE_SIZE + self.PLATFORM_ARCADE_GAP
            


class Collidable_Platform(Platform):
    """A class of which inherits every sprite that might move, or not, and that have not spatial hash disabled
    """
    
    def movement(self) -> None:
        """Movement of platforms like Lava, Exit or Interruptors (not walls)
        """
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x  >= 0 and (self.boundary_right is not None):
            if self.center_x  + self.PLATFORM_ARCADE_GAP >= self.boundary_right:
                self.change_x *= -1
        elif (self.boundary_left is not None):
            if self.center_x - self.PLATFORM_ARCADE_GAP  <= self.boundary_left :
                self.change_x *= -1

        if self.change_y >= 0 and (self.boundary_top is not None):
            if self.center_y + self.PLATFORM_ARCADE_GAP >= self.boundary_top:
                self.change_y *= -1
        elif (self.boundary_bottom is not None):
            if self.center_y  + self.PLATFORM_ARCADE_GAP <= self.boundary_bottom :
                self.change_y *= -1

    

@dataclass
class Trajectory:
    """Dataclass that represents how much the platform block moves on each direction 
    """
    left_movement : float
    right_movement : float
    up_movement : float
    down_movement : float

    def __init__(self) -> None:
        self.left_movement = 0
        self.right_movement = 0
        self.up_movement = 0 
        self.down_movement = 0
