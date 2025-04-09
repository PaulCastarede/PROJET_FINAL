from __future__ import annotations
import arcade
import math
import monsters 
import gameview

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
    jump_sound : arcade.Sound

    def __init__(self, path_or_texture : str, center_x : float, center_y : float, scale : float) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y )
        self.death = False
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
    
    def dies(self, dangers : list[arcade.SpriteList[arcade.Sprite]]) -> None:
        if arcade.check_for_collision_with_lists(self, dangers):
            self.death = True

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

    


        