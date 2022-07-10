'''
Methods to import from .txt and .rle formats.
'''
import re
from os.path import exists

def read(name):
    try:
        file = open(name)
    except FileNotFoundError:
        print(f'Unable to import {name}, ignoring.')
        return None
    else: 
        return [line.strip() for line in file.readlines()]

def getRules(rulestring):
    '''
    Converts a rulestring of the form B/S to usable values.
    '''
    rules = re.compile(r'B(\d*)/S(\d*)').search(rulestring)
    if rules:
        return([int(c) for c in rules.group(1)], [int(c) for c in rules.group(2)])
    else:
        return None

def parseTXT(name):
    '''
    Import from a .txt file.

    Format: string of 0, 1. E.g., a glider is:
    010
    001
    111
    '''
    rows = read(f'patterns\{name}.txt')        
    if rows:
        return [[1 if cell == '1' else 0 for cell in line] for line in rows]
    return None

def parseRLE(name):
    '''
    Import from a .rle file.

    Format: standard life .rle formatting.
    https://conwaylife.com/wiki/Run_Length_Encoded
    '''
    rows = read(f'patterns\{name}.rle')
    if not rows:
        return None

    rows = [row for row in rows if row[0] != '#']

    config = rows[0]
    pattern = ''.join(rows[1:]).strip('\n')

    config = re.compile(r'x\s?=\s?(\d+).*?y\s?=\s?(\d+).*?(B\d+.*?S\d+.)').search(config)
    size = (int(config.group(1)), int(config.group(2)))
    rulestring = config.group(3)
    
    pattern = re.compile(r'(\d*)([bo$!])').findall(pattern)
    pattern = [(1, match[1]) if match[0] == '' else (int(match[0]), match[1]) for match in pattern]

    board = [[0 for i in range(size[0])] for j in range(size[1])]
    row = 0
    col = 0

    for pair in pattern:
        for i in range(pair[0]):
            if pair[1] == 'b':
                board[row][col] = 0
                col += 1
            elif pair[1] == 'o':
                board[row][col] = 1
                col += 1
            elif pair[1] == '$':
                row += 1
                col = 0

    return (board, name, rulestring)

def exportTXT(pattern, name = 'export'):
    '''
    Writes the input pattern (a 2D array of binary values) to a .txt file.
    '''
    file = open(f'patterns\{name}.txt', 'w')
    file.write(str(pattern).replace(', ', '').replace('[', '').replace(']', '\n').replace('\n\n\n', ''))
    file.close()