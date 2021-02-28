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

At issue is the fact that, once in the corner, the AI can take two courses of action that result in its leaving the corner. One sends it down the wrong hallway, the other sends it down the correct one.

We can take for granted that a fully savvy bot, having explored its full environment and built a fully populated state transition diagram, will be able to use a minimax search to find its way to and from the start to the corner, and will always execute one of the two maneuvers that result in its departure from the corner. We can thus abstract the bot's actions, from the bot's POV, with the following simplified state transitions:
1. Start --> Hallway
1. Hallway --> Reward *OR* Corner *OR* Start, no way to predict
1. Corner --> Hallway (via ```TURN LEFT``` *OR* via ```TURN AROUND```, doesn't matter)

That, of course, is how the bot sees its situation. We humans know the situation is a little bit more complex, but also more predictable. I'll leave out the wrong paths, because we never need to traverse those if we can differentiate the correct ones from the wrong ones.
1. Start --> Hallway Before Corner
1. Hallway Before Corner --> Corner
1. Corner --> Hallway After Corner
1. Hallway After Corner --> Reward

So here's where I'm going with all of this. The key issue is that there exists a *hidden state*, a state that the bot unwittingly affects but that isn't part of its immediate sensorium. Put roughly, the situation goes like this:
1. The bot is in some observable state *H*.
1. The bot takes some action ```F``` that puts it into observable state *C*.
1. In state *C*, the bot can take two different actions, call them ```L``` and ```B```.
   1. ```B``` will put the bot back into state *H*.
   1. ```L``` will put the bot into state state *H'*.
   1. According to the bot's sensors, *H* is indistinguishable from *H'*.
1. In state *H'*, taking action ```F``` results in a reward.

Framed thus, the question of states and actions and all that jazz almost becomes moot. We can arguably smooth this entire matter down into the following scenario:
1. The bot is in a locked room. The room has a door (with a crashbar) and a button. The bot receives a reward for opening the door.
1. The bot has a vocabulary of two actions: ```PUSH DOOR``` and ```PUSH BUTTON```
1. The door has an unobservable locked/unlocked state. The door starts in the locked state.
1. If the bot tries to ```PUSH DOOR``` while the door is locked, then nothing happens.
1. If the bot performs ```PUSH BUTTON```, then the door transitions to an unlocked state. If it was already unlocked, then it stays unlocked. The bot doesn't hear a "click" or somesuch transition indicator.
1. If the bot tries to ```PUSH DOOR``` while the door is unlocked, then the bot wins and receives its reward.

I'll also add an operation called ```RESET``` that permits the agent the opportunity to return the puzzle to its starting state.

So here's the state transition diagram in its entirety.

**Pigeon Table: Experimenter's POV**

| Observed State (Unobserved) | ```PUSH_BUTTON```          | ```PUSH_DOOR```       | ```RESET```             | Reward |
|-----------------------------|----------------------------|-----------------------|-------------------------|--------|
| Captivity (Door Locked)     | Captivity (Door Unlocked)  | *(IDENTITY)*          | *(IDENTITY)*            |        |
| Captivity (Door Unlocked)   | *(IDENTITY)*               | Freedom               | Captivity (Door Locked) |        |
| Freedom                     | *(IDENTITY)*               | *(IDENTITY)*          | Captivity (Door Locked) | +1     |

And, as they say: And that's the show!

(NOTE: Later we can see what happens when the button only works 50% of the time.)

The trouble is that this isn't what the bot perceives. What the bot perceives is this.

**Pigeon Table: Pigeon's POV**

| Observed State | ```PUSH_BUTTON```  | ```PUSH_DOOR```                                 | ```RESET```   | Reward |
|----------------|--------------------|-------------------------------------------------|---------------|--------|
| Captivity      | *(IDENTITY)*       | Sometimes: *(IDENTITY)*, Sometimes: Freedom     | *(IDENTITY)*  |        |
| Freedom        | *(N/A)*            | *(N/A)*                                         | Captivity     | +1     |

As far as the bot sees things, based on its experience of trying random things and noting results,
pressing the button never does anything, whereas pushing the door seems to work about 50% of the time.
So it makes no sense to ever push the button; your best bet is to just keep trying the door.

How do we get the bot to realize that there's a causal link between pressing the button
and the door being openable?

That's a hard question.

## Proposing a Solution

This scenario of realizing that one first has to push a button to unlock a door is intriguing because it addresses
whether or not the agent can infer causation. This is, of course, ultimately an epistemological problem, not just
a statistical one. That's *why* it's hard.

### Theory: An Assumption of Causality is Parsimonious

Note that a pigeon in a Skinner box can, of course, be taught to press a button in order to open a hatch that
contains a reward. We know from an extraordinary number of actual experiments, as well as application of
Morgan's Canon, as well as straight-up common sense, that the pigeon does in fact learn that pressing the button
causes the reward. However, the pigeon doesn't necessarily *have* to learn this -- that is, it doesn't necessarily
follow from some kind of "first principles" that the pigeon *must* learn that the button opens the hatch.
It would be entirely rational for the pigeon to believe that, hey, maybe the hatch just opens on its own sometimes,
and the pressing of the button has nothing to do with anything.

I propose that the fact that the pigeon does in fact learn to press the button to open the hatch comes from
the application of a built-in bias within cognitive systems to assume that the world is "linear",
for want of a more fitting term. That is,
the world in any time frame can almost always be assumed to be the same as it was in the previous time frame,
except in ways that the organism explicitly *made* it be different. Objects stay where you put them; events
don't just spontaneously happen for no reason; and if a dropped apple would fall to the ground yesterday, then
it will still fall to the ground today, and will still do so tomorrow.

Mind you, by "linear" I don't merely
mean "deterministic", but something even more rigid: deterministic in an observable, predictable, static
sort of way. That is, some might argue that the rolling of a die is "deterministic" on the level of molecular
kinematics; but, unless you had some kind of impossible instrument that could measure the positions and velocities
of every molecule of the die without affecting them, then that determinism is not usable in any way by any
cognitive system. Therefore, from the point of view of an intelligent agent, there's no functional difference between
a "deterministic" die versus one that is genuinely nondeterministic. If one had two dice, one that was
genuinely nondeterministic due to some kind of quantum magic, and the other kinematically deterministic
but whose predictability was based solely on a corpus of data inaccessible to the experimenter (i.e. the
positions and velocities of every constituent molecule of the die), then no possible experiment could
distinguish one from the other. As such, the notion that a physical die is "deterministic" reduces the
notion of determinism to something purely academic, and ultimately useless.
In other words, what I'm seeking
to describe is more than just physical determinism, but a sort of "perceptual determinism", or "actionable
determinism", with relevance to a problem-solving agent.

Reality isn't actually "linear" in this sense. But reality is *close enough* to
what I'm loosely imagining as "linear" that intelligence bothered to evolve in the first place.
If the laws of physics and the nature of reality were more "linear" than they actually are,
i.e. simpler and more predictable, with a more static and unchanging environment,
then intelligence would be unnecessary (and arguably there wouldn't be sufficient variance in structure
to permit the rise of biological life in the first place anyway). If nature was less linear, i.e.
more chaotic and unpredictable, with events occurring through unseen antecedents or possibly
with no antecedents whatsoever, then intelligence wouldn't be useful to evolve because it would
be futile. It is only within this narrow band of predictability that animal intelligence, up
to and including Homo sapiens, could arise.

Therefore, the pigeon *must* assume that *something **causes** the door to get unlocked*, and that this
"something" *must be something that the pigeon itself does*.

Let's put this contrapositively: The pigeon *could* assume that the door just sometimes opens by itself
sometimes. But then the pigeon would have to believe that it exists in a universe in which things
sometimes just happen by themselves. That is a much more disruptive assumption, with much more far-reaching
and frankly terrifying ramifications, than for the pigeon to believe that its locus of control is still
internal. It is in fact *simpler*, i.e. more *parsimonius*, for the pigeon to believe that it lives
in an observable, deterministic, mostly-static universe, and that the hatch is controlled by the button
which is in turn controlled by the pigeon; than for it to believe that the hatch just opens
sometimes by itself.

Naturally, we all know that the pigeon *does* live in a universe in which things "just happen".
The pigeon probably knows this to an extent as well, in the same way that we all do, per Morgan's Canon.
The pigeon is not spared the existential horror of Lovecraftian revelations merely by
trying to believe in the controllability of this one door. None of us are. Think of the citizens of Pompeii,
having lived for generations at the base of this (as far as they knew) unique geological formation, when
one day, for absolutely no reason and no warning, the Earth itself turned inside out, causing the air
itself to choke them and the ground to flow like water and burn hotter than fire, in direct contradiction
to every fundamental law of reality they had ever conceived of; and the whole time, a significant
portion of them were recorded to ask, "What did we do to cause this? How did we anger the gods?"

However, the fact remains that a *tendency* towards this assumption, even if false and even
in situations in which it's ultimately futile, is the only approach that's *useful*. You can,
of course, just assume that everything is chaos and randomness and the universe has no order, sure.
But doing so makes you miss the little bits of predictability that *do* exist, the small sunlit
"placid island[s] of ignorance in the midst of black seas of infinity[.]" It ultimately comes down
to Pascal's Wager: Insofar as the world is ordered, seeking that order confers a bit of gain;
and insofar as the world is chaotic, seeking order anyway confers no loss. In fact, it doesn't
even guaranteeably confer a loss of time or energy, because you can't take for granted that
you would have that time or energy to begin with, or that any saving of time or energy can be
counted on, if the universe were truly pure chaos; that is, if one makes the argument, "It's
all futile, so you might as well save your breath," one is implicitly acknowledging that the
act of saving your breath is itself not simply also destined to be futile.

Besides, it appears that the laws of reality are such that "linearity" does tend to increase with locality.
The Pompeiians couldn't control the Earth's magma; the dinosaurs couldn't control the trajectories
of asteroids; but that pigeon can at least control the hatch in its box. In the words of Jordan Peterson,
you might not be able to put the whole world in order, but you can at least clean your room.

I suppose it would be fair to summarize all of the above thus: Just as the thermodynamicist (or
Aristotle) asserts that nature abhors a vacuum, the intelligent agent likewise asserts that
nature abhors uncontrollability. It may not be *true* -- i.e. nature might be totally fine
with being outside the control of the agent -- but the intelligent agent must make the *assumption*
that uncontrollability is the exception rather than the norm.
To the intelligent agent, an event that lacks observably deterministic controllability
provides a clue that there is in fact some precursory action that the agent is actually
performing without knowing it. The agent must function under the assumption that it is fact
doing *something* to please or anger the gods; the agent just needs to find out what that
something is.

### Inventing Hidden Variables to Blame

Let's take a close look at *Pigeon Table: Pigeon's POV*. Specifically, look at the cell (Captivity, ```PUSH_DOOR```).
The fact that its transition is labeled as *sometimes* going to one subsequent state and *sometimes* to another
should be a critical indicator that there is some hidden variable in play, some unobserved property of the
world that gets set by something that the agent does.

We don't know what that variable is, how it gets set, or how many values it might possibly have
(or if, indeed, it is discrete or continuous, and if continuous then what its range is). But let's 
crawl before we fly. 

Let's make some simplifying assumptions.
* The hidden variable is Boolean. This is a pretty safe baseline assumption -- either it *is* a thing, or it isn't. Even if it were a continuous variable, then nonetheless an intelligent agent would only care about its value insofar as it *is* or it *isn't* beyond some threshold or within some range. The act of making a decision collapses the metaphorical wave function.
* The hidden variable entirely determines the outcome of the seemingly unpredictable process.

The latter assumption makes it possible to narrow down the range of options as to what exactly causes the transition of the variable. That is, if I try the door and find that it's locked, and then I go do some stuff, and then I come back and try the door again and find that it's *not* locked, then we can assume that one of the things we did caused the door to become unlocked.

### Walking Through the Pigeon Box by Hand

Let's go step by step through the actions of an agent in the pigeon box.

~~The agent starts out in the observable state of Captivity. It is tasked with populating a state transition table so as to develop a model that will enable it to reliably acquire a reward. This table is, of course, a means to an end; when complete, the agent will be able to simply run a search algorithm to make optimal decisions to get from its present state to its goal state. However, its ability to make optimal decisions is dependent on the completeness of this table. It will therefore be motivated by an intrinsic tradeoff between going straight for the acquisition of a goal and the filling of its table. This can be thought of as a "curiosity" hyperparameter, and it can depend on how much reward the agent has recently acquired -- that is, an agent that has recently been "sated", i.e. has acquired enough nutrients to be comfortable, may have a higher curiosity than one that is starving.~~ This is great for later, but is largely a distraction for now. Let's put a pin in this. For now, the agent will use its search capabilities for the more straightforward task of just seeking reward directly.

The agent starts out in the observable state of Captivity. The agent's state transition table starts out looking like this -- all unknown. Note that even Reward is unknown, because Reward is only doled out upon arrival into a state, and the agent never performs an action that involves arriving in the state of Captivity.

| State Observed        | ```BUTTON```        | ```DOOR```        | ```RESET```   | Reward |
|-----------------------|---------------------|-------------------|---------------|--------|
| Captivity             | ???                 | ???               | ???           | ???    |

From this state, based on this knowledge, the agent has absolutely no idea which action to take. None will lead it to any subsequent known reward transitions. As such, it can just randomly pick some action or another purely at random.

By sheer coincidence, the agent could immediately execute a series of moves that grant it a reward, and then return it to its initial state. Or, the agent can be temporarily placed under player control -- "possessed" by the player, as it were, while it simply observes helplessly -- to make a specific sequence of actions for purely pedagogical purposes. Specifically, these actions are: ```BUTTON```, ```DOOR```, and ```RESET```, in that order. It will log the actions it performed and the states achieved. It may seem that we are giving the agent far too much credit to presume that it could immediately randomly pick exactly the right actions that will give it perfect performance, but the truth is that, in doing so, we are doing it no favors; this sequence of actions confers upon the agent the *least* possible amount of information about its world. By leading it down this garden path, we are actually tricking the agent into thinking that its world is simpler than it actually is.

| State Observed        | ```BUTTON```        | ```DOOR```        | ```RESET```   | Reward |
|-----------------------|---------------------|-------------------|---------------|--------|
| Captivity             | Captivity           | Freedom           | ???           | 0      |
| Freedom               | ???                 | ???               | **Captivity** | +1     |

At this point, remember that the last thing the bot did was ```RESET```. The bot is now back in the observable state of Captivity; and, unbeknownst to it, the door is back in a state of Locked. 

From here, according to the bot's state transition table, its search algorithm can easily see that, if it performs the action ```DOOR```, it will follow the transition to Freedom and receive a reward. So it performs ```DOOR```. 

And finds that, after performing ```DOOR```, it's still in a state of Captivity. And it says, "Huh!?"

| State Observed        | ```BUTTON```        | ```DOOR```                      | ```RESET```   | Reward |
|-----------------------|---------------------|---------------------------------|---------------|--------|
| Captivity             | Captivity           | **~~Freedom~~ Captivity?!?!**   | ???           | 0      |
| Freedom               | ???                 | ???                             | Captivity     | +1     |

Well, there's only two explanations for why ```DOOR``` would have taken us to Freedom before but takes us to Captivity now: 
1. The transition is inherently nondeterministic.
1. The transition is mediated by a hidden variable that we somehow changed.

Because of the reasons laid out in all of that philosophizing in the previous section, we choose to believe the latter.

The agent, then, has to imagine that there exists a hidden variable, one that the agent can't directly observe but whose state can be inferred by the operation of the door. The agent can *define* the hidden variable as a Boolean whose value was False when the ```DOOR``` action produced the previously observed Freedom transition, but is True now that it's producing the Captivity transition. The agent has no way to know what the variable's state was when prior actions were taken -- specifically, when it performed ```BUTTON``` or ```RESET```. It also has no way to know whether or not the variable's state *stays* True after it performs the revelatory action.

| State Observed + Hidden Variable | ```BUTTON```        | ```DOOR```                      | ```RESET```      | Reward |
|----------------------------------|---------------------|---------------------------------|------------------|--------|
| Captivity + False                | Captivity + ???     | Freedom + ???                   | ???              | 0      |
| Captivity + True                 | Captivity + ???     | **Captivity + ???**             | ???              | 0      |
| Freedom + ???                    | ???                 | ???                             | Captivity + ???  | +1     |

So now here the agent is, having just tried the door and having found it to return it to the observable Captivity state. It just followed the transition ("Captivity + True", ```DOOR```) -> "Captivity + ???" (marked in bold). That is, we know that the origin state has a hidden variable value of True because -- much like Einstein defined time as "the phenomenon of nature that is measured with a clock" -- we *defined* the hidden variable to be whatever it is in the world that, when we are in the observable Captivity state,  makes ```DOOR``` take us to the observable Freedom state when it's False and back to the observable Captivity state when it's True.

Well, the agent is in a bit of a conundrum now. Having just followed that transition to "Captivity + ???", the agent now has no idea what state it's in. Fortunately, it can find out -- by trying the door! Remember, the hidden variable is that which makes the door work. Because we are currently in the observable Captivity state, if we try the door now and find that it takes us to Freedom, we will know that the state we came from had a hidden variable value of False. Of course, we will transition to some other state, Freedom + ???, and within that state we won't know the hidden variable's value because we don't know what exactly makes the variable change. But we can at least try it now and get some information about the state we are in now.

The search algorithm isn't interested directly in populating the table, though. The search algorithm is interested in getting to a Reward state, which it knows is "Freedom + ???". The bot might currently be in "Captivity + True" or "Captivity + False", it doesn't know. (It's in "Captivity + True", but shh, don't tell it that.) The search engine will search both possibilities. If the bot is currently in state "Captivity + False", then ```DOOR``` will lead it straight to victory, which is an instant win. If we're currently in "Captivity + True", then ```DOOR``` will take us right back to where we are now -- which will reveal to us that the current state is "Captivity + True", and will tell us that we need to try some other course of action. This entire analysis is *also* true if the agent goes for ```BUTTON``` and ```RESET```, except for one thing: the bot already knows that ("Captivity + False", ```DOOR```) will result in reward -- and is, in fact, the *only* action that results in reward. So all possible actions are simply efforts to try to reach the state "Captivity + False", so that we can perform ```DOOR```. But there's a chance we're already *in* state "Captivity + False", so performing anything other than ```DOOR``` is simply reaching Freedom with extra steps. Therefore, if the search algorithm is constructed properly, it should return ```DOOR``` as the action with the shortest path to a reward.

So, the agent tries ```DOOR``` and finds that, sure enough, it's still locked. So we know that we must have been in "Captivity + True". And, indeed, still are.

| State Observed + Hidden Variable | ```BUTTON```        | ```DOOR```                      | ```RESET```      | Reward |
|----------------------------------|---------------------|---------------------------------|------------------|--------|
| Captivity + False                | Captivity + ???     | Freedom + ???                   | ???              | 0      |
| Captivity + True                 | Captivity + ???     | **Captivity + True**            | ???              | 0      |
| Freedom + ???                    | ???                 | ???                             | Captivity + ???  | +1     |

At this point the agent doesn't have a lot of options. The agent has established that, at "Captivity + True", the action ```DOOR``` is a reflexive cycle, so it can at least rule out trying the door again. It has incomplete information about what happens if it performs ```BUTTON```, and no information at all about what happens if it performs ```RESET```. Which one should it try first?

In accordance with the old Dungeons & Dragons adage that it's better to kill one than wound two, let's suppose that it's better to get complete information about something previously thought known but now evidently laden with hidden meaning. So let's suppose that the agent chooses to investigate the state of the hidden variable in ```BUTTON``` transition.

Actually, there's an incredibly good reason why the agent would want to try the button: Because the hidden variable is defined based on what happens when we try ```DOOR``` in the Captivity observed state, the value of the variable can only be tested when in the Captivity observed state. Therefore, the agent can prefer to seek out transitions that will put them into a state from which it can test its hidden variable.

Ultimately, it's up to the search algorithm, which will seek the shortest route to a reward. The search algorithm *could* say, "Hey, you've never tried ```RESET```. When you're in an observed Captivity state, ```RESET``` could be an immediate reward button. You don't know!" And that's true, we don't. But we *do* know that we can reach a reward from "Captivity + False", and we know that there's a 50/50 chance that ```BUTTON``` will take us to "Captivity + False". The devil we know, in this case, is probably better than the devil we don't. If the devil we know involved many extra steps, and if we had some better way to quantify the uncertainty of the ```RESET``` action from this state, then we might ultimately choose to try ```RESET``` after all. But in this case, depending on how we engineer the search algorithm, the risk/reward doesn't seem worth it.

So the bot tries ```BUTTON```, and finds itself in state "Captivity + ???". 

| State Observed + Hidden Variable | ```BUTTON```        | ```DOOR```                      | ```RESET```      | Reward |
|----------------------------------|---------------------|---------------------------------|------------------|--------|
| Captivity + False                | Captivity + ???     | Freedom + ???                   | ???              | 0      |
| Captivity + True                 | **Captivity + ???** | Captivity + True                | ???              | 0      |
| Freedom + ???                    | ???                 | ???                             | Captivity + ???  | +1     |

From here, it does what it always does when it's in a Captivity state with an unknown hidden variable: it tries the door, which is its quickest best hope for freedom. It finds, lo and behold, that the door opens! The bot's new observable state is Freedom! That means that the state it transitioned from must have a hidden variable value of False.

| State Observed + Hidden Variable | ```BUTTON```        | ```DOOR```                      | ```RESET```      | Reward |
|----------------------------------|---------------------|---------------------------------|------------------|--------|
| Captivity + False                | Captivity + ???     | **Freedom + ???**               | ???              | 0      |
| Captivity + True                 | Captivity + False   | Captivity + True                | ???              | 0      |
| Freedom + ???                    | ???                 | ???                             | Captivity + ???  | +1     |

Well, now that it's in a state of Freedom and has received its reward, there's not much for it to do but to try to get back to a state of "Captivity + False". From "Freedom + ???", we can temporarily assume that the hidden variable doesn't affect transitions in Freedom, though this may ultimately prove to be untrue. In Freedom, ```BUTTON``` and ```DOOR``` may well return it to "Captivity + False" (they won't), but ```RESET``` will definitely return it to Captivity + *something*. So, again, the search algorithm should choose the devil it knows.

So, in the Freedom observed state, it performs ```RESET```, and finds itself in a state of "Captivity + ???". Well, sure enough, from here it tries the door, and finds it locked. So it knows that it had just come to "Captivity + True", and is therefore now in "Captivity + True" as well. 

| State Observed + Hidden Variable | ```BUTTON```        | ```DOOR```                      | ```RESET```      | Reward |
|----------------------------------|---------------------|---------------------------------|------------------|--------|
| Captivity + False                | Captivity + ???     | Freedom + ???                   | ???              | 0      |
| Captivity + True                 | Captivity + False   | **Captivity + True**            | ???              | 0      |
| Freedom + ???                    | ???                 | ???                             | Captivity + True | +1     |

This now provides the bot with all the information it needs to solve the game perfectly indefinitely.


