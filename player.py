import arcade
import math

PLAYER_MOVEMENT_SPEED = 5
"""Lateral speed of the player, in pixels per frame."""

PLAYER_GRAVITY = 1
"""Gravity applied to the player, in pixels per frame²."""

PLAYER_JUMP_SPEED = 18
"""Instant vertical speed for jumping, in pixels per frame."""


class Player(arcade.Sprite):   
    player_sprite : arcade.Sprite
    death : bool

    def __init__(self, path_or_texture : str, center_x : float, center_y : float, scale : float) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y )
        death = False
    