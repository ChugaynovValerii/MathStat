import math

import matplotlib.pyplot as plt
import numpy.random as random


# uniform
def uniform(r_low, r_up):
    return int((r_up - r_low + 1) * random.uniform()) + r_low


def get_uniform_sample(r_low, r_up, size):
    return [uniform(r_low, r_up) for _ in range(size)]


# binomial
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


# geometric
def geometric1(p):
    p_aim = random.uniform()
    p_r = p
    r = 0
    while p_aim > p_r:
        p_aim -= p_r
        r += 1
        p_r *= (1 - p)
    return r


def get_geometric1_sample(p, size):
    return [geometric1(p) for _ in range(size)]


def geometric2(p):
    r = 0
    while random.uniform() > p:
        r += 1
    return r


def get_geometric2_sample(p, size):
    return [geometric2(p) for _ in range(size)]


def geometric3(p):
    return int(math.log(random.uniform()) / math.log(1 - p))


def get_geometric3_sample(p, size):
    return [geometric3(p) for _ in range(size)]


# poisson
def poisson1(mu):
    p_aim = random.uniform()
    p_r = math.exp(-mu)
    r = 0
    while p_aim > p_r:
        p_aim -= p_r
        r += 1
        p_r *= (mu / r)
    return r


def get_poisson1_sample(mu, size):
    return [poisson1(mu) for _ in range(size)]


def poisson2(mu):
    exp = math.exp(-mu)
    prod = random.uniform()
    r = 0
    while prod >= exp:
        prod *= random.uniform()
        r += 1
    return r


def get_poisson2_sample(mu, size):
    return [poisson2(mu) for _ in range(size)]


def get_poisson3_sample(mu, size):
    return [int(random.normal(mu, mu ** 0.5)) for _ in range(size)]


# logarithmic
def logarithmic(p):
    p_aim = random.uniform()
    q = 1 - p
    p_r = -q / math.log(p)
    r = 1
    while p_aim > p_r:
        p_aim -= p_r
        r += 1
        p_r *= (q * (r - 1) / r)
    return r


def get_logarithmic_sample(p, size):
    return [logarithmic(p) for _ in range(size)]


def draw_graphs(sample, title, args, bins, r):
    plt.hist(sample, density=True, bins=bins, range=r)
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Эмпирическая функция плотности\n({} {})'.format(title, args))
    plt.savefig('res2/Функция плотности ({}).png'.format(title))
    plt.close()

    delta = (r[1] - r[0]) / bins
    n = len(sample)
    weights = [0 for _ in range(bins)]
    for i in range(n):
        weights[int((sample[i] - r[0]) / delta)] += 1
    for i in range(1, bins):
        weights[i] += weights[i - 1]
    x = [delta * i for i in range(bins + 1)]
    weights = [0] + weights
    plt.plot(x, [y / n for y in weights])
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.title('Эмпирическая функция распределения\n({} {})'.format(title, args))
    plt.savefig('res2/Функция распределения ({}).png'.format(title))
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
    uniform_sample = get_uniform_sample(a, b, n)
    collect_stat(uniform_sample, (a + b) / 2, ((b - a + 1) ** 2 - 1) / 12)
    draw_graphs(uniform_sample, 'равномерное распределение', 'a={} b={}'.format(a, b), 10, (a, b + 1))

    binomial_p = 0.5
    N = 10
    binomial_sample = get_binomial_sample(N, binomial_p, n)
    collect_stat(binomial_sample, N * binomial_p, N * binomial_p * (1 - binomial_p))
    draw_graphs(binomial_sample, 'биномиальное распределение', 'N={} p={}'.format(N, binomial_p), 11, (0, N + 1))

    geometric_p = 0.5
    geometric1_sample = get_geometric1_sample(geometric_p, n)
    collect_stat(geometric1_sample, (1 - geometric_p) / geometric_p, (1 - geometric_p) / geometric_p ** 2)
    draw_graphs(geometric1_sample, 'геометрическое распределение №1', 'p={}'.format(geometric_p),
                 max(geometric1_sample) + 1, (0, max(geometric1_sample) + 1))

    geometric2_sample = get_geometric2_sample(geometric_p, n)
    collect_stat(geometric2_sample, (1 - geometric_p) / geometric_p, (1 - geometric_p) / geometric_p ** 2)
    draw_graphs(geometric2_sample, 'геометрическое распределение №2', 'p={}'.format(geometric_p),
                 max(geometric2_sample) + 1, (0, max(geometric2_sample) + 1))

    geometric3_sample = get_geometric3_sample(geometric_p, n)
    collect_stat(geometric3_sample, (1 - geometric_p) / geometric_p, (1 - geometric_p) / geometric_p ** 2)
    draw_graphs(geometric3_sample, 'геометрическое распределение №3', 'p={}'.format(geometric_p),
                 max(geometric3_sample) + 1, (0, max(geometric3_sample) + 1))

    mu = 10
    poisson1_sample = get_poisson1_sample(mu, n)
    collect_stat(poisson1_sample, mu, mu)
    draw_graphs(poisson1_sample, 'распределение Пуассона №1', 'mu={}'.format(mu),
                 max(poisson1_sample) + 1, (0, max(poisson1_sample) + 1))

    poisson2_sample = get_poisson2_sample(mu, n)
    collect_stat(poisson2_sample, mu, mu)
    draw_graphs(poisson2_sample, 'распределение Пуассона №2', 'mu={}'.format(mu),
                 max(poisson2_sample) + 1, (0, max(poisson2_sample) + 1))

    big_mu = 1000
    poisson3_sample = get_poisson3_sample(big_mu, n)
    collect_stat(poisson3_sample, big_mu, big_mu)
    draw_graphs(poisson3_sample, 'распределение Пуассона №3', 'mu={}'.format(big_mu),
                 max(poisson3_sample) + 1, (0, max(poisson3_sample) + 1))

    log_p = 0.5
    log_q = 1 - log_p
    logarithmic_sample = get_logarithmic_sample(log_p, n)
    collect_stat(logarithmic_sample, -log_q / (log_p * math.log(log_p)),
                 -log_q * (log_q + math.log(log_p)) / ((log_p ** 2) * (math.log(log_p) ** 2)))
    draw_graphs(logarithmic_sample, 'логарифмическое распределение', 'p={}'.format(log_p),
                 max(logarithmic_sample), (1, max(logarithmic_sample) + 1))


if __name__ == '__main__':
    main()
