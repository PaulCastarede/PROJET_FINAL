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


    #DECLARATION DES ATTRIBUTS
    player_sprite_list : arcade.SpriteList[arcade.Sprite]
    wall_list : arcade.SpriteList[arcade.Sprite]
    no_go_list : arcade.SpriteList[arcade.Sprite]
    slimes_list : arcade.SpriteList[arcade.Sprite]
    coins_list : arcade.SpriteList[arcade.Sprite]
    test_position_list : arcade.SpriteList[arcade.Sprite]
    Sword_Sprite : arcade.Sprite 
    score : int 


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
        self.right_pressed = False
        self.left_pressed = False
        self.test_position_list = arcade.SpriteList()
        self.map_width = 0  
        self.map_height = 0
        self.S_x = 0
        self.S_y = 0

       

        self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.death = False
        # Setup our game
        self.setup()

    def readmap(self) -> None:

        # Ouvrir le fichier sous l'acronyme 'file'
        with open("maps/map1.txt", "r", encoding="utf-8") as file:

            for line in file:
                stripped_line = line.strip()  # Supprimer chaque espace / saut

                # Lire chaque ligne jusqu'à la premiere "---"
                if stripped_line == "---":
                    break  # Fin de la configuration

                if ": " in stripped_line:
                    key, value = stripped_line.split(": ", 1)  # Diviser en 2 la ligne : clé, valeur
                    key = key.strip()  # Retirer les espaces
                    value = value.strip()  # Retirer les espaces

                    # Bloc if, try, except pour ne pas utiliser if, else :
                    if key in ("width", "height"):  # On va convertir en type int la valeur de la clé  
                        try:
                            value_int = int(value) 

                            if value_int <= 0: # On vérifie que la valeur de la clé est un entier positif
                                raise ValueError(f"Valeur invalide pour la clé : {key}: {value}")

                            if key == "width":
                                self.map_width = value_int  # On définit la largeur de la carte

                            else:
                                self.map_height = value_int  # On définit la longueur de la carte

                        except ValueError as e: 
                            raise ValueError(f"Valeur invalide pour la clé {key}: {value}") from e

            # Vérifier que les dimensions sont des entiers strictement positifs
            if self.map_width <= 0 or self.map_height <= 0:
                raise ValueError("Les dimensions dans la configuration sont invalides")

            # Initier les listes
            self.wall_list.clear()
            self.coins_list.clear()
            self.slimes_list.clear()
            self.no_go_list.clear()
            self.player_sprite_list.clear()

            # Lire les caractères de la carte après le ("---")
            map_lines = []

            for A in range(self.map_height):
                line = file.readline().rstrip('\n')  # Lire sans sauter une ligne

                if len(line) > self.map_width:
                    raise ValueError(f"La ligne dépasse la longueur de la config {self.map_width}")

                map_lines.append(line)

            # Vérifier que le fichier se termine par "---"
            end_line = file.readline().strip() # Ligne +1 après dernière ligne de la boucle 
            if end_line != "---":
                raise ValueError("Le fichier ne se termine pas par :  '---' ")

            for i, line in enumerate(map_lines): 
                for j, character in enumerate(line):
                    x = 64 * j  # (64 pixels par element)
                    y = 64 * (len(map_lines)-i) # (Car renversé)

                    match character:
                        case "=":  # Grass block
                            grass = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5, center_x=x, center_y=y)
                            self.wall_list.append(grass)
                        case "-":  # Half grass block
                            half_grass = arcade.Sprite(":resources:images/tiles/grassHalf_mid.png", scale=0.5, center_x=x, center_y=y)
                            self.wall_list.append(half_grass)
                        case "x":  # Crate
                            crate = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=0.5, center_x=x, center_y=y)
                            self.wall_list.append(crate)
                        case "*":  # Coin
                            coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.5, center_x=x, center_y=y)
                            self.coins_list.append(coin)
                        case "o":  # Slime enemy
                            slime = arcade.Sprite(":resources:images/enemies/slimeBlue.png", scale=0.5, center_x=x, center_y=y)
                            slime.change_x = SLIMES_SPEED  # Slime movement speed
                            self.slimes_list.append(slime)
                        case "£":  # Lava
                            lava = arcade.Sprite(":resources:images/tiles/lava.png", scale=0.5, center_x=x, center_y=y)
                            self.no_go_list.append(lava)
                        case "S":  # Player start position
                            self.S_x = x
                            self.S_y = y

    def setup(self) -> None:
        """Set up the game here."""

        self.readmap()     #Génération de la map

        
        self.player_sprite = arcade.Sprite( 
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",            #Génération du joueur
            center_x=self.S_x,
            center_y=self.S_y, scale=0.5
        )
        self.death = False
        self.score = 0
        self.player_sprite_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY)

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
        #Waiting for a new version mypy
        self.camera.position = self.player_sprite.position  #type: ignore
        

        for slime in self.slimes_list:                                            #Comportement des slimes 
            slime.center_x += slime.change_x 
            below = arcade.Sprite(center_x = slime.center_x + slime.change_x * 85, center_y = slime.center_y - 30 )
            below_collision = arcade.check_for_collision_with_list(below, self.wall_list)                                             #Check s'il y a un wall en dessous de l'endroit ou le slime se dirige                   
            front = arcade.Sprite(scale = 0.005, center_x= slime.center_x + slime.change_x * 22 , center_y = slime.center_y - 15 )
            front_collision = arcade.check_for_collision_with_list(front, self.wall_list)                                             #Check s'il y a un obstacle en face du slime
            self.test_position_list.append(front)
            if not below_collision or front_collision:
                slime.change_x *= -1                        #S'il y a un obstacle, le slime fait demit-tour


        collided_coins = arcade.check_for_collision_with_list(
            self.player_sprite, 
            self.coins_list                                             #Vérifie si le joueur est en contact avec des pièces
        )
        for coin in collided_coins:
            self.score += len(collided_coins)                           #Incrémente le score du nombre de pièces  
            coin.remove_from_sprite_lists()                             #Retire les pièces en contact avec le joueur
            arcade.play_sound(self.coin_sound)
                                                        

        collided_no_go = arcade.check_for_collision_with_list(
            self.player_sprite, 
            self.no_go_list)
        collided_slimes = arcade.check_for_collision_with_list(         #Vérifie si le joueur est en contact avec un élément léthal
            self.player_sprite, 
            self.slimes_list)
        
        if not(not collided_no_go) or not(not collided_slimes)  :    #Si le joueur est en collision avec la lave ou un monstre...
            self.death = True                                        #...le joueur meurt.
        

        if self.death :
            arcade.play_sound(self.death_sound)
            self.player_sprite_list.clear()                             # Si le joueur est mort, déclenche l'animation et le son de mort
            time.sleep(0.25)
            self.setup()

    def on_draw(self) -> None:                                       #Affichage de tous les sprites
        self.clear()
        with self.camera.activate():
            self.wall_list.draw()
            self.player_sprite_list.draw()
            self.coins_list.draw()
            self.no_go_list.draw()
            self.slimes_list.draw()