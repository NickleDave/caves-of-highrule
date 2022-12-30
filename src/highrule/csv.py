from __future__ import annotations
from csv import reader


def import_csv_layout(csv_path) -> list[list]:
    """"""
    with open(csv_path) as fp:
        layout_csv = reader(fp, delimiter=',')
        return [list(row) for row in layout_csv]
