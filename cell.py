'''
Creates a cell object at given coordinates, keeps track of neighbors, and handles the cell's status based on the rules.
'''

class cell:

    def __init__(self, coords):
        '''Initialize the cell at a given location.'''
        
        self.coords = coords
        self.state = 0
        self.next = 0
        self.neighbors = []
        return None

    def get_neighbor_sum(self):
        '''Sum the states of neighbor cells to compute next for self.'''
        neighborSum = 0
        for cell in self.neighbors:
            neighborSum += cell.get_state()
        return neighborSum

    def set_next(self, x):
        '''Sets the value of the cell in the next generation.'''
        self.next = x
        return self

    def set_alive(self):
        '''Sets the next value to alive.'''
        self.next = 1
        return None
    
    def set_dead(self):
        '''Sets the next value to dead.'''
        self.next = 0
        return None

    def get_next(self):
        '''Returns the value of the cell in the next generation.'''
        return self.next

    def set_state(self, x):
        '''Sets the value of the cell.'''
        self.state = x
        return self

    def get_state(self):
        '''Return the current state of the cell.'''
        return self.state

    def is_alive(self):
        '''Returns true if the cell is alive.'''
        return self.state == 1

    def add_neighbor(self, neighbor):
        '''Add a cell object to the current cell's neighborhood.'''
        self.neighbors.append(neighbor)

    def get_neighbors(self):
        '''Return a list of the current cell's neighbor cell objects.'''
        return self.neighbors

    def getCoords(self):
        '''Return the cell location.'''
        return self.coords

    def __str__(self):
        '''Return the cell location and the cell state.'''
        return f'({self.coords[0]},{self.coords[1]}): {self.state}'