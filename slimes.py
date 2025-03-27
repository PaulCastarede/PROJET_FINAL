import arcade 


SLIMES_SPEED = 1
"""Speed of the slimes, in pixels per frame"""

class Slime(arcade.Sprite):
    front : arcade.Sprite
    below : arcade.Sprite

    def __init__(self, path_or_texture : str, center_x : float, center_y : float, scale : float) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y )