# Turn Left
A deceptively difficult AI problem: navigate an L-shaped maze.

## The Problem
An AI player for a roguelike game needs to navigate a hallway. The hallway is an L-shaped maze --
it has a left turn halfway down its length. At the end of the hallway is a reward.

```
############
R          #
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

If the bot attempts an impossible action, it will fail silently as a NOOP.

When the bot reaches the reward, the environment is immediately reset, with the bot back at the starting location in its original orientation. At no time can the bot have a position "beyond" the reward position.

## The Difficulty
All of the above is, of course, ridiculously easy to implement in principle. Indeed, it can be solved with a two-line subroutine. This assumes that the subroutine is called once per timestep or "turn", each instruction has an optional precondition, and the output of the subroutine is whatever the value of the output register is when the subroutine exits:

```
IF true THEN OUTPUT="GoForward"
IF isWallAhead THEN OUTPUT="TurnLeft"
```

The question is: How do you get the AI player to write this program?

### Let's Try Brownian motion

Sure, the AI player can simply perform a random move once per turn. This will eventually make it reach its goal, albeit with a number of attempts that is exponential in the length of the hallway. An exponential traversal of the hallway might be fine initially, but the problem with just using a random move generator is that, obviously, *it doesn't get better*. A second run down the same hallway will *still* take exponential time; as will the run after that, and the run after that, and so on. The "AI", if it can even be called that, stays naive forever.

### Let's Try Genetic Programming (and perhaps NEAT)

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

Now, there are two programs within this search space that will reach the reward. We already showed one above. Here's the other:
```
IF true THEN OUTPUT="TurnLeft"
IF !isWallAhead THEN OUTPUT="GoForward"
```

As such, at *minimum*, one out of every (128/2)=64 random constructions of the program, within the aforementioned constraints, will produce a successful result. This has been confirmed through experimentation via automated exhaustive iteration through this program space.

Obviously, the challenge isn't searching such a tiny search space -- heck, it can be searched by hand! The challenge, rather, is that this approach doesn't lend itself to iterative improvement upon partial successes. The AI has no opportunity to explore or experiment within its environment; it either finds a successful soup-to-nuts solution from the outset, or it doesn't. What we *want* is for an agent to be able to explore the environment freely, take notes about how its environment is affected by its actions, and eventually recognize that there's a sequence of operations it can perform that will enable it to intentionally seek rewards through deliberate action.

Let's be clear: the ultimate goal of this project isn't to develop a Turn Left Machine. It's to devise a framework that will enable us to present arbitrary simple tasks to a general AI, and have it iteratively learn how to perform those tasks. As such, an inability to explore its environment or exhibit real-time learning isn't particularly interesting.

It *is* worth noting that this genetic programming approach *may* be instructive in coaxing the evolution of insect-like behaviors. These evolved programs are theoretically capable of handling branching situations, even if this particular L-maze doesn't have one. We can devise a system where the AI agent can store a working-memory state in a memo register, or possibly even hard-code auxiliary sensory neurons that describe a primary neuron's rate of change over some recent time period -- short-term integrators, as it were. These approaches would dramatically increase the range of activities that a stateless subroutine would be able to describe -- because, in effect, they would outsource the state-keeping. However, as I said, the problem with these approaches is that they afford no opportunity for an individual organism to *learn*; they only permit the recording of working memory. Learning, instead, would have to happen over thousands or millions of generations. Indeed, this is exactly consistent with insect evolution. It's also consistent with NEAT architectures, and it's not clear what advantages, if any, that genetic programming offers over NEAT approaches in this scenario.

### Let's Try Q-Learning (or TD-Learning)

Watch this video: https://www.youtube.com/watch?v=aCEvtRtNO-M

Q-learning has strong potential for potentially performing extremely well in this toy problem. Unfortunately, Q-learning works best when the full state of the agent is knowable and quantifiable. In this toy problem, we do of course objectively know the full state of the agent, but we want to make the agent figure it out for itself!

The problem is this: From the point of view of an agent executing a correct path, *the hallway **before** the left turn looks exactly like the hallway **after** the left turn!*. From the agent's POV, it still looks like the same state. A naive agent has no way to know that turning left and then going forward doesn't just end it up in exactly the same state that it had come from!

Now, from a strictly behaviorist standpoint, one might ask: What does it matter? Just always go forward when you can, otherwise turn left. Whether you're going forward on the upper leg or the lower one of the L-maze, who cares? Going forward is the action that ultimately results in some probability of reward. Just go forward. And how do we know to turn left? Because when we get to the intersection and there's a wall ahead of us and we *can't* go forward, the action ```TURN LEFT``` is what restores us to a state in which we can go forward again.

Well that's great, but there's a huge problem: *the action ```TURN AROUND``` **also** restores us to a state in which we can go "forward" again.* Unfortunately, the hallway looks the same coming as it does going, so the agent has no way to know that it's simply proceeding back towards its starting point.

## Rephrasing the Problem in Terms of State Transition

From a top-down view, we human operators of the maze know that each position and orientation of the bot constitutes a unique state; that is, there are hundreds or thousands of states, depending on the length of the hallway -- four possible orientations for every valid coordinate. However, the bot doesn't see any of that. The bot only sees its immediate sensory input.

The bot's immediate sensory input, in its totality, consists of four Boolean variables, so it can be in any one of sixteen states. Each of those states has some probability of conferring a reward (though this is actually 0 almost everywhere; we humans know this but the bot doesn't, at least not at first). From each state, the bot can perform any one of four actions.

After fully exploring its environment and trying every combination of its sensory states and actions, the bot will construct the following table of possible state transitions. Let's not worry yet about probabilities; we'll do those later. Right now, let's just focus on which subsequent states the bot discovers are *possible* to enter from preceding states and actions. Our notation for representing a sensory state will be ```[isWallLeft, isWallAhead, isWallRight, isWallBehind]```, abbreviated as a four-digit binary number. E.g. ```1001``` would mean, "There's a wall to our left and a wall behind us."

Note that the table, in the interest of brevity, doesn't bother to fill in some "From" sensory states that the bot will never encounter during its navigation of this toy problem. For example, it will never be in a situation in which it is completely enclosed in walls (```1111```), or in which it is only adjacent to one wall (```1000```), to name a few examples.

For sake of clarity, we'll use "(IDENTITY)" to designate actions whose result is the same sensorium as the state they start from. Note that this does not mean that the bot didn't do anything; it just means that the bot has no immediate way to *know* it did something.

I'll use a "Label" designation for various reachable positions, to make it easier for humans to read the table.

The "desired" action in any given state, i.e. the one that indicates that the bot is on the correct path (or puts the bot on the correct path if it's gotten off of it), is marked with an asterisk. Note that, when the bot is ```SIDEWAYS```, it's impossible without further information to know whether the correct action should be to turn left or right. One will send it towards its goal, the other will send it back down the way it came. It depends on *how it turned sideways*, and that information is lost without further state retention. Fortunately, if the bot follows the asterisk-marked actions from start to finish, then there should be no way for it to end up in a sideways state; and even if it does, then as long as it proceeds down the hallway in either direction, it will eventually come to a landmark state from whence it can deterministically regain its correct orientation, as long as it follows the asterisk-marked actions.

The "Reward?" column indicates whether or not there's the possibility that the bot will receive a reward when entering this state.

| Sensor state  | Label                   | ```TURN LEFT```           | ```GO FORWARD```    | ```TURN RIGHT```        | ```TURN AROUND```         | Reward? |
|---------------|-------------------------|---------------------------|---------------------|-------------------------|---------------------------|---------|
| ```0011```    | ```CORNER_AFTER_TURN``` | ```CORNER_BACKWARDS```    | * ```HALLWAY```     | ```CORNER```            | ```CORNER_WRONG_TURN```   |         |
| ```0101```    | ```SIDEWAYS```          | * ```HALLWAY```           | (IDENTITY)          | * ```HALLWAY```         | (IDENTITY)                |         |
| ```0110```    | ```CORNER```            | * ```CORNER_AFTER_TURN``` | (IDENTITY)          | ```CORNER_WRONG_TURN``` | ```CORNER_BACKWARDS```    |         |
| ```0111```    | ```START_RT```          | * ```START```             | (IDENTITY)          | ```START_BK```          | ```START_LF```            |         |
| ```1001```    | ```CORNER_BACKWARDS```  | ```CORNER_WRONG_TURN```   | ```HALLWAY```       | ```CORNER_AFTER_TURN``` | * ```CORNER```            |         |
| ```1010```    | ```HALLWAY```           | ```SIDEWAYS```            | * (IDENTITY), ```CORNER```, ```CORNER_WRONG_TURN```, ```START_BK``` | ```SIDEWAYS``` | (IDENTITY) | YES |
| ```1011```    | ```START```             | ```START_LF```            | * ```HALLWAY```     | ```START_RT```          | ```START_BK```            |         |
| ```1100```    | ```CORNER_WRONG_TURN``` | ```CORNER```              | (IDENTITY)          | ```CORNER_BACKWARDS```  | * ```CORNER_AFTER_TURN``` |         |
| ```1101```    | ```START_LF```          | ```START_BK```            | (IDENTITY)          | * ```START```           | ```START_RT```            |         |
| ```1110```    | ```START_BK```          | ```START_RT```            | (IDENTITY)          | ```START_LF```          | * ```START```             |         |

If a bot executes the asterisk-marked actions, it will guaranteeably reach the reward from the start position every time. Indeed, it will converge upon the reward from any valid position and orientation at any occupiable point anywhere in the L-maze.

The problem is that the asterisk-marked actions are curated by humans! They are not deterministically discoverable by the bot!

The breakdown in discoverability comes, unsurprisingly, at the corner. There, the bot can either turn left and go forward, or turn around and go forward. Both will lead the bot into a hallway. The bot has no way to know that these are two different legs of the hallway -- that the hallway after a left turn is fundamentally different than the hallway after turning back.

Suppose the maze is relatively small. Imagine it looks like this:
```
####
R  #
## #
 # #
 ###
