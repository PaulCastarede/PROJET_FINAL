from __future__ import annotations
import arcade
import Map_Create.world_sprites
from dataclasses import dataclass
import platforming.block_detecting
PLATFORM_SPEED = 1.5



class Platform(arcade.Sprite):
    platform_trajectory : Trajectory

    def __init__(self,path_or_texture : str, scale : float, center_x : float, center_y : float,  angle : float, platform_trajectory : Trajectory) -> None:
        super().__init__(path_or_texture, scale, center_x, center_y, angle )
        self.platform_trajectory = platform_trajectory
        self.change_x = PLATFORM_SPEED
        self.change_y = PLATFORM_SPEED

    def define_boundaries(self) -> None:
        self.boundary_right = self.center_x + self.platform_trajectory.right_movement*64
        self.boundary_left = self.center_x - self.platform_trajectory.left_movement*64
        self.boundary_top = self.center_y + self.platform_trajectory.up_movement*64
        self.boundary_bottom = self.center_y - self.platform_trajectory.down_movement*64
    
class Exit_Platform(Platform, Map_Create.world_sprites.Exit_Sprite):
    ...

class Lava_Platform(Platform, Map_Create.world_sprites.Lava_Sprite):
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







    
