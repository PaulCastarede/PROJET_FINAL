from __future__ import annotations
import platforming.platforms as platforms
import create_world as create_world


class Lava_Sprite(platforms.Collidable_Platform):
    """Sprite for the lava (no-go) blocks. Deadly for players"""
    def __init__(self, path_or_texture : str = ":resources:images/tiles/lava.png", center_x : float = 0, center_y : float = 0, scale : float = 0.5, angle : float = 0,  platform_trajectory : platforms.Trajectory = platforms.Trajectory()) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y, angle, platform_trajectory)
    

