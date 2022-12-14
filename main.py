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
import importer
import board
import pygame

def main():
    # CA parameters
    rulestring = 'b3/S23' # Life B3/S23 Day and Night B3678/S34678
    cells_x = 200
    cells_y = 200
    board_wrapped = True

    # pygame parameters
    update_interval = 60 # pygame clock tick rate
    screen_size = 800 # square pixels

    cell_size = screen_size / max(cells_x, cells_y)

    g = board.game((cells_x, cells_y), cell_size, rulestring)
    g.init(wrap = board_wrapped)

    # MANUALLY IMPORT CA PATTERNS HERE
    g.density(0)
    # g.rand()
    # g.add_to_board(importer.get_rle_from_file('gosper'), (40, 40))
    
    g.add_to_board(importer.get_rle_from_web('germ'), (100, 100))
    # g.add_to_board(importer.get_rle_from_file('1234_synth'), (50, 50))
    # g.add_to_board(importer.get_rle_from_file('newgun2'), (150, 150))

    # if requested by args
    """ if newArgs.export:
        g.export(fileType = 'txt') """
    
    gen = 0
    active = False # allows the simulation to proceed

    # start pygame and draw gen 0
    pygame.init()
    surface = pygame.display.set_mode((cell_size * cells_x, cell_size * cells_y))
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
            clock.tick(update_interval)
            # surface.fill((0, 0, 0))
            g.gen(surface)
            pygame.display.update()
            gen += 1
    return None

if __name__ == '__main__':
    main()