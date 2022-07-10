import cell
import random
import pygame

class game:
    '''
    A class that contains methods to display the board and update its values.
    '''

    def __init__(self, n, cellSize):
        '''
        Create the blank board and define its size.
        '''
        
        self.__sizeX = n[0]
        self.__sizeY = n[1]
        self.__cell = cellSize
        self.board = [[0 for i in range(self.__sizeX)] for i in range(self.__sizeY)]
        self.update = set()

        # create a cell for every coordinate
        for i, row in enumerate(self.board):
            for j, _ in enumerate(row):
                self.board[i][j] = cell.cell((i,j))

        return None
    
    def rand(self):
        '''
        Generate a random board.
        '''
        random.seed()
        for i, row in enumerate(self.board):
            for j, _ in enumerate(row):
                self.board[i][j].setState(random.getrandbits(1))
        return None

    def export(self, name = 'export'):
        '''
        Write the current board to a text file.
        '''
        file = open(f'configs\{name}.txt', 'w')
        file.write(str(self.board).replace(', ', '').replace('[', '').replace(']', '\n').replace('\n\n\n', ''))
        file.close()

    def __str__(self):
        '''
        Print the current board as an n-by-n grid.
        '''
        s = ''
        for i, row in enumerate(self.board):
            for j, _ in enumerate(row):
                s += str(self.board[i][j].getState())
            s += '\n'
        return s

    def addToBoard(self, figure, head = (0,0)):
        '''
        Places imported figures onto the board.
        '''
        if figure:
            for i in range(len(figure)):
                for j in range(len(figure[i])):
                    self.board[(i + head[0]) % self.__sizeY][(j + head[1]) % self.__sizeX].setState(figure[i][j])
        return None

    def draw(self, surface):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(self.board[i]):
                if self.board[i][j].isAlive():
                    pygame.draw.rect(surface, (255, 255, 255), (self.board[i][j].getCoords()[1] * self.__cell, self.board[i][j].getCoords()[0] * self.__cell, self.__cell - 1, self.__cell - 1))
        return None  

    def initBox(self):
        '''
        Finite bounded topography.
        Create the cells and set their neighbors.

        Optimization: when adding neighbor A to cell B, could also add neighbor B to cell A
        '''

        # for each coordinate, add the appropriate neighbors to each cell
        for i, row in enumerate(self.board):
            for j, _ in enumerate(row):
                if (0 < i < (self.__sizeY - 1)) and (0 < j < (self.__sizeX - 1)):
                    self.board[i][j].addNeighbor(self.board[i-1][j-1]) # top left
                    self.board[i][j].addNeighbor(self.board[i-1][j])   # top
                    self.board[i][j].addNeighbor(self.board[i-1][j+1]) # top right
                    self.board[i][j].addNeighbor(self.board[i][j-1])   # left
                    self.board[i][j].addNeighbor(self.board[i][j+1])   # right
                    self.board[i][j].addNeighbor(self.board[i+1][j-1]) #  bot left
                    self.board[i][j].addNeighbor(self.board[i+1][j])   # bot
                    self.board[i][j].addNeighbor(self.board[i+1][j+1]) # bot right
                elif (i == 0) or (i == self.__sizeY - 1):
                    if i == 0:
                        if j == 0:
                            self.board[i][j].addNeighbor(self.board[i][j+1])
                            self.board[i][j].addNeighbor(self.board[i+1][j])
                            self.board[i][j].addNeighbor(self.board[i+1][j+1])
                        elif j == self.__sizeX - 1:
                            self.board[i][j].addNeighbor(self.board[i][j-1])
                            self.board[i][j].addNeighbor(self.board[i+1][j-1])
                            self.board[i][j].addNeighbor(self.board[i+1][j])
                        else:
                            self.board[i][j].addNeighbor(self.board[i][j-1])
                            self.board[i][j].addNeighbor(self.board[i][j+1])
                            self.board[i][j].addNeighbor(self.board[i+1][j-1])
                            self.board[i][j].addNeighbor(self.board[i+1][j])
                            self.board[i][j].addNeighbor(self.board[i+1][j+1])
                    elif i == self.__sizeY - 1:
                        if j == 0:
                            self.board[i][j].addNeighbor(self.board[i-1][j])
                            self.board[i][j].addNeighbor(self.board[i-1][j+1])
                            self.board[i][j].addNeighbor(self.board[i][j+1])
                        elif j == self.__sizeX - 1:
                            self.board[i][j].addNeighbor(self.board[i-1][j-1])
                            self.board[i][j].addNeighbor(self.board[i-1][j])
                            self.board[i][j].addNeighbor(self.board[i][j-1])
                        else:
                            self.board[i][j].addNeighbor(self.board[i-1][j-1])
                            self.board[i][j].addNeighbor(self.board[i-1][j])
                            self.board[i][j].addNeighbor(self.board[i-1][j+1])
                            self.board[i][j].addNeighbor(self.board[i][j-1])
                            self.board[i][j].addNeighbor(self.board[i][j+1])
                elif (j == 0) or (j == self.__sizeX - 1):
                    if j == 0:
                        self.board[i][j].addNeighbor(self.board[i-1][j])
                        self.board[i][j].addNeighbor(self.board[i-1][j+1])
                        self.board[i][j].addNeighbor(self.board[i][j+1])
                        self.board[i][j].addNeighbor(self.board[i+1][j])
                        self.board[i][j].addNeighbor(self.board[i+1][j+1])
                    elif j == self.__sizeX - 1:
                        self.board[i][j].addNeighbor(self.board[i-1][j-1])
                        self.board[i][j].addNeighbor(self.board[i-1][j])
                        self.board[i][j].addNeighbor(self.board[i][j-1])
                        self.board[i][j].addNeighbor(self.board[i+1][j-1])
                        self.board[i][j].addNeighbor(self.board[i+1][j])
                self.update.add(self.board[i][j])
        return None

    def initToroid(self):
        '''
        Toroidal topography.
        Create the cells and set their neighbors.

        Optimization: when adding neighbor A to cell B, could also add neighbor B to cell A
        '''
        # for each coordinate, add the appropriate neighbors to each cell
        for i, row in enumerate(self.board):
            for j, _ in enumerate(row):
                self.board[i][j].addNeighbor(self.board[(i-1) % self.__sizeY][(j-1) % self.__sizeX]) # top left
                self.board[i][j].addNeighbor(self.board[(i-1) % self.__sizeY][(j) % self.__sizeX])   # top
                self.board[i][j].addNeighbor(self.board[(i-1) % self.__sizeY][(j+1) % self.__sizeX]) # top right
                self.board[i][j].addNeighbor(self.board[(i) % self.__sizeY][(j-1) % self.__sizeX])   # left
                self.board[i][j].addNeighbor(self.board[(i) % self.__sizeY][(j+1) % self.__sizeX])   # right
                self.board[i][j].addNeighbor(self.board[(i+1) % self.__sizeY][(j-1) % self.__sizeX]) #  bot left
                self.board[i][j].addNeighbor(self.board[(i+1) % self.__sizeY][(j) % self.__sizeX])   # bot
                self.board[i][j].addNeighbor(self.board[(i+1) % self.__sizeY][(j+1) % self.__sizeX]) # bot right
                self.update.add(self.board[i][j])
        return None

    def unpackRules(self, Rulestring):
        rules = Rulestring.split('/')
        birth = rules.find('B')
        survival = rules.find('S')
        print(birth, survival)

    def gen(self, birth, survival, surface):
        
        nextUpdate = set()
        for cell in self.update:
            if (not cell.isAlive()) and (cell.getNeighborSum() in birth):
                cell.toggleNext()
                nextUpdate.add(cell)
                nextUpdate.update(cell.neighbors)
            elif (cell.isAlive()) and (cell.getNeighborSum() not in survival):
                cell.toggleNext()
                nextUpdate.add(cell)
                nextUpdate.update(cell.neighbors)
            else:
                cell.setNext(cell.getState())

        self.draw(surface)

        for cell in self.update:
            cell.setState(cell.getNext())

        self.update = nextUpdate

        return None