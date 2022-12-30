import sys

import pygame

from . import (
    settings
)
from .debug import debug
from .level import Level
from .parser import get_parser


class Game:
    """Class that represent ``highrule`` game"""
    def __init__(self, debug=False):

        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption('Caves of High Rule')
        self.clock = pygame.time.Clock()
        self.level = Level()

        self.debug = debug

    def run(self):
        """Method that runs entire game"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()

            if self.debug:
                debug('write debug info here.')

            pygame.display.update()
            self.clock.tick(settings.FPS)


def main(debug=False):
    """Main function, used as entry point when highrule is run from the command line"""
    game = Game(debug=debug)
    game.run()


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(debug=args.debug)
