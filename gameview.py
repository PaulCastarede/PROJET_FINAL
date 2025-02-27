import arcade

PLAYER_MOVEMENT_SPEED = 5
"""Lateral speed of the player, in pixels per frame."""

PLAYER_GRAVITY = 1
"""Gravity applied to the player, in pixels per frame²."""

PLAYER_JUMP_SPEED = 18
"""Instant vertical speed for jumping, in pixels per frame."""

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
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, walls=self.wall_list,gravity_constant=PLAYER_GRAVITY)    

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        match key:
            case arcade.key.RIGHT:
                # start moving to the right
                self.player_sprite.change_x = +PLAYER_MOVEMENT_SPEED
            case arcade.key.LEFT:
                # start moving to the left
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            case arcade.key.UP: 
                # jump by giving an initial vertical speed
                self.player_sprite.change_y = PLAYER_JUMP_SPEED   

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
        match key:
            case arcade.key.RIGHT | arcade.key.LEFT:
                # stop lateral movement
                self.player_sprite.change_x = 0

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances", or "ticks".
        """
        self.physics_engine.update()

    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()
        self.player_sprite_list.draw()
        self.wall_list.draw()