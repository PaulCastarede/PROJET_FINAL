A platformer game project.

HOW TO PLAY:
In the terminal, write "uv run main.py" to launch the game.

RULES:
-Make your way through the level to get to the 'EXIT' sign.
-Dodge lava, slimes and bats, or you will die.
-You can kill slimes and bats with your weapons.
-You have two weapons: a sword and a bow. The more you keep the right button pressed with the bow, the further the arrow will go. Forget about spamming.
-If you die, you'll lose a life and get back to the last checkpoint.
-You get a extra life every 10 coins.
-Once you've lost all your lives, you'll get a gameover and have to start it all over again. Play safe!

COMMANDS:
-Use the directionnal arrows to move, up arrow to jump.
-Press the left button to use your weapon.
-Press the right button to switch weapon.
-Press 'Esc'/'Echap' to restart the game.


(BONUS) HOW TO CREATE YOUR OWN MAP:
-Create a new file '(choose_map_name).txt' the project folder.
-Copy/paste the following template:
width: x
height: y
(next-map : (next_map_name).txt)
---
...
...
...
---
-Replace the ... with the elements you want with the convention:
    "=":   Grass block
    "-":   Half grass block
    "x":   Crate
    "*":   Coin
    "o":   Slime enemy
    "v":   Bat enemy
    "£":   Lava
    "S":   Player start position
    "C":   Checkpoint
    "↓", "→", "←", "↑" : direction of platforms
    "|":   Portal
    "^":   Interruptor (activate portals)
    "E":   Map end
-Replace x with the width of your map in numbers of characters (spaces included), y with the height.
-Write after 'next-map' the name of the level you want the sign exit to lead to. Dont write this line if you want this level to be the last level.


HAVE FUN!



PS : I was too lazy to describe how to configure portals, just follow this template lol
width: 24
height: 8
switches:
  - x: 0
    y: 7
    # this switch is off by default (no 'state')
    # it opens the gate at position (6, 1), then disables itself
    # (that means we won't be able to switch it back off, so nothing to do there)
    switch_on:
      - action: open-gate
        x: 6
        y: 1
      - action: disable
  - x: 8
    y: 6
    state: on # this switch is on by default
    # when we turn it off, we open access to the coin,
    # but we close access to the exit
    switch_off:
      - action: open-gate
        x: 14
        y: 2
      - action: close-gate
        x: 18
        y: 5
    # when we turn it back on, we do the opposite
    switch_on:
      - action: close-gate
        x: 14
        y: 2
      - action: open-gate
        x: 18
        y: 5
gates:
  - x: 18
    y: 5
    state: open # this gate is open when the game starts
  # the other gates start closed
---
^     x           x
--    x ^         x
      x-----      |
   ---x           =
      x   -----   =
---   x   x   |  x=
 S    |  xx * x  x=  E
========================
---



Credit :
"HeatleyBros - Royalty Free Video Game Music",  for the ambient music.
All sounds and sprites are under free to use license.
This game is not for commercial purposes.
