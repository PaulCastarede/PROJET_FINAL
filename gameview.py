import arcade
import time 
import math
import random
import dataclasses
from typing import Final

class Bat(arcade.Sprite): 
    x_spawn : Final[float]
    y_spawn : Final[float]
    time_travel : int
    theta : float

    def __init__(self, path_or_texture : str, center_x : float, center_y : float, scale : float) -> None:
        super().__init__(path_or_texture,scale, center_x, center_y )
        self.x_spawn = self.center_x
        self.y_spawn = self.center_y
        self.time_travel = 0
        self.theta = 0
    
    #Calcul de la distance entre la position de la bat et son point d'apparition
    def distance_from_spawn(self) -> float: 
        return math.sqrt((self.center_x - self.x_spawn)**2 + (self.center_y - self.y_spawn)**2) 
    


PLAYER_MOVEMENT_SPEED = 5
"""Lateral speed of the player, in pixels per frame."""

PLAYER_GRAVITY = 1
"""Gravity applied to the player, in pixels per frame²."""

PLAYER_JUMP_SPEED = 18
"""Instant vertical speed for jumping, in pixels per frame."""

SLIMES_SPEED = 1
"""Speed of the slimes, in pixels per frame"""

BAT_SPEED = 2
"""Speed of the slimes, in pixels per frame"""

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1


class GameView(arcade.View):
    """Main in-game view."""
    


    #DECLARATION DES ATTRIBUTS
    player_sprite_list : arcade.SpriteList[arcade.Sprite]
    wall_list : arcade.SpriteList[arcade.Sprite]
    no_go_list : arcade.SpriteList[arcade.Sprite]
    slimes_list : arcade.SpriteList[arcade.Sprite]
    bats_list : arcade.SpriteList[Bat]
    monsters_list : arcade.SpriteList[arcade.Sprite]
    coins_list : arcade.SpriteList[arcade.Sprite]

    
    test_position_list : arcade.SpriteList[arcade.Sprite]


    exit_list : arcade.SpriteList[arcade.Sprite]
    sword_sprite_list : arcade.SpriteList[arcade.Sprite] 
    score : int 
    score_UI : arcade.Text
    timetravel_UI : arcade.Text
    victory_text : arcade.Text
    Next_map : str
    last_level : bool
    Victory : bool

    # INITIALISATION DE LA PARTIE
    def __init__(self) -> None:
        super().__init__()
        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        
        #Initialisation des tributs
        self.player_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.no_go_list = arcade.SpriteList(use_spatial_hash=True)
        self.slimes_list = arcade.SpriteList()
        self.bats_list = arcade.SpriteList()
        self.camera = arcade.camera.Camera2D()
        self.idle_camera = arcade.camera.Camera2D()
        self.coins_list = arcade.SpriteList(use_spatial_hash=True)
        self.exit_list = arcade.SpriteList(use_spatial_hash=True)
        self.right_pressed = False
        self.left_pressed = False
        self.mouse_left_pressed = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.test_position_list = arcade.SpriteList()
        self.map_width = 0  
        self.map_height = 0
        self.S_x = 0
        self.S_y = 0
        self.slime_textures = []
        self.sword_sprite_list = arcade.SpriteList()

        
        
        #On ajoute le sprite du slime qui regarde à gauche
        texture = arcade.load_texture(":resources:/images/enemies/slimeBlue.png")    
        self.slime_textures.append(texture)   
        #Et celui du slime regardant a droite                                    
        texture = arcade.load_texture("assets/slimeBlue.png",)
        self.slime_textures.append(texture)
       

        self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.death = False
        # Setup our game
        self.setup()

    def readmap(self, map : str) -> None:

        # Ouvrir le fichier sous l'acronyme 'file'
        with open(f"maps/{map}", "r", encoding="utf-8") as file:

            self.last_level = True

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
                    if key in ("width", "height", "next-map"):  # On va convertir en type int la valeur de la clé  
                        try:
                            if key in ("width", "height"):
                                if int(value) <= 0:             # On vérifie que la valeur de la clé est un entier positif
                                    raise ValueError(f"Valeur invalide pour la clé : {key}: {value}")

                            if key == "width":
                                self.map_width = int(value) # On définit la largeur de la carte

                            if key == "height":
                                self.map_height = int(value)  # On définit la longueur de la carte

                            if key == "next-map":
                                self.last_level = False
                                self.Next_map = value        # On définit le niveau suivant 

                        except ValueError as e: 
                            raise ValueError(f"Valeur invalide pour la clé {key}: {value}") from e

            # Vérifier que les dimensions sont des entiers strictement positifs
            if self.map_width <= 0 or self.map_height <= 0:
                raise ValueError("Les dimensions dans la configuration sont invalides")

            # Effacer les sprites précédents
            self.wall_list.clear()
            self.coins_list.clear()
            self.slimes_list.clear()
            self.no_go_list.clear()
            self.player_sprite_list.clear()
            self.exit_list.clear()
            self.bats_list.clear()
            self.test_position_list.clear()

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
                            slime = arcade.Sprite("assets\slimeBlue.png", scale=0.5, center_x=x, center_y=y)
                            slime.change_x = SLIMES_SPEED  # Slime movement speed
                            self.slimes_list.append(slime)
                        case "v":  # Bat enemy
                             
                            bat = Bat("assets/kenney-extended-enemies-png/bat.png", scale=0.5, center_x=x, center_y=y)
                            self.bats_list.append(bat)
                        case "£":  # Lava
                            lava = arcade.Sprite(":resources:images/tiles/lava.png", scale=0.5, center_x=x, center_y=y)
                            self.no_go_list.append(lava)
                        case "S":  # Player start position
                            self.player_sprite =  arcade.Sprite( 
                           ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",            #Génération du joueur
                            center_x=x,
                            center_y=y, scale=0.5)
                            self.player_sprite_list.append(self.player_sprite)


                            self.physics_engine = arcade.PhysicsEnginePlatformer(
                            self.player_sprite, 
                            walls=self.wall_list,                                     #On définit les lois physiques qui s'appliquent sur le sprite Player
                            gravity_constant=PLAYER_GRAVITY)

                        case "E":  #Map end
                            exit = arcade.Sprite(":resources:/images/tiles/signExit.png", scale = 0.5, center_x = x, center_y = y)
                            self.exit_list.append(exit)

    def setup(self) -> None:
        """Set up the game here."""

        self.readmap("map1.txt")     #Génération de la map
        
        self.death = False
        self.Victory = False
        self.score = 0              #Reset du score au début du jeu/ à chaque mort

    

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
   
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        # Mettre à jour les coordonnées de la souris
        self.mouse_x = x
        self.mouse_y = y
        
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_left_pressed = True

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT : 
            self.mouse_left_pressed = False
            self.sword_sprite_list.clear()
    


    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances", or "ticks".
        """
        self.player_sprite.change_x = 0
        if self.right_pressed:
            self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED       #Joueur avance si -> pressed
        if self.left_pressed:                 
            self.player_sprite.change_x -= PLAYER_MOVEMENT_SPEED       #Joueur recule si <- pressed
        
        self.physics_engine.update()
        #Waiting for a new version mypy
        self.camera.position = self.player_sprite.position  #type: ignore
        
        
        #COMPORTEMENT DES SLIMES
        for slime in self.slimes_list:          
            slime.center_x += slime.change_x 
            below = arcade.Sprite(center_x = slime.center_x + slime.change_x * 85, center_y = slime.center_y - 30 )
            below_collision = arcade.check_for_collision_with_list(below, self.wall_list)                                             #Check s'il y a un wall en dessous de l'endroit ou le slime se dirige                   
            front = arcade.Sprite(scale = 0.005, center_x= slime.center_x + slime.change_x * 22 , center_y = slime.center_y - 15 )
            front_collision = arcade.check_for_collision_with_list(front, self.wall_list)                                             #Check s'il y a un obstacle en face du slime
            self.test_position_list.append(front)
            if not below_collision or front_collision:
                #S'il y a un obstacle, le slime fait demi-tour
                slime.change_x *= -1  
            
            #On adapte le sprite du slime en fonction de sa direction
            if slime.change_x < 0:
                slime.texture = self.slime_textures[TEXTURE_LEFT]
            elif slime.change_x > 0:
                slime.texture = self.slime_textures[TEXTURE_RIGHT]

            
        #COMPORTEMENT DES BATS 
        for bats in self.bats_list:
            bats.center_x += bats.change_x
            bats.center_y += bats.change_y
            bats.change_x = BAT_SPEED*math.cos(bats.theta)
            bats.change_y = BAT_SPEED*math.sin(bats.theta)
            bats.time_travel += 1
            ###########
            if  bats.distance_from_spawn() > 200.0 and bats.time_travel > 30:
                bats.theta += math.pi
                bats.time_travel = 0
            if bats.time_travel%15 == 0:
                bats.theta = random.normalvariate(bats.theta, math.pi/10)



        if self.mouse_left_pressed:
            world_coords = self.camera.unproject((self.mouse_x, self.mouse_y))
            world_x = world_coords[0]
            world_y =  world_coords[1]

            self.position_x = 0
            # Calculer l'angle entre le joueur et la position de la souris dans le monde
            self.angle = math.atan2(world_y - self.player_sprite.center_y, world_x - self.player_sprite.center_x)
            print(f"Clic écran: ({self.mouse_x}, {self.mouse_y})")
            print(f"Clic monde (unproject): ({world_x}, {world_y})")
            print(f"Joueur monde: ({self.player_sprite.center_x}, {self.player_sprite.center_y})")
            print(f"Angle (radians): ({self.angle}, (degrés): {math.degrees(self.angle)}")

            if abs(math.degrees(self.angle)) > 90:
                self.position_x = -20
            else : 
                self.position_x =20


            if len(self.sword_sprite_list)==0:
                self.sword_sprite = arcade.Sprite(
                                    "assets/kenney-voxel-items-png/sword_silver.png",
                                    scale=0.5 * 0.7,
                                    center_x=self.player_sprite.center_x + self.position_x,
                                    center_y=self.player_sprite.center_y - 10,
                                    angle=-math.degrees(self.angle)+45)
                self.sword_sprite_list.append(self.sword_sprite)
            else :
                self.sword_sprite_list[0].center_x = self.player_sprite.center_x + self.position_x
                self.sword_sprite_list[0].center_y = self.player_sprite.center_y-10
                self.sword_sprite_list[0].angle=-math.degrees(self.angle)+45


            
        if self.mouse_left_pressed and len(self.sword_sprite_list) > 0:  
                 touched_slimes = arcade.check_for_collision_with_list(self.sword_sprite_list[0], self.slimes_list)
                 touched_bats = arcade.check_for_collision_with_list(self.sword_sprite_list[0], self.bats_list)

                 for slime in touched_slimes or touched_bats:
                     self.score += len(touched_slimes)     
                     slime.remove_from_sprite_lists()
                     arcade.play_sound(self.coin_sound)
 


        collided_coins = arcade.check_for_collision_with_list(
            self.player_sprite, 
            self.coins_list               #Vérifie si le joueur est en contact avec des pièces
        )
        for coin in collided_coins:
            self.score += len(collided_coins)              #Incrémente le score du nombre de pièces  
            coin.remove_from_sprite_lists()                #Retire les pièces en contact avec le joueur
            arcade.play_sound(self.coin_sound)


        self.score_UI = arcade.Text( x =  70, y = 650, font_size = 20, text = f"Score : {str(self.score)}"    )                                   
        
        collided_no_go = arcade.check_for_collision_with_list(          #
            self.player_sprite,                                         #
            self.no_go_list)                                            #
        collided_slimes = arcade.check_for_collision_with_list(         #Vérifie si le joueur est en contact avec un élément léthal
            self.player_sprite,                                         # 
            self.slimes_list)                                           #
        collided_bats = arcade.check_for_collision_with_list(           #     
            self.player_sprite,                                         #
            self.bats_list)                                             #
        
        if collided_no_go or  collided_slimes or collided_bats  :    #Si le joueur est en collision avec la lave ou un monstre...
            self.death = True                                                         #...le joueur meurt.
        

        #NEXT LEVEL
        if arcade.check_for_collision_with_list(self.player_sprite, self.exit_list) :
            if not(self.last_level):
                self.readmap( map = self.Next_map)
            #VICTORY !
            else:
                self.victory_text = arcade.Text(x = 400, y = 360, font_size = 100, text = "YOU WON" )
                self.Victory = True
                



            
        #GAME OVER SET
        if self.death :
             arcade.play_sound(self.death_sound)
             self.player_sprite_list.clear()                             # Si le joueur est mort, déclenche l'animation et le son de mort
             time.sleep(0.25)
             self.setup()
    


    #AFFICHAGE DES SPRITES
    def on_draw(self) -> None:                                 
        self.clear()
        with self.camera.activate():
            self.wall_list.draw()
            self.player_sprite_list.draw()
            self.coins_list.draw()
            self.no_go_list.draw()
            self.slimes_list.draw()
            self.bats_list.draw()
            self.exit_list.draw()
            #self.test_position_list.draw()
            if self.mouse_left_pressed:
                self.sword_sprite_list.draw()
            #for elem in self.bats_list:
                #arcade.draw_circle_outline(elem.x_spawn,elem.y_spawn, 200, arcade.color.RED)
        with self.idle_camera.activate():
             self.score_UI.draw()
             if self.Victory :                
                 self.victory_text.draw()
        