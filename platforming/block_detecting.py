from __future__ import annotations
import math
import create_world
import platforming.platforms

from world_sprites_types.checkpoint import Checkpoint
from world_sprites_types.exit import Exit_Sprite
from world_sprites_types.lava import Lava_Sprite

from dataclasses import dataclass

TILE_SIZE = 64.0
"""64 pixels par element"""

TOO_MANY_ARROWS_ERROR = RuntimeError("There are two or more sets of the same arrow linked to the same platform")

x_index: int = 0
y_index: int = 1

def detect_block(position_in_map : tuple[int,int],
                map_lines : list[list[str]], 
                trajectory : platforming.platforms.Trajectory, 
                world : create_world.World,
                map_path : str,
                force_detection : bool = False ) -> None:       
    """

    Args:
        position_in_map (tuple[int,int]): coord (x,y) in the map-matrix
        map_lines (list[list[str]]): the map repr as a matrix of str
        trajectory (Trajectory): How much the platform moves on each direction
        world (map_create.create_world.World)
        force_detection (bool) : Used to make sure the directionnal arrows are linked to a platform (or raises an error)
    Returns:
        Platforms: Adds the platforms block detected to a sprite list
    """

    match map_lines[position_in_map[y_index]][position_in_map[x_index]]:
        case "←" : 
            if trajectory.left_movement > 0:
                raise TOO_MANY_ARROWS_ERROR
            trajectory.left_movement += 1
            detect_arrows_set((position_in_map[x_index], position_in_map[y_index]), map_lines, trajectory, world, "←")
            detect_right((int(position_in_map[x_index]+trajectory.left_movement-1), position_in_map[y_index]), map_lines, trajectory, world, map_path, force_detection=True)
        case "→" :
            if trajectory.right_movement > 0:
                raise TOO_MANY_ARROWS_ERROR
            trajectory.right_movement += 1
            detect_arrows_set((position_in_map[x_index],position_in_map[y_index]), map_lines, trajectory, world, "→")
            detect_left((position_in_map[x_index],position_in_map[y_index]), map_lines, trajectory, world, map_path, force_detection=True)
        case "↑" :
            if trajectory.up_movement > 0:
                raise TOO_MANY_ARROWS_ERROR
            trajectory.up_movement += 1
            detect_arrows_set((position_in_map[x_index],position_in_map[y_index]), map_lines, trajectory, world, "↑")
            detect_down((position_in_map[x_index], int(position_in_map[y_index]+trajectory.up_movement-1)), map_lines, trajectory, world, map_path, force_detection=True)
        case "↓" :
            if trajectory.down_movement > 0:
                raise TOO_MANY_ARROWS_ERROR
            trajectory.down_movement += 1
            detect_arrows_set((position_in_map[x_index],position_in_map[y_index]), map_lines, trajectory, world, "↓")
            detect_up((position_in_map[x_index],position_in_map[y_index]), map_lines, trajectory, world, map_path, force_detection=True)

        case "=" :
            Grass = platforming.platforms.Platform(":resources:images/tiles/grassMid.png", scale=0.5,center_x=position_in_map[x_index]*TILE_SIZE, center_y=(len(map_lines)-1-position_in_map[y_index])*TILE_SIZE, platform_trajectory = trajectory, angle = 0)
            map_lines[position_in_map[y_index]][position_in_map[x_index]] = " "
            world.moving_platforms_list.append(Grass)
            detect_surrounding(position_in_map , map_lines, trajectory , world, map_path)

        case "-" :
            half_grass = platforming.platforms.Platform(":resources:images/tiles/grassHalf_mid.png", scale=0.5, center_x=position_in_map[x_index]*TILE_SIZE, center_y=(len(map_lines)-1-position_in_map[y_index])*TILE_SIZE, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y_index]][position_in_map[x_index]] = " "
            world.moving_platforms_list.append(half_grass)
            detect_surrounding(position_in_map , map_lines, trajectory , world, map_path)
        case "x" :
            crate = platforming.platforms.Platform(":resources:images/tiles/boxCrate_double.png", scale=0.5, center_x=position_in_map[x_index]*TILE_SIZE, center_y=(len(map_lines)-1-position_in_map[y_index])*TILE_SIZE, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y_index]][position_in_map[x_index]] = " "
            world.moving_platforms_list.append(crate)
            detect_surrounding(position_in_map , map_lines, trajectory , world, map_path)
        case "£" :
            lava = Lava_Sprite(":resources:images/tiles/lava.png", scale=0.5, center_x=position_in_map[x_index]*TILE_SIZE, center_y=(len(map_lines)-1-position_in_map[y_index])*TILE_SIZE, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y_index]][position_in_map[x_index]] = " "
            world.no_go_list.append(lava)
            detect_surrounding(position_in_map , map_lines, trajectory , world, map_path)
        case "E" :
            exit = Exit_Sprite(":resources:/images/tiles/signExit.png",  center_x=position_in_map[x_index]*TILE_SIZE, center_y=(len(map_lines)-1-position_in_map[y_index])*TILE_SIZE, scale = 0.5, platform_trajectory = trajectory, angle = 0)
            map_lines[position_in_map[y_index]][position_in_map[x_index]] = " "
            world.exit_list.append(exit)
            world.set_exit = True
            detect_surrounding(position_in_map , map_lines, trajectory , world, map_path)
        case "C":
            checkpoint = Checkpoint(linked_map = map_path, center_x=position_in_map[x_index]*TILE_SIZE, center_y=(len(map_lines)-1-position_in_map[y_index])*TILE_SIZE-6, platform_trajectory = trajectory)
            map_lines[position_in_map[y_index]][position_in_map[x_index]] = " "
            world.checkpoint_list.append(checkpoint)
            detect_surrounding(position_in_map , map_lines, trajectory , world, map_path)
        case "^":
            for switch in world.switches_list:
                if switch.center_x == position_in_map[x_index]*TILE_SIZE and switch.center_y == (len(map_lines)-1-position_in_map[y_index])*TILE_SIZE:
                    switch.platform_trajectory = trajectory
        case _:
            if force_detection and math.sqrt(trajectory.right_movement**2 + trajectory.left_movement**2 + trajectory.up_movement**2 + trajectory.down_movement**2) == trajectory.right_movement + trajectory.down_movement + trajectory.left_movement + trajectory.up_movement:
                # This ugly condition is the only way we found to check (in one-line) if there is exactly 0 or 1 trajectory direction different to 0
                # Indeed, if there is more than 1 direction it means there was a platform that has already been removed due to other arrow sets
                # Which implies that the arrow set is actually linked to a platform, no more appearing
                raise RuntimeError("Some arrow set is not linked to any platform")
            return None
        

