from __future__ import annotations
from typing import Final
import arcade
import player
import gameview
import Map_Create.create_world


checkpoint_textures = []
#On ajoute le sprite du checkpoint pas encore validé
texture = arcade.load_texture(":resources:/images/items/flagRed1.png")    
checkpoint_textures.append(texture)   
#Et celui du checkpoint validé                                    
texture = arcade.load_texture(":resources:/images/items/flagGreen2.png")
checkpoint_textures.append(texture)

# Index des textures pour le checkpoint
TEXTURE_RED = 0
"""Texture of the checkpoint when it has not been yet visited by the player"""
TEXTURE_GREEN = 1
"""Texture of the checkpoint when it has been visited by the player"""


class Exit_Sprite(arcade.Sprite):
    """Sprite for the exit signs, represents the end of a level"""

    def exit(self, game_view : gameview.GameView) -> None:
        """Gets the player to the next level when he touches it"""
        if arcade.check_for_collision_with_list(self, game_view.world.player_sprite_list) :
            if not(game_view.world.last_level):    
                #Si ce n'est pas le dernier niveau, lit la prochaine map       
                Map_Create.create_world.readmap(game_view.world, map = game_view.world.next_map)
            else:
                game_view.UI.victory = True
        

class Lava_Sprite(arcade.Sprite):
    """Sprite for the lava (no-go) blocks. Deadly for players"""
    ...
    

class Checkpoint(arcade.Sprite):
    """Class of the Checkpoint Sprite. If visited, the player will respawn there after he dies.

    Args:
        linked_map (str) : The name of the map to which the checkpoint belongs
    """
    linked_map : Final[str]

    def __init__(self, linked_map, path_or_texture : str = ":resources:/images/items/flagRed1.png", center_x : float = 0, center_y : float = 0, scale : float = 0.4, angle : float = 0) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y, angle)
        self.linked_map = linked_map

    def set_respawn(self, player_list : arcade.SpriteList[player.Player]):
        if arcade.check_for_collision_with_list(self, player_list):   
            player_list[0].respawn_point = (self.center_x, self.center_y)
            player_list[0].respawn_map = self.linked_map
            self.texture = checkpoint_textures[1]

