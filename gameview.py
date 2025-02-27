import arcade
class GameView(arcade.View):
    player_sprite: arcade.Sprite
    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    """Main in-game view."""

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.player_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Setup our game
        self.setup()

    def setup(self) -> None:
        """Set up the game here."""
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            center_x=64,
            center_y=128
        )
        self.player_sprite_list.append(self.player_sprite)

        for i in range(0, 1187, 64):
            grass_sprite = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5)
            grass_sprite.center_x = i
            grass_sprite.center_y = 32
            self.wall_list.append(grass_sprite)
        
        for i in range(256,769, 256):
            boxCrate_sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=0.5)
            boxCrate_sprite.center_x = i 
            boxCrate_sprite.center_y = 96
            self.wall_list.append(boxCrate_sprite)

    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()
        self.player_sprite_list.draw()
        self.wall_list.draw()