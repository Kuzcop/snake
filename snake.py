class snake:
    def __init__(self, pos_head = (1,0), pos_tail = (0,0), dir = 'right'):
        self.pos_head = pos_head   # Measured in terms of sqaures
        self.pos_tail = pos_tail   # Measured in terms of squares
        self.dir      = dir
        self.body     = [(1,0), (0,0)]

    def get_head(self):
        return self.pos_head
    
    def get_tail(self):
        return self.pos_tail
    
    def get_dir(self):
        return self.dir
    
    def get_length(self):
        return len(self.body)
    
    def set_head(self, coordinate):
        self.pos_head = coordinate
        self.body[0] = self.get_head()

    def set_tail(self, coordinate):
        self.pos_tail = coordinate

    def set_dir(self, heading):
        self.dir = heading

    def update_body(self):
        for i in reversed(range(1, self.get_length())):
            self.body[i] = self.body[i - 1]
        self.set_tail = self.body[-1]

    

