import numpy as np
import da
import param as p
import tests as t

dim = 10
agents = 50
it = 1999
lb = -100 * np.ones(dim)
ub = 100 * np.ones(dim)
s, r = False, True

n = 10
results = np.zeros((n, 4))
for i in range(n):
    x, results[i, 0], _ = da.dragonfly_algorithm(t.bent_cigar(s, r), agents, lb, ub, it, p.params1, False)
    x, results[i, 1], _ = da.dragonfly_algorithm(t.rosenbrock(s, r), agents, lb, ub, it, p.params1, False)
    x, results[i, 2], _ = da.dragonfly_algorithm(t.rastrigin(s, r), agents, lb, ub, it, p.params1, False)
    x, results[i, 3], _ = da.dragonfly_algorithm(t.zakharov(s, r), agents, lb, ub, it, p.params1, False)
    print i, results[i, :]


print np.mean(results, 0)
