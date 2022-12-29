import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug', action='store_true'
    )
    return parser
