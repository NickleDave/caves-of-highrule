from os import walk
import pathlib

import pygame


def img_folder_to_surfaces(folder_path):
    surface_list = []

    for _, _, img_files in walk(folder_path):
        img_files = sorted(img_files)
        for img_file in img_files:
            img_path = pathlib.Path(folder_path) / img_file
            img_surface = pygame.image.load(img_path).convert_alpha()
            surface_list.append(img_surface)

    return surface_list
