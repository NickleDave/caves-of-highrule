from collections import namedtuple

import pygame

from . import settings


WEAPONS_ROOT = settings.GRAPHICS_ROOT / 'weapons'

WeaponData = namedtuple('WeaponData', ('cooldown', 'damage', 'image_path'))

WEAPON_DATA = {
    'sword': WeaponData(cooldown=100, damage=15, image_path=WEAPONS_ROOT / 'sword/full.png'),
    'lance': WeaponData(cooldown=400, damage=30, image_path=WEAPONS_ROOT / 'lance/full.png'),
    'axe': WeaponData(cooldown=300, damage=20, image_path=WEAPONS_ROOT / 'axe/full.png'),
    'rapie': WeaponData(cooldown=50, damage=8, image_path=WEAPONS_ROOT / 'rapier/full.png'),
    'sai': WeaponData(cooldown=80, damage=10, image_path=WEAPONS_ROOT / 'sai/full.png')
}


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.status.split('_')[0]

        # graphic
        image_path = WEAPONS_ROOT / f'{player.weapon}/{direction}.png'
        self.image = pygame.image.load(image_path).convert_alpha()

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(- 10, 0))
