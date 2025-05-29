from __future__ import annotations
from typing import Final
import arcade
import player
import platforming.platforms as platforms
import create_world as create_world


TEXTURE_GREEN = arcade.load_texture(":resources:/images/items/flagGreen2.png")
"""Texture of the checkpoint when it has been visited by the player"""


class Checkpoint(platforms.Collidable_Platform):
    """Class of the Checkpoint Sprite. If visited, the player will respawn there after he dies.

    Args:
        linked_map (str) : The name of the map to which the checkpoint belongs
    """
    linked_map : str
    __spawn_x : Final[float]
    __spawn_y : Final[float]

    def __init__(self, linked_map : str, path_or_texture : str = ":resources:/images/items/flagRed1.png", center_x : float = 0, center_y : float = 0, scale : float = 0.4, angle : float = 0,  platform_trajectory : platforms.Trajectory = platforms.Trajectory()) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y, angle, platform_trajectory)
        self.linked_map = linked_map
        self.__spawn_x = self.center_x
        self.__spawn_y = self.center_y

    def set_respawn(self, player : player.Player) -> None:
        if arcade.check_for_collision(self, player):   
            player.respawn_point = (self.__spawn_x, self.__spawn_y)
            player.respawn_map = self.linked_map
            self.texture = TEXTURE_GREEN
