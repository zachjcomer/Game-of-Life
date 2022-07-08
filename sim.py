'''
FIXME:  gen() ruleset interpreter

        rulestring interpreter

        txt importer

TODO:   .rle importer

        infinite plane conditions
        arbitrary wall boundaries

        import rotations, reflections

        set canvas size from import bounds

        * cells only need to be updated if they or their neighbors change state *

        arbitrary lattice configurations
        von-neumann neighborhoods, etc

'''
import importPattern
import cell
import random
import argparse
import math
import pygame
from os.path import exists

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

    def importToBoard(self, figure, head):
        '''
        Places imported figures onto the board.
        '''
        for i in range(len(figure)):
            for j in range(len(figure[i])):
                self.board[(i + head[0]) % self.__sizeY][(j + head[1]) % self.__sizeX] = figure[i][j]
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

def main():
    active = False # allows the simulation to proceed]

    parser = argparse.ArgumentParser('Configure the Game of Life')
    parser.add_argument('--size', dest = 'N', nargs = '+', type = int, required = False, help = 'The size of the grid. Enter one integer for a square or two for a rectangle. Default = 100 x 100 cells')
    parser.add_argument('--interval', dest = 'T', type = int, required = False, help = 'Set the clock tick rate for pygame. Default = 30 ticks/sec.')
    parser.add_argument('--closed', action = 'store_true', required = False, help = 'Set the topology to closed, so boundary cells have less than 8 neighbors. Default topology is toroidal.')
    parser.add_argument('--export', action = 'store_true', required = False, help = 'Write the initial setup to an export file called export.txt')
    args = parser.parse_args()

    # configure cellular automaton rules
    rulestring = 'B3/S23'
    birth = (3, 4, 9)
    survival = (9, 10)

    # configure the grid and cell sizes
    SCREEN = 1000 # max screen size
    Nx = 100 # number of horizontal cells
    Ny = 100 # number of vertical cells
    if args.N and len(args.N) > 1 and args.N[0] > 0 and args.N[1] > 0:
        Nx = args.N[0]
        Ny = args.N[1]
    elif args.N and args.N[0] > 0:
        Nx, Ny = args.N[0], args.N[0]
    cellSize = SCREEN / max(Nx, Ny)

    # configure pygame
    updateInterval = 30 # pygame clock tick rate
    if args.T and args.T > 0:
        updateInterval = args.T
    
    gen = 0

    # take optional arguements from parser to config initial gen
    g = game((Nx, Ny), cellSize)
    g.initBox()
    g.rand()

    # if requested by args
    '''
    if args.export:
        g.export()
    '''

    # start pygame and draw gen 0
    pygame.init()
    surface = pygame.display.set_mode((cellSize * Nx, cellSize * Ny))
    pygame.display.set_caption(f'Game of Life: Gen = {gen}, Running = {active}')
    clock = pygame.time.Clock()
    g.draw(surface)
    pygame.display.update()

    if args.closed:
        # loop through generations while allowed
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        active = not active
                        pygame.display.set_caption(f'Game of Life: Gen = {gen}, Running = {active}')
            if active:
                pygame.display.set_caption(f'Game of Life: Gen = {gen}, Running = {active}')
                clock.tick(updateInterval)
                surface.fill((0, 0, 0))
                g.gen(birth, survival, surface)
                pygame.display.update()
                gen += 1
    else:
        # loop through generations while allowed
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        active = not active
                        pygame.display.set_caption(f'Game of Life: Gen = {gen}, Running = {active}')
            if active:
                pygame.display.set_caption(f'Game of Life: Gen = {gen}, Running = {active}')
                clock.tick(updateInterval)
                surface.fill((0, 0, 0))
                g.gen(birth, survival, surface)
                pygame.display.update()
                gen += 1

    return None

if __name__ == '__main__':
    main()