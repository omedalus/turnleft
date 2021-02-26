# Turn Left
A deceptively difficult AI problem: turn left at the end of a hallway.

## The Problem
An AI player for a roguelike game needs to navigate a hallway. The hallway has a left turn halfway down its length. At the end of the hallway is a reward.

```
############
# R        #
########## #
         # #
         # #
         # #
         #S#
         ###

S = start position
R = reward
```

The AI player has a position and an orientation relative to its environment. The AI doesn't intrinsically know these values.

The AI player can perceive its world through four Boolean sensors, detecting the presence or absence of a wall immediately to its left or right, behind it, or ahead of it. The AI player may also have an additional sensor indicating that it received a reward as a result of its last action.

The AI player can interact with its world through the performing of four discrete actions: ```TURN LEFT```, ```TURN RIGHT```, ```TURN BACK```, or ```GO FORWARD``` (these can have various abbreviations when implemented). These cause it to rotate its orientation 90 degrees left or right, 180 degrees, or to step forward (if a space is available), respectively. Each action is considered atomic and instantaneous, with the AI player's sensorium subsequently updated.

## The Difficulty
All of the above is, of course, ridiculously easy to implement in principle. Indeed, it can be solved with a two-line program:

```
IF !isWallAhead THEN "GoForward"
ELSE "TurnLeft"
```

The question is: How do you get the AI player to write this program?


