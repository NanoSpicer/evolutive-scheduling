"""
Some utilities
"""
def windowed(items: list, window_size: int)-> list:
    n_items = len(items)
    start = 0
    final_index = start + window_size
    result = []

    while final_index <= n_items:
        sublista = items[start:final_index]
        result.append(sublista)
        start += 1
        final_index = start + window_size

    return result

def all_items_are_same(items: list) -> bool:
    if len(items) == 0 or len(items) == 1:
        return True
    primero = items[0]
    for item in items:
        if item != primero:
            return False

    return True


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
