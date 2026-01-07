def scalar_multiply(k, point, mod):
    if point is None:  # Point at infinity
        return None

    curr = point

    for i in range(k - 1):
        curr = add_points(curr, point, mod)
        if curr is None:  # Hit point at infinity
            return None

    return curr


def double_point(g, mod):
    x, y = g

    # Special case: if y = 0
    if y == 0:
        return None  # Point at infinity

    # slope = (3x²) / (2y)
    numerator = (3 * x ** 2) % mod
    denominator = (2 * y) % mod
    inv_mod = find_mod_inv(denominator, mod)
    slope = (numerator * inv_mod) % mod

    x3 = (slope ** 2 - 2 * x) % mod
    y3 = (slope * (x - x3) - y) % mod

    return x3, y3


def add_points(a, b, mod):
    # Handle point at infinity
    if a is None:
        return b
    if b is None:
        return a

    x1, y1 = a
    x2, y2 = b

    # Check if same point
    if x1 == x2 and y1 == y2:
        return double_point(a, mod)

    # Check if inverses
    if x1 == x2 and (y1 + y2) % mod == 0:
        return None

    numerator = (y2 - y1) % mod
    denominator = (x2 - x1) % mod
    inv_mod = find_mod_inv(denominator, mod)
    slope = (numerator * inv_mod) % mod

    x3 = (slope ** 2 - x1 - x2) % mod
    y3 = (slope * (x1 - x3) - y1) % mod

    return x3, y3


def find_mod_inv(denominator, mod):
    for x in range(1, mod):
        if (denominator * x) % mod == 1:
            return x
    return None
