from __future__ import annotations
import arcade
import time 
import math
import random
import dataclasses
from typing import Final
from monsters import *
import player
import commandes 
import weapons
from create_world import *


SWORD_INDEX = 0
BOW_INDEX = 1

class GameView(arcade.View):
    """Main in-game view."""
    
    #DECLARATION DES ATTRIBUTS
    world : World      # --> create_world.py
    score : int 
    score_UI : arcade.Text
    timetravel_UI : arcade.Text
    Victory : bool
    weapons_list : arcade.SpriteList[weapons.Weapon]
    arrow : weapons.Arrow
    # INITIALISATION DE LA PARTIE
    def __init__(self) -> None:
        super().__init__()
        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        #Initialisation des Attributs
        self.world = World()
        self.camera = arcade.camera.Camera2D()
        self.idle_camera = arcade.camera.Camera2D()
        self.right_pressed = False
        self.left_pressed = False
        self.mouse_left_pressed = False
        self.weapons_list = arcade.SpriteList()
        self.active_weapon = SWORD_INDEX
        self.mouse_x = 0
        self.mouse_y = 0
        self.angle : float = 0
        self.world_x : float = 0
        self.world_y : float = 0


        self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        # Setup our game
        self.setup()
    

    def setup(self) -> None:
        """Set up the game here."""
         
        readmap(self.world, "map1.txt")     #Génération de la map
        self.Victory = False
        self.score = 0  #Reset du score au début du jeu/ à chaque mort
        self.arrow = weapons.Arrow("assets/kenney-voxel-items-png/arrow.png", scale=0.4,center_x=0,center_y=0, angle = 0)
        self.sword = weapons.Sword("assets/kenney-voxel-items-png/sword_silver.png",scale=0.4 * 0.7, center_x=0,center_y=0, angle = 0)
        self.bow = weapons.Weapon("assets/kenney-voxel-items-png/bow.png", scale=0.4, center_x=0,center_y=0, angle = 0)
        self.weapons_list.append(self.sword)
        self.weapons_list.append(self.bow)
  

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
                if self.world.physics_engine.can_jump():
                    self.world.player_sprite.jump()
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
        self.angle = math.atan2(self.world_y - self.world.player_sprite.center_y, self.world_x - self.world.player_sprite.center_x) # Calculer l'angle entre le joueur et la position de la souris dans le monde

    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_left_pressed = True
        if button == arcade.MOUSE_BUTTON_RIGHT:
            if self.active_weapon == SWORD_INDEX:
                self.active_weapon = BOW_INDEX
            else : 
                self.active_weapon = SWORD_INDEX

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT : 
            self.mouse_left_pressed = False
            if self.active_weapon == BOW_INDEX :
                self.arrow.released = True 
                self.world.arrow_sprite_list.append(self.arrow)
                self.world.arrow_sprite_list[-1].change_x = weapons.ARROW_SPEED * math.cos(self.angle)
                self.world.arrow_sprite_list[-1].change_y = weapons.ARROW_SPEED * math.sin(self.angle)
    

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances", or "ticks".
        """
 
        self.world.physics_engine.update()
        #Waiting for a new version mypy
        self.camera.position = self.world.player_sprite.position  #type: ignore
        
        #Mouvement du joueur
        self.world.player_sprite.movement(self)

        #COMPORTEMENT DES MONSTRES
        for monster in self.world.monsters_list:
            monster.movement()         
            

        if self.mouse_left_pressed:
            self.arrow = weapons.Arrow("assets/kenney-voxel-items-png/arrow.png", scale=0.4,  center_x=self.world.player_sprite.center_x + self.bow.position_respecting_to_player + 5, center_y=self.world.player_sprite.center_y - 5, angle=self.bow.angle + 55)
            self.weapons_list[self.active_weapon].adapt_weapon_position(self.angle)
            self.weapons_list[self.active_weapon].manage(self)
            #On adapte l'angle de l'arc (différent de l'épée de par son sprite)
            self.bow.angle -= 70
            if self.active_weapon == BOW_INDEX:
                self.arrow.behavior_before_release(self.bow)

        for arrow in self.world.arrow_sprite_list:
            #Trajectoire de la flèche
            arrow.arrows_movement(self.world.wall_list)
            # Tuer les monstres rencontrés
            arrow.kills_monsters(self)

        self.sword.kills_monsters(self)

        #Vérifie si le joueur est en contact avec des pièces
        collided_coins = arcade.check_for_collision_with_list(
            self.world.player_sprite, 
            self.world.coins_list               
        )
        #Retire les pièces en contact avec le joueur
        for coin in collided_coins:
            #Incrémente le score du nombre de pièces 
            self.score += len(collided_coins)               
            coin.remove_from_sprite_lists()                
            arcade.play_sound(self.coin_sound)


        self.score_UI = arcade.Text( x =  70, y = 650, font_size = 20, text = f"Score : {str(self.score)}"    )                                   
        
        #Check if player should die to monsters or lava
        self.world.player_sprite.dies([self.world.no_go_list, self.world.monsters_list])
        

        #NEXT LEVEL
        if arcade.check_for_collision_with_list(self.world.player_sprite, self.world.exit_list) :
            if not(self.world.last_level):           #Si ce n'est pas le dernier niveau, lit la prochaine
                readmap(self.world, map = self.world.Next_map)
            #VICTORY !
            else:
                self.victory_text = arcade.Text(x = 400, y = 360, font_size = 100, text = "YOU WON" )
                self.Victory = True
                

        #GAME OVER SET
        if self.world.player_sprite.death :
             arcade.play_sound(self.death_sound)
             self.world.player_sprite_list.clear()                             
             time.sleep(0.25)  
             self.setup()
        
    

    #AFFICHAGE DES SPRITES
    def on_draw(self) -> None:                                 
        self.clear()
        with self.camera.activate():
            self.world.draw()
            if self.mouse_left_pressed:
                arcade.draw_sprite(self.weapons_list[self.active_weapon])
                if self.active_weapon == BOW_INDEX:
                    arcade.draw_sprite(self.arrow)
        with self.idle_camera.activate():
             self.score_UI.draw()

             #WEAPON UI - affiche l'arme active en bas a gauche de l'ecran
             if self.active_weapon == BOW_INDEX:
                    arcade.draw_sprite(arcade.Sprite("assets/kenney-voxel-items-png/bow.png", scale=1, center_x=80,center_y=80, angle = -70))
             elif self.active_weapon == SWORD_INDEX:
                    arcade.draw_sprite(arcade.Sprite("assets/kenney-voxel-items-png/sword_silver.png",scale=0.9, center_x=80,center_y=80, angle = 0))
             if self.Victory :                
                 self.victory_text.draw()