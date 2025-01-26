class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()
        
    def length(self):
        return self.direction.magnitude() 