from __future__ import annotations
import arcade
import gameview
import alt_game_views.endgame as endgame
import platforming.platforms as platforms
import create_world as create_world


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
        