def detect_right(position_in_map : tuple[int,int], 
                 map_lines : list[list[str]], 
                 trajectory : platforming.platforms.Trajectory, 
                 world : create_world.World,
                 map_path : str,
                 force_detection : bool = False ) -> None:
    """Applies detect_block to the right tile
    """
    if position_in_map[x_index] < len(map_lines[position_in_map[y_index]]) - 1 and not(map_lines[position_in_map[y_index]][position_in_map[x_index]+1] in ("↓","←","↑" )): 
        detect_block((position_in_map[x_index]+1,position_in_map[y_index]), map_lines, trajectory, world, map_path, force_detection)

def detect_left(position_in_map : tuple[int,int], 
                map_lines : list[list[str]], 
                trajectory : platforming.platforms.Trajectory, 
                world : create_world.World,
                map_path : str,
                force_detection : bool = False ) -> None:
    """Applies detect_block to the left tile"""
    if position_in_map[x_index] > 0 and not(map_lines[position_in_map[y_index]][position_in_map[x_index]-1] in  ("→", "↓" , "↑")): 
        detect_block((position_in_map[x_index]-1,position_in_map[y_index]), map_lines, trajectory, world, map_path, force_detection)

def detect_down(position_in_map : tuple[int,int], 
                map_lines : list[list[str]], 
                trajectory : platforming.platforms.Trajectory, 
                world : create_world.World,
                map_path : str,
                force_detection : bool = False  ) -> None:
    """Applies detect_block to the bottom tile
    """
    if position_in_map[y_index] < len(map_lines) - 1 and not(map_lines[position_in_map[y_index]+1][position_in_map[x_index]] in  ("→", "←", "↑")): 
        detect_block((position_in_map[x_index],position_in_map[y_index]+1), map_lines, trajectory, world, map_path, force_detection)

