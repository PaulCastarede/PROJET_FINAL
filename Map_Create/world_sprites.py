from __future__ import annotations
import arcade
import player
import gameview
import Map_Create.create_world

class Exit_Sprite(arcade.Sprite):

    def exit(self, game_view : gameview.GameView) -> None:
        if arcade.check_for_collision_with_list(self, game_view.world.player_sprite_list) :
            if not(game_view.world.last_level):    
                #Si ce n'est pas le dernier niveau, lit la prochaine map       
                Map_Create.create_world.readmap(game_view.world, map = game_view.world.next_map)
            else:
                game_view.UI.victory = True
                game_view.UI.update(self)
        

class Lava_Sprite(arcade.Sprite):

    def kills(self, game_view : gameview.GameView) -> None:
        ...
    