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

        self.q_values = defaultdict(create_zeroes_array)

        self.lr              = learning_rate
        self.discount_factor = discount_factor
        self.epsilon         = initial_epsilon
        self.epsilon_decay   = epsilon_decay
        self.final_epsilon   = final_epsilon
        self.training_error  = []

        self._action_to_direction = {
            0: 'up',
            1: 'down',
            2: 'left',
            3: 'right',
        }

    def get_action(self, obs, env) -> int:
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """

        dir = obs['dir']

        obs = (obs['snake'][0], obs['snake'][1],
               obs['apple'][0], obs['apple'][1])
                
        while True:

            # with probability epsilon return a random action to explore the environment
            if np.random.random() < self.epsilon:
                action = env.action_space.sample()

            # with probability (1 - epsilon) act greedily (exploit)
            else:
                action = int(np.argmax(self.q_values[obs]))

            chosen_direction = self._action_to_direction[action]
            
            if self.is_move_valid(dir, chosen_direction):
                return action


    def update(
        self,
        obs,
        action: int,
        reward: float,
        terminated: bool,
        next_obs,
    ):
        """Updates the Q-value of an action."""
        obs      = (obs['snake'][0], obs['snake'][1],
                    obs['apple'][0], obs['apple'][1])
        next_obs = (next_obs['snake'][0], next_obs['snake'][1],
                    next_obs['apple'][0], next_obs['apple'][1])

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
        
    def is_move_valid(self, action, dir):
        if   (action == 'up' and (dir == 'down')):
            return False
        elif (action == 'down' and (dir == 'up')):
            return False
        elif (action == 'left' and (dir == 'right')):
            return False
        elif (action == 'right' and (dir == 'left')):
            return False
        else:
                return True 