def detect_up(position_in_map : tuple[int,int], 
              map_lines : list[list[str]], 
              trajectory : platforming.platforms.Trajectory, 
              world : create_world.World,
              map_path : str,
              force_detection : bool = False   ) -> None:   
    """Applies detect_block to the top tile
    """    
    if position_in_map[y_index] > 0 and not(map_lines[position_in_map[y_index]-1][position_in_map[x_index]] in ("→", "←", "↓")):
        detect_block((position_in_map[x_index],position_in_map[y_index]-1), map_lines, trajectory, world, map_path, force_detection)


def detect_surrounding(position_in_map : tuple[int,int], 
                       map_lines : list[list[str]], 
                       trajectory : platforming.platforms.Trajectory, 
                       world : create_world.World,
                        map_path : str ) -> None:
    """Applies detect_block but on the 4 sides of the sprite

    Args:
        position_in_map (tuple[int,int]): coord (x,y) in the map-matrix
        map_lines (list[list[str]]): the map repr as a matrix of str
        trajectory (Trajectory): How much the platform moves on each direction
        moving_platforms_list (arcade.SpriteList[Platform]): the block of platform "analysed" by the function
    """
    
    detect_up((position_in_map[x_index],position_in_map[y_index]), map_lines, trajectory, world, map_path)
    detect_down((position_in_map[x_index],position_in_map[y_index]), map_lines, trajectory, world, map_path)
    detect_right((position_in_map[x_index],position_in_map[y_index]), map_lines, trajectory, world, map_path)
    detect_left((position_in_map[x_index],position_in_map[y_index]), map_lines, trajectory, world, map_path)


def detect_arrows_set(position_in_map : tuple[int,int], 
                      map_lines : list[list[str]], 
                      trajectory : platforming.platforms.Trajectory, 
                      world : create_world.World, 
                      char : str ) -> None:
    """Detect how long a set of the same arrow is

    Args:
        position_in_map (tuple[int,int]): coord (x,y) in the map-matrix
        map_lines (list[list[str]]): the map repr as a matrix of str
        trajectory (Trajectory): How much the platform moves on each direction
        moving_platforms_list (arcade.SpriteList[Platform]): the block of platform "analysed" by the function
        char (str): the arrow of which we want to return the length of the set
        """
    map_lines[position_in_map[y_index]][position_in_map[x_index]] = " "
    match char: 
        case "→":
            if position_in_map[x_index] < len(map_lines[position_in_map[y_index]]):
                if map_lines[position_in_map[y_index]][position_in_map[x_index]+1] == "→":
                    trajectory.right_movement += 1
                    detect_arrows_set((position_in_map[x_index]+1,position_in_map[y_index]), map_lines, trajectory, world,"→" )
        case  "←" : 
            if map_lines[position_in_map[y_index]][position_in_map[x_index]+1] == "←":
                trajectory.left_movement += 1
                detect_arrows_set((position_in_map[x_index]+1,position_in_map[y_index]), map_lines, trajectory, world,"←" )
        case "↑" :
            if map_lines[position_in_map[y_index]+1][position_in_map[x_index]] == "↑":
                trajectory.up_movement += 1
                detect_arrows_set((position_in_map[x_index],position_in_map[y_index]+1), map_lines, trajectory, world,"↑" )
        case "↓" :
            if position_in_map[y_index] < len(map_lines):
                if map_lines[position_in_map[y_index]+1][position_in_map[x_index]] == "↓":
                    trajectory.down_movement += 1
                    detect_arrows_set((position_in_map[x_index],position_in_map[y_index]+1), map_lines, trajectory, world,"↓" )   