from __future__ import annotations
import arcade
import platforming.platforms
import Map_Create.world_sprites
from dataclasses import dataclass

x = 0
y = 1

def detect_block(position_in_map : tuple[int,int], map_lines : list[list[str]], trajectory : platforming.platforms.Trajectory, moving_platforms_list : arcade.SpriteList[platforming.platforms.Platform] ) -> None:
    """

    Args:
        position_in_map (tuple[int,int]): coord (x,y) in the map-matrix
        map_lines (list[list[str]]): the map repr as a matrix of str
        trajectory (Trajectory): How much the platform moves on each direction
        moving_platforms_list (arcade.SpriteList[Platform]): the block of platform "analysed" by the function

    Returns:
        Platforms: Adds the platforms block detected to a sprite list
    """

    match map_lines[position_in_map[y]][position_in_map[x]]:
        case "←" : 
            trajectory.left_movement += 1
            detect_arrows_set((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list, "←")
            detect_right((position_in_map[x]+trajectory.left_movement-1,position_in_map[y]), map_lines, trajectory, moving_platforms_list)
        case "→" :
            trajectory.right_movement += 1
            detect_arrows_set((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list, "→")
            detect_left((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)
        case "↑" :
            trajectory.up_movement += 1
            detect_arrows_set((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list, "↑")
            detect_down((position_in_map[x],position_in_map[y]-trajectory.up_movement+1), map_lines, trajectory, moving_platforms_list)
        case "↓" :
            trajectory.down_movement += 1
            detect_arrows_set((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list, "↓")
            detect_up((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)

        case "=" :
            Grass = platforming.platforms.Platform(":resources:images/tiles/grassMid.png", scale=0.5,center_x=position_in_map[x]*64, center_y=(len(map_lines)-position_in_map[y])*64, platform_trajectory = trajectory, angle = 0)
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            moving_platforms_list.append(Grass)
            detect_surrounding(position_in_map , map_lines, trajectory , moving_platforms_list)

        case "-" :
            half_grass = platforming.platforms.Platform(":resources:images/tiles/grassHalf_mid.png", scale=0.5, center_x=position_in_map[x]*64, center_y=(len(map_lines)-position_in_map[y])*64, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            moving_platforms_list.append(half_grass)
            detect_surrounding(position_in_map , map_lines, trajectory , moving_platforms_list)
        case "x" :
            crate = platforming.platforms.Platform(":resources:images/tiles/boxCrate_double.png", scale=0.5, center_x=position_in_map[x]*64, center_y=(len(map_lines)-position_in_map[y])*64, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            moving_platforms_list.append(crate)
            detect_surrounding(position_in_map , map_lines, trajectory , moving_platforms_list)
        case "£" :
            lava = platforming.platforms.Platform(":resources:images/tiles/lava.png", scale=0.5, center_x=position_in_map[x]*64, center_y=(len(map_lines)-position_in_map[y])*64, platform_trajectory = trajectory, angle = 0 )
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            moving_platforms_list.append(lava)
            detect_surrounding(position_in_map , map_lines, trajectory , moving_platforms_list)
        case "E" :
            exit = platforming.platforms.Exit_Platform(":resources:/images/tiles/signExit.png",  center_x=position_in_map[x]*64, center_y=(len(map_lines)-position_in_map[y])*64, scale = 0.5, platform_trajectory = trajectory, angle = 0)
            map_lines[position_in_map[y]][position_in_map[x]] = " "
            moving_platforms_list.append(exit)
            detect_surrounding(position_in_map , map_lines, trajectory , moving_platforms_list)
        case _:
            return None
        

def detect_right(position_in_map : tuple[int,int], map_lines : list[list[str]], trajectory : platforming.platforms.Trajectory, moving_platforms_list : arcade.SpriteList[platforming.platforms.Platform] ) -> None:
    if position_in_map[x] < len(map_lines[position_in_map[y]]):
        detect_block((position_in_map[x]+1,position_in_map[y]), map_lines, trajectory, moving_platforms_list)

def detect_left(position_in_map : tuple[int,int], map_lines : list[list[str]], trajectory : platforming.platforms.Trajectory, moving_platforms_list : arcade.SpriteList[platforming.platforms.Platform] ) -> None:
    if position_in_map[x] > 0:
        detect_block((position_in_map[x]-1,position_in_map[y]), map_lines, trajectory, moving_platforms_list)

def detect_down(position_in_map : tuple[int,int], map_lines : list[list[str]], trajectory : platforming.platforms.Trajectory, moving_platforms_list : arcade.SpriteList[platforming.platforms.Platform] ) -> None:
    if position_in_map[y] < len(map_lines):
        detect_block((position_in_map[x],position_in_map[y]+1), map_lines, trajectory, moving_platforms_list)

def detect_up(position_in_map : tuple[int,int], map_lines : list[list[str]], trajectory : platforming.platforms.Trajectory, moving_platforms_list : arcade.SpriteList[platforming.platforms.Platform] ) -> None:       
    if position_in_map[y] > 0:
        detect_block((position_in_map[x],position_in_map[y]-1), map_lines, trajectory, moving_platforms_list)


def detect_surrounding(position_in_map : tuple[int,int], map_lines : list[list[str]], trajectory : platforming.platforms.Trajectory, moving_platforms_list : arcade.SpriteList[platforming.platforms.Platform] ) -> None:
    """Applies detect_block but on the 4 sides of the sprite

    Args:
        position_in_map (tuple[int,int]): coord (x,y) in the map-matrix
        map_lines (list[list[str]]): the map repr as a matrix of str
        trajectory (Trajectory): How much the platform moves on each direction
        moving_platforms_list (arcade.SpriteList[Platform]): the block of platform "analysed" by the function
    """
    detect_up((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)
    detect_down((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)
    detect_right((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)
    detect_left((position_in_map[x],position_in_map[y]), map_lines, trajectory, moving_platforms_list)


def detect_arrows_set(position_in_map : tuple[int,int], map_lines : list[list[str]], trajectory : platforming.platforms.Trajectory, moving_platforms_list : arcade.SpriteList[platforming.platforms.Platform], char : str ) -> None:
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
                    detect_arrows_set((position_in_map[x]+1,position_in_map[y]), map_lines, trajectory, moving_platforms_list,"→" )
        case  "←" : 
            if map_lines[position_in_map[y]][position_in_map[x]+1] == "←":
                trajectory.left_movement += 1
                detect_arrows_set((position_in_map[x]+1,position_in_map[y]), map_lines, trajectory, moving_platforms_list,"←" )
        case "↑" :
            if map_lines[position_in_map[y]-1][position_in_map[x]] == "↑":
                trajectory.up_movement += 1
                detect_arrows_set((position_in_map[x],position_in_map[y]+1), map_lines, trajectory, moving_platforms_list,"↑" )
        case "↓" :
            if position_in_map[y] < len(map_lines):
                if map_lines[position_in_map[y]-1][position_in_map[x]] == "↓":
                    trajectory.down_movement += 1
                    detect_arrows_set((position_in_map[x],position_in_map[y]+1), map_lines, trajectory, moving_platforms_list,"↓" )   
                