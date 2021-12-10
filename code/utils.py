"""
Some utilities
"""


def pairwise(items: list) -> list:
    previous = None
    pairs = []
    for current in items:
        pairs.append((previous, current))
        previous = current
    return pairs[1:]  # remove first element as previous is going to be none


def items_as_pairs(items: list) -> list:
    por_pares = pairwise(items)
    # Filtra aquellos items cuyo indice es par
    por_pares_saltando_uno = filter(
        lambda tupla_index_item: tupla_index_item[0] % 2 == 0,
        [(idx, item) for idx, item in enumerate(por_pares)]
    )
    resultado = map(
        lambda tupla_index_item: tupla_index_item[1],
        por_pares_saltando_uno
    )
    return list(resultado)
