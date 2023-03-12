from __future__ import annotations

import pygame


class SpriteSheet:

    def __init__(self, filename: str, sprite_size: int = 32):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
            self.sheet_width, self.sheet_height = self.sheet.get_size()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)
        self.sprite_size = sprite_size
        if not self.sheet_width % self.sprite_size == 0:
            raise ValueError(
                'sprite size does not divide evenly into sheet size width'
            )
        if not self.sheet_height % self.sprite_size == 0:
            raise ValueError(
                'sprite size does not divide evenly into sheet size height'
            )
        self.n_row = self.sheet_height / self.sprite_size
        self.n_col = self.sheet_width / self.sprite_size

    def image_at(self, rectangle: tuple[int, int, int, int], colorkey = None):
        """Load sprite from sheet, located at rectangle (x, y, x offset, y offset)."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
    
    def load(self):
        """Load all images using"""
        sprites = []
        for row in range(self.n_row):
            for col in range(self.n_col):
                sprites.append(
                    self.image_at(
                        (row * self.sprite_size, col * self.sprite_size, self.sprite_size, self.sprite_size)
                    )
                )
        return sprites