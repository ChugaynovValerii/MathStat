import random


def generate(n, m):
    return [int(random.random() * m) for _ in range(n)]


def calculate_lens(arr, alpha, beta, max_len):
    acc = 0
    lens = [0 for _ in range(max_len)]
    for x in arr:
        if alpha <= x <= beta:
            acc += 1
        elif acc != 0:
            lens[min(acc - 1, max_len - 1)] += 1
            acc = 0
    return lens


def calculate_statistic(lens, alpha, beta, m):
    nu = sum(lens)
    acc = 0
    temp1 = (beta - alpha) / (2 ** m)
    for i in range(len(lens)):
        temp2 = nu * temp1 * ((1 - temp1) ** i)
        acc += ((lens[i] - temp2) ** 2) / temp2
    return acc


def main():
    n = 10000
    m = 8
    x = generate(n, 2 ** m)
    alpha = 0
    beta = 2 ** (m - 1) - 1
    max_len = 15
    lens = calculate_lens(x, alpha, beta, max_len)
    print(calculate_statistic(lens, alpha, beta, m))


if __name__ == '__main__':
    main()
