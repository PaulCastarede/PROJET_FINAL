from typing import Final
import arcade

class Gate(arcade.Sprite):
    __wall_list : None | arcade.SpriteList[arcade.Sprite]
    def __init__(self, center_x: float, center_y: float, state: bool = False) -> None:
        """Initialize a gate.
        
        Args:
            center_x: X coordinate of the gate
            center_y: Y coordinate of the gate
            state: True if the gate is open (invisible), False if closed (visible)
        """
        super().__init__(":resources:/images/tiles/stoneCenter_rounded.png", scale=0.5, center_x=center_x, center_y=center_y)
        self.state = state
        self.visible = not state
        self.__wall_list = None

    def set_wall_list(self, wall_list: arcade.SpriteList[arcade.Sprite]) -> None:
        """Set the wall list reference for collision handling.
        
        Args:
            wall_list: The SpriteList containing wall sprites
        """
        self.__wall_list = wall_list
        if not self.state and self.__wall_list is not None:
            self.__wall_list.append(self)

    def open(self) -> None:
        """Opens the gate (disappears and becomes passable)."""
        if not self.state:  # Only act if gate is currently closed
            self.state = True
            self.visible = False
            if self.__wall_list is not None and self in self.__wall_list:
                self.__wall_list.remove(self)

    def close(self) -> None:
        """Closes the gate (appears and becomes a wall)."""
        if self.state:  # Only act if gate is currently open
            self.state = False
            self.visible = True
            if self.__wall_list is not None and self not in self.__wall_list:
                self.__wall_list.append(self)

    def update_texture(self) -> None:
        if not self.state:
            self.texture = arcade.load_texture(self._get_texture_path())
            self.visible = True
        else:
            self.visible = False

    def _get_texture_path(self) -> str:
        return ":resources:/images/tiles/stoneCenter_rounded.png"
