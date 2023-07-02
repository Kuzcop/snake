import numpy as np

class snake:
    def __init__(self):
        self.body = [[(0,0),'right']]
        self.pos  = [(0,0)]

    def get_head(self):
        return self.body[0][0]
    
    def get_tail(self):
        return self.body[-1]
    
    def get_dir(self):
        return self.body[0][1]
    
    def get_length(self):
        return len(self.body)
    
    def set_head(self, coordinate):
        self.body[0][0] = coordinate

    def set_dir(self, heading):
        self.body[0][1] = heading

    def move(self):
        for i in reversed(range(1, self.get_length())):
            self.body[i][0] = self.body[i - 1][0]
            self.body[i][1] = self.body[i - 1][1]

    def grow_body(self):

        curr_tail_pos, curr_tail_dir = self.get_tail()       

        new_tail_pos = (0,0)
        new_tail_dir = curr_tail_dir

        if curr_tail_dir == 'up':
            new_tail_pos = (curr_tail_pos[0], curr_tail_pos[1] + 1)   
        if curr_tail_dir == 'down':
            new_tail_pos = (curr_tail_pos[0], curr_tail_pos[1] - 1)  
        if curr_tail_dir == 'left':
            new_tail_pos = (curr_tail_pos[0] + 1, curr_tail_pos[1])  
        if curr_tail_dir == 'right':
            new_tail_pos = (curr_tail_pos[0] - 1, curr_tail_pos[1])              

        self.body.append([new_tail_pos, new_tail_dir])
        self.pos.append((new_tail_pos))

    def is_eating_body(self):
        for i in range(1, self.get_length()):
            if (np.array(self.get_head()) == np.array(self.body[i][0])).all():
                return True
        return False
    
    def is_new_apple_in_body(self, coordinate):
        for i in range(self.get_length()):
            if (np.array(coordinate) == np.array(self.body[i][0])).all():
                return True
        return False
    
    def reset(self):
        self.body = [[(0,0),'right']]
        self.pos  = [(0,0)]

    def is_crashing_into_wall(self, length_squares):
        curr_head_pos = self.get_head()
        return curr_head_pos[0] < 0 or curr_head_pos[0] == length_squares or curr_head_pos[1] < 0 or curr_head_pos[1] == length_squares
    
    def is_eating_apple(self, apple):
        curr_head_pos = self.get_head()
        return (np.array(curr_head_pos) == np.array(apple)).all()
    
    def get_center_of_mass(self):
        x_total = 0
        y_total = 0
        length  = self.get_length()

        for i in range(length):
            x_total = x_total + self.body[i][0][0]
            y_total = y_total + self.body[i][0][1]

        x_avg = x_total/length
        y_avg = y_total/length

        return (x_avg, y_avg)
