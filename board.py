import cell
import random

import pygame
import parser
import numpy as np

'''
Micro-optimizations:
* gen() -> any way to get around checking each rule with every calculation?
    cell.getNeighborSum() in self.birth
    cell.getNeighborSum() not in self.survival
* gen() -> lots of overlap in adding/checking if neighbors are in set
    self.next_update.update(cell.getNeighbors())
'''

class game:
    '''
    A class that contains methods to display the board and update its values.
    '''

    def __init__(self, n, cellSize, rulestring):
        '''
        Create the blank board and define its size.
        '''
        
        self.__sizeX = n[0]
        self.__sizeY = n[1]
        self.__cell = cellSize
        
        self.rules = rulestring
        self.birth, self.survival = parser.getRules(self.rules)
        self.board = [[cell.cell((i, j)) for j in range(self.__sizeX)] for i in range(self.__sizeY)] # 2d array of cells
        self.update = set()
        self.next_update = set()

        return None

    def gen(self, surface):
        '''
        The true logic of the simulation. Update cells that need updating.
        ''' 
        self.next_update = set()
        
        for cell in self.update:
            if (not cell.isAlive()) and (cell.getNeighborSum() in self.birth):
                cell.setAlive()
                self.next_update.add(cell)
                self.next_update.update(cell.getNeighbors())
            elif (cell.isAlive()) and (cell.getNeighborSum() not in self.survival):
                cell.setDead()
                self.next_update.add(cell)
                self.next_update.update(cell.getNeighbors())
            else:
                cell.setNext(cell.getState())

        self.draw(surface)

        for cell in self.update:
            cell.setState(cell.getNext())

        self.update = self.next_update

        return None

    def draw(self, surface):
        for cell in self.update:
            if cell.isAlive():
                pygame.draw.rect(surface, (255, 255, 255), (cell.getCoords()[1] * self.__cell, cell.getCoords()[0] * self.__cell, self.__cell - 1, self.__cell - 1))
            else:
                pygame.draw.rect(surface, (0, 0, 0), (cell.getCoords()[1] * self.__cell, cell.getCoords()[0] * self.__cell, self.__cell - 1, self.__cell - 1))
        return None 
    
    def rand(self):
        '''
        Generate a random board.
        '''
        random.seed()
        for i, row in enumerate(self.board):
            for j, _ in enumerate(row):
                rand = random.getrandbits(1)
                self.board[i][j].setState(rand)
        return None

    def density(self, density):
        '''
        Generate a random board based on a density.
        '''
        random.seed()
        for i, row in enumerate(self.board):
            for j, _ in enumerate(row):
                randFloat = random.random()
                if randFloat <= density:
                    self.board[i][j].setState(1)
                else:
                    self.board[i][j].setState(0)
        return None

    def addToBoard(self, pattern, head = (0,0)):
        '''
        Places imported figures onto the board.
        '''
        figure = pattern[0]
        name = pattern[1]
        rules = pattern[2]

        if rules:
            if rules != self.rules:
                print(f'Warning: {name} has rules {rules} while simulation has rules {self.rules}.')

        if figure:
            for i in range(len(figure)):
                for j in range(len(figure[i])):
                    self.board[(i + head[0]) % self.__sizeY][(j + head[1]) % self.__sizeX].setState(figure[i][j])
        return None

    def init(self, **config):
        '''
        Finite bounded topography.
        Create the cells and set their neighbors.

        Optimization: when adding neighbor A to cell B, could also add neighbor B to cell A
        '''
        if not 'wrap' in config.keys():
            print('No boundary given')
            config['wrap'] = False
        if not config['wrap']:
            # for each coordinate, add the appropriate neighbors to each cell
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
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
        else:
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
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

    def export(self, **kwargs):
        if 'fileType' in kwargs.keys():
            if kwargs['fileType'] == 'rle':
                return None
            else:
                return parser.exportTXT([[cell.getState() for cell in row] for row in self.board])

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
    