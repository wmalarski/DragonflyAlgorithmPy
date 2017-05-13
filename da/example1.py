import numpy as np
import da
import param as p
import tests as t

dim = 10
agents = 30
it = 500
lb = -100 * np.ones(dim)
ub = 100 * np.ones(dim)
s, r = True, True

n = 300
results = np.zeros((n, 5))


def kw(x):
    return np.sum(np.power(x + 25, 2.0), 1)


for i in range(n):
    cnt = np.zeros(5)
    # x, results[i, 0], cnt[0] = da.dragonfly_algorithm(kw, agents, lb, ub, it)  # , 100)
    results[i, 1], cnt[1] = da.dragonfly_algorithm(t.bent_cigar(s, r), agents, lb, ub, it)[1:]  # , 100)
    results[i, 2], cnt[2] = da.dragonfly_algorithm(t.zakharov(s, r), agents, lb, ub, it)[1:]  # , 300)
    results[i, 3], cnt[3] = da.dragonfly_algorithm(t.rosenbrock(s, r), agents, lb, ub, it)[1:]  # , 400)
    results[i, 4], cnt[4] = da.dragonfly_algorithm(t.rastrigin(s, r), agents, lb, ub, it)[1:]  # , 500)
    print i, results[i, :], cnt


print np.mean(results, 0)
print np.std(results, 0)
print np.median(results, 0)
# 0.00151779