```
In such a maze, there are three ```HALLWAY``` segments: one between ```START``` and ```CORNER```, one between ```CORNER_AFTER_TURN``` and the reward, and one containing the reward itself. As such, the probability of getting a reward in ```HALLWAY``` is 33%. So a goal-seeking AI will try to enter the ```HALLWAY``` state in any way possible.

From the AI's perspective, the following two chains of action are equivalent right up until the end:

1. ```START``` --(```GO FORWARD```)-->
1. ```HALLWAY``` --(```GO FORWARD```)-->
1. ```CORNER``` --(```TURN LEFT```)-->
1. ```CORNER_AFTER_TURN``` --(```GO FORWARD```)-->
1. ```HALLWAY``` --(```GO FORWARD```)-->
1. ```HALLWAY``` +1 Reward

and

1. ```START``` --(```GO FORWARD```)-->
1. ```HALLWAY``` --(```GO FORWARD```)-->
1. ```CORNER``` --(```TURN AROUND```)-->
1. ```CORNER_BACKWARDS``` --(```GO FORWARD```)-->
1. ```HALLWAY``` --(```GO FORWARD```)-->
1. ```START_BK``` Wtf? Why am I here? Where's my reward?

Basically, it thinks that being in a ```HALLWAY``` and going forward has an equal probability of leading to a reward as it does to leading to a ```START_BK```. It has no way to distinguish the hallway leading to the reward from the hallway leading back to the start position, so it has no reason to prefer turning left over turning around. Sure, sometimes it'll turn left and sometimes it'll turn around with 50/50 odds. But, from a local greedy state perspective, choosing the correct action confers no observable difference from choosing the incorrect one. The AI just figures, "Hey, either one will get me back to a hallway. And sometimes a hallway leads me to a reward, and sometimes it doesn't. Eh. No way to tell." Without retaining some additional state, the AI will never learn to prefer one over the other, no matter how many times the wrong turn causes it to backtrack nor however many times the correct turn leads it to its prize.

## Distilling the Conundrum




