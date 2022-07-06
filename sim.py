'''
TODO:   infinite plane conditions
        arbitrary wall boundaries

        more boundary verifications

        import rotations, reflections

        set canvas size from import bounds

        rewrite cells to be objects
        * cells only need to be updated if they or their neighbors change state *
'''
import importPattern
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
        return None
    
    def rand(self):
        '''
        Generate a random board.
        '''
        random.seed()
        self.board = [[random.getrandbits(1) for i in range(self.__sizeX)] for i in range(self.__sizeY)]
        return None

    def importFromTxt(self, name, head = (0, 0)):
        '''
        Import from a txt file.
        '''
        if exists(f'configs\{name}.txt'):
            file = open(f'configs\{name}.txt').read()
        else:
            return False

        r = 1 + file.count('\n')
        pattern = file.replace('\n', '')
        c = len(pattern) // r
        board = [[0 for i in range(c)] for i in range(r)]
        for i in range(r):
            for j in range(c):
                board[i][j] = int(pattern[j + c * i])
        self.importToBoard(board, head)

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
        for i in range(self.__sizeY):
            s += f'{self.board[i][:]}\n'
        return s

    def importToBoard(self, figure, head):
        '''
        Places imported figures onto the board.
        '''
        for i in range(len(figure)):
            for j in range(len(figure[i])):
                self.board[(i + head[0]) % self.__sizeY][(j + head[1]) % self.__sizeX] = figure[i][j]
        return None

    def forceDraw(self, surface):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(self.board[i]):
                if self.board[i][j] == 1:
                    pygame.draw.rect(surface, (255, 255, 255), (j * self.__cell, i * self.__cell, self.__cell - 1, self.__cell - 1))
        return None  

    def finite(self, surface):
        '''
        Finite boundary conditions.
        '''
        next = [[0 for i in range(self.__sizeX)] for i in range(self.__sizeY)]
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                living = 0
                if (0 < i < (self.__sizeY - 1)) and (0 < j < (self.__sizeX - 1)):
                    living += self.board[(i-1) % self.__sizeY][(j-1) % self.__sizeX] # top left
                    living += self.board[(i-1) % self.__sizeY][(j) % self.__sizeX] # top
                    living += self.board[(i-1) % self.__sizeY][(j+1) % self.__sizeX] # top right
                    living += self.board[(i) % self.__sizeY][(j-1) % self.__sizeX] # left
                    living += self.board[(i) % self.__sizeY][(j+1) % self.__sizeX] # right
                    living += self.board[(i+1) % self.__sizeY][(j-1) % self.__sizeX] #  bot left
                    living += self.board[(i+1) % self.__sizeY][(j) % self.__sizeX] # bot
                    living += self.board[(i+1) % self.__sizeY][(j+1) % self.__sizeX] # bot right
                elif (i == 0) or (i == self.__sizeY - 1):
                    if i == 0:
                        if j == 0:
                            living += self.board[(i) % self.__sizeY][(j+1) % self.__sizeX] # right
                            living += self.board[(i+1) % self.__sizeY][(j) % self.__sizeX] # bot
                            living += self.board[(i+1) % self.__sizeY][(j+1) % self.__sizeX] # bot right
                        elif j == self.__sizeX - 1:
                            living += self.board[(i) % self.__sizeY][(j-1) % self.__sizeX] # left
                            living += self.board[(i+1) % self.__sizeY][(j-1) % self.__sizeX] #  bot left
                            living += self.board[(i+1) % self.__sizeY][(j) % self.__sizeX] # bot
                        else:
                            living += self.board[(i) % self.__sizeY][(j-1) % self.__sizeX] # left
                            living += self.board[(i) % self.__sizeY][(j+1) % self.__sizeX] # right
                            living += self.board[(i+1) % self.__sizeY][(j-1) % self.__sizeX] #  bot left
                            living += self.board[(i+1) % self.__sizeY][(j) % self.__sizeX] # bot
                            living += self.board[(i+1) % self.__sizeY][(j+1) % self.__sizeX] # bot right

                    elif i == self.__sizeY - 1:
                        if j == 0:
                            living += self.board[(i-1) % self.__sizeY][(j) % self.__sizeX] # top
                            living += self.board[(i-1) % self.__sizeY][(j+1) % self.__sizeX] # top right
                            living += self.board[(i) % self.__sizeY][(j+1) % self.__sizeX] # right
                        elif j == self.__sizeX - 1:
                            living += self.board[(i-1) % self.__sizeY][(j-1) % self.__sizeX] # top left
                            living += self.board[(i-1) % self.__sizeY][(j) % self.__sizeX] # top
                            living += self.board[(i) % self.__sizeY][(j-1) % self.__sizeX] # left
                        else:
                            living += self.board[(i-1) % self.__sizeY][(j-1) % self.__sizeX] # top left
                            living += self.board[(i-1) % self.__sizeY][(j) % self.__sizeX] # top
                            living += self.board[(i-1) % self.__sizeY][(j+1) % self.__sizeX] # top right
                            living += self.board[(i) % self.__sizeY][(j-1) % self.__sizeX] # left
                            living += self.board[(i) % self.__sizeY][(j+1) % self.__sizeX] # right

                elif (j == 0) or (j == self.__sizeX - 1):
                    if j == 0:
                        living += self.board[(i-1) % self.__sizeY][(j) % self.__sizeX] # top
                        living += self.board[(i-1) % self.__sizeY][(j+1) % self.__sizeX] # top right
                        living += self.board[(i) % self.__sizeY][(j+1) % self.__sizeX] # right
                        living += self.board[(i+1) % self.__sizeY][(j) % self.__sizeX] # bot
                        living += self.board[(i+1) % self.__sizeY][(j+1) % self.__sizeX] # bot right
                    elif j == self.__sizeX - 1:
                        living += self.board[(i-1) % self.__sizeY][(j-1) % self.__sizeX] # top left
                        living += self.board[(i-1) % self.__sizeY][(j) % self.__sizeX] # top
                        living += self.board[(i) % self.__sizeY][(j-1) % self.__sizeX] # left
                        living += self.board[(i+1) % self.__sizeY][(j-1) % self.__sizeX] #  bot left
                        living += self.board[(i+1) % self.__sizeY][(j) % self.__sizeX] # bot
            
                # RULES TO GAME OF LIFE
                if (living == 2 or living == 3) and self.board[i][j] == 1:
                    next[i][j] = 1
                    pygame.draw.rect(surface, (255, 255, 255), (j * self.__cell, i * self.__cell, self.__cell - 1, self.__cell - 1))
                elif living == 3 and self.board[i][j] == 0:
                    next[i][j] = 1
                    pygame.draw.rect(surface, (255, 255, 255), (j * self.__cell, i * self.__cell, self.__cell - 1, self.__cell - 1))
                else:
                    next[i][j] = 0

        self.board = next
        return None

    def toroid(self, surface):
        '''
        Toroidal boundary conditions.
        '''
        next = [[0 for i in range(self.__sizeX)] for i in range(self.__sizeY)]
        for i, row in enumerate(self.board):
            for j, col in enumerate(self.board[i]):
                living = 0
                living += self.board[(i-1) % self.__sizeY][(j-1) % self.__sizeX] # top left
                living += self.board[(i-1) % self.__sizeY][(j) % self.__sizeX] # top
                living += self.board[(i-1) % self.__sizeY][(j+1) % self.__sizeX] # top right
                living += self.board[(i) % self.__sizeY][(j-1) % self.__sizeX] # left
                living += self.board[(i) % self.__sizeY][(j+1) % self.__sizeX] # right
                living += self.board[(i+1) % self.__sizeY][(j-1) % self.__sizeX] #  bot left
                living += self.board[(i+1) % self.__sizeY][(j) % self.__sizeX] # bot
                living += self.board[(i+1) % self.__sizeY][(j+1) % self.__sizeX] # bot right

                # RULES TO GAME OF LIFE
                if (living == 2 or living == 3) and self.board[i][j] == 1:
                    next[i][j] = 1
                    pygame.draw.rect(surface, (255, 255, 255), (j * self.__cell, i * self.__cell, self.__cell - 1, self.__cell - 1))
                elif living == 3 and self.board[i][j] == 0:
                    next[i][j] = 1
                    pygame.draw.rect(surface, (255, 255, 255), (j * self.__cell, i * self.__cell, self.__cell - 1, self.__cell - 1))
                else:
                    next[i][j] = 0

        self.board = next
        return None

