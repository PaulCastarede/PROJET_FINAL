import arcade

PLAYER_MOVEMENT_SPEED = 5
"""Lateral speed of the player, in pixels per frame."""

PLAYER_GRAVITY = 1
"""Gravity applied to the player, in pixels per frame²."""

PLAYER_JUMP_SPEED = 18
"""Instant vertical speed for jumping, in pixels per frame."""

class GameView(arcade.View):
    """Main in-game view."""

    # INITIALISATION DE LA PARTIE
    def __init__(self) -> None:
        super().__init__()
        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.player_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.camera = arcade.camera.Camera2D()
        self.coins_list = arcade.SpriteList(use_spatial_hash=True)
        self.right_pressed = False
        self.left_pressed = False

        self.camera_margin_left = 150
        self.camera_margin_right = 200  
        self.camera_margin_top = 150
        self.camera_margin_bottom = 200
        # Setup our game
        self.setup()

    def setup(self) -> None:
        """Set up the game here."""
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            center_x=64,
            center_y=128
        )
        self.player_sprite_list.clear()
        self.player_sprite_list.append(self.player_sprite)
        self.wall_list.clear()

        for i in range(0, 1187, 64):
            grass_sprite = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5)
            grass_sprite.center_x = i
            grass_sprite.center_y = 32
            self.wall_list.append(grass_sprite)
        
        for i in range(256, 769, 256):
            boxCrate_sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=0.5)
            boxCrate_sprite.center_x = i 
            boxCrate_sprite.center_y = 96
            self.wall_list.append(boxCrate_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY
        )

        self.coins_list.clear()
        for i in range(128, 1251, 256):
            coin_sprite = arcade.Sprite(
                ":resources:images/items/coinGold.png",
                center_x=i,
                center_y=96,
                scale=0.5
            )  
            self.coins_list.append(coin_sprite)

    # COMMANDES
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        match key:
            case arcade.key.RIGHT:
                # start moving to the right
                self.right_pressed = True
            case arcade.key.LEFT:
                # start moving to the left
                self.left_pressed = True
            case arcade.key.UP: 
                if self.physics_engine.can_jump():
                    # jump by giving an initial vertical speed
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
            case arcade.key.ESCAPE:
                # resets the game
                self.setup()

    def on_key_release(self, key: int, modifiers: int) -> None:
        match key:
            case arcade.key.RIGHT:
                self.right_pressed = False
            case arcade.key.LEFT:
                self.left_pressed = False

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances", or "ticks".
        """
        self.player_sprite.change_x = 0
        if self.right_pressed:
            self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED
        if self.left_pressed:
            self.player_sprite.change_x -= PLAYER_MOVEMENT_SPEED
        
        self.physics_engine.update()
        self.camera.position = self.player_sprite.position

        collided_coins = arcade.check_for_collision_with_list(
            self.player_sprite, 
            self.coins_list
        )
        for coin in collided_coins:
            coin.remove_from_sprite_lists()
        self.update_camera()

    def update_camera(self) -> None:
        # Position du joueur
        player_x = self.player_sprite.center_x
        player_y = self.player_sprite.center_y

        # Position actuelle de la caméra
        camera_x, camera_y = self.camera.position

        # Largeur et hauteur de la vue de la caméra
        screen_width, screen_height = self.window.width, self.window.height

        # Calculer les limites de la zone de suivi
        left_boundary = camera_x - (screen_width / 2) + self.camera_margin_left
        right_boundary = camera_x + (screen_width / 2) - self.camera_margin_right
        top_boundary = camera_y + (screen_height / 2) - self.camera_margin_top
        bottom_boundary = camera_y - (screen_height / 2) + self.camera_margin_bottom

        # Déplacer la caméra si le joueur dépasse les marges
        if player_x < left_boundary:
            camera_x -= left_boundary - player_x
        elif player_x > right_boundary:
            camera_x += player_x - right_boundary

        if player_y < bottom_boundary:
            camera_y -= bottom_boundary - player_y
        elif player_y > top_boundary:
            camera_y += player_y - top_boundary

        # Appliquer la nouvelle position de la caméra
        self.camera.position = (camera_x, camera_y)

    # AFFICHAGE #
    def on_draw(self) -> None:
        self.clear()
        with self.camera.activate():
            self.wall_list.draw()
            self.player_sprite_list.draw()
            self.coins_list.draw()