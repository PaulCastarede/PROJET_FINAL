from __future__ import annotations
import arcade
import create_world
from weapons import Arrow, Sword
import platforming.platforms as platforms
import world_sprites_types
import world_sprites_types.gates
import world_sprites_types.switches

class TestSwitchesGates:
    window: arcade.Window
    world: create_world.World
    
    def setup_method(self) -> None:
        """Configuration initiale pour chaque test"""
        self.window = arcade.Window(1280, 720, "Test Window")
        self.world = create_world.World()
        self.world.switches_list = arcade.SpriteList()

    def test_switch_initial_state(self) -> None:
        """Test l'état initial des switches et gates lors du chargement"""
        switch = world_sprites_types.switches.Switch(
            center_x=100,
            center_y=100,
            state=True
        )
        gate = world_sprites_types.gates.Gate(
            center_x=200,
            center_y=200,
            state=False
        )
        
        switch.actions_on = [{"action": "open-gate", "x": 200, "y": 200}]
        self.world.switches_list.append(switch)
        self.world.gates_dict[(200, 200)] = gate
        
        for sw in self.world.switches_list:
            if sw.state:
                for action in sw.actions_on:
                    if action["action"] == "open-gate" and (action["x"], action["y"]) in self.world.gates_dict:
                        self.world.gates_dict[(action["x"], action["y"])].open()
        assert gate.state == True

    def test_switch_weapon_hit(self) -> None:
        """Test l'interaction entre les armes et les switches"""
        switch = world_sprites_types.switches.Switch(
            center_x=100,
            center_y=100,
            state=False,
            enabled=True
        )
        gate = world_sprites_types.gates.Gate(
            center_x=200,
            center_y=200,
            state=False
        )
        
        switch.actions_on = [{"action": "open-gate", "x": 200, "y": 200}]
        switch.actions_off = [{"action": "close-gate", "x": 200, "y": 200}]
        
        self.world.switches_list.append(switch)
        self.world.gates_dict[(200, 200)] = gate
        
        arrow = Arrow(
            path_or_texture="assets/kenney-voxel-items-png/arrow.png",
            center_x=100,
            center_y=100
        )
        
        hit_switches = arcade.check_for_collision_with_list(arrow, self.world.switches_list)
        for sw in hit_switches:
            sw.on_hit_by_weapon(self.world.gates_dict)

        assert switch.state == True

    def test_switch_disable_action(self) -> None:
        """Test l'action de désactivation d'un switch"""
        switch = world_sprites_types.switches.Switch(
            center_x=100,
            center_y=100,
            enabled=True
        )
        gate = world_sprites_types.gates.Gate(
            center_x=200,
            center_y=200
        )
        
        switch.actions_on = [
            {"action": "open-gate", "x": 200, "y": 200},
            {"action": "disable"}
        ]
        
        self.world.gates_dict[(200, 200)] = gate

        switch.toggle(self.world.gates_dict)
        assert not switch.enabled
        assert gate.state
        
        initial_gate_state = gate.state
        switch.toggle(self.world.gates_dict)
        assert gate.state == initial_gate_state

    def test_gate_wall_management(self) -> None:
        """Test la gestion de la wall_list par les gates"""
        gate = world_sprites_types.gates.Gate(center_x=100, center_y=100)
        wall_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        
        gate.set_wall_list(wall_list)
        assert gate in wall_list
        
        gate.open()
        assert gate not in wall_list
        assert not gate.visible
        
        gate.close()
        assert gate in wall_list
        assert gate.visible

