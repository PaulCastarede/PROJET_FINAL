import pytest
import arcade
from gameview import GameView
import player
import weapons
import monsters
import math
from monsters import *

def test_bat_distance() -> None:
    """Test de la distance de la chauve-souris par rapport à son point de spawn."""
    bat = Bat("assets/kenney-extended-enemies-png/bat.png", center_x=100, center_y=100, scale=0.5)
    bat.center_x = 200
    bat.center_y = 100
    assert bat.distance_from_spawn() == 100  # Distance entre (100,100) et (200,100)

def test_bat_movement() -> None:
    """Test du mouvement de la chauve-souris."""
    bat = Bat("assets/kenney-extended-enemies-png/bat.png", center_x=100, center_y=100, scale=0.5)
    bat.__theta = math.pi / 4  # 45 degrés
    bat.change_x = 2 * math.cos(bat.__theta)
    bat.change_y = 2 * math.sin(bat.__theta)
    bat.center_x += bat.change_x
    bat.center_y += bat.change_y
    assert bat.center_x > 100
    assert bat.center_y > 100

def test_game_setup() -> None:
    """Test l'initialisation du jeu."""
    game = GameView()
    assert game.world.player_sprite.score == 0
    assert game.UI.victory is False
    assert game.world.player_sprite.death is False
    assert len(game.world.wall_list) == 0  # Doit être vide avant chargement d'une carte

def test_player_movement() -> None:
    """Test du déplacement du joueur."""
    game = GameView()
    game.world.player_sprite = player.Player(center_x=100, center_y=100)
    game.right_pressed = True
    game.on_update(1 / 60)
    assert game.world.player_sprite.center_x > 100  # Il doit avancer vers la droite
