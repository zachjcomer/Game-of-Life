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
        self.next = None
        self.neighbors = []
        return None

    def __str__(self):
        '''
        Return the cell location and the cell state.
        '''
        return f'({self.coords[0]},{self.coords[1]}): {self.state}'

    def getCoords(self):
        '''
        Return the cell location.
        '''
        return self.coords

    def getNeighbors(self):
        '''
        Return a list of the current cell's neighbor cell objects.
        '''
        s = '\n'
        for neighbor in self.neighbors:
            s += (f'{neighbor.getCoords()}: {neighbor.getState()}\n')
        return s

    def addNeighbor(self, neighbor):
        '''
        Add a cell object to the current cell's neighborhood.
        '''
        self.neighbors.append(neighbor)

    def getNeighborSum(self):
        neighborSum = 0
        for cell in self.neighbors:
            neighborSum += cell.getState()
        return neighborSum

    def getState(self):
        '''
        Return the current state of the cell.
        '''
        return self.state
    
    def isAlive(self):
        '''
        Returns true if the cell is alive.
        '''
        return self.state == 1

    def setState(self, x):
        '''
        Sets the value of the cell.
        '''
        self.state = x
        return None

    def setNext(self, x):
        '''
        Sets the value of the cell in the next generation.
        '''

        self.next = x
        return None

    def getNext(self):
        '''
        Returns the value of the cell in the next generation.
        '''
        return self.next

    def toggleNext(self):
        '''
        Toggle the state of the cell.
        '''
        if self.state == 0:
            self.next = 1
        else:
            self.next = 0

        return None