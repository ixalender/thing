from typing import List
from functools import reduce


def _find_widest_field(col_name: str, data: List[dict]) -> int:
    return len(
        str(max(
            data, default=dict(), key=lambda p: len(str(p[col_name]))
        ).get(col_name, ''))
    )


def _reduce_col_sizes(m: dict, p: dict) -> dict:
    m.update(p)
    return m


def print_data(data: List[dict]):
    col_sizes: dict = reduce(
        _reduce_col_sizes,
        map(lambda k: {k: _find_widest_field(k, data)}, data[0].keys()),
        dict()
    )
    print()
    for r in data:
        for c, v in r.items():
            print('{0:{width}}'.format(str(v), width=col_sizes[c] + 1), end=' ')
        print()
    print()
