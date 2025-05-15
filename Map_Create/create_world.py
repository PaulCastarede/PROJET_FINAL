from __future__ import annotations 
import arcade 
import yaml
import Map_Create.world_sprites
import monsters
import platforming.block_detecting
import player
import coins
import platforming.platforms as platforms
import platforming
import switches
import gates

TILE_SIZE = 64.0
"""64 pixels par element"""


class World:
    player_sprite : player.Player
    player_sprite_list : arcade.SpriteList[player.Player]
    player_set_spawn : bool
    set_exit : bool
    wall_list : arcade.SpriteList[arcade.Sprite]
    moving_platforms_list : arcade.SpriteList[platforms.Platform]
    no_go_list : arcade.SpriteList[Map_Create.world_sprites.Lava_Sprite]
    monsters_list : arcade.SpriteList[monsters.Monster]
    switches_list : arcade.SpriteList[switches.Switch]
    gates_list : arcade.SpriteList[gates.Gate]
    coins_list : arcade.SpriteList[coins.Coin]
    physics_engine : arcade.PhysicsEnginePlatformer
    exit_list : arcade.SpriteList[Map_Create.world_sprites.Exit_Sprite]
    checkpoint_list : arcade.SpriteList[Map_Create.world_sprites.Checkpoint]
    next_map : str
    last_level : bool
    map_width : int
    map_height : int 
    gates_dict: dict[tuple[int, int], gates.Gate]
    
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
        self.gates_list = arcade.SpriteList(use_spatial_hash=True)
        self.switches_list = arcade.SpriteList(use_spatial_hash=True)
        self.checkpoint_list = arcade.SpriteList(use_spatial_hash=True)
        self.map_width = 0  
        self.map_height = 0
        self.gates_dict = {}

    def draw(self)-> None:
        self.player_sprite_list.draw()
        self.wall_list.draw()
        self.moving_platforms_list.draw()
        self.no_go_list.draw()
        self.monsters_list.draw()
        self.coins_list.draw()
        self.exit_list.draw()
        self.switches_list.draw()
        self.gates_list.draw()
        self.checkpoint_list.draw()

    def clear(self, clear_player : bool = False) -> None:
        # Réinitialisation du monde
        self.wall_list.clear()
        self.moving_platforms_list.clear()
        self.coins_list.clear()
        self.monsters_list.clear()
        self.no_go_list.clear()
        self.checkpoint_list.clear()
        self.exit_list.clear()
        self.switches_list.clear()
        self.gates_list.clear()
        self.player_set_spawn = False
        self.set_exit = False
        if clear_player :
            self.player_sprite_list.clear()



