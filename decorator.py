import pygame

import game
import importer

patterns = dict()

def get_pattern(name):
    '''
    Attempts to find pattern {name}.
    Priority:
        1. self.patterns
        2. /patterns/
        3. web scraper
    '''
    if not patterns.get(name):
        if importer.file_exists_in_dir(name):
            patterns[name] = importer.get_from_file(name)
        elif importer.file_exists_on_web(name):
            patterns[name] = importer.get_from_web(name)
            
    return patterns.get(name)

def place_pattern(name, pos):
    pattern = get_pattern(name)
    if pattern:
        game.game.game_singleton.add_to_board(pattern, pos)

def fill_with_noise():
    game.game.game_singleton.rand()

def fill_with_noise(noise_density):
    game.game.game_singleton.density(noise_density)
