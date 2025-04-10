from __future__ import annotations
import arcade
import math
import monsters 
import gameview
import coins

PLAYER_MOVEMENT_SPEED = 5
"""Lateral speed of the player, in pixels per frame."""

PLAYER_GRAVITY = 1
"""Gravity applied to the player, in pixels per frame²."""

PLAYER_JUMP_SPEED = 18
"""Instant vertical speed for jumping, in pixels per frame."""


class Player(arcade.Sprite):   
    player_sprite : arcade.Sprite
    score : int
    death : bool
    death_sound : arcade.Sound
    jump_sound : arcade.Sound

    def __init__(self, path_or_texture : str = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", center_x : float = 0, center_y : float = 0, scale : float = 0.5) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y )
        self.death = False
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.score = 0
    
    def dies(self, no_go : arcade.SpriteList[arcade.Sprite], monsters : arcade.SpriteList[monsters.Monster]) -> None:
        no_go_touched = arcade.check_for_collision_with_list(self, no_go) 
        monsters_touched = arcade.check_for_collision_with_list(self, monsters)
        if no_go_touched or monsters_touched:
            self.death = True
            arcade.play_sound(self.death_sound)

    def movement(self, gameview : gameview.GameView) -> None:
        self.change_x = 0
        if gameview.right_pressed:
            self.change_x += PLAYER_MOVEMENT_SPEED       #Joueur avance si -> pressed
        if gameview.left_pressed:                 
            self.change_x -= PLAYER_MOVEMENT_SPEED       #Joueur recule si <- pressed

    def jump(self) -> None:
        # jump by giving an initial vertical speed
        self.change_y = PLAYER_JUMP_SPEED
        arcade.play_sound(self.jump_sound)

    def collect_coins(self, coins_list : arcade.SpriteList[coins.Coin]) -> None:
        #Vérifie si le joueur est en contact avec des pièces
        collided_coins = arcade.check_for_collision_with_list(self, coins_list)
        #Retire les pièces en contact avec le joueur
        for coin in collided_coins:
            #Incrémente le score du nombre de pièces 
            self.score += len(collided_coins)               
            coin.remove_from_sprite_lists()                
            arcade.play_sound(coin.coin_sound)

    


        