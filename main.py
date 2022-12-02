'''
FIXME:  gen() ruleset interpreter

        rulestring interpreter

TODO:   dynamic size and ruleset interpretation from imports

        infinite plane conditions
        arbitrary wall boundaries

        import rotations, reflections

        set canvas size from import bounds

        * cells only need to be updated if they or their neighbors change state *

        arbitrary lattice configurations
        von-neumann neighborhoods, etc

'''

import board

import pygame
import args
import numpy as np

def main():
    # CA parameters
    rulestring = 'B3/S23' # Life B3/S23 Day and Night B3678/S34678
    cellsX = 200
    cellsY = 200
    boardWrapped = True

    # pygame parameters
    updateInterval = 144 # pygame clock tick rate
    screenSize = 1200 # square pixels

    cellSize = screenSize / max(cellsX, cellsY)

    g = board.game((cellsX, cellsY), cellSize, rulestring)
    g.init(wrap = boardWrapped)

    # MANUALLY IMPORT CA PATTERNS HERE
    # g.density(0)
    g.rand()
    # g.addToBoard(parser.parseRLE('gosper'), (40, 40))
    # g.addToBoard(parser.parseRLE('newgun2'), (150, 150))

    # if requested by args
    """ if newArgs.export:
        g.export(fileType = 'txt') """

    gen = 0
    active = False # allows the simulation to proceed

    # start pygame and draw gen 0
    pygame.init()
    surface = pygame.display.set_mode((cellSize * cellsX, cellSize * cellsY))
    pygame.display.set_caption(f'Game of Life: Gen = {gen}, Running = {active}')
    clock = pygame.time.Clock()
    g.draw(surface) # initial board configuration
    pygame.display.update() # draw the initial config

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
            # surface.fill((0, 0, 0))
            g.gen(surface)
            pygame.display.update()
            gen += 1
    return None

if __name__ == '__main__':
    main()