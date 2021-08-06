from math import log

from numpy.random import uniform

t = 8760
t_a = 2.58  # alpha=0.995
p0 = 0.995
eps = 0.0025
n = int((t_a ** 2) * p0 * (1 - p0) / (eps ** 2))
l_i = [40 * (10 ** (-6)), 10 * (10 ** (-6)), 80 * (10 ** (-6)), 30 * (10 ** (-6))]
n_i = [4, 2, 6, 4]
m = 4


def x_t(x):
    return x > t


def workability_function(x):
    return (x_t(x[0]) and x_t(x[1]) or x_t(x[2]) and x_t(x[3])) \
           and x_t(x[4]) and x_t(x[5]) \
           and (x_t(x[6]) and x_t(x[7])
                or x_t(x[8]) and x_t(x[9])
                or x_t(x[10]) and x_t(x[11])) \
           and (x_t(x[12]) or x_t(x[13])) \
           and (x_t(x[14]) or x_t(x[15]))


def uptime_probability(l_temp):
    d = 0
    for _ in range(n):
        x = [0 for _ in range(sum(n_i))]
        start_range = end_range = 0
        for i in range(m):
            end_range += n_i[i]
            for k in range(n_i[i]):
                x[k + start_range] = -log(uniform()) / l_i[i]
            for k in range(l_temp[i]):
                min_i = start_range
                min_x = x[min_i]
                for z in range(start_range, end_range):
                    if min_x > x[z]:
                        min_i = z
                        min_x = x[z]
                x[min_i] -= log(uniform()) / l_i[i]
            start_range += n_i[i]
        if not workability_function(x):
            d += 1
    return 1 - d / n


def update_l(l):
    l_new = [(l[i][0].copy(), 0.0) for i in range(len(l)) for _ in range(m)]
    for i in range(len(l_new)):
        l_new[i][0][i % m] += 1
    return l_new


from progress.bar import IncrementalBar


def main():
    print(n)
    l_count = [([3, 2, 4, 2], 0.0)]
    is_found = False
    while not is_found or sum(l_count[0])<18:
        sum_res = 0

        #l_count = sorted(l_count, key=lambda tup: tup[1])[max(0, len(l_count) - 20):]
        # if len(l_count)>20:
        #     l_count = sorted(l_count, key=lambda tup: -tup[1])[:int(len(l_count)*0.5)+1]

        # l_count = sorted(l_count, key=lambda tup: -tup[1])[:min(20, len(l_count))+1]
        if len(l_count) > 19:
            l_count = sorted(l_count, key=lambda tup: -tup[1])[:int(len(l_count)*0.75)+1]

        l_count = update_l(l_count)
        l_new = []
        for i in l_count:
            if i not in l_new:
                l_new.append(i)
        l_count = l_new
        max_res = 0
        max_index = -1
        # bar = IncrementalBar('Countdown', max=len(l_count))

        for j in range(len(l_count)):
            # bar.next()
            l_count[j] = (l_count[j][0], uptime_probability(l_count[j][0]))

            if max_res < l_count[j][1]:
                max_res = l_count[j][1]
                max_index = j
            sum_res += l_count[j][1]
            if l_count[j][1] >= p0:
                is_found = True
                print('Appropriate set is {} with prob={}\n'.format(l_count[j][0], l_count[j][1]))
        # bar.finish()
        print('Average res is {}'.format(sum_res / len(l_count)))
        print('The best set of {} sets is {} with res={}\n'.format(len(l_count), l_count[max_index][0], max_res))
    q = sorted(l_count, key=lambda tup: -tup[1])[:20]
    for i in q:
        print(i)



if __name__ == '__main__':
    main()
