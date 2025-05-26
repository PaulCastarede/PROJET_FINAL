A platformer game project.

HOW TO PLAY:
In the terminal, write "uv run main.py" to launch the game.

RULES:
-Make your way through the level to get to the 'EXIT' sign.
-Dodge lava, slimes and bats, or you will die.
-You can kill slimes and bats with your weapon.
-Killing monsters and getting coins will increase your score. Try go get the highest!
-If you die, you restart from the beginning. Play safe!

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
    "E":   Map end
-Replace x with the width of your map in numbers of characters (spaces included), y with the height.
-Write after 'next-map' the name of the level you want the sign exit to lead to. Dont write this line if you want this level to be the last level.


HAVE FUN!

Credit :
"HeatleyBros - Royalty Free Video Game Music",  for the ambient music
