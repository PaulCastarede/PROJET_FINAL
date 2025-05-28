from __future__ import annotations
import arcade
import cProfile
import math
import platforming.platforms
import user_interface
import dataclasses
import gameover
from typing import Final
from monsters import *
import weapons
from map_create.create_world import *

import platforming.platforms as platforms

from switches import Switch
from gates import Gate

SWORD_INDEX = 0
BOW_INDEX = 1

class GameView(arcade.View):
    """Main in-game view."""
    
    #DECLARATION DES ATTRIBUTS
    world : World      # --> create_world.py
    weapons_list : arcade.SpriteList[weapons.Weapon]
    arrow : weapons.Arrow
    arrow_sprite_list : arcade.SpriteList[weapons.Arrow]
    UI : user_interface.UI
    profiler: cProfile.Profile
    ambient_music : Final[arcade.Sound] = arcade.load_sound("assets/ambient_music.mp3", streaming=True)
    

    camera_shake : arcade.camera.grips.ScreenShake2D

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
        self.arrow_sprite_list = arcade.SpriteList()
        self.active_weapon = SWORD_INDEX
        self.mouse_x = 0
        self.mouse_y = 0
        self.angle : float = 0
        self.world_x : float = 0
        self.world_y : float = 0
        self.profiler = cProfile.Profile()
        
        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.camera.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0
        )
        # Setup our game
        self.setup()
    

    def setup(self) -> None:
        """Set up the game here."""
        #Reset the eventual previous elements
        self.weapons_list.clear()
        self.arrow_sprite_list.clear()
        self.world.clear(clear_player=True)
        self.active_weapon = SWORD_INDEX
        #MAP SET UP
        self.profiler.enable()
        readmap(self.world, "map1.txt")    
        self.profiler.disable()
        #WEAPONS SET UP
        self.arrow = weapons.Arrow(center_x=0, center_y=0)
        self.sword = weapons.Sword("assets/kenney-voxel-items-png/sword_silver.png",scale=0.5 * 0.7, center_x=0,center_y=0, angle = 0)
        self.bow = weapons.Bow("assets/kenney-voxel-items-png/bow.png", scale=0.4, center_x=0,center_y=0, angle = 0)
        self.weapons_list.append(self.sword)
        self.weapons_list.append(self.bow)
        #UI SET UP
        self.UI = user_interface.UI()
        #MUSIC SET UP
        self.music_playback = arcade.play_sound(self.ambient_music, volume = 0.3, loop = True)

  

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
            case arcade.key.ESCAPE | arcade.key.R :
                # resets the game
                self.setup()


    def on_key_release(self, key: int, modifiers: int) -> None:
        match key:
            case arcade.key.RIGHT:
                self.right_pressed = False
            case arcade.key.LEFT:
                self.left_pressed = False

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        """Met à jour les coordonnées de la souris et l'angle entre le joueur et la souris
        """
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
            # Check for sword collision with switches when using sword
            if self.active_weapon == SWORD_INDEX:
                hit_switches = arcade.check_for_collision_with_list(self.sword, self.world.switches_list)
                for switch in hit_switches:
                    switch.on_hit_by_weapon(self.world.gates_dict)
            self.arrow = weapons.Arrow()
        if button == arcade.MOUSE_BUTTON_RIGHT:
            #Switch the active weapon when mouse right pressed
            if self.active_weapon == SWORD_INDEX:
                self.active_weapon = BOW_INDEX
            else : 
                self.active_weapon = SWORD_INDEX
            self.UI.update_weapon(self)
            

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT : 
            self.mouse_left_pressed = False
            if self.active_weapon == BOW_INDEX :
                self.arrow.released = True 
                self.arrow.charge_level_increases_speed()
                self.arrow_sprite_list.append(self.arrow)
                self.arrow_sprite_list[-1].change_x = self.arrow.speed * math.cos(self.angle)
                self.arrow_sprite_list[-1].change_y = self.arrow.speed * math.sin(self.angle)
    

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances", or "ticks".
        """
        self.camera_shake.update(delta_time)
        self.profiler.enable()
        self.do_on_update(delta_time)
        self.profiler.disable()

        #Waiting for a new version mypy
        self.camera.position = self.world.player_sprite.position  #type: ignore
        
        #Mouvement du joueur
        self.world.player_sprite.movement(self)

        #Mouvement des plateformes autres que "wall"

        for sprite in [sprite 
                       for platform_types in [self.world.moving_platforms_list,self.world.exit_list,self.world.no_go_list, self.world.checkpoint_list, self.world.switches_list] 
                       for sprite in platform_types if isinstance(sprite,platforms.Collidable_Platform)
                    ]:
            sprite.movement()

        #COMPORTEMENT DES MONSTRES
        for monster in self.world.monsters_list:
            monster.movement()         

        if self.mouse_left_pressed:
            self.weapons_list[self.active_weapon].adapt_weapon_position(self.angle)
            self.weapons_list[self.active_weapon].weapon_movement(self)
            #On adapte l'angle de l'arc (différent de l'épée de par son sprite)
            self.bow.angle -= 70
            if self.active_weapon == BOW_INDEX:
                self.arrow.behavior_before_release(self.bow, self.angle)
                       
        for arrow in self.arrow_sprite_list:
            # Trajectoire de la flèche
            arrow.arrows_movement(self.world)
            # Tuer les monstres rencontrés
            arrow.kills_monsters(self.world.monsters_list)
            # Active les interrupteurs
            arrow.check_arrow_hits(self.world)
        

        self.world.player_sprite.collect_coins(self)                                   
        

        #Check if player should die to monsters or lava
        self.world.player_sprite.respawn_or_dies(self)

        for checkpoint in self.world.checkpoint_list:
            checkpoint.set_respawn(self.world.player_sprite)
        
        #NEXT LEVEL
        for exit_signs in self.world.exit_list:
            exit_signs.exit(self)
          

        #GAME OVER SET
        if self.world.player_sprite.death:
            self.window.show_view(gameover.GameOverView(self))

       
    def do_on_update(self, delta_time: float) -> None:
        self.world.physics_engine.update()

        
    
    #AFFICHAGE DES SPRITES
    def on_draw(self) -> None:    
        """Draw all the things that should"""  
        self.camera_shake.update_camera()                           
        self.clear()
        with self.camera.activate():
            self.world.draw()
            self.arrow_sprite_list.draw()
            #Draw weapons
            if self.mouse_left_pressed:
                arcade.draw_sprite(self.weapons_list[self.active_weapon])
                if self.active_weapon == BOW_INDEX:
                    arcade.draw_sprite(self.arrow)
                    if not self.arrow.released:
                        self.arrow.draw_trajectory(self.bow, self)
        with self.idle_camera.activate():
             self.UI.draw()
        self.camera_shake.readjust_camera()
