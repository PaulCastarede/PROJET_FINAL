from __future__ import annotations
import arcade
import gameview

class GameOverView(arcade.View):
    """Vue affichée lorsque le joueur perd toutes ses vies"""

    def __init__(self, game_view: gameview.GameView) -> None:
        super().__init__()
        self.game_view = game_view
        
    @property
    def game_over_text(self) -> arcade.Text:
        return arcade.Text("GAME OVER", 
                            self.window.width // 2, 
                            self.window.height // 2 + 50,
                            arcade.csscolor.WHITE, 
                            font_size=60, 
                            anchor_x="center")
    
    @property 
    def restart_text(self) -> arcade.Text:
        return arcade.Text("Appuyez sur ENTER pour recommencer", 
                        self.window.width // 2, 
                        self.window.height // 2 - 50,
                        arcade.csscolor.WHITE, 
                        font_size=24, 
                        anchor_x="center")
    
    def on_show(self) -> None:
        """Cette méthode est appelée quand la vue devient active"""
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self) -> None:
        """Dessine l'écran de game over"""
        self.clear()
        # Dessine le texte GAME OVER
        self.game_over_text.draw()
        # Instructions pour redémarrer
        self.restart_text.draw()
    
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Gère les touches pressées sur l'écran de game over"""
        if key == arcade.key.ENTER:
            # Réinitialiser le jeu et revenir à la vue du jeu
            game_view = gameview.GameView()
            self.window.show_view(game_view)

      

