class snake:
    def __init__(self):
        self.body = [ [(0,0),'right']]

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

        curr_tail_pos = self.get_tail()[0]
        curr_tail_dir = self.get_tail()[1]        

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

    def eat_body(self):
        for i in range(1, self.get_length()):
            if self.get_head() == self.body[i][0]:
                return True
        return False
    
    def is_new_apple_in_body(self, coordinate):
        for i in range(self.get_length()):
            if coordinate == self.body[i][0]:
                return True
        return False
    
    def reset(self):
        self.body = [[(0,0),'right']]



    

