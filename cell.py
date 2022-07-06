'''
Creates a cell object at given coordinates, keeps track of neighbors, and handles the cell's status based on the rules.
'''

class cell:

    def __init__(self, coords):
        '''
        Initialize the cell at a given location.
        '''
        self.coords = coords
        self.state = 0
        self.neighbors = []
        return None

    def __str__(self):
        '''
        Return the cell location and the cell state.
        '''
        return f'({self.coords[0]},{self.coords[1]}): {self.state}.'

    def getNeighbors(self):
        '''
        Return a list of the current cell's neighbor cell objects.
        '''
        return self.neighbors

    def addNeighbor(self, neighbor):
        '''
        Add a cell object to the current cell's neighborhood.
        '''
        self.neighbors.append(neighbor)

    def getState(self):
        '''
        Return the current state of the cell.
        '''
        return self.state

    def setState(self):
        '''
        Toggle the state of the cell.
        '''
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0

        return None