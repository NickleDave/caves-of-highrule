import pathlib

PACKAGE_ROOT = pathlib.Path(__file__).parent
ASSETS_ROOT = PACKAGE_ROOT / 'assets'
GRAPHICS_ROOT = ASSETS_ROOT / 'graphics'
MAP_ROOT = ASSETS_ROOT / 'map'

WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
