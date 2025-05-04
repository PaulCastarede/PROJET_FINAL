from __future__ import annotations
import arcade
import math
import Map_Create.world_sprites
from enum import Enum
from enum import auto
from dataclasses import dataclass

PLATFORM_SPEED = 1.5
x = 0
y = 1


def detect_block(position_in_map : tuple[int,int], map_lines : list[list[str]], trajectory : Trajectory, moving_platforms_list : arcade.SpriteList[Platform] ) -> None:
    """_summary_

    Args:
        position_in_map (tuple[int,int]): _description_
        map_lines (list[list[str]]): _description_
        trajectory (Trajectory): _description_
        moving_platforms_list (arcade.SpriteList[Platform]): _description_

    Returns:
        _type_: _description_
    """

   
    match map_lines[position_in_map[y]][position_in_map[x]]:
        case "←" : 
            trajectory.left_movement += 1
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            detect_right_left((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)
        case "→" :
            trajectory.right_movement += 1
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            detect_right_left((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)
        case "↑" :
            trajectory.up_movement += 1
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            detect_up_down((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)

        case "↓" :
            trajectory.down_movement += 1
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            detect_up_down((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)

        case "=" :
            Grass = Platform(":resources:images/tiles/grassMid.png", scale=0.5,center_x=position_in_map[x]*64, center_y=(len(map_lines)-position_in_map[y])*64, platform_trajectory = trajectory, angle = 0)
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            moving_platforms_list.append(Grass)
            detect_surrounding(position_in_map , map_lines, trajectory , moving_platforms_list)

        case "-" :
            half_grass = Platform(":resources:images/tiles/grassHalf_mid.png", scale=0.5, center_x=position_in_map[x]*64, center_y=(len(map_lines)-position_in_map[y])*64, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            moving_platforms_list.append(half_grass)
            detect_surrounding(position_in_map , map_lines, trajectory , moving_platforms_list)
        case "x" :
            crate = Platform(":resources:images/tiles/boxCrate_double.png", scale=0.5, center_x=position_in_map[x]*64, center_y=(len(map_lines)-position_in_map[y])*64, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            moving_platforms_list.append(crate)
            detect_surrounding(position_in_map , map_lines, trajectory , moving_platforms_list)
        case "£" :
            lava = Platform(":resources:images/tiles/lava.png", scale=0.5, center_x=position_in_map[x]*64, center_y=(len(map_lines)-position_in_map[y])*64, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            moving_platforms_list.append(lava)
            detect_surrounding(position_in_map , map_lines, trajectory , moving_platforms_list)
        case "E" :
            exit = Exit_Platform(":resources:/images/tiles/signExit.png",  center_x=position_in_map[x]*64, center_y=(len(map_lines)-position_in_map[y])
                            *64, scale = 0.5, platform_trajectory = trajectory, angle = 0)
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            moving_platforms_list.append(exit)
            detect_surrounding(position_in_map , map_lines, trajectory , moving_platforms_list)
        case _:
            return None


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

@dataclass
class Trajectory:
    left_movement : int
    right_movement : int
    up_movement : int
    down_movement : int

    def __init__(self) -> None:
        self.left_movement = 0
        self.right_movement = 0
        self.up_movement = 0 
        self.down_movement = 0


def detect_surrounding(position_in_map : tuple[int,int], map_lines : list[list[str]], trajectory : Trajectory, moving_platforms_list : arcade.SpriteList[Platform] ) -> None:
    """Applies detect_block but on the 4 sides of the sprite

    Args:
        position_in_map (tuple[int,int]): _description_
        map_lines (list[list[str]]): _description_
        trajectory (Trajectory): _description_
        moving_platforms_list (arcade.SpriteList[Platform]): _description_
    """
    detect_up_down((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)
    detect_right_left((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)

def detect_right_left(position_in_map : tuple[int,int], map_lines : list[list[str]], trajectory : Trajectory, moving_platforms_list : arcade.SpriteList[Platform] ) -> None:
    if position_in_map[x] < len(map_lines[position_in_map[y]]):
        detect_block((position_in_map[x]+1,position_in_map[y]), map_lines, trajectory, moving_platforms_list)
    if position_in_map[x] > 0:
        detect_block((position_in_map[x]-1,position_in_map[y]), map_lines, trajectory, moving_platforms_list)

def detect_up_down(position_in_map : tuple[int,int], map_lines : list[list[str]], trajectory : Trajectory, moving_platforms_list : arcade.SpriteList[Platform] ) -> None:
    if position_in_map[y] > 0:
        detect_block((position_in_map[x],position_in_map[y]-1), map_lines, trajectory, moving_platforms_list)
    if position_in_map[y] < len(map_lines):
        detect_block((position_in_map[x],position_in_map[y]+1), map_lines, trajectory, moving_platforms_list)