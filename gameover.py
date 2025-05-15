from __future__ import annotations
import arcade
import gameview

def gameover(gameview : gameview.GameView) -> None:
    gameview.world.clear(clear_player=True)
    gameview.background_color = arcade.csscolor.BLACK

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        match key:
            case arcade.key.R:
                gameview.setup()
      

