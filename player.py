from __future__ import annotations
from typing import Final
import arcade
import monsters 
import gameview
import Map_Create.create_world
import coins
import user_interface

PLAYER_MOVEMENT_SPEED = 5
"""Lateral speed of the player, in pixels per frame."""

PLAYER_GRAVITY = 1.7
"""Gravity applied to the player, in pixels per frame²."""

PLAYER_JUMP_SPEED = 25
"""Instant vertical speed for jumping, in pixels per frame."""

INITIAL_PLAYER_LIVES = 5
"""How many lives the player has when (s)he starts the game"""


class Player(arcade.Sprite):   
    player_sprite : arcade.Sprite
    lives : int
    death : bool
    respawn_point : arcade.Vec2
    respawn_map : str
    death_sound : Final[arcade.Sound]
    jump_sound : Final[arcade.Sound]

    def __init__(self, respawn_map, path_or_texture : str = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", center_x : float = 0, center_y : float = 0, scale : float = 0.5) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y )
        self.death = False
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.lives = INITIAL_PLAYER_LIVES
        self.respawn_point = (self.center_x,self.center_y)
        self.respawn_map = respawn_map
    
    def respawn_or_dies(self, gameview : gameview.GameView) -> None:
        no_go_touched = arcade.check_for_collision_with_list(self, gameview.world.no_go_list) 
        monsters_touched = arcade.check_for_collision_with_list(self, gameview.world.monsters_list)
        if no_go_touched or monsters_touched or self.center_y < -64:
            self.lives -= 1
            self.respawn(gameview)
            gameview.UI.update_player_lives(self)
            if self.lives < 0:
                self.death = True
                arcade.play_sound(self.death_sound)
            
    

    def respawn(self, gameview : gameview.GameView) -> None:
        Map_Create.create_world.readmap(gameview.world, self.respawn_map)
        self.center_x, self.center_y = self.respawn_point

    def movement(self, gameview : gameview.GameView) -> None:
        self.change_x = 0
        if gameview.right_pressed:
            self.change_x += PLAYER_MOVEMENT_SPEED       #Joueur avance si -> pressed
        if gameview.left_pressed:                 
            self.change_x -= PLAYER_MOVEMENT_SPEED       #Joueur recule si <- pressed

    def jump(self) -> None:
        """Jump by giving an initial vertical speed. Called when user presses "Up Arrow"
        """
        self.change_y = PLAYER_JUMP_SPEED
        arcade.play_sound(self.jump_sound)

    def collect_coins(self, gameview : gameview.GameView) -> None:
        #Vérifie si le joueur est en contact avec des pièces
        collided_coins = arcade.check_for_collision_with_list(self, gameview.world.coins_list)
        #Retire les pièces en contact avec le joueur
        for coin in collided_coins:
            #Incrémente le score du nombre de pièces 
            gameview.score += len(collided_coins)  
            coin.remove_from_sprite_lists()                
            arcade.play_sound(coin.coin_sound)
        if gameview.score >= 10:
            gameview.score -= 10 
            self.lives += 1
            gameview.UI.update_player_lives(self)
        gameview.UI.update_score(gameview)
    


        