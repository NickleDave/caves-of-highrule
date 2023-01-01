import random

import pygame

from . import (
    csv,
    folder,
    settings,
    weapon,
)
from .player import Player
from .tile import Tile


class YSortCameraGroup(pygame.sprite.Group):
    """Camera that centers player on screen
    by drawing other sprites offset from its position.

    Also sorts sprites by y-coordinate
    so sprites higher on the screen are "behind"
    sprites lower on screen.
    """
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load(
            settings.GRAPHICS_ROOT / 'tilemap/ground.png'
        ).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.weapon_sprite = None

        self.create_map()

    def create_map(self):
        style_layout_map = {
            'boundary': csv.import_csv_layout(settings.MAP_ROOT / 'map_FloorBlocks.csv'),
            'grass': csv.import_csv_layout(settings.MAP_ROOT / 'map_Grass.csv'),
            'object': csv.import_csv_layout(settings.MAP_ROOT / 'map_LargeObjects.csv'),
        }
        graphics_surfaces_map = {
            'grass': folder.img_folder_to_surfaces(settings.GRAPHICS_ROOT / 'grass'),
            'objects': folder.img_folder_to_surfaces(settings.GRAPHICS_ROOT / 'objects')
        }
        for style, layout in style_layout_map.items():
            for row_index, row in enumerate(layout):
                for col_index, col_char in enumerate(row):
                    if col_char != '-1':
                        x = col_index * settings.TILESIZE
                        y = row_index * settings.TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites,], 'invisible')
                        elif style == 'grass':
                            random_grass_image = random.choice(graphics_surfaces_map['grass'])
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites,],
                                'grass',
                                random_grass_image
                            )
                        elif style == 'object':
                            object_image = graphics_surfaces_map['objects'][int(col_char)]
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites,],
                                'object',
                                object_image
                            )
        self.player = Player(
                        (2000, 1430),
                        [self.visible_sprites],
                        self.obstacle_sprites,
                        self.create_weapon,
                        self.destroy_weapon
                    )

    def create_weapon(self):
        self.weapon_sprite = weapon.Weapon(self.player, [self.visible_sprites])

    def destroy_weapon(self):
        if self.weapon_sprite:
            self.weapon_sprite.kill()
            self.weapon_sprite = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
