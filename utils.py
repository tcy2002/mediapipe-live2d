from math import hypot, pow, acos


def sum_p(args):
    ans = [0, 0]
    for p in args:
        ans[0] += p[0]
        ans[1] += p[1]
    return ans


def avg_p(args):
    size = len(args)
    avg = sum_p(args)
    return [avg[0] / size, avg[1] / size]


def dist_p(p1, p2):
    return hypot(p1[0] - p2[0], p1[1] - p2[1])


def square(n1):
    return pow(n1, 2)


def angle(opposite, adjacent1, adjacent2):
    res = (square(adjacent1) + square(adjacent2) - square(opposite)) / \
          (2 * adjacent1 * adjacent2)
    return acos(res)
