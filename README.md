# Turn Left
A deceptively difficult AI problem: navigate an L-shaped maze.

## The Problem
An AI player for a roguelike game needs to navigate a hallway. The hallway is an L-shaped maze --
it has a left turn halfway down its length. At the end of the hallway is a reward.

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
All of the above is, of course, ridiculously easy to implement in principle. Indeed, it can be solved with a two-line subroutine. This assumes that the subroutine is called once per timestep or "turn", each instruction has an optional precondition, and the output of the subroutine is whatever the value of the output register is when the subroutine exits:

```
IF true THEN OUTPUT="GoForward"
IF isWallAhead THEN OUTPUT="TurnLeft"
```

The question is: How do you get the AI player to write this program?

### Not Brownian motion

Sure, the AI player can simply perform a random move once per turn. This will eventually make it reach its goal, albeit with a number of attempts that is exponential in the length of the hallway. An exponential traversal of the hallway might be fine initially, but the problem with just using a random move generator is that, obviously, *it doesn't get better*. A second run down the same hallway will *still* take exponential time; as will the run after that, and the run after that, and so on. The "AI", if it can even be called that, stays naive forever.

### Not Genetic Programming

Given that the desired program is only two instructions, the problem lacks reducibility. Indeed, if one explores the entirety of all possible programs within a constrained program space, one can easily compute the odds of stumbling across that one particular solution. Specifically, we can constrain the program space thusly:
 * The program must consist of two instructions.
 * Each instruction specifies one possible value for the output register.
 * The first instruction must have no precondition. It sets the default behavior in the event that the second instruction's precondition is not met.
 * The second instruction must have exactly one precondition. This precondition specifies a sensor and a value.

This is already a very highly constrained search space. We can explicitly count how many elements it contains.
```
Number of output register values: 4
Number of sensors: 4
Number of values per sensor: 2

Number of possible first instructions =
  # output values =
  4

Number of possible second instructions =
  # output values * # sensors * # values per sensor =
  4 * 4 * 2 =
  32

Number of possible combinations of the two instructions =
  4 * 32 =
  128
```
