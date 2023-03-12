import json
import pathlib


def load_tilemap_from_aseprite_json(ase_path, layer=1, cel=0):
    """Load a tilemap from a json file
    exported from aseprite.

    The json file must be exported by the lua script here:
    https://github.com/dacap/export-aseprite-file
    using the cli
    https://www.aseprite.org/docs/cli/

    Default is to load from layer 1, cel 0.
    """
    with pathlib.Path(ase_path).open('r') as fp:
        ase_json = json.load(fp)

    tilemap = ase_json["layers"][layer]["cels"][cel]['tilemap']
    tiles = tilemap['tiles']
    w = tilemap['width']
    h = tilemap['height']

    tiles = [tiles[i * w:i * w + w] for i in range(h)]  # list of lists, h list each of len w

    assert len(tiles) == h
    assert all([len(el) == w for el in tiles])

    return tiles
