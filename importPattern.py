'''
Methods to import from .txt and .rle formats.
'''

from os.path import exists

def import_txt(name):
    '''
    Import from a .txt file.

    Format: string of 0, 1 with $ as a newline char. E.g., a glider is:
    010$
    001$
    111$
    '''
    if exists(f'configs\{name}.txt'):
        file = open(f'configs\{name}.txt').read()
    else:
        return False

    r = file.count('$')
    pattern = file.replace('$', '').replace('\n', '')
    c = len(pattern) // r
    board = [[0 for i in range(c)] for i in range(r)]
    for i in range(r):
        for j in range(c):
            board[i][j] = int(pattern[j + c * i])
        

    return None

def import_rle():
    '''
    Import from a .rle file.

    Format: standard life .rle formatting.
    https://conwaylife.com/wiki/Run_Length_Encoded
    '''

    return None