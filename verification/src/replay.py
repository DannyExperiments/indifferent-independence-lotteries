"""Finite positive-mass coupling and convex-class diagnostics on a rational grid."""

from collections import Counter, defaultdict
from itertools import combinations_with_replacement, product


# Four equally weighted tickets. Coordinates are represented in units of 1/4.
POINTS = tuple(product((-4, 0, 4), repeat=2))


def dominates(x, y):
    return x[0] >= y[0] and x[1] >= y[1]


def mean(lottery):
    assert all(sum(p[i] for p in lottery) % 4 == 0 for i in range(2))
    return tuple(sum(p[i] for p in lottery) // 4 for i in range(2))


def good(lottery):
    return all(dominates(x, y) or dominates(y, x) for x in lottery for y in lottery)


def coupling(f, g):
    # On equal-weight tickets, a dominating coupling exists iff the allowed
    # bipartite matching is perfect. The subset DP tests that matching exactly.
    masks = [sum(1 << j for j, y in enumerate(g) if dominates(x, y)) for x in f]
    achievable = {0}
    for allowed in masks:
        achievable = {seen | (1 << j) for seen in achievable for j in range(4)
                      if allowed & (1 << j) and not seen & (1 << j)}
    return 15 in achievable


def mixture(f, g, n):
    weights = Counter()
    for point in f:
        weights[point] += n
    for point in g:
        weights[point] += 4 - n
    if any(w % 4 for w in weights.values()):
        return None
    return tuple(sorted(p for p, w in weights.items() for _ in range(w // 4)))


def finite_census():
    base = list(combinations_with_replacement(POINTS, 4))
    all_lotteries = sorted(set(base) | {4 * (mean(f),) for f in base})
    ids = {f: j for j, f in enumerate(all_lotteries)}
    classes = defaultdict(set)
    for f in all_lotteries:
        if good(f):
            classes[mean(f)].add(f)
    # Restrict the convex generation moves to the finite listed family.
    added = 0
    for group in classes.values():
        while True:
            candidate = {mixed for f, g in product(group, repeat=2) for n in (1, 2, 3)
                         if (mixed := mixture(f, g, n)) in ids}
            fresh = candidate - group
            if not fresh:
                break
            group.update(fresh)
            added += len(fresh)
    count = len(all_lotteries)
    reach = [1 << i for i in range(count)]
    for group in classes.values():
        group_mask = sum(1 << ids[f] for f in group)
        for f in group:
            reach[ids[f]] |= group_mask
    means = list(map(mean, all_lotteries))
    couplings = 0
    for i, g in enumerate(all_lotteries):
        for j, f in enumerate(all_lotteries):
            if not dominates(means[j], means[i]) or i == j:
                continue
            if coupling(f, g):
                reach[i] |= 1 << j
                assert means[i] != means[j]
                couplings += 1
    for j in range(count):
        marker = 1 << j
        for i in range(count):
            if reach[i] & marker:
                reach[i] |= reach[j]
    strict = 0
    for i, g in enumerate(all_lotteries):
        for j, f in enumerate(all_lotteries):
            if not reach[i] & (1 << j):
                continue
            assert dominates(means[j], means[i])
            if reach[j] & (1 << i):
                assert i == j or f in classes[means[i]] and g in classes[means[i]]
                assert means[i] == means[j]
            else:
                strict += 1
                assert any(x != y and dominates(x, y) for x in f for y in g)

    h = ((-4, 0),) * 2 + ((4, 0),) * 2
    v = ((0, -4),) * 2 + ((0, 4),) * 2
    c = ((0, 0),) * 4
    cross = mixture(h, v, 2)
    diagonal = ((-4, 4),) * 2 + ((4, -4),) * 2
    assert cross in classes[(0, 0)] and not good(cross)
    assert reach[ids[c]] & (1 << ids[cross]) and reach[ids[cross]] & (1 << ids[c])
    assert not reach[ids[c]] & (1 << ids[diagonal]) and not reach[ids[diagonal]] & (1 << ids[c])
    print(f"{count} lotteries; convex additions: {added}; strict coupling moves: {couplings}.")
    print(f"All {strict} represented strict comparisons have a support witness.")
    print("Cross-shaped mixture is indifferent to the zero Dirac; antidiagonal lottery is incomparable.")


if __name__ == "__main__":
    finite_census()
