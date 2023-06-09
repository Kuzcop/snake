# snake

## **Summer 2023 Self-Project into RL**

This repository contains files to play the snake game as yourself, or to let an agent play the game:

- [Snake](snake.py): This file holds the snake class, with attributes describing the position of the body and special methods to check against different collisions.
- [RL Snake Play](RL_snake_play.py): To play the game using RL agents, run this file with the name of the agent model you wish to play the game. Currently there is support for A2C and Q-learning
- [Snake Environment](snake_environment): This environment follows the OpenAi Gymnasium structure for environments. The action space for all agents is the same, spaces.Discrete(3), but the observation space differs. reset() will put the snake back in the starting position, top left of the screen, reposition the apple, and reset distance measurements to the apple. step() moves the snake and then checks if the agent has crashed into a wall, eaten its body, or eating an apple. The first two cases are negatively rewarded but is positively rewarded for eating the apple and moving closer to it. Currently working on a method to avoid crashing into its body; using the idea of its center of mass as a target to move away from.
- [Snake Game](snake_game.py): To play the snake game yourself, run this file. Arrow keys to move.
- [Snake Helper](snake_helper.py): Miscellaneous functions for generating and saving learning curves plots
- [agent_AtoB.rar](agent_AtoB.rar): Unzip the rar file to run a working version of the Q-learning agent 
- [Snake Agent](snake_agent.py): File contains the class for creating a Q-learning snake agent.