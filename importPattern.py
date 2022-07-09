'''
Methods to import from .txt and .rle formats.
'''

import re
from os.path import exists

def import_txt(name):
    '''
    Import from a .txt file. Returns an array of binary values of the same size as the .txt file grid.

    Format: string of 0, 1 with $ as a newline char. E.g., a glider is:
    010$
    001$
    111$
    '''
    if exists(f'patterns\{name}.txt'):
        file = open(f'patterns\{name}.txt').read()
    else:
        return False

    r = file.count('$')
    pattern = file.replace('$', '').replace('\n', '')
    c = len(pattern) // r
    board = [[0 for i in range(c)] for i in range(r)]
    for i in range(r):
        for j in range(c):
            board[i][j] = int(pattern[j + c * i])
        

    return board

def import_rle(name):
    '''
    Import from a .rle file.

    Format: standard life .rle formatting.
    https://conwaylife.com/wiki/Run_Length_Encoded
    '''
    if exists(f'patterns\{name}.rle'):
        file = open(f'patterns\{name}.rle').read()
    else:
        return False


    return None