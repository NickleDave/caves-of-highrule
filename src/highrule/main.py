import sys

import pygame

from . import (
    settings
)
from .debug import debug
from .level import Level


class Game:
    """Class that represent ``highrule`` game"""
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption('Caves of High Rule')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        """Method that runs entire game"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()

            pygame.display.update()
            self.clock.tick(settings.FPS)


def main():
    """Main function, used as entry point when highrule is run from the command line"""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
