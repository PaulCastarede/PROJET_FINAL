from __future__ import annotations
import arcade
import gameview
import player
class UI:
    """UI stands for user interface
    """
    __score_UI : arcade.Text
    __ui_coin : arcade.Sprite
    __weapons_UI : arcade.Sprite
    __victory_UI : arcade.Text
    __player_lives_ui : arcade.Sprite
    __player_lives_number_UI : arcade.Text
    victory : bool

    def __init__(self) -> None:
        self.__score_UI = arcade.Text( x =  80, y = 650, font_size = 20, text =  " X  0")
        self.__ui_coin = arcade.Sprite(":resources:images/items/coinGold.png", scale = 0.6 , center_x = 50, center_y = 660, angle = 0)

        self.__player_lives_ui = arcade.Sprite("assets/femaleAdventurer_idle.png", scale = 1.0 , center_x = 1100, center_y = 650, angle = 0)
        self.__player_lives_number_UI = arcade.Text(x = 1150, y = 630, font_size= 30, text = f"x  {player.INITIAL_PLAYER_LIVES}")

        self.__weapons_UI = arcade.Sprite("assets/kenney-voxel-items-png/sword_silver.png",scale=0.9, center_x=80,center_y=80, angle = 0)
        self.__victory_UI = arcade.Text(x = 300, y = 360, font_size = 100, text = "WELL PLAYED")
        self.victory = False

    def update_score(self, game_view : gameview.GameView) -> None:
        """Fait correspondre le score affiché avec le score du joueur"""

        self.__score_UI.text = f"X  {game_view.score}"
    
    def update_weapon(self, game_view : gameview.GameView) -> None:
        """Fait correspondre l'arme affichée avec l'arme équipée"""
        if game_view.active_weapon == gameview.SWORD_INDEX:
            self.__weapons_UI = arcade.Sprite("assets/kenney-voxel-items-png/sword_silver.png",scale=0.9, center_x=80,center_y=80, angle = 0)
        elif game_view.active_weapon == gameview.BOW_INDEX:
            self.__weapons_UI = arcade.Sprite("assets/kenney-voxel-items-png/bow.png", scale=1, center_x=80,center_y=80, angle = -70)
    
    def update_player_lives(self, player : player.Player) -> None:
        """Met à jour le nombre de vies restantes lorsque ce nombre est modifié
        """
        self.__player_lives_number_UI.text = f"x  {player.lives}"
    
    def draw(self) -> None:
        """Affiche à l'écran l'interface utilisateur """
        self.__score_UI.draw()
        self.__player_lives_number_UI.draw()
        arcade.draw_sprite(self.__weapons_UI)
        arcade.draw_sprite(self.__ui_coin)
        arcade.draw_sprite(self.__player_lives_ui)
        if self.victory:
            self.__victory_UI.draw()
