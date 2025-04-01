import arcade 
from monsters import Bat
from monsters import Slime
from player import *
from monsters import *
from weapons import *

class World:
    player : Player
    player_sprite_list : arcade.SpriteList[Player]
    wall_list : arcade.SpriteList[arcade.Sprite]
    no_go_list : arcade.SpriteList[arcade.Sprite]
    monsters_list : arcade.SpriteList[Monster]
    coins_list : arcade.SpriteList[arcade.Sprite]
    physics_engine : arcade.PhysicsEnginePlatformer
    exit_list : arcade.SpriteList[arcade.Sprite]
    arrow_sprite_list : arcade.SpriteList[Arrow]
    Next_map : str
    last_level : bool
    map_width : int
    map_height : int 
    
    def __init__(self)-> None:
        self.player_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.no_go_list = arcade.SpriteList(use_spatial_hash=True)
        self.monsters_list = arcade.SpriteList()
        self.coins_list = arcade.SpriteList(use_spatial_hash=True)
        self.exit_list = arcade.SpriteList(use_spatial_hash=True)
        self.arrow_sprite_list = arcade.SpriteList()
        self.map_width = 0  
        self.map_height = 0

    def draw(self)-> None:
        self.player_sprite_list.draw()
        self.wall_list.draw()
        self.no_go_list.draw()
        self.monsters_list.draw()
        self.coins_list.draw()
        self.exit_list.draw()
        self.arrow_sprite_list.draw()


def readmap(self : World, map : str) -> None:

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
            self.arrow_sprite_list.clear()
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
                            self.player =  Player( 
                            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",            #Génération du joueur
                            center_x=x,
                            center_y=y, scale=0.5)
                            self.player_sprite_list.append(self.player)


                            self.physics_engine = arcade.PhysicsEnginePlatformer(
                            self.player, 
                            walls=self.wall_list,                                     #On définit les lois physiques qui s'appliquent sur le sprite Player
                            gravity_constant=PLAYER_GRAVITY)

                        case "E":  #Map end
                            exit = arcade.Sprite(":resources:/images/tiles/signExit.png", scale = 0.5, center_x = x, center_y = y)
                            self.exit_list.append(exit)


            for slimes in [monsters for monsters in self.monsters_list if type(monsters) == Slime] :
                slimes.wall_list = self.wall_list
