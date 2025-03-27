import arcade
import time 
import math
import random
import dataclasses
from typing import Final
from monsters import *


PLAYER_MOVEMENT_SPEED = 5
"""Lateral speed of the player, in pixels per frame."""

PLAYER_GRAVITY = 1
"""Gravity applied to the player, in pixels per frame²."""

PLAYER_JUMP_SPEED = 18
"""Instant vertical speed for jumping, in pixels per frame."""

ARROW_SPEED = 15
"""Speed of the arrows, in pixels per frame"""

ARROW_GRAVITY = 0.4
"""Lateral speed of the arrows, in pixels per frame"""



class GameView(arcade.View):
    """Main in-game view."""
    


    #DECLARATION DES ATTRIBUTS
    player_sprite : arcade.Sprite
    player_sprite_list : arcade.SpriteList[arcade.Sprite]
    wall_list : arcade.SpriteList[arcade.Sprite]
    no_go_list : arcade.SpriteList[arcade.Sprite]
    monsters_list : arcade.SpriteList[Monster]
    coins_list : arcade.SpriteList[arcade.Sprite]
    physics_engine : arcade.PhysicsEnginePlatformer
    
    test_position_list : arcade.SpriteList[arcade.Sprite]


    exit_list : arcade.SpriteList[arcade.Sprite]
    arrow_sprite_list : arcade.SpriteList[arcade.Sprite]
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
        self.monsters_list = arcade.SpriteList()
        self.coins_list = arcade.SpriteList(use_spatial_hash=True)
        self.exit_list = arcade.SpriteList(use_spatial_hash=True)
        self.test_position_list = arcade.SpriteList()
        self.arrow_sprite_list = arcade.SpriteList()

        self.camera = arcade.camera.Camera2D()
        self.idle_camera = arcade.camera.Camera2D()
        self.arrow = arcade.Sprite("assets/kenney-voxel-items-png/arrow.png", scale=0.5) 


        self.right_pressed = False
        self.left_pressed = False
        self.mouse_left_pressed = False
        self.arrow_release = False
        
        self.active_weapon = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.map_width = 0  
        self.map_height = 0
        self.S_x = 0
        self.S_y = 0
        self.angle : float = 0
        self.world_x : float = 0
        self.world_y : float = 0

        
       

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
            self.monsters_list.clear()
            self.no_go_list.clear()
            self.player_sprite_list.clear()
            self.exit_list.clear()
            self.test_position_list.clear()
            self.arrow_sprite_list.clear()

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
                            slime = Slime("assets/slimeBlue.png", scale=0.5, center_x=x, center_y=y)
                            self.monsters_list.append(slime)
                        case "v":  # Bat enemy
                                
                            bat = Bat("assets/kenney-extended-enemies-png/bat.png", scale=0.5, center_x=x, center_y=y)
                            self.monsters_list.append(bat)
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

            for slimes in [monsters for monsters in self.monsters_list if type(monsters) == Slime] :
                slimes.wall_list = self.wall_list



    def setup(self) -> None:
        """Set up the game here."""

        self.readmap( "map1.txt")     #Génération de la map
        
        self.death = False
        self.Victory = False
        self.score = 0 #Reset du score au début du jeu/ à chaque mort
        self.weapons_list = []
        self.weapons_list.append(arcade.Sprite("assets/kenney-voxel-items-png/sword_silver.png",scale=0.5 * 0.7))
        self.weapons_list.append(arcade.Sprite("assets/kenney-voxel-items-png/bow.png", scale=0.5))
        self.sword = self.weapons_list[0]
        self.bow = self.weapons_list[1]

     

    

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
        world_coords = self.camera.unproject((self.mouse_x, self.mouse_y)) #Coordonnées monde
        self.world_x = world_coords[0]
        self.world_y =  world_coords[1]
        self.angle = math.atan2(self.world_y - self.player_sprite.center_y, self.world_x - self.player_sprite.center_x) # Calculer l'angle entre le joueur et la position de la souris dans le monde
    
        
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_left_pressed = True
            if self.active_weapon == 1 :
                self.arrow = arcade.Sprite("assets/kenney-voxel-items-png/arrow.png", scale=0.5,  center_x=self.player_sprite.center_x + self.position_x + 5, center_y=self.player_sprite.center_y - 5, angle=self.bow.angle + 55)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            if self.active_weapon == 0:
                self.active_weapon =1
            else : 
                self.active_weapon =0

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT : 
            self.mouse_left_pressed = False
            if self.active_weapon == 1 :
                self.arrow_release = True
                self.arrow_sprite_list.append(self.arrow)
                self.arrow_sprite_list[-1].change_x = ARROW_SPEED * math.cos(self.angle)
                self.arrow_sprite_list[-1].change_y = ARROW_SPEED * math.sin(self.angle)



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
        
        
        #COMPORTEMENT DES MONSTRES
        for monster in self.monsters_list:
            monster.movement()         
            

        if self.mouse_left_pressed:
            self.position_x = 0
            if abs(math.degrees(self.angle)) > 90:
                self.position_x = -20
            else: 
                self.position_x = 20

            if self.active_weapon == 0:
                # Gestion de l'épée (inchangé)
                self.sword.center_x = self.player_sprite.center_x + self.position_x
                self.sword.center_y = self.player_sprite.center_y - 10
                self.sword.angle = -math.degrees(self.angle) + 45
            else:
                # Position et angle de l'arc
                self.bow.center_x = self.player_sprite.center_x + self.position_x 
                self.bow.center_y = self.player_sprite.center_y - 10
                self.bow.angle = -math.degrees(self.angle) - 35  # Angle de l'arc
                
                # Position statique de la flèche (même centre que l'arc)
                self.arrow.center_x = self.player_sprite.center_x + self.position_x + 5
                self.arrow.center_y = self.player_sprite.center_y - 5
                
                # Angle de la flèche 
                self.arrow.angle = -math.degrees(self.angle) + 55

        for arrow in self.arrow_sprite_list:
            # Appliquer la physique
            arrow.change_y -= ARROW_GRAVITY
            arrow.center_x += arrow.change_x
            arrow.center_y += arrow.change_y
            #arrow.angle = math.degrees(math.atan2(arrow.change_y, arrow.change_x)) + 90
            
            # Vérifier les collisions avec les murs
            if arcade.check_for_collision_with_list(arrow, self.wall_list):
                arrow.remove_from_sprite_lists()
                self.arrow_release = False
            
            # Vérifier les collisions avec les monstres
            touched_by_shot_monsters = arcade.check_for_collision_with_list(arrow, self.monsters_list)
            for monster in touched_by_shot_monsters:
                monster.remove_from_sprite_lists()
                arrow.remove_from_sprite_lists()
                self.score += 1
                arcade.play_sound(self.coin_sound)

            if (arrow.bottom > self.camera.viewport_height or arrow.top < 0 or arcade.check_for_collision_with_list(arrow, self.wall_list)):
                arrow.remove_from_sprite_lists()
            self.arrow_release = False
            
        if self.mouse_left_pressed:  
                 touched_monsters = arcade.check_for_collision_with_list(self.weapons_list[0], self.monsters_list)
                 for monster in touched_monsters: 
                     monster.remove_from_sprite_lists()
                     self.score += 1    
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
        collided_monsters = arcade.check_for_collision_with_list(         #Vérifie si le joueur est en contact avec un élément léthal
            self.player_sprite,                                         # 
            self.monsters_list)                                           #
        
        if collided_no_go or  collided_monsters  :    #Si le joueur est en collision avec la lave ou un monstre...
            self.death = True                                                         #...le joueur meurt.
        

        #NEXT LEVEL
        if arcade.check_for_collision_with_list(self.player_sprite, self.exit_list) :
            if not(self.last_level):
                self.readmap(map = self.Next_map)
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
            self.arrow_sprite_list.draw()
            self.wall_list.draw()
            self.player_sprite_list.draw()
            self.coins_list.draw()
            self.no_go_list.draw()
            self.monsters_list.draw()
            self.exit_list.draw()
            if self.mouse_left_pressed:
                arcade.draw_sprite(self.weapons_list[self.active_weapon])
                if self.active_weapon == 1:
                    arcade.draw_sprite(self.arrow)
            #self.test_position_list.draw()
            #for elem in self.bats_list:
                #arcade.draw_circle_outline(elem.x_spawn,elem.y_spawn, 200, arcade.color.RED)
        with self.idle_camera.activate():
             self.score_UI.draw()
             if self.Victory :                
                 self.victory_text.draw()