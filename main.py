import arcade
from gameview import GameView
import alt_game_views.endgame as endgame
# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

def main() -> None:
    """Main function."""

    # Create the (unique) Window, setup our GameView, and launch
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    try : 
        game_view = GameView()
        window.show_view(game_view)
        arcade.run()
        game_view.profiler.dump_stats("profile.prof")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()  