# **Summer 2023 Self-Project into RL (Snake Game)**

![](misc/snake_game.gif)
*Q-learning agent after training for 500 episodes reaching 51 points*

As a way to learn more about RL, I created this project to play the snake game using a simple Q-learning agent, as well as, A2C and PPO agents from Stable-baselines3. Snake game made using pygame library, and environment follows an OpenAI structure to enable use of gymnasium and Stable-baselines3.

## Implementation Overiew

Actions:
- 0: Turn Left
- 1: Continue in current direction
- 2: Turn Right

Reward function:
- **-500**: If snake agent crashes into any of the four boundaries, or itself
- **-1**: For each action the agent takes to reach the apple
- **+100**: For eating the apple

Observations:
- **0-7**: The quadrant apple position is from snake's head, with south as 0 and increasing CCW to 7 at SW
- **[0-1, 0-1, 0-1]**: Three element array that contains 0 if there is no wall/body in each adjacent sqaure around the snake's head, 1 if otherwise.

## Installation


## Repo Overview
This repository contains files to play the snake game as yourself, or to let an agent play the game:

- [Snake](snake.py): This file holds the snake class, with attributes describing the position of the body and special methods to check against different collisions.
- [RL Snake Play](RL_snake_play.py): To play the game using RL agents, run this file with the name of the agent model you wish to play the game. Currently there is support for A2C and Q-learning and PPO. Use --h to learn more on how to run the file from the terminal. <br />
Example: <br />  (To train) python RL_snake_play.py -s 20 -m qlearn --train <br /> (To test) python RL_snake_play.py -s 20 -m qlearn --test
- [Snake Environment](snake_environment): This environment follows the OpenAi Gymnasium structure for environments. The action space for all agents is the same, spaces.Discrete(3), but the observation space may differ. reset() will put the snake back in the starting position, top left of the screen, reposition the apple, and reset distance measurements to the apple. step() moves the snake and then checks if the agent has crashed into a wall, eaten its body, or eating an apple. The first two cases and inefficient moves are negatively rewarded but is positively rewarded for eating the apple. Currently, the agent is able to dodge its body or the wall by passing in the observation information about any immediate hazards around the snake's head.
- [Snake Game](snake_game.py): To play the snake game yourself, run this file. Arrow keys to move.
- [Snake Helper](snake_helper.py): Miscellaneous functions for generating and saving learning curve plots. Also contains the code used to facilitate training and testing different models
- [Snake Agent](snake_agent.py): The file contains the class for creating a Q-learning snake agent.
- [q_learn.pkl](q_learn.pkl): Pickle file to run a working version of the Q-learning agent 
