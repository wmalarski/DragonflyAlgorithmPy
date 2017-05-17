import numpy as np
import da
import param as p
import tests as t

# Skrypt oblicza wyniki dla roznych kombinacji parametrow
# s - speracji, a - align, c - cohesion

dim = 10
agents = 50
it = 2000
lb = -100 * np.ones(dim)
ub = 100 * np.ones(dim)
shift, rotation = True, True
tests = 30

s_list = [0.1, 0.7, 1.3]
a_list = [0.1, 0.7, 1.3]
c_list = [0.1, 0.7, 1.3]
ind = 0
params = np.zeros((3**3, 3))
for c in c_list:
    for a in a_list:
        for s in s_list:
            params[ind, :] = [c, a, s]
            ind += 1

for r in params:
    pm = p.params(
        wc=r[0], wa=r[1], ws=r[2],
        we=1.0, wf=2.0
    )
    results = np.zeros((tests, 4))
    for i in range(tests):
        results[i, 0] = da.dragonfly_algorithm(t.bent_cigar(shift, rotation), agents, lb, ub, it, pm)[1]
        results[i, 1] = da.dragonfly_algorithm(t.zakharov(shift, rotation), agents, lb, ub, it, pm)[1]
        results[i, 2] = da.dragonfly_algorithm(t.rosenbrock(shift, rotation), agents, lb, ub, it, pm)[1]
        results[i, 3] = da.dragonfly_algorithm(t.rastrigin(shift, rotation), agents, lb, ub, it, pm)[1]

    mean = np.mean(results, 0)
    std = np.std(results, 0)
    median = np.median(results, 0)

    print '%1.1f & %1.1f & %1.1f' % (r[0], r[1], r[2]),
    for i in range(0, 4):
        print '& %.5f & %.5f & %.5f' % (mean[i], std[i], median[i]),
    print '\\\\'
