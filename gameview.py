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


   # INITIALISATION DE LA PARTIE

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.player_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.camera = arcade.camera.Camera2D()
        self.coins_list = arcade.SpriteList(use_spatial_hash=True)
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
        
        for i in range(128, 1251, 256) :
            coin_sprite = arcade.Sprite(":resources:images/items/coinGold.png",
              center_x = i,
              center_y = 96,
              scale = 0.5)  
            self.coins_list.append(coin_sprite)




 # COMMANDES

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        match key:
            case arcade.key.RIGHT:
                # start moving to the right
                self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED
            case arcade.key.LEFT:
                # start moving to the left
                self.player_sprite.change_x -= PLAYER_MOVEMENT_SPEED
            case arcade.key.UP: 
                # jump by giving an initial vertical speed
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
            case arcade.key.ESCAPE:
                # resets the game
                self.__init__()
   
            
    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
        match key:
            case arcade.key.RIGHT :
                # stop lateral movement
                self.player_sprite.change_x -= 5
            case arcade.key.LEFT :
                self.player_sprite.change_x += 5 





    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances", or "ticks".
        """
        self.physics_engine.update()
        self.camera.position = self.player_sprite.position #type : ignore 
        a = len(arcade.check_for_collision_with_list(self.player_sprite, self.coins_list))
        if a > 0 :
            for i in range(a):
                arcade.check_for_collision_with_list(self.player_sprite, self.coins_list)[i].remove_from_sprite_lists()




    # AFFICHAGE #
    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()
        with self.camera.activate():
          self.wall_list.draw()
          self.player_sprite_list.draw()
          self.coins_list.draw()