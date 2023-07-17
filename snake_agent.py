from collections import defaultdict
import numpy as np
from snake_environment import SnakeEnv


def create_zeroes_array():
    return np.zeros(size_of_action_space)

class snakeAgent:


    def __init__(
        self,
        learning_rate: float,
        initial_epsilon: float,
        epsilon_decay: float,
        final_epsilon: float,
        discount_factor: float = 0.95,
        env: SnakeEnv = None
    ):
        """Initialize a Reinforcement Learning agent with an empty dictionary
        of state-action values (q_values), a learning rate and an epsilon.

        Args:
            learning_rate: The learning rate
            initial_epsilon: The initial epsilon value
            epsilon_decay: The decay for epsilon
            final_epsilon: The final epsilon value
            discount_factor: The discount factor for computing the Q-value
        """
        global size_of_action_space
        size_of_action_space = env.action_space.n

        self.q_values        = defaultdict(create_zeroes_array)
        self.lr              = learning_rate
        self.discount_factor = discount_factor
        self.epsilon         = initial_epsilon
        self.epsilon_decay   = epsilon_decay
        self.final_epsilon   = final_epsilon
        self.training_error  = []

        self._action_to_direction = {
            'up':   0,
            'down': 1,
            'left': 2,
            'right':3,
        }

    def get_action(self, obs, env, is_training = True):
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        obs = (obs['quad_apple'], 
               #obs['quad_c_of_m'], 
               obs['surroundings'][0], obs['surroundings'][1], obs['surroundings'][2]
              )       
        if is_training:
            # with probability epsilon return a random action to explore the environment
            if np.random.random() < self.epsilon:
                return env.action_space.sample()
            # with probability (1 - epsilon) act greedily (exploit)
            else:
                return (np.argmax(self.q_values[obs]))
        else:
            return (np.argmax(self.q_values[obs]))

    def update(
        self,
        obs,
        action: int,
        reward: float,
        terminated: bool,
        next_obs,
    ):
        """Updates the Q-value of an action."""
        obs = (obs['quad_apple'], 
               #obs['quad_c_of_m'], 
               obs['surroundings'][0], obs['surroundings'][1], obs['surroundings'][2]
               )
        next_obs = (next_obs['quad_apple'], 
                    #next_obs['quad_c_of_m'], 
                    next_obs['surroundings'][0], next_obs['surroundings'][1], next_obs['surroundings'][2]
                    )
        future_q_value = (not terminated) * np.max(self.q_values[next_obs])
        temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[obs][action]
        )
        self.q_values[obs][action] = (
            self.q_values[obs][action] + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)