def main():
    active = False # allows the simulation to proceed]

    parser = argparse.ArgumentParser('Configure the Game of Life')
    parser.add_argument('--size', dest = 'N', nargs = '+', type = int, required = False, help = 'The size of the grid. Enter one integer for a square or two for a rectangle. Default = 100 x 100 cells')
    parser.add_argument('--interval', dest = 'T', type = int, required = False, help = 'Set the clock tick rate for pygame. Default = 30 ticks/sec.')
    parser.add_argument('--closed', action = 'store_true', required = False, help = 'Set the topology to closed, so boundary cells have less than 8 neighbors. Default topology is toroidal.')
    parser.add_argument('--export', action = 'store_true', required = False, help = 'Write the initial setup to an export file called export.txt')
    args = parser.parse_args()

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
    updateInterval = 60 # pygame clock tick rate
    if args.T and args.T > 0:
        updateInterval = args.T
    
    gen = 0

    # take optional arguements from parser to config initial gen
    g = game((Nx, Ny), cellSize)
    g.importFromTxt('acorn', (30, 30))

    # if requested by args
    if args.export:
        g.export()

    # start pygame and draw gen 0
    pygame.init()
    surface = pygame.display.set_mode((cellSize * Nx, cellSize * Ny))
    pygame.display.set_caption(f'Game of Life: Gen = {gen}, Running = {active}')
    clock = pygame.time.Clock()
    g.forceDraw(surface)
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
                g.finite(surface)
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
                g.toroid(surface)
                pygame.display.update()
                gen += 1

if __name__ == '__main__':
    main()