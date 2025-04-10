from __future__ import annotations
import arcade
import gameview
class UI:
    score_UI : arcade.Text
    weapons_UI : arcade.Sprite
    victory_UI : arcade.Text

    def __init__(self) -> None:
        self.score_UI = arcade.Text( x =  70, y = 650, font_size = 20, text = f"Score : 0")
        self.weapons_UI = arcade.Sprite("assets/kenney-voxel-items-png/sword_silver.png",scale=0.9, center_x=80,center_y=80, angle = 0)
        self.victory_UI = arcade.Text(x = 400, y = 360, font_size = 100, text = "")

    def update(self, game_view : gameview.GameView) -> None:
        self.score_UI.text = f"Score : {game_view.world.player_sprite.score}"
        if game_view.active_weapon == gameview.SWORD_INDEX:
            self.weapons_UI = arcade.Sprite("assets/kenney-voxel-items-png/sword_silver.png",scale=0.9, center_x=80,center_y=80, angle = 0)
        elif game_view.active_weapon == gameview.BOW_INDEX:
            self.weapons_UI = arcade.Sprite("assets/kenney-voxel-items-png/bow.png", scale=1, center_x=80,center_y=80, angle = -70)
        if game_view.Victory == True:
            self.victory_UI.text = "WELL PLAYED"

    
    def draw(self) -> None:
        self.score_UI.draw()
        arcade.draw_sprite(self.weapons_UI)
        self.victory_UI.draw()
