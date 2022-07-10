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

def import_txt(name):
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

def getRules(rulestring):
    '''
    Converts the interpreted rle string to a usable array.
    '''
    

def import_rle(name):
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

    config_comp = re.compile(r'x\s?=\s?(\d+).*?y\s?=\s?(\d+).*?B(\d+).*?S(\d+.)')
    config_match = config_comp.search(config)
    config_x = int(config_match.group(1))
    config_y = int(config_match.group(2))
    config_rules = (config_match.group(3), config_match.group(4))
    
    pattern_comp = re.compile(r'(\d*)([bo$!])')
    pattern_match = pattern_comp.findall(pattern)
    pattern_match = [(1, match[1]) if match[0] == '' else (int(match[0]), match[1]) for match in pattern_match]

    print(pattern_match)

    return None