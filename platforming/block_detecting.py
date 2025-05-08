from __future__ import annotations
import arcade
import math
import Map_Create.create_world
import platforming.platforms
import Map_Create
from dataclasses import dataclass

TILE_SIZE = 64.0
"""64 pixels par element"""

TOO_MANY_ARROWS_ERROR : RuntimeError = "There is two set of the same arrow linked to the same platform"

x = 0
y = 1

def detect_block(position_in_map : tuple[int,int],
                map_lines : list[list[str]], 
                trajectory : platforming.platforms.Trajectory, 
                world : Map_Create.create_world.World,
                force_detection : bool = False ) -> None:       
    """

    Args:
        position_in_map (tuple[int,int]): coord (x,y) in the map-matrix
        map_lines (list[list[str]]): the map repr as a matrix of str
        trajectory (Trajectory): How much the platform moves on each direction
        world (Map_Create.create_world.World)
        force_detection (bool) : Used to make sure the directionnal arrows are linked to a platform (or raises an error)
    Returns:
        Platforms: Adds the platforms block detected to a sprite list
    """

    match map_lines[position_in_map[y]][position_in_map[x]]:
        case "←" : 
            if trajectory.left_movement > 0:
                raise TOO_MANY_ARROWS_ERROR
            trajectory.left_movement += 1
            detect_arrows_set((position_in_map[x], position_in_map[y]), map_lines, trajectory, world, "←")
            detect_right((position_in_map[x]+trajectory.left_movement-1,position_in_map[y]), map_lines, trajectory, world, force_detection=True)
        case "→" :
            if trajectory.right_movement > 0:
                raise TOO_MANY_ARROWS_ERROR
            trajectory.right_movement += 1
            detect_arrows_set((position_in_map[x],position_in_map[y]), map_lines, trajectory, world, "→")
            detect_left((position_in_map[x],position_in_map[y]), map_lines, trajectory, world, force_detection=True)
        case "↑" :
            if trajectory.up_movement > 0:
                raise TOO_MANY_ARROWS_ERROR
            trajectory.up_movement += 1
            detect_arrows_set((position_in_map[x],position_in_map[y]), map_lines, trajectory, world, "↑")
            detect_down((position_in_map[x],position_in_map[y]+trajectory.up_movement-1), map_lines, trajectory, world, force_detection=True)
        case "↓" :
            if trajectory.down_movement > 0:
                raise TOO_MANY_ARROWS_ERROR
            trajectory.down_movement += 1
            detect_arrows_set((position_in_map[x],position_in_map[y]), map_lines, trajectory, world, "↓")
            detect_up((position_in_map[x],position_in_map[y]), map_lines, trajectory, world, force_detection=True)

        case "=" :
            Grass = platforming.platforms.Platform(":resources:images/tiles/grassMid.png", scale=0.5,center_x=position_in_map[x]*TILE_SIZE, center_y=(len(map_lines)-position_in_map[y])*TILE_SIZE, platform_trajectory = trajectory, angle = 0)
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            world.moving_platforms_list.append(Grass)
            detect_surrounding(position_in_map , map_lines, trajectory , world)

        case "-" :
            half_grass = platforming.platforms.Platform(":resources:images/tiles/grassHalf_mid.png", scale=0.5, center_x=position_in_map[x]*TILE_SIZE, center_y=(len(map_lines)-position_in_map[y])*TILE_SIZE, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            world.moving_platforms_list.append(half_grass)
            detect_surrounding(position_in_map , map_lines, trajectory , world)
        case "x" :
            crate = platforming.platforms.Platform(":resources:images/tiles/boxCrate_double.png", scale=0.5, center_x=position_in_map[x]*TILE_SIZE, center_y=(len(map_lines)-position_in_map[y])*TILE_SIZE, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            world.moving_platforms_list.append(crate)
            detect_surrounding(position_in_map , map_lines, trajectory , world)
        case "£" :
            lava = platforming.platforms.Lava_Platform(":resources:images/tiles/lava.png", scale=0.5, center_x=position_in_map[x]*TILE_SIZE, center_y=(len(map_lines)-position_in_map[y])*TILE_SIZE, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            world.no_go_list.append(lava)
            detect_surrounding(position_in_map , map_lines, trajectory , world)
        case "E" :
            exit = platforming.platforms.Exit_Platform(":resources:/images/tiles/signExit.png",  center_x=position_in_map[x]*TILE_SIZE, center_y=(len(map_lines)-position_in_map[y])*TILE_SIZE, scale = 0.5, platform_trajectory = trajectory, angle = 0)
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            world.exit_list.append(exit)
            world.set_exit = True
            detect_surrounding(position_in_map , map_lines, trajectory , world)
        case _:
            if force_detection and math.sqrt(trajectory.right_movement^2+trajectory.left_movement^2+trajectory.up_movement^2+trajectory.down_movement^2) == trajectory.right_movement + trajectory.down_movement +trajectory.left_movement + trajectory.up_movement :
                raise RuntimeError("Some arrow set is not linked to any platform")
            return None
        

def detect_right(position_in_map : tuple[int,int], 
                 map_lines : list[list[str]], 
                 trajectory : platforming.platforms.Trajectory, 
                 world : Map_Create.create_world.World,
                 force_detection : bool = False ) -> None:
    if position_in_map[x] < len(map_lines[position_in_map[y]]) - 1 and not(map_lines[position_in_map[y]][position_in_map[x]+1] in ("↓","←","↑" )): 
        detect_block((position_in_map[x]+1,position_in_map[y]), map_lines, trajectory, world, force_detection)

def detect_left(position_in_map : tuple[int,int], 
                map_lines : list[list[str]], 
                trajectory : platforming.platforms.Trajectory, 
                world : Map_Create.create_world.World,
                force_detection : bool = False ) -> None:
    if position_in_map[x] > 0 and not(map_lines[position_in_map[y]][position_in_map[x]-1] in  ("→", "↓" , "↑")): 
        detect_block((position_in_map[x]-1,position_in_map[y]), map_lines, trajectory, world, force_detection)

def detect_down(position_in_map : tuple[int,int], 
                map_lines : list[list[str]], 
                trajectory : platforming.platforms.Trajectory, 
                world : Map_Create.create_world.World,
                force_detection : bool = False  ) -> None:
    if position_in_map[y] < len(map_lines) - 1 and not(map_lines[position_in_map[y]+1][position_in_map[x]] in  ("→", "←", "↑")): 
        detect_block((position_in_map[x],position_in_map[y]+1), map_lines, trajectory, world, force_detection)

def detect_up(position_in_map : tuple[int,int], 
              map_lines : list[list[str]], 
              trajectory : platforming.platforms.Trajectory, 
              world : Map_Create.create_world.World,
              force_detection : bool = False   ) -> None:       
    if position_in_map[y] > 0 and not(map_lines[position_in_map[y]-1][position_in_map[x]] in ("→", "←", "↓")):
        detect_block((position_in_map[x],position_in_map[y]-1), map_lines, trajectory, world, force_detection)


def detect_surrounding(position_in_map : tuple[int,int], 
                       map_lines : list[list[str]], 
                       trajectory : platforming.platforms.Trajectory, 
                       world : Map_Create.create_world.World ) -> None:
    """Applies detect_block but on the 4 sides of the sprite

    Args:
        position_in_map (tuple[int,int]): coord (x,y) in the map-matrix
        map_lines (list[list[str]]): the map repr as a matrix of str
        trajectory (Trajectory): How much the platform moves on each direction
        moving_platforms_list (arcade.SpriteList[Platform]): the block of platform "analysed" by the function
    """
    
    detect_up((position_in_map[x],position_in_map[y]), map_lines, trajectory, world)
    detect_down((position_in_map[x],position_in_map[y]), map_lines, trajectory, world)
    detect_right((position_in_map[x],position_in_map[y]), map_lines, trajectory, world)
    detect_left((position_in_map[x],position_in_map[y]), map_lines, trajectory, world)


def detect_arrows_set(position_in_map : tuple[int,int], 
                      map_lines : list[list[str]], 
                      trajectory : platforming.platforms.Trajectory, 
                      world : Map_Create.create_world.World, 
                      char : str ) -> None:
    """Detect how long a set of the same arrow is

    Args:
        position_in_map (tuple[int,int]): coord (x,y) in the map-matrix
        map_lines (list[list[str]]): the map repr as a matrix of str
        trajectory (Trajectory): How much the platform moves on each direction
        moving_platforms_list (arcade.SpriteList[Platform]): the block of platform "analysed" by the function
        char (str): the arrow of which we want to return the length of the set
        """
    map_lines[position_in_map[y]][position_in_map[x]] = " "
    match char: 
        case "→":
            if position_in_map[x] < len(map_lines[position_in_map[y]]):
                if map_lines[position_in_map[y]][position_in_map[x]+1] == "→":
                    trajectory.right_movement += 1
                    detect_arrows_set((position_in_map[x]+1,position_in_map[y]), map_lines, trajectory, world,"→" )
        case  "←" : 
            if map_lines[position_in_map[y]][position_in_map[x]+1] == "←":
                trajectory.left_movement += 1
                detect_arrows_set((position_in_map[x]+1,position_in_map[y]), map_lines, trajectory, world,"←" )
        case "↑" :
            if map_lines[position_in_map[y]+1][position_in_map[x]] == "↑":
                trajectory.up_movement += 1
                detect_arrows_set((position_in_map[x],position_in_map[y]+1), map_lines, trajectory, world,"↑" )
        case "↓" :
            if position_in_map[y] < len(map_lines):
                if map_lines[position_in_map[y]+1][position_in_map[x]] == "↓":
                    trajectory.down_movement += 1
                    detect_arrows_set((position_in_map[x],position_in_map[y]+1), map_lines, trajectory, world,"↓" )   