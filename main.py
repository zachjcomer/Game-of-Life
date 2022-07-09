'''
FIXME:  gen() ruleset interpreter

        rulestring interpreter

        .txt importer

TODO:   .rle importer

        infinite plane conditions
        arbitrary wall boundaries

        import rotations, reflections

        set canvas size from import bounds

        * cells only need to be updated if they or their neighbors change state *

        arbitrary lattice configurations
        von-neumann neighborhoods, etc

'''
import parser
import board
import argparse
import pygame

def main():
    active = False # allows the simulation to proceed]

    argparser = argparse.ArgumentParser('Configure the Game of Life')
    argparser.add_argument('--size', dest = 'N', nargs = '+', type = int, required = False, help = 'The size of the grid. Enter one integer for a square or two for a rectangle. Default = 100 x 100 cells')
    argparser.add_argument('--interval', dest = 'T', type = int, required = False, help = 'Set the clock tick rate for pygame. Default = 30 ticks/sec.')
    argparser.add_argument('--closed', action = 'store_true', required = False, help = 'Set the topology to closed, so boundary cells have less than 8 neighbors. Default topology is toroidal.')
    argparser.add_argument('--export', action = 'store_true', required = False, help = 'Write the initial setup to an export file called export.txt')
    args = argparser.parse_args()

    # configure cellular automaton rules
    rulestring = 'B3/S23'
    birth = (3, 6, 7, 8)
    survival = (3, 4, 6, 7, 8)

    # configure the grid and cell sizes
    SCREEN = 800 # max screen size
    Nx = 200 # number of horizontal cells
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
    g = board.game((Nx, Ny), cellSize)
    g.initToroid()
    g.rand()
    g.addToBoard(parser.import_txt('gosper'), (80, 80))

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