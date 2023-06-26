import pygame
import math
import random
import gymnasium as gym
import numpy     as np
from   snake       import snake
from   gymnasium   import spaces

class SnakeEnv(gym.Env):

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10}

    def __init__(self, render_mode=None, size=20):
        self.x_max = 600
        self.y_max = 600
        self.length_squares = size
        self.line_width = 2
        self.square_size = math.floor(self.x_max / self.length_squares)
        self.score = 0
        self.snake = snake()
        self.apple = (random.randint(1, self.length_squares - 1), random.randint(1, self.length_squares - 1))
        self.prev_distance = self.dist_to_apple()

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        '''self.observation_space = spaces.Dict({
                "snake": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "apple": spaces.Box(0, size - 1, shape=(2,), dtype=int),
            })'''
        
        self.observation_space = spaces.Dict(
            {
                'snake': spaces.Tuple((spaces.Discrete(self.length_squares), spaces.Discrete(self.length_squares))),
                'apple': spaces.Tuple((spaces.Discrete(self.length_squares), spaces.Discrete(self.length_squares))),
                'dir'  : spaces.Discrete(4)
            }
        )

        self.action_space = spaces.Discrete(4)

        """
        The following dictionary maps abstract actions from `self.action_space` to 
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            0: 'up',
            1: 'down',
            2: 'left',
            3: 'right',
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

    def _get_obs(self):
        return {"snake": self.snake.get_head(),
                "apple": tuple(self.apple),
                "dir"  : self.snake.get_dir()}

    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                np.array(self.snake.get_head()) - np.array(self.apple), ord=1
            )
        }

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.snake.reset()

        #self.reset_apple()

        self.prev_distance = math.dist(self.snake.get_head(), self.apple)

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):

        direction = self._action_to_direction[action]
        
        self.snake.move()

        curr_head_pos = self.snake.get_head()

        if (direction == 'up'):
            self.snake.set_head((curr_head_pos[0], curr_head_pos[1] - 1))
        elif (direction == 'down'):
            self.snake.set_head((curr_head_pos[0], curr_head_pos[1] + 1))
        elif (direction == 'left'):
            self.snake.set_head((curr_head_pos[0] - 1, curr_head_pos[1]))
        elif (direction == 'right'):
            self.snake.set_head((curr_head_pos[0] + 1, curr_head_pos[1]))          


        # Check to see if snake head is going to hit a wall, end game if true
        terminated = False
        reward = 0

        if self.snake.is_crashing_into_wall(self.length_squares) or self.snake.is_eating_body():
            reward = -1
            terminated = True

        elif self.snake.is_eating_apple(self.apple):
            self.snake.grow_body()
            reward = 1
            self.reset_apple()
            self.prev_distance = self.dist_to_apple()
        
        elif self.prev_distance > self.dist_to_apple():
            self.prev_distance = self.dist_to_apple()
            reward = 0.5
        else:
            reward = -0.5
        
        if self.render_mode == "human":
            self._render_frame()

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            size = (self.x_max, self.y_max)
            self.window = pygame.display.set_mode(size)
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        # Render
        self.window.fill("black")

        # Drawing apple
        x = self.square_size*self.apple[0]
        y = self.square_size*self.apple[1]
        pygame.draw.rect(self.window, 'red', [x, y, self.square_size, self.square_size])

        # Drawing snake
        for i in range(self.snake.get_length()):
            x = self.square_size*(self.snake.body[i][0][0])
            y = self.square_size*(self.snake.body[i][0][1])
            pygame.draw.rect(self.window, 'green', [x, y, self.square_size, self.square_size])

        # Drawing grid play area
        for i in range(1,self.length_squares):
            pygame.draw.line(self.window, 'white', [self.square_size*(i), 0], [self.square_size*(i), self.y_max], self.line_width)
            pygame.draw.line(self.window, 'white', [0, self.square_size*(i)], [self.x_max, self.square_size*(i)], self.line_width)


        if self.render_mode == "human":
            pygame.display.flip()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            pass

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    def reset_apple(self):
         while True:
            self.apple = tuple(self.np_random.integers(0, self.length_squares, size=2, dtype=int))
            if not self.snake.is_new_apple_in_body(self.apple):
                break
    
    def dist_to_apple(self):
        return math.dist(self.snake.get_head(), self.apple)
