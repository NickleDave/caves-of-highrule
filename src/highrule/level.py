import pygame

from . import settings
from .player import Player
from .tile import Tile


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(settings.WORLD_MAP):
            for col_index, col_char in enumerate(row):
                x = col_index * settings.TILESIZE
                y = row_index * settings.TILESIZE
                if col_char == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col_char == 'p':
                    Player((x, y), [self.visible_sprites])

    def run(self):
        self.visible_sprites.draw(
            self.display_surface
        )
