import random

import matplotlib.pyplot as plt


def main():
    m_t = 0.5
    d_t = 1 / 12
    print('n\t\tM_T\t\t\tM_E\t\t\tОтклонение M\t\tD_T\t\t\t\tD_E\t\tОтклонение D')
    for n in [10, 100, 1000, 10000]:
        u = [random.random() for _ in range(n)]
        m_e = sum(u) / n
        d_e = sum([(u[i] - m_e) ** 2 for i in range(n)]) / n
        print('{:5d}\t{}\t\t{:8.5f}\t\t{:8.5f}\t\t{:8.5f}\t\t{:8.5f}\t\t{:8.5f}'
              .format(n, m_t, m_e, m_t - m_e, d_t, d_e, d_t - d_e))

        k = [0 for _ in range(n)]
        for f in range(1, n):
            s = 0
            for i in range(n - f):
                s += (u[i] - m_e) * (u[i + f] - m_e)
            k[f] = s / (d_e * n)
        plt.plot([f for f in range(1, n + 1)], k)
        plt.grid()
        plt.xlabel('f')
        plt.ylabel('K(f)')
        plt.title('Коррелограмма (n = {})'.format(n))
        plt.savefig('res/Коррелограмма{}.png'.format(n))
        plt.close()

    size = 20
    delta = 1 / size
    n = len(u)
    weights = [0 for _ in range(size)]
    for i in range(n):
        weights[int(u[i] / delta)] += 1
    plt.hist(u, density=True, bins=20)
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Эмпирическая функция плотности для n = 10000')
    plt.savefig('res/Функция плотности.png')
    plt.close()

    acc = [weights[i] for i in range(size)]
    for i in range(1, size):
        acc[i] += acc[i - 1]
    acc = [0] + acc
    x = [i / size for i in range(size)] + [1]
    plt.plot(x, [y / n for y in acc])
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.title('Эмпирическая функция распределения для n = 10000')
    plt.savefig('res/Функция распределения.png')
    plt.close()


if __name__ == '__main__':
    main()
