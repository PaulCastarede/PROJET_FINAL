from __future__ import annotations
from typing import Final
import arcade
import gameview
import create_world
import alt_game_views.gameover as gameover

INITIAL_PLAYER_LIVES = 5
"""How many lives the player has when (s)he starts the game"""


class Player(arcade.Sprite):   
    PLAYER_MOVEMENT_SPEED : Final[float] = 5
    """Lateral speed of the player, in pixels per frame."""

    PLAYER_GRAVITY : Final[float] = 1.7
    """Gravity applied to the player, in pixels per frame²."""

    PLAYER_JUMP_SPEED : Final[float] = 25
    """Instant vertical speed for jumping, in pixels per frame."""


    player_sprite : arcade.Sprite
    coins_possessed : int
    lives : int
    respawn_point : tuple[float, float]
    respawn_map : str
    death_sound : Final[arcade.Sound] = arcade.load_sound(":resources:sounds/gameover1.wav")
    jump_sound : Final[arcade.Sound] = arcade.load_sound(":resources:sounds/jump1.wav")


    def __init__(self, respawn_map: str, path_or_texture : str = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", center_x : float = 0, center_y : float = 0, scale : float = 0.5) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y )
        self.death = False
        self.lives = INITIAL_PLAYER_LIVES
        self.coins_possessed = 0
        self.respawn_point = (self.center_x,self.center_y)
        self.respawn_map = respawn_map
        
    
    def dies(self, gameview : gameview.GameView) -> None:
        """Checks if the player should die to anything in which case the method decreases its number of lives and calls respawn(), or launch the gameover view if needed"""
        no_go_touched = arcade.check_for_collision_with_list(self, gameview.world.no_go_list) 
        monsters_touched = arcade.check_for_collision_with_list(self, gameview.world.monsters_list)
        if no_go_touched or monsters_touched or self.center_y < -64:
            self.lives -= 1
            self.respawn(gameview)
            #UPDATE UI
            gameview.UI.update_player_lives(self)
            #CAMERA SHAKES WHEN PLAYER DIES
            gameview.camera_shake.duration = 0.5
            gameview.camera_shake.max_amplitude = 50.0
            gameview.camera_shake.shake_frequency = 15.0
            gameview.camera_shake.start()
            #Play death sound
            arcade.play_sound(self.death_sound)
            #Launch gameover if needed
            if self.lives < 0:
                if gameview.music_playback:
                    #If the music is playing, stop it
                    arcade.stop_sound(gameview.music_playback)
                gameview.window.show_view(gameover.GameOverView(gameview))
                    

    def respawn(self, gameview : gameview.GameView) -> None:
        """Makes the player get back to the last checkpoint he met/to his initial spawnpoint"""
        create_world.readmap(gameview.world, self.respawn_map)
        self.center_x, self.center_y = self.respawn_point


    def movement(self, gameview : gameview.GameView) -> None:
        """Manages the player movement by updating his position. Should be called every tick (in on_update method)
        """
        self.change_x = 0
        if gameview.right_pressed:
            self.change_x += self.PLAYER_MOVEMENT_SPEED       #Joueur avance si -> pressed
        if gameview.left_pressed:                 
            self.change_x -= self.PLAYER_MOVEMENT_SPEED       #Joueur recule si <- pressed

    def jump(self) -> None:
        """Jump by giving an initial vertical speed. Called when user presses "Up Arrow"
        """
        self.change_y = self.PLAYER_JUMP_SPEED
        arcade.play_sound(self.jump_sound)

    def collect_coins(self, gameview : gameview.GameView) -> None:
        """Checks if the player collides coins and gathers them if needed, updating the score in the UI"""
        #Vérifie si le joueur est en contact avec des pièces
        collided_coins = arcade.check_for_collision_with_list(self, gameview.world.coins_list)
        #Retire les pièces en contact avec le joueur
        for coin in collided_coins:
            #Incrémente le score du nombre de pièces 
            self.coins_possessed += len(collided_coins)  
            coin.remove_from_sprite_lists()                
            arcade.play_sound(coin.coin_sound)
        #Augmente le nombre de vies si le nombre de pièces >= 10
        if self.coins_possessed >= 10:
            self.coins_possessed -= 10 
            self.lives += 1
            gameview.UI.update_player_lives(self)
        #Update UI 
        gameview.UI.update_score(gameview)
    


        