'''
Methods to import from .txt and .rle formats.
'''
import re
from os.path import exists

import requests

def read(name):
    '''Get a string from a file (.txt or .rle)'''
    try:
        file = open(name)
    except FileNotFoundError:
        print(f'Unable to import {name}, ignoring.')
        return None
    else: 
        return [line.strip() for line in file.readlines()]

def get_rules(rulestring):
    '''Converts a rulestring of the form B/S to usable values.'''

    rules = re.compile(r'[bB](\d*)/[sS](\d*)').search(rulestring)
    if rules:
        return([int(c) for c in rules.group(1)], [int(c) for c in rules.group(2)])
    else:
        return None

def parse_txt(name):
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

def parse_rle(name, rows):

    rule_pattern = re.compile(r'x\s?=\s?(\d+).*?y\s?=\s?(\d+).*?([bB]\d+.*?[sS]\d+.)')

    config = rows[0]
    config = rule_pattern.search(config)

    size = (int(config.group(1)), int(config.group(2)))
    rulestring = config.group(3)

    pattern = ''.join(rows[1:]).strip('\r\n')
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

# Sends a GET request to https://conwaylife.com/patterns/{name}.rle or https://copy.sh/life/examples/{name}.rle
# If conwaylife.com fails to respond, try copy.sh.
def get_rle_from_web(name):
    print(f'Trying https://conwaylife.com/patterns/{name}.rle...')
    page = requests.get(f'https://conwaylife.com/patterns/{name}.rle')
    if not page.status_code == 200:
        if page.status_code == 404:
            print(f'Error 404: unable to find {name}.rle at https://conwaylife.com/patterns/')
        else:
            print(f'Error {page.status_code}: unable to connect to https://conwaylife.com/patterns/{name}.rle')
    else:
        print(f'Success: importing {name}.rle to board.')
        rows = clean_rle_from_web(page)
        rows = [row for row in rows if (row != '' and row[0] != '#')]

        return parse_rle(name, rows)

    print(f'Trying https://copy.sh/life/examples/{name}.rle instead...')
    page = requests.get(f'https://copy.sh/life/examples/{name}.rle')
    if not page.status_code == 200:
        if page.status_code == 404:
            print(f'Error 404: unable to find {name}.rle at https://copy.sh/life/examples/')
        else:
            print(f'Error {page.status_code}: unable to connect to https://copy.sh/life/examples/{name}.rle')
    else:
        print(f'Success: importing {name}.rle to board.')
        rows = clean_rle_from_web(page)
        rows = [row for row in rows if (row != '' and row[0] != '#')]

        return parse_rle(name, rows)

'''
Import from a .rle file.

Format: standard life .rle formatting.
https://conwaylife.com/wiki/Run_Length_Encoded
'''
def get_rle_from_file(name):
    rows = read(f'patterns\{name}.rle')
    if not rows:
        return None

    rows = [row for row in rows if row[0] != '#']

    return parse_rle(name, rows)

# Clean the page text from conwaylife.com and return rows with comments removed.
def clean_rle_from_web(page):
    page_string = [row.decode("utf-8") for row in page]
    page_string_merged = ''.join(page_string)
    page_carriage = page_string_merged.split('\r\n')

    rows = [row for row in page_carriage if (row != '' and row[0] != '#')]

    return rows

def exportTXT(pattern, name = 'export'):
    '''
    Writes the input pattern (a 2D array of binary values) to a .txt file.
    '''
    file = open(f'patterns\{name}.txt', 'w')
    file.write(str(pattern).replace(', ', '').replace('[', '').replace(']', '\n').replace('\n\n\n', ''))
    file.close()