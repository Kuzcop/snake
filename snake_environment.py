import pygame
import math
import random
import gymnasium as gym
import numpy     as np
from   snake       import snake
from   gymnasium   import spaces

class SnakeEnv(gym.Env):

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

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
        # Choose Observation space depending on model
        if self.model == 'q_learn':
            self.observation_space = spaces.Dict(
                {
                    'quad_apple'  : spaces.Discrete(8),
                    #'quad_c_of_m'  : spaces.Discrete(9),
                    'surroundings' : spaces.Box(0, 1, shape=(3,), dtype=int)
                }
            )
        else:
            self.observation_space =  spaces.Dict(
                {
                    'quad_apple'  : spaces.Discrete(8),
                    #'quad_c_of_m' : spaces.Discrete(9),
                    'surroundings' : spaces.Box(0, 1, shape=(3,), dtype=int)
                }
            )
        # Agent is only capable of turning the snake left, continuing straight, or turning right
        self.action_space = spaces.Discrete(3)
        """
        The dictionary maps actions from `self.action_space` to 
        the new direction the snake will move in if that action is taken, 
        depending on the snake's current direction.
        0 - turning left, 1 - go straight, 2 - turning right
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
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window      = None
        self.clock       = None

    def _get_obs(self):
        if self.model == 'q_learn':
            return {
                    "quad_apple" : self.rotate(self.get_quadrant(self.apple)),
                    #'quad_c_of_m': self.rotate(self.get_quadrant(self.snake.get_center_of_mass())),
                    "surroundings": self.get_surroundings()
                   }
        else:
            return {
                    "quad_apple" : self.rotate(self.get_quadrant(self.apple)),
                    "surroundings": np.array(self.get_surroundings())
                   }

    def _get_info(self):
        return {
            "quad_apple" : self.rotate(self.get_quadrant(self.apple)),
            "surroundings": self.get_surroundings()
        }

    # Resets the snake to top-left of the play screen, apple's current position and score
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.snake.reset()
        self.reset_apple()
        self.score = 0         
        self.prev_distance_to_apple = math.dist(self.snake.get_head(), self.apple)
        #self.prev_distance_to_c_of_m = 0
        observation = self._get_obs()
        info        = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
        

    def step(self, action):
        # Use action_to_direction dict to translate agent action
        curr_direction, new_direction = self.snake.get_dir(), action
        new_direction = self._action_to_direction[curr_direction][int(new_direction)]
        # Move snake body and head
        self.snake.move()
        curr_head_pos = self.snake.get_head()
        self.move_head(new_direction, curr_head_pos)
        terminated = False
        reward = 0

        # Check to see if snake head is beyond the walls or in its body, end episode if true
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
                '''if self.prev_distance_to_apple > self.dist_to_apple():
                    reward =  -0.5'''
                
                '''if self.snake.get_length() > 10:
                    if self.prev_distance_to_c_of_m < self.dist_to_center_of_mass():
                        reward = -0.5'''

        self.prev_distance_to_apple  = self.dist_to_apple()
        #self.prev_distance_to_c_of_m = self.dist_to_center_of_mass()
        
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
        '''cm = self.snake.get_center_of_mass()
        x = self.square_size*cm[0]
        y = self.square_size*cm[1]
        pygame.draw.rect(self.window, 'blue', [x, y, self.square_size, self.square_size])'''

        # Drawing grid play area
        for i in range(1,self.length_squares):
            pygame.draw.line(self.window, 'white', [self.square_size*(i), 0], [self.square_size*(i), self.y_max], self.line_width)
            pygame.draw.line(self.window, 'white', [0, self.square_size*(i)], [self.x_max, self.square_size*(i)], self.line_width)


        if self.render_mode == "human":
            pygame.display.flip()
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:
            pass

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    # Returns once new apple coordinate no longer is in snake's body
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

        if   ((target_x - snake_head_x) == 0) and ((target_y - snake_head_y) < 0 ):
            return 0
        elif ((target_x - snake_head_x) > 0 ) and ((target_y - snake_head_y) < 0 ):
            return 1
        elif ((target_x - snake_head_x) > 0 ) and ((target_y - snake_head_y) == 0):
            return 2
        elif ((target_x - snake_head_x) > 0 ) and ((target_y - snake_head_y) > 0 ):
            return 3
        elif ((target_x - snake_head_x) == 0) and ((target_y - snake_head_y) > 0 ):
            return 4
        elif ((target_x - snake_head_x) < 0 ) and ((target_y - snake_head_y) > 0 ):
            return 5
        elif ((target_x - snake_head_x) < 0 ) and ((target_y - snake_head_y) == 0):
            return 6
        elif ((target_x - snake_head_x) < 0 ) and ((target_y - snake_head_y) < 0 ):
            return 7
        else:
            return 8 # Snake is in the same space as target
        
    # get_quadrant() assumes snake is moving up and finds relative quadrant apple is in to the snake's head
    # rotate() uses the snake's direction to ensure quadrant number is indifferent to direction
    def rotate(self, quadrant):
        snake_dir = self.snake.get_dir()
        if snake_dir == 'right':
            return (quadrant + 6) % 8
        elif snake_dir == 'down':
            return (quadrant + 4) % 8
        elif snake_dir == 'left':
            return (quadrant + 2) % 8
        return quadrant

    # Checks if surrounding blocks are:
    # 0 - Empty/Apple, 1 - Wall, 2 - Body
    def get_surroundings(self):
        snake_head_pos = np.array(self.snake.get_head())
        snake_head_dir = self.snake.get_dir()
        hazards = [0, 0, 0]
        spaces_around_head = {
                             'up'   : snake_head_pos + np.array([0, -1]),
                             'right': snake_head_pos + np.array([1, 0]),
                             'down' : snake_head_pos + np.array([0, 1]),
                             'left' : snake_head_pos + np.array([-1, 0])
                            }
    
        spaces_to_look     = self._action_to_direction[snake_head_dir].values()
        spaces_around_head = [spaces_around_head[space] for space in spaces_to_look]
                                    
        assert len(spaces_around_head) == 3

        for i, space in enumerate(spaces_around_head):
            if space[0] < 0 or space[0] == self.length_squares or space[1] < 0 or space[1] == self.length_squares:
                hazards[i] = 1
            elif self.snake.is_new_apple_in_body(space): # Reusing code for apple in body collision
                hazards[i] = 1
        return hazards

        
