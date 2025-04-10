import arcade
from typing import Final



class Coin(arcade.Sprite):
    coin_sound :  Final[arcade.Sound] = arcade.load_sound(":resources:sounds/coin1.wav")

    def __init__(self, path_or_texture : str = ":resources:images/items/coinGold.png", scale : float = 0.5, center_x : int = 0 , center_y : int = 0, angle : int = 0):
        super().__init__(path_or_texture, scale, center_x, center_y, angle)
