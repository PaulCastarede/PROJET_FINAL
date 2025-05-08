from __future__ import annotations 
import arcade 
import Map_Create.world_sprites
import monsters
import platforming.block_detecting
import player
import coins
import platforming.platforms as platforms
import platforming

TILE_SIZE = 64.0
"""64 pixels par element"""


class World:
    
    """Une classe qui contient toutes les SpriteLists inhérentes au monde chargé (les monstres, les murs, la lave, les pièces et même le joueur !)

    Args
    """
    player_sprite : player.Player
    player_sprite_list : arcade.SpriteList[player.Player]
    player_set_spawn : bool
    set_exit : bool
    wall_list : arcade.SpriteList[arcade.Sprite]
    moving_platforms_list : arcade.SpriteList[platforms.Platform]
    no_go_list : arcade.SpriteList[Map_Create.world_sprites.Lava_Sprite]
    monsters_list : arcade.SpriteList[monsters.Monster]
    coins_list : arcade.SpriteList[coins.Coin]
    physics_engine : arcade.PhysicsEnginePlatformer
    exit_list : arcade.SpriteList[Map_Create.world_sprites.Exit_Sprite]
    next_map : str
    last_level : bool
    map_width : int
    map_height : int 
    
    def __init__(self)-> None:
        self.player_sprite_list = arcade.SpriteList()
        self.player_set_spawn = False
        self.set_exit = False
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.moving_platforms_list = arcade.SpriteList()
        self.no_go_list = arcade.SpriteList(use_spatial_hash=True)
        self.monsters_list = arcade.SpriteList()
        self.coins_list = arcade.SpriteList(use_spatial_hash=True)
        self.exit_list = arcade.SpriteList(use_spatial_hash=True)
        self.map_width = 0  
        self.map_height = 0

    def draw(self)-> None:
        self.player_sprite_list.draw()
        self.wall_list.draw()
        self.moving_platforms_list.draw()
        self.no_go_list.draw()
        self.monsters_list.draw()
        self.coins_list.draw()
        self.exit_list.draw()


def readmap(world : World, map : str) -> None:


    # Ouvrir le fichier sous l'acronyme 'file'
        with open(f"maps/{map}", "r", encoding="utf-8") as file:

            world.last_level = True

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
                                world.map_width = int(value) # On définit la largeur de la carte

                            if key == "height":
                                world.map_height = int(value)  # On définit la longueur de la carte

                            if key == "next-map":
                                world.last_level = False
                                world.next_map = value        # On définit le niveau suivant 

                        except ValueError as e: 
                            raise ValueError(f"Valeur invalide pour la clé {key}: {value}") from e

            # Vérifier que les dimensions sont des entiers strictement positifs
            if world.map_width <= 0 or world.map_height <= 0:
                raise ValueError("Les dimensions dans la configuration sont invalides")

            # Effacer les sprites précédents
            world.wall_list.clear()
            world.moving_platforms_list.clear()
            world.coins_list.clear()
            world.monsters_list.clear()
            world.no_go_list.clear()
            world.player_sprite_list.clear()
            world.exit_list.clear()
            world.player_set_spawn = False

            # Lire les caractères de la carte après le ("---")
            map_lines = []

            for _ in range(world.map_height):
                line = file.readline().rstrip('\n')  # Lire sans sauter une ligne

                if len(line) > world.map_width:                
                    raise ValueError(f"La ligne dépasse la longueur de la config {world.map_width}")

                map_lines.append(list(line))

            # Vérifier que le fichier se termine par "---"
            end_line = file.readline().strip() # Ligne +1 après dernière ligne de la boucle 
            if end_line != "---":
                raise ValueError("Le fichier ne se termine pas par :  '---' ")
            
            for index_y, line in enumerate(map_lines): 
                for index_x, character in enumerate(line):
                    if character == "←" or character == "→" or character == "↑" or character == "↓":
                        platforming.block_detecting.detect_block((index_x,index_y), map_lines, trajectory = platforms.Trajectory(), world=world)
            
            for platform in [platform 
                             for platform_types in [world.moving_platforms_list,world.exit_list,world.no_go_list] 
                             for platform in  platform_types if isinstance(platform, platforms.Platform)]:
                platform.define_boundaries()



            for index_y, line in enumerate(map_lines): 
                for index_x, character in enumerate(line):
                    row_number = len(map_lines)-index_y   # (Car renversé)
                    column_number = index_x
                    x : float = TILE_SIZE * column_number  # Real coord in game
                    y : float = TILE_SIZE * row_number 

                    match character:
                        case "=":  # Grass block
                            grass = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5, center_x=x, center_y=y)
                            world.wall_list.append(grass)
                        case "-":  # Half grass block
                            half_grass = arcade.Sprite(":resources:images/tiles/grassHalf_mid.png", scale=0.5, center_x=x, center_y=y)
                            world.wall_list.append(half_grass)
                        case "x":  # Crate
                            crate = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=0.5, center_x=x, center_y=y)
                            world.wall_list.append(crate)
                        case "*":  # Coin
                            coin = coins.Coin(center_x=x, center_y=y)
                            world.coins_list.append(coin)
                        case "o":  # Slime enemy
                            slime = monsters.Slime(scale=0.5, center_x=x, center_y=y, wall_list = world.wall_list)
                            world.monsters_list.append(slime)
                        case "v":  # Bat enemy  
                            bat = monsters.Bat(center_x=x, center_y=y)
                            world.monsters_list.append(bat)
                        case "£":  # Lava
                            lava = arcade.Sprite(":resources:images/tiles/lava.png", scale=0.5, center_x=x, center_y=y)
                            world.no_go_list.append(lava)
                        case "S":  # Player start position
                            if not(world.player_set_spawn):
                                world.player_sprite =  player.Player(center_x=x, center_y=y,)
                                world.player_sprite_list.append(world.player_sprite)
                                world.player_set_spawn = True
                                #On définit le moteur physique à partir des sprites
                                world.physics_engine = arcade.PhysicsEnginePlatformer(
                                world.player_sprite, 
                                walls=world.wall_list, 
                                platforms = world.moving_platforms_list,
                                gravity_constant=player.PLAYER_GRAVITY)
                            else:
                                raise RuntimeError("Le joueur ne peut avoir qu'un seul spawn")

                        case "E":  #Map end
                            exit = Map_Create.world_sprites.Exit_Sprite(":resources:/images/tiles/signExit.png", scale = 0.5, center_x = x, center_y = y)
                            world.exit_list.append(exit)
                            world.set_exit = True

            if not(world.player_set_spawn):
                raise RuntimeError("Un endroit où le joueur 'spawn' doit être spécifié")
            if not(world.set_exit):
                raise RuntimeError("La fin du niveau doit être spécifiée")




