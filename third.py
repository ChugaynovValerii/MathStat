import math

import matplotlib.pyplot as plt
import numpy.random as random


# uniform
def uniform(r_low, r_up):
    return (r_up - r_low + 1) * random.uniform() + r_low


# normal
def normal1(m, sigma, N):
    s = sum([random.uniform() for _ in range(N)])
    return m + sigma * (s - 0.5 * N) * 6 / (math.sqrt(3 * N))


def normal2():
    return math.sqrt(-2 * math.log(random.uniform())) * math.cos(2 * math.pi * random.uniform())


# exponential
def exponential(beta):
    return -beta * math.log(random.uniform())


# chi_square
def chi_square(N):
    return sum([normal2() ** 2 for _ in range(N)])


# student
def student(N):
    return normal2() / math.sqrt(chi_square(N) / N)

import pandas as pd
def draw_graphs(sample, title, args, bins, r):
    plt.hist(sample, density=True, bins=bins, range=r)
    s = pd.Series(sample)
    s.plot.kde()
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Эмпирическая функция плотности\n({} {})'.format(title, args))
    plt.savefig('res3/Функция плотности ({}).png'.format(title))
    plt.close()

    delta = (r[1] - r[0]) / bins
    n = len(sample)
    weights = [0 for _ in range(bins)]
    for i in range(n):
        weights[int((sample[i] - r[0]) / delta)] += 1
    for i in range(1, bins):
        weights[i] += weights[i - 1]
    x = [r[0] + delta * i for i in range(bins + 1)]
    weights = [0] + weights
    plt.plot(x, [y / n for y in weights])
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.title('Эмпирическая функция распределения\n({} {})'.format(title, args))
    plt.savefig('res3/Функция распределения ({}).png'.format(title))
    plt.close()


def collect_stat(sample, m_t, d_t):
    n = len(sample)
    m_e = sum(sample) / n
    d_e = sum([(sample[i] - m_e) ** 2 for i in range(n)]) / n
    print('{:5d}\t{:8.5f}\t{:8.5f}\t{:8.5f}\t{:8.5f}\t{:8.5f}\t{:8.5f}'
          .format(n, m_t, m_e, m_t - m_e, d_t, d_e, d_t - d_e))


def main():
    n = 10000
    print('\tn\t\tM_T\t\t\tM_E\t\t Откл. M\t\tD_T\t\t\tD_E\t\t Откл. D')

    a = 1
    b = 100
    uniform_sample = [uniform(a, b) for _ in range(n)]
    collect_stat(uniform_sample, (a + b) / 2, ((b - a + 1) ** 2 - 1) / 12)
    draw_graphs(uniform_sample, 'равномерное распределение', 'a={} b={}'.format(a, b), 10, (a, b + 1))

    m = 0
    sigma = 1
    N_normal = 12

    normal_sample1 = [normal1(m, sigma, N_normal) for _ in range(n)]
    collect_stat(normal_sample1, m, sigma ** 2)
    max_deviation = int(max(m - min(normal_sample1), max(normal_sample1) - m)) + 1
    count_per_half = 4
    draw_graphs(normal_sample1, 'нормальное распределение №1', 'm={} d={}'.format(m, sigma ** 2),
                max_deviation * count_per_half + 1,
                (m - max_deviation - 1 / count_per_half, m + max_deviation + 1 / count_per_half))

    normal_sample2 = [normal2() for _ in range(n)]
    collect_stat(normal_sample2, 0, 1)
    max_deviation = int(max(-min(normal_sample2), max(normal_sample2))) + 1
    draw_graphs(normal_sample2, 'нормальное распределение №2', 'm={} d={}'.format(0, 1),
                max_deviation * count_per_half + 1,
                (-max_deviation - 1 / count_per_half, max_deviation + 1 / count_per_half))

    beta = 1
    exponential_sample = [exponential(beta) for _ in range(n)]
    collect_stat(exponential_sample, 1 / beta, (1 / beta) ** 2)
    draw_graphs(exponential_sample, 'экспоненциальное распределение', 'beta={}'.format(beta),
                count_per_half * (int(max(exponential_sample)) + 1), (0, int(max(exponential_sample)) + 1))

    N_chi_square = 10
    chi_square_sample = [chi_square(N_chi_square) for _ in range(n)]
    collect_stat(chi_square_sample, N_chi_square, 2 * N_chi_square)
    draw_graphs(chi_square_sample, 'распределение хи-квадрат', 'N={}'.format(N_chi_square),
                (int(max(chi_square_sample)) + 1), (0, int(max(chi_square_sample)) + 1))

    student_sample = [student(N_chi_square) for _ in range(n)]
    collect_stat(student_sample, 0, N_chi_square / (N_chi_square - 2))
    max_deviation = int(max(-min(student_sample), max(student_sample))) + 1
    draw_graphs(student_sample, 'распределение Стьюдента', 'N={}'.format(N_chi_square),
                max_deviation * count_per_half + 1,
                (-max_deviation - 1 / count_per_half, max_deviation + 1 / count_per_half))


if __name__ == '__main__':
    main()
