from __future__ import annotations
from typing import Final
import arcade
from pyglet.graphics import Batch

characters_texture_list = [":resources:/images/animated_characters/female_person/femalePerson_walk7.png",":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",":resources:/images/animated_characters/male_adventurer/maleAdventurer_walk0.png" ]

class EndGame(arcade.View):
    __victory_text : arcade.Text 
    __escape_text : arcade.Text 
    __victory_music : arcade.Sound = arcade.load_sound("assets/Game_music.mp3", streaming=True)
    

    def __init__(self) -> None:
        super().__init__()
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.__victory_text = arcade.Text(x = self.window.width // 2, y = 500, font_size = 70, text = "WELL PLAYED", color = arcade.csscolor.FLORAL_WHITE, anchor_x="center")
        arcade.play_sound(self.__victory_music)
        self.__escape_text =  arcade.Text(x = 20, y = 20, font_size = 20, text = "Press Esc. to leave the game", color = arcade.csscolor.BLACK)

    @property
    def __end_roll(self) -> list[arcade.Text]:
        credit_1 = arcade.Text(x = 1100, y = 700, font_size=15, text = "Game by Paul Castarède and Mikail Bulut", anchor_x="center" )
        credit_2 = arcade.Text(x = 1300, y = 830, font_size=10, text = "Thanks to arcade python for providing us a free use library", anchor_x="center")
        credit_3 = arcade.Text(x = 1300, y = 860, font_size=10, text = "Thanks too to our CS teacher Sebastien Doerane", anchor_x="center" )
        credit_4 = arcade.Text(x = 1300, y = 890, font_size=7, text = "Credit to HeatleyBros - Royalty Free Video Game Music,  for the ambient music and Kenney voxel assets", anchor_x="center" )
        end_roll = [credit_1, credit_2, credit_3, credit_4]
        return end_roll

    @property
    def __victory_sprite_list(self) -> arcade.SpriteList[arcade.Sprite]:
        victory_sprite_list : arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        #AJOUTE UNE PLATEFORME DE FIN DE JEU
        for x in range(8,13):
            victory_sprite_list.append(arcade.Sprite(":resources:images/tiles/grassMid.png", center_x=x*64, center_y= 300,scale=0.5 ))
        #AJOUTE DES PERSONNAGES HEUREUX
        for i in range(len(characters_texture_list)):
            victory_sprite_list.append(arcade.Sprite(characters_texture_list[i], center_x = (9+i)*64, center_y=370, scale = 0.6))

        return victory_sprite_list
    
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Gère les touches pressées sur l'écran de fin"""
        if key == arcade.key.ESCAPE:
            arcade.exit()
    
    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances", or "ticks".
        """
        for credit in self.__end_roll:
            credit.y  -= 100

    def on_draw(self) -> None:
        self.clear()
        self.__victory_sprite_list.draw()
        self.__victory_text.draw()
        self.__escape_text.draw()
        for credit in self.__end_roll:
            credit.draw()

    

        

