from typing import List
from functools import reduce


def _find_widest_field(col_name: str, data: List[dict]) -> int:
    m: dict = max(data, default=dict(), key=lambda p: len(str(p[col_name])))
    return len(str(m.get(col_name)))


def _reduce_col_sizes(m: dict, p: dict) -> dict:
    m.update(p)
    return m


def print_table(data: List[dict]) -> None:
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


def print_object(data: dict) -> None:
    print_table(list(map(lambda it: dict(label=it[0], value=it[1]), data.items())))

