from __future__ import annotations
from typing import Final
import arcade
import Map_Create.world_sprites
from dataclasses import dataclass
import platforming.block_detecting
PLATFORM_SPEED = 1.5


class Platform(arcade.Sprite):
    __x_spawn : Final[float]
    __y_spawn : Final[float]
    platform_trajectory : Trajectory

    def __init__(self,path_or_texture : str, scale : float, center_x : float, center_y : float,  angle : float, platform_trajectory : Trajectory) -> None:
        super().__init__(path_or_texture, scale, center_x, center_y, angle )
        self.platform_trajectory = platform_trajectory
        self.__x_spawn = self.center_x
        self.__y_spawn = self.center_y
        self.change_x = PLATFORM_SPEED
        self.change_y = PLATFORM_SPEED

    def define_boundaries(self) -> None:
        self.boundary_right = self.__x_spawn + self.platform_trajectory.right_movement*platforming.block_detecting.TILE_SIZE
        self.boundary_left = self.__x_spawn - self.platform_trajectory.left_movement*platforming.block_detecting.TILE_SIZE
        self.boundary_top = self.__y_spawn + self.platform_trajectory.up_movement*platforming.block_detecting.TILE_SIZE
        self.boundary_bottom = self.__y_spawn - self.platform_trajectory.down_movement*platforming.block_detecting.TILE_SIZE


class Collidable_Platform(Platform):
    
    def movement(self) -> None:
        """Movement of platforms like Lava, Exit or Interruptors
        """
        #if not(self.platform_trajectory.left_movement == 0) and not(self.platform_trajectory.right_movement == 0):
        self.center_x += self.change_x
        if not(self.platform_trajectory.up_movement == 0) and not(self.platform_trajectory.down_movement == 0):    
            self.center_y += self.change_y
        if self.center_x > self.boundary_right or self.center_x < self.boundary_left :
            self.change_x *= -1
        if self.center_y > self.boundary_top or self.center_y < self.boundary_bottom :
            self.change_y *= -1
        

    
class Exit_Platform(Collidable_Platform, Map_Create.world_sprites.Exit_Sprite):
    ...

class Lava_Platform(Collidable_Platform, Map_Create.world_sprites.Lava_Sprite):
    ...

@dataclass
class Trajectory:
    """Dataclass that represents how much the platform block moves on each direction 
    """
    left_movement : int
    right_movement : int
    up_movement : int
    down_movement : int

    def __init__(self) -> None:
        self.left_movement = 0
        self.right_movement = 0
        self.up_movement = 0 
        self.down_movement = 0
