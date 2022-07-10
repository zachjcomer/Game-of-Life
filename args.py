import argparse

def new():
    argparser = argparse.ArgumentParser('Configure the Game of Life')
    argparser.add_argument('--size', dest = 'N', nargs = '+', type = int, required = False, help = 'The size of the grid. Enter one integer for a square or two for a rectangle. Default = 100 x 100 cells')
    argparser.add_argument('--interval', dest = 'T', type = int, required = False, help = 'Set the clock tick rate for pygame. Default = 30 ticks/sec.')
    argparser.add_argument('--wrap', action = 'store_true', required = False, help = 'Set the topology to closed, so boundary cells have less than 8 neighbors. Default topology is toroidal.')
    argparser.add_argument('--export', action = 'store_true', required = False, help = 'Write the initial setup to an export file called export.txt')
    return argparser.parse_args()