def readmap(world: World, map: str) -> None:
    """Charge une carte depuis un fichier et initialise le monde.
    
    Args:
        world: Instance de World à initialiser
        map: Nom du fichier de carte à charger
    """
    def load_config(file) -> dict:
        """Charge la configuration YAML depuis le fichier."""
        config_lines = []
        for line in file:
            if line.strip() == "---":
                break
            config_lines.append(line)
        return yaml.safe_load("".join(config_lines))

    def validate_map_dimensions(map_lines: list[list[str]], width: int, height: int) -> None:
        """Valide que les dimensions de la carte correspondent à la configuration."""
        if len(map_lines) != height:
            raise ValueError(f"La hauteur de la carte ({len(map_lines)}) ne correspond pas à la configuration ({height})")
        for i, line in enumerate(map_lines):
            if len(line) > width:
                raise ValueError(f"Ligne {i+1} dépasse la largeur configurée ({width})")

    def process_gates(config: dict, world: World) -> None:
        """Process gates defined in the configuration.
        
        Args:
            config: The YAML configuration dictionary
            world: The World instance to add gates to
        """
        world.gates_dict = {}
        for gate_data in config.get("gates", []):
            gx, gy = gate_data["x"], gate_data["y"]
            gate = gates.Gate(
                center_x=gx * TILE_SIZE,
                center_y=gy * TILE_SIZE,
                state=gate_data.get("state") == "open")
            
            # Set the wall list reference for collision handling
            gate.set_wall_list(world.wall_list)
            
            world.gates_list.append(gate)
            world.gates_dict[(gx, gy)] = gate

    def process_switches(config: dict, world: World) -> None:
        """Traite les interrupteurs définis dans la configuration."""
        for sw_data in config.get("switches", []):
            sx, sy = sw_data["x"], sw_data["y"]
            
            switch = switches.Switch(
                center_x=sx * TILE_SIZE,
                center_y=sy * TILE_SIZE,
                state=sw_data.get("state", "off") == "on"
            )
            switch.set_actions(
                sw_data.get("switch_on", []),
                sw_data.get("switch_off", [])
            )
            world.switches_list.append(switch)

    def process_map_lines(map_lines: list[list[str]], world: World) -> None:
        """Traite les lignes de la carte pour détecter les plateformes mobiles."""
        for index_y, line in enumerate(map_lines): 
            for index_x, character in enumerate(line):
                if character in ("←", "→", "↑", "↓"):
                    platforming.block_detecting.detect_block(
                        (index_x, index_y),
                        map_lines,
                        trajectory=platforms.Trajectory(),
                        world=world
                    )

    def create_sprite(character: str, x: float, y: float, world: World) -> None:
        match character:
            case "=":
                world.wall_list.append(arcade.Sprite(
                    ":resources:images/tiles/grassMid.png",
                    scale=0.5,
                    center_x=x,
                    center_y=y
                ))
            case "-":
                world.wall_list.append(arcade.Sprite(
                    ":resources:images/tiles/grassHalf_mid.png",
                    scale=0.5,
                    center_x=x,
                    center_y=y
                ))
            case "x":
                world.wall_list.append(arcade.Sprite(
                    ":resources:images/tiles/boxCrate_double.png",
                    scale=0.5,
                    center_x=x,
                    center_y=y
                ))
            case "*":
                world.coins_list.append(coins.Coin(center_x=x, center_y=y))
            case "o":
                world.monsters_list.append(monsters.Slime(
                    scale=0.5,
                    center_x=x,
                    center_y=y,
                    wall_list=world.wall_list
                ))
            case "v":
                world.monsters_list.append(monsters.Bat(center_x=x, center_y=y))
            case "£":
                world.no_go_list.append(arcade.Sprite(
                    ":resources:images/tiles/lava.png",
                    scale=0.5,
                    center_x=x,
                    center_y=y
                ))
            case "S":
                if world.player_set_spawn:
                    raise RuntimeError("Le joueur ne peut avoir qu'un seul spawn")
                if not(world.player_sprite_list):
                    world.player_sprite = player.Player(center_x=x, center_y=y, respawn_map = map)
                    world.player_sprite_list.append(world.player_sprite)
                else :
                    world.player_sprite_list[0].center_x = x
                    world.player_sprite_list[0].center_y = y

                world.physics_engine = arcade.PhysicsEnginePlatformer(
                        world.player_sprite,
                        walls=world.wall_list,
                        platforms=world.moving_platforms_list,
                        gravity_constant=player.PLAYER_GRAVITY
                    )
                world.player_set_spawn = True
            case "E":
                world.exit_list.append(Map_Create.world_sprites.Exit_Sprite(
                    ":resources:/images/tiles/signExit.png",
                    scale=0.5,
                    center_x=x,
                    center_y=y
                ))
                world.set_exit = True
            case "^":
                # Ne rien faire ici - les interrupteurs sont gérés par la configuration YAML
                pass
            case "|":
                # Gates in the map are always closed by default
                gate = gates.Gate(center_x=x, center_y=y, state=False)
                gate.set_wall_list(world.wall_list)
                world.gates_list.append(gate)
                # Store in gates_dict for switch actions
                map_x = int(x / TILE_SIZE)
                map_y = int(y / TILE_SIZE)
                world.gates_dict[(map_x, map_y)] = gate
            case "C":
                world.checkpoint_list.append(Map_Create.world_sprites.Checkpoint(center_x=x,center_y=y-0.5, linked_map = map))

    # Chargement du fichier
    with open(f"maps/{map}", "r", encoding="utf-8") as file:
        # Chargement de la configuration
        config = load_config(file)
        
        try:
            world.map_width = int(config["width"])
            world.map_height = int(config["height"])
            world.next_map = config.get("next-map", "")
            world.last_level = "next-map" not in config
        except (KeyError, ValueError) as e:
            raise ValueError(f"Erreur dans la configuration YAML : {e}")

        world.clear()

        # Traitement des éléments configurés
        process_gates(config, world)
        process_switches(config, world)

        # Lecture de la carte
        map_lines = [list(file.readline().rstrip('\n')) for _ in range(world.map_height)]
        validate_map_dimensions(map_lines, world.map_width, world.map_height)

        # Vérification de la fin de fichier
        if file.readline().strip() != "---":
            raise ValueError("Le fichier ne se termine pas par : '---'")

        # Traitement des plateformes mobiles
        process_map_lines(map_lines, world)

        # Définition des limites des plateformes
        for platform in [p for lst in [world.moving_platforms_list, world.exit_list, world.no_go_list]
                        for p in lst if isinstance(p, platforms.Platform)]:
            platform.define_boundaries()

        # Création des sprites
        for index_y, line in enumerate(map_lines):
            for index_x, character in enumerate(line):
                row_number = len(map_lines) - 1 - index_y
                x = TILE_SIZE * index_x
                y = TILE_SIZE * row_number
                create_sprite(character, x, y, world)

        # Validation finale
        if not world.player_set_spawn:
            raise RuntimeError("Un endroit où le joueur 'spawn' doit être spécifié")
        if not world.set_exit:
            raise RuntimeError("La fin du niveau doit être spécifiée")
        
    for switch in world.switches_list:
        if switch.state:  # Si l'interrupteur est activé
            for action in switch.actions_on:
                if action["action"] == "open-gate" and (action["x"], action["y"]) in world.gates_dict:
                    world.gates_dict[(action["x"], action["y"])].open()
                if action["action"] == "close-gate" and (action["x"], action["y"]) in world.gates_dict:
                    world.gates_dict[(action["x"], action["y"])].close()
        else:  # Si l'interrupteur est désactivé
            for action in switch.actions_off:
                if action["action"] == "open-gate" and (action["x"], action["y"]) in world.gates_dict:
                    world.gates_dict[(action["x"], action["y"])].open()
                elif action["action"] == "close-gate" and (action["x"], action["y"]) in world.gates_dict:
                    world.gates_dict[(action["x"], action["y"])].close()
        