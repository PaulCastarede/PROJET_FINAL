from __future__ import annotations
import arcade
import time 
import math
import user_interface
import dataclasses
from typing import Final
from monsters import *
import weapons
from create_world import *

SWORD_INDEX = 0
BOW_INDEX = 1

class GameView(arcade.View):
    """Main in-game view."""
    
    #DECLARATION DES ATTRIBUTS
    world : World      # --> create_world.py
    score_UI : arcade.Text
    Victory : bool
    weapons_list : arcade.SpriteList[weapons.Weapon]
    arrow : weapons.Arrow
    arrow_sprite_list : arcade.SpriteList[weapons.Arrow]
    UI : user_interface.UI

    # INITIALISATION DE GAMEVIEW
    def __init__(self) -> None:
        super().__init__()
        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        #Initialisation des Attributs
        self.UI = user_interface.UI()
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
        self.arrow_sprite_list = arcade.SpriteList()

        # Setup our game
        self.setup()
    

    def setup(self) -> None:
        """Set up the game here."""
        #Reset the eventual previous elements
        self.weapons_list.clear()
        self.arrow_sprite_list.clear()
        self.Victory = False
        self.active_weapon = SWORD_INDEX
        #MAP SET UP
        readmap(self.world, "map1.txt")    
        #WEAPONS SET UP
        self.arrow = weapons.Arrow(center_x=0, center_y=0)
        self.sword = weapons.Sword("assets/kenney-voxel-items-png/sword_silver.png",scale=0.5 * 0.7, center_x=0,center_y=0, angle = 0)
        self.bow = weapons.Bow("assets/kenney-voxel-items-png/bow.png", scale=0.4, center_x=0,center_y=0, angle = 0)
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
            self.sword.kills_monsters(self.world.monsters_list)
            self.arrow = weapons.Arrow( center_x=self.world.player_sprite.center_x + self.bow.position_respecting_to_player + 5, center_y=self.world.player_sprite.center_y - 5, angle=self.bow.angle + 55)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            #Switch the active weapon when mouse right pressed
            if self.active_weapon == SWORD_INDEX:
                self.active_weapon = BOW_INDEX
            else : 
                self.active_weapon = SWORD_INDEX

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT : 
            self.mouse_left_pressed = False
            if self.active_weapon == BOW_INDEX :
                self.arrow.released = True 
                self.arrow.charge_level_increases_speed()
                self.arrow_sprite_list.append(self.arrow)
                self.arrow_sprite_list[-1].change_x = self.arrow.ARROW_SPEED * math.cos(self.angle)
                self.arrow_sprite_list[-1].change_y = self.arrow.ARROW_SPEED * math.sin(self.angle)
    

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
            self.weapons_list[self.active_weapon].adapt_weapon_position(self.angle)
            self.weapons_list[self.active_weapon].weapon_movement(self)
            #On adapte l'angle de l'arc (différent de l'épée de par son sprite)
            self.bow.angle -= 70
            if self.active_weapon == BOW_INDEX:
                self.arrow.behavior_before_release(self.bow)
                
                
        
        

            

        for arrow in self.arrow_sprite_list:
            #Trajectoire de la flèche
            arrow.arrows_movement(self.world.wall_list)
            # Tuer les monstres rencontrés
            arrow.kills_monsters(self.world.monsters_list)
        


        self.world.player_sprite.collect_coins(self.world.coins_list)                                   
        
        #Check if player should die to monsters or lava
        self.world.player_sprite.dies(self.world.no_go_list, self.world.monsters_list)
        
        #NEXT LEVEL
        if arcade.check_for_collision_with_list(self.world.player_sprite, self.world.exit_list) :
            if not(self.world.last_level):    
                #Si ce n'est pas le dernier niveau, lit la prochaine map       
                readmap(self.world, map = self.world.Next_map)
            else:
                self.Victory = True

        self.UI.update(self)  

        #GAME OVER SET
        if self.world.player_sprite.death :
             self.world.player_sprite_list.clear()                             
             time.sleep(0.25)  
             self.setup()
        
    
    #AFFICHAGE DES SPRITES
    def on_draw(self) -> None:                                 
        self.clear()
        with self.camera.activate():
            self.world.draw()
            self.arrow_sprite_list.draw()
            if self.mouse_left_pressed:
                arcade.draw_sprite(self.weapons_list[self.active_weapon])
                if self.active_weapon == BOW_INDEX:
                    arcade.draw_sprite(self.arrow)
        with self.idle_camera.activate():
             self.UI.draw()
