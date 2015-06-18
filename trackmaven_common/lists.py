def split_every(l, size):
    """
    Splits a list, into a subsut of lists that are seperated every X element.

    Example:

    >>> l = [1, 2, 3, 4]
    >>> split_every(1, 2)
    [[1, 2], [3, 4]]
    """
    return [l[i:i + size] for i in range(0, len(l), size)]


def uniquify(l):
    """
    For a list of dictionaries, removes all duplicate dict, and returns the
    resulting list.

    Example:

    >>> l = [{"foo": "bar}, {"foo": "bar"}]
    >>> uniquify(l)
    [{"foo": "bar"}]
    """
    seen = {}
    unique = []
    for i in l:
        keys = [str(k) for k in i.keys()]
        values = [str(v) for v in i.values()]
        marker = "k_".join(keys) + "v_".join(values)
        if marker in seen:
            continue
        seen[marker] = 1
        unique.append(i)
    return unique


def get_index(x, index, default=None):
    """
    Get the element at the index of the list or return None

    Example:

    >>> example = [1, 2]
    >>> get_index(example, 1)
    2
    >>> get_index(example, 7)
    None
    """
    if len(x) > index:
        return x[index]
    else:
        return default

