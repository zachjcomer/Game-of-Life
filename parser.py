'''
Methods to import from .txt and .rle formats.
'''
import re
from os.path import exists

def read(name):
    with open(name) as file:
        return [line.strip() for line in file.readlines()]

def import_txt(name):
    '''
    Import from a .txt file.

    Format: string of 0, 1. E.g., a glider is:
    010
    001
    111
    '''
    rows = read(f'patterns\{name}.txt')        

    return [[1 if cell == '1' else 0 for cell in line] for line in rows]

def import_rle(name):
    '''
    Import from a .rle file.

    Format: standard life .rle formatting.
    https://conwaylife.com/wiki/Run_Length_Encoded
    '''
    rows = read(f'patterns\{name}.rle')
    rows = [row for row in rows if row[0] != '#']

    print(rows)

    return None