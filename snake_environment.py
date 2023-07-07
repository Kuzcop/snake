import pygame
import math
import random
import gymnasium as gym
import numpy     as np
from   snake       import snake
from   gymnasium   import spaces

class SnakeEnv(gym.Env):

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10}

    def __init__(self, render_mode=None, size=20, model = 'q_learn'):
        self.x_max = 600
        self.y_max = 600
        self.length_squares = size
        self.line_width = 2
        self.square_size = math.floor(self.x_max / self.length_squares)
        self.score = 0
        self.snake = snake()
        self.apple = (random.randint(1, self.length_squares - 1), random.randint(1, self.length_squares - 1))
        self.prev_distance_to_apple = self.dist_to_apple()
        self.prev_distance_to_c_of_m = 0
        self.model = model

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        '''self.observation_space = spaces.Dict({
                "snake": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "apple": spaces.Box(0, size - 1, shape=(2,), dtype=int),
            })'''
        
        if self.model == 'q_learn':
            self.observation_space = spaces.Dict(
                {
                    'snake': spaces.Tuple((spaces.Discrete(self.length_squares), spaces.Discrete(self.length_squares))),
                    'apple': spaces.Tuple((spaces.Discrete(self.length_squares), spaces.Discrete(self.length_squares))),
                    'quad_apple'  : spaces.Discrete(8),
                    'quad_c_of_m'  : spaces.Discrete(9),
                    'dir'  : spaces.Discrete(4),
                    'quad_tail'  : spaces.Discrete(9)
                }
            )

        else:
            self.observation_space =  spaces.Dict(
                {
                    'snake'       : spaces.Box(-1, self.length_squares, shape=(2,), dtype=int),
                    'apple'       : spaces.Box(-1, self.length_squares, shape=(2,), dtype=int),
                    #'quad_apple'  : spaces.Discrete(8),
                    #'quad_c_of_m' : spaces.Discrete(9),
                    #'dir'         : spaces.Discrete(4)
                }
            )

        self.action_space = spaces.Discrete(3)

        """
        The following dictionary maps abstract actions from `self.action_space` to 
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            'up': {
                0: 'left',
                1: 'up',
                2: 'right',
            },
            'down':{
                0: 'right',
                1: 'down',
                2: 'left',
            },
            'left':{
                0: 'down',
                1: 'left',
                2: 'up',
            },
            'right':{
                0: 'up',
                1: 'right',
                2: 'down',
            }
        }

        self.get_direction = {
            0: 'up',
            1: 'down',
            2: 'left',
            3: 'right'
        }

        self._head_direction = {
            'up':    0,
            'right': 1,
            'down':  2,
            'left':  3 
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
        if self.model == 'q_learn':
            return {
                    "snake": self.snake.get_head(),
                    "apple": tuple(self.apple),
                    "quad_apple" : self.get_quadrant(self.apple),
                    'quad_c_of_m': self.get_quadrant(self.snake.get_center_of_mass()),
                    "dir"  : self._head_direction[self.snake.get_dir()],
                    "quad_tail"  : self.get_quadrant(self.snake.get_tail()[0])
                   }
        else:
            return {
                    "snake": self.snake.get_head(),
                    "apple": tuple(self.apple),
                   }

    def _get_info(self):
        return {
            'quad_c_of_m': self.get_quadrant(self.snake.get_center_of_mass())
        }

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.snake.reset()

        self.reset_apple()

        self.score = 0         

        self.prev_distance_to_apple = math.dist(self.snake.get_head(), self.apple)
        self.prev_distance_to_c_of_m = 0

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):

        curr_direction, new_direction = self.snake.get_dir(), action

        new_direction = self._action_to_direction[curr_direction][int(new_direction)]
        
        self.snake.move()

        curr_head_pos = self.snake.get_head()
        self.move_head(new_direction, curr_head_pos)

        # Check to see if snake head is going to hit a wall, end episode if true
        terminated = False
        reward = 0

        #if self.snake.is_crashing_into_wall(self.length_squares) or self.snake.is_eating_body():
        if self.snake.is_crashing_into_wall(self.length_squares) or self.snake.is_eating_body():
            reward = -500
            terminated = True
        else:
            if self.snake.is_eating_apple(self.apple):
                self.snake.grow_body()
                self.score = self.score + 1
                reward = 100
                self.reset_apple()
            else:
                reward = -1
                
                if self.prev_distance_to_apple > self.dist_to_apple():
                    reward =  0
                '''
                if self.prev_distance_to_c_of_m != 0:
                    if self.prev_distance_to_c_of_m < self.dist_to_center_of_mass():
                        reward = reward + 1
                    else:
                        reward = reward - 50'''

        self.prev_distance_to_apple  = self.dist_to_apple()
        self.prev_distance_to_c_of_m = self.dist_to_center_of_mass()
        
        if self.render_mode == "human":
            self._render_frame()

        observation = self._get_obs()
        info        = self._get_info()

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

        # Drawing cm
        cm = self.snake.get_center_of_mass()
        x = self.square_size*cm[0]
        y = self.square_size*cm[1]
        pygame.draw.rect(self.window, 'blue', [x, y, self.square_size, self.square_size])

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
    
    def dist_to_center_of_mass(self):
        c_of_m = self.snake.get_center_of_mass()
        return math.dist(self.snake.get_head(), c_of_m)
    
    def move_head(self, direction, curr_head_pos):
        if (direction == 'up'):
            self.snake.set_head((curr_head_pos[0], curr_head_pos[1] - 1))
            self.snake.set_dir('up')
        elif (direction == 'down'):
            self.snake.set_head((curr_head_pos[0], curr_head_pos[1] + 1))
            self.snake.set_dir('down')
        elif (direction == 'left'):
            self.snake.set_head((curr_head_pos[0] - 1, curr_head_pos[1]))
            self.snake.set_dir('left')
        elif (direction == 'right'):
            self.snake.set_head((curr_head_pos[0] + 1, curr_head_pos[1]))
            self.snake.set_dir('right')

    def get_quadrant(self, target):
        snake_head_x, snake_head_y = self.snake.get_head()
        target_x     , target_y    = target

        if   ((snake_head_x - target_x) == 0) and ((snake_head_y - target_y) < 0 ):
            return 0
        elif ((snake_head_x - target_x) > 0 ) and ((snake_head_y - target_y) < 0 ):
            return 1
        elif ((snake_head_x - target_x) > 0 ) and ((snake_head_y - target_y) == 0):
            return 2
        elif ((snake_head_x - target_x) > 0 ) and ((snake_head_y - target_y) > 0 ):
            return 3
        elif ((snake_head_x - target_x) == 0) and ((snake_head_y - target_y) > 0 ):
            return 4
        elif ((snake_head_x - target_x) < 0 ) and ((snake_head_y - target_y) > 0 ):
            return 5
        elif ((snake_head_x - target_x) < 0 ) and ((snake_head_y - target_y) == 0):
            return 6
        elif ((snake_head_x - target_x) < 0 ) and ((snake_head_y - target_y) < 0 ):
            return 7
        else:
            return 8
