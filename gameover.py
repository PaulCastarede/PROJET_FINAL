from __future__ import annotations
import arcade
import gameview

class GameOverView(arcade.View):
    """Vue affichée lorsque le joueur perd toutes ses vies"""
    
    def __init__(self, game_view: gameview.GameView) -> None:
        super().__init__()
        self.game_view = game_view
        
    def on_show(self) -> None:
        """Cette méthode est appelée quand la vue devient active"""
        arcade.set_background_color(arcade.csscolor.BLACK)
        
    def on_draw(self) -> None:
        """Dessine l'écran de game over"""
        self.clear()
        
        # Dessine le texte GAME OVER
        arcade.draw_text("GAME OVER", 
                        self.window.width // 2, 
                        self.window.height // 2 + 50,
                        arcade.csscolor.WHITE, 
                        font_size=60, 
                        anchor_x="center")
        
        # Instructions pour redémarrer
        arcade.draw_text("Appuyez sur ENTER pour recommencer", 
                        self.window.width // 2, 
                        self.window.height // 2 - 50,
                        arcade.csscolor.WHITE, 
                        font_size=24, 
                        anchor_x="center")
    
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Gère les touches pressées sur l'écran de game over"""
        if key == arcade.key.ENTER:
            # Réinitialiser le jeu et revenir à la vue du jeu
            game_view = gameview.GameView()
            self.window.show_view(game_view)


def gameover(game_view: gameview.GameView) -> None:
    """Bascule vers l'écran de game over"""
    game_over_view = GameOverView(game_view)
    game_view.window.show_view(game_over_view)
      

