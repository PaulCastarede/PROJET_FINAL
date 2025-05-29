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

    def on_draw(self) -> None:
        self.clear()
        self.__victory_sprite_list.draw()
        self.__victory_text.draw()
        self.__escape_text.draw()


    

        

