import math
from itertools import combinations

import numpy.random as random


def binomial(N, p):
    if N > 100:
        return random.normal(N * p, (N * p * (1.0 - p)) ** 0.5)
    p_aim = random.uniform()
    p_r = (1 - p) ** N
    r = 0
    while p_aim > p_r:
        p_aim -= p_r
        r += 1
        p_r *= (((N - r + 1) * p) / (r * (1 - p)))
    return r


def get_binomial_sample(N, p, size):
    return [binomial(N, p) for _ in range(size)]


def probability(p, n, k):
    return math.pow(p, k) * math.pow(1 - p, n - k) * len(list(combinations(range(1, n + 1), k)))


def count_between(arr, left, right):
    count = 0
    for i in arr:
        if left <= i < right:
            count += 1
    return count


def main():
    binomial_p = 0.3
    N = 20
    F = [0 for _ in range(N + 1)]
    temp_sum = 0
    for i in range(N + 1):
        temp_sum += probability(binomial_p, N, i)
        F[i] = temp_sum

    n = 50
    binomial_sample = get_binomial_sample(N, binomial_p, n)

    chi_square = 0
    n_start = count_between(binomial_sample, 0, 3)
    chi_square += (((n_start - n * F[2]) ** 2) / (n * F[2]))
    n_end = count_between(binomial_sample, 10, N + 1)
    chi_square += (((n_end - n * (1 - F[9])) ** 2) / (n * (1 - F[9])))
    for i in range(3, 9):
        n_i = count_between(binomial_sample, i, i + 1)
        chi_square += (((n_i - n * (F[i] - F[i - 1])) ** 2) / (n * (F[i] - F[i - 1])))
    print(chi_square)


if __name__ == '__main__':
    main()
