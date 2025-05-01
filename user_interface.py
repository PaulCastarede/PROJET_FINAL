from __future__ import annotations
import arcade
import gameview
class UI:
    __score_UI : arcade.Text
    __weapons_UI : arcade.Sprite
    __victory_UI : arcade.Text
    victory : bool

    def __init__(self) -> None:
        self.__score_UI = arcade.Text( x =  70, y = 650, font_size = 20, text = f"Score : 0")
        self.__weapons_UI = arcade.Sprite("assets/kenney-voxel-items-png/sword_silver.png",scale=0.9, center_x=80,center_y=80, angle = 0)
        self.__victory_UI = arcade.Text(x = 300, y = 360, font_size = 100, text = "WELL PLAYED")
        self.victory = False

    def update(self, game_view : gameview.GameView) -> None:
        #Fait correspondre le score affiché avec le score du joueur 
        self.__score_UI.text = f"Score : {game_view.score}"
        if game_view.active_weapon == gameview.SWORD_INDEX:
            self.__weapons_UI = arcade.Sprite("assets/kenney-voxel-items-png/sword_silver.png",scale=0.9, center_x=80,center_y=80, angle = 0)
        elif game_view.active_weapon == gameview.BOW_INDEX:
            self.__weapons_UI = arcade.Sprite("assets/kenney-voxel-items-png/bow.png", scale=1, center_x=80,center_y=80, angle = -70)
    
    
    def draw(self) -> None:
        self.__score_UI.draw()
        arcade.draw_sprite(self.__weapons_UI)
        if self.victory:
            self.__victory_UI.draw()
