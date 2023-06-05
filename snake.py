class snake:
    def __init__(self, pos_head, pos_tail, dir, body):
        self.pos_head = (1,0)   # Measured in terms of sqaures
        self.pos_tail = (0,0)   # Measured in terms of squares
        self.dir      = 'right'
        self.body     = [pos_head, pos_tail]

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

    def set_tail(self, coordinate):
        self.pos_tail = coordinate

    def set_dir(self, heading):
        self.dir = heading

    

