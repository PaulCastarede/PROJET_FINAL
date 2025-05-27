from typing import Final, Tuple, Dict, List, Any
import arcade
import gameview
from gates import Gate
import platforming.platforms as platforms
        
class Switch(platforms.Collidable_Platform):
    """A switch that can be toggled by weapons to control gates.
    
    The switch has two states (on/off) and can be enabled/disabled.
    When hit by a weapon, it toggles its state and performs configured actions.
    """
    state: bool
    enabled: bool
    actions_on: List[Dict[str, Any]]
    actions_off: List[Dict[str, Any]]
    
    def __init__(self, center_x: int, center_y: int, state: bool = False, enabled: bool = True, path_or_texture: str = ":resources:/images/tiles/leverLeft.png", platform_trajectory: platforms.Trajectory = platforms.Trajectory(), scale: float = 0.5, angle: float = 0) -> None:
        """Initialize a switch.
        
        Args:
            center_x: X coordinate of the switch
            center_y: Y coordinate of the switch
            state: Initial state of the switch (True = on, False = off)
            enabled: Whether the switch can be toggled (True by default)
        """
        super().__init__(path_or_texture, scale, center_x, center_y, angle, platform_trajectory)
        self.state = state
        self.enabled = enabled
        self.actions_on = []  # Actions to perform when switch is turned on
        self.actions_off = [] # Actions to perform when switch is turned off
        self.update_texture()

    def __get_texture_path(self) -> str:
        """Get the appropriate texture path based on switch state."""
        return ":resources:/images/tiles/leverRight.png" if self.state else ":resources:/images/tiles/leverLeft.png"

    def toggle(self, gates_dict: Dict[Tuple[int, int], Gate]) -> None:
        """Toggle the switch state and perform associated actions.
        
        Args:
            gates_dict: Dictionary mapping (x,y) coordinates to Gate objects
        """
        if not self.enabled:
            print("Switch is disabled")
            return

        self.state = not self.state
        print(f"Switch toggled to state: {self.state}")
        self.update_texture()

        actions = self.actions_on if self.state else self.actions_off
        print(f"Actions to perform: {actions}")
        for action in actions:
            action_type = action["action"]
            
            if action_type == "disable":
                print("Disabling switch")
                self.enabled = False
            else:
                # Only get coordinates for gate-related actions
                x, y = int(action["x"]), int(action["y"])  # Ensure coordinates are integers
                # Ajustement des coordonnées y pour corriger le décalage
                print(f"Looking for gate at ({x}, {y})")
                print(f"Available gates: {list(gates_dict.keys())}")
                if (x, y) in gates_dict:
                    print(f"Found gate at ({x}, {y})")
                    if action_type == "open-gate":
                        gates_dict[(x, y)].open()
                    elif action_type == "close-gate":
                        gates_dict[(x, y)].close()
                else:
                    print(f"No gate found at ({x}, {y})")

    def update_texture(self) -> None:
        """Update the switch texture based on its current state."""
        self.texture = arcade.load_texture(self.__get_texture_path())

    def on_hit_by_weapon(self, gates_dict: Dict[Tuple[int, int], Gate]) -> None:
        """Handle being hit by a weapon.
        
        Args:
            gates_dict: Dictionary mapping (x,y) coordinates to Gate objects
        """
        if self.enabled:
            self.toggle(gates_dict)

    def set_actions(self, actions_on: List[Dict[str, Any]], actions_off: List[Dict[str, Any]]) -> None:
        """Set the actions to perform when the switch is toggled.
        
        Args:
            actions_on: List of actions to perform when switch is turned on
            actions_off: List of actions to perform when switch is turned off
        """
        self.actions_on = actions_on
        self.actions_off = actions_off