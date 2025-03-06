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
        self.monster_list = arcade.SpriteList(use_spatial_hash=True)
        self.camera = arcade.camera.Camera2D()
        self.coins_list = arcade.SpriteList(use_spatial_hash=True)
        self.no_go_list = arcade.SpriteList(use_spatial_hash=True)
        self.right_pressed = False
        self.left_pressed = False
        self.map_width = 0
        self.map_height = 0
        self.S_x = 0
        self.S_y = 0
        # Setup our game
        self.readmap()
        self.setup()


    def readmap(self) -> None:
        with open("maps/map1.txt", "r") as file:
            for i in range(2):
                    line = file.readline()  # Retirer les espaces et sauts de ligne
                    if ": " in line:
                        key, value = line.split(":", 1)  # Séparer la clé et la valeur
                        key = key.strip()
                        value = int(value.strip())  # Convertir la valeur en entier
                        if key == "width":
                            self.map_width = value
                        elif key == "height":
                            self.map_height = value

            if self.map_width == 0 or self.map_height == 0 : 
                    raise ValueError()
            
            for i, line in enumerate(file, start=3):
                if i > self.map_height + 3 :
                    break
                for j, character in enumerate(line):
                    match character :
                        case "=":   
                            grass= arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5, center_x=64*j, center_y= 64*(self.map_height - i))
                            self.wall_list.append(grass)
                                
                        case "-":   
                            half_grass = arcade.Sprite(":resources:/images/tiles/grassHalf_mid.png", scale=0.5, center_x=64*j, center_y= 64*(self.map_height - i))
                            self.wall_list.append(half_grass)
                    
                        case "x":   
                            crate= arcade.Sprite(":resources:/images/tiles/boxCrate_double.png", scale=0.5, center_x=64*j, center_y= 64*(self.map_height - i))
                            self.wall_list.append(crate)
                                        
                        case "*":   
                            coin = arcade.Sprite(":resources:/images/items/coinGold.png", scale=0.5, center_x=64*j, center_y= 64*(self.map_height - i))
                            self.coins_list.append(coin)
                    
                        case "o":   
                            monster = arcade.Sprite(":resources:/images/enemies/slimeBlue.png", scale=0.5, center_x=64*j, center_y= 64*(self.map_height - i))
                            self.monster_list.append(monster)
                    
                        case "£":   
                            lava = arcade.Sprite(":resources:/images/tiles/lava.png", scale=0.5, center_x=64*j, center_y= 64*(self.map_height - i))
                            self.no_go_list.append(lava)
                    
                        case "S":   
                            self.S_x = 64*j
                            self.S_y = 64*(self.map_height - i)
                    
    def setup(self) -> None:
        """Set up the game here."""
        self.player_sprite_list.clear()
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            center_x=self.S_x,
            center_y=self.S_y, scale=0.5
        )
        self.player_sprite_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY
        )

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


    # AFFICHAGE #
    def on_draw(self) -> None:
        self.clear()
        with self.camera.activate():
            self.wall_list.draw()
            self.player_sprite_list.draw()
            self.coins_list.draw()
            self.no_go_list.draw()
            self.monster_list.draw()