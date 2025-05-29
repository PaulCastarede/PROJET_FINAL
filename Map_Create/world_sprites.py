from __future__ import annotations
from typing import Final
import arcade
import player
import gameview
import endgame
import platforming.platforms as platforms
import map_create.create_world as create_world


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


class Exit_Sprite(platforms.Collidable_Platform):
    """Sprite for the exit signs, represents the end of a level"""

    def __init__(self,  path_or_texture : str =  ":resources:/images/tiles/signExit.png", center_x : float = 0, center_y : float = 0, scale : float = 0.5, angle : float = 0,  platform_trajectory : platforms.Trajectory = platforms.Trajectory()) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y, angle, platform_trajectory)

    def exit(self, game_view : gameview.GameView) -> None:
        """Gets the player to the next level when he touches it"""
        if arcade.check_for_collision_with_list(self, game_view.world.player_sprite_list) :
            if not(game_view.world.last_level):    
                #Si ce n'est pas le dernier niveau, lit la prochaine map       
                create_world.readmap(game_view.world, map = game_view.world.next_map)
            else:
                if game_view.music_playback is not None:
                    #If the music is playing, stop it
                    arcade.stop_sound(game_view.music_playback)
                game_view.window.show_view(endgame.EndGame())
        

class Lava_Sprite(platforms.Collidable_Platform):
    """Sprite for the lava (no-go) blocks. Deadly for players"""
    def __init__(self, path_or_texture : str = ":resources:images/tiles/lava.png", center_x : float = 0, center_y : float = 0, scale : float = 0.5, angle : float = 0,  platform_trajectory : platforms.Trajectory = platforms.Trajectory()) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y, angle, platform_trajectory)
    

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
            self.texture = checkpoint_textures[1]

