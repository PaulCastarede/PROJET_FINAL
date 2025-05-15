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

# Index des textures, rouge -> pas encore visité, vert -> visité
TEXTURE_RED = 0
TEXTURE_GREEN = 1


class Exit_Sprite(arcade.Sprite):

    def exit(self, game_view : gameview.GameView) -> None:
        if arcade.check_for_collision_with_list(self, game_view.world.player_sprite_list) :
            if not(game_view.world.last_level):    
                #Si ce n'est pas le dernier niveau, lit la prochaine map       
                Map_Create.create_world.readmap(game_view.world, map = game_view.world.next_map)
            else:
                game_view.UI.victory = True
        

class Lava_Sprite(arcade.Sprite):
    ...
    

class Checkpoint(arcade.Sprite):
    linked_map : Final[str]

    def __init__(self, linked_map, path_or_texture : str = ":resources:/images/items/flagRed1.png", center_x : float = 0, center_y : float = 0, scale : float = 0.4, angle : float = 0) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y, angle)
        self.linked_map = linked_map

    def set_respawn(self, player_list : arcade.SpriteList[player.Player]):
        if arcade.check_for_collision_with_list(self, player_list):
            player_list[0].respawn_point = (self.center_x, self.center_y)
            self.texture = checkpoint_textures[1]

