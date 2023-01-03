import pathlib


def load_blocking_txt(blocking_txt_path):
    """Load the blocking map from a .txt file"""
    blocking_txt_path = pathlib.Path(blocking_txt_path)
    with blocking_txt_path.open('r') as fp:
        lines = fp.read().splitlines()
    return lines


def load_overworld_tile_txt(overworld_tile_txt_path):
    """Load the overworld tile map from a .txt file"""
    overworld_tile_txt_path = pathlib.Path(overworld_tile_txt_path)
    with overworld_tile_txt_path.open('r') as fp:
        lines = fp.read().splitlines()
    # below, [:1] to remove empty space that we get at index 0 because lines start with spaces.
    lines = [row.split(' ')[1:] for row in lines]
    return lines
