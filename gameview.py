import arcade
import time 

PLAYER_MOVEMENT_SPEED = 5
"""Lateral speed of the player, in pixels per frame."""

PLAYER_GRAVITY = 1
"""Gravity applied to the player, in pixels per frame²."""

PLAYER_JUMP_SPEED = 18
"""Instant vertical speed for jumping, in pixels per frame."""

SLIMES_SPEED = 1
"""Speed of the slimes, in pixels per frame"""

class GameView(arcade.View):
    """Main in-game view."""

    # INITIALISATION DE LA PARTIE
    def __init__(self) -> None:
        super().__init__()
        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.player_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.no_go_list = arcade.SpriteList(use_spatial_hash=True)
        self.slimes_list = arcade.SpriteList()
        self.camera = arcade.camera.Camera2D()
        self.coins_list = arcade.SpriteList(use_spatial_hash=True)
        self.no_go_list = arcade.SpriteList(use_spatial_hash=True)
        self.right_pressed = False
        self.left_pressed = False
        self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/gameover1.wav.")
        self.death = False
        
    

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
        self.death = False
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            center_x=self.S_x,
            center_y=self.S_y, scale=0.5
        )
        self.player_sprite_list.append(self.player_sprite)
        self.wall_list.clear()
        self.player_sprite_death = arcade.Sprite(
        ":resources:/images/animated_characters/female_adventurer/femaleAdventurer_fall.png",
        center_x=self.player_sprite.center_x,
        center_y=self.player_sprite.center_y
        )



    

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
                    arcade.play_sound(self.jump_sound)
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
        

        for slime in self.slimes_list:
            slime.change_x += SLIMES_SPEED
            below = arcade.check_for_collision_with_list(slime, self.wall_list)
            front = arcade.Sprite(center_x= slime.center_x + slime.change_x * 10, center_y= 1000) #slime.center_y + 20)
            front_collision = arcade.check_for_collision_with_list(front, self.wall_list)
            
            if not below or front_collision:
                slime.change_x *= -1


        collided_coins = arcade.check_for_collision_with_list(
            self.player_sprite, 
            self.coins_list
        )
        for coin in collided_coins:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.coin_sound)

        collided_no_go = arcade.check_for_collision_with_list(
            self.player_sprite, 
            self.no_go_list)
        collided_slimes = arcade.check_for_collision_with_list(
            self.player_sprite, 
            self.slimes_list)
        
        if not(not collided_no_go) or not(not collided_slimes)  :    #Si le joueur est en collision avec la lave ou un monstre...
            self.death = True                                        #...le joueur meurt.
        
        self.update_camera()

        if self.death :
            arcade.play_sound(self.death_sound)
            self.player_sprite_list.clear()                             # Si le joueur est mort, déclenche l'animation et le son de mort
            self.player_sprite_list.append(self.player_sprite_death)
            time.sleep(1)
            self.setup()

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
            self.no_go_list.draw()
            self.slimes_list.draw()