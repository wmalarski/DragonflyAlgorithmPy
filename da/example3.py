import da
import numpy as np
import param as p
import tests as tt


agents = 50
it = 2000
lb = -100 * np.ones(10)
ub = 100 * np.ones(10)
tests = 30
shift, rotation = True, True

f_list = [1.5, 2., 2.5]
e_list = [0.01, 0.1, 1]
c = np.zeros((3**2, 2))
ind = 0
for e in e_list:
    for f in f_list:
        c[ind, :] = [e, f]
        ind += 1

for r in c:
    param = p.params(ws=0.1, wa=0.1, wc=0.1, we=r[0], wf=r[1])
    results = np.zeros((tests, 4))
    for i in range(tests):
        results[i, 0] = da.dragonfly_algorithm(tt.bent_cigar(shift, rotation), agents, lb, ub, it, param)[1]
        results[i, 1] = da.dragonfly_algorithm(tt.zakharov(shift, rotation), agents, lb, ub, it, param)[1]
        results[i, 2] = da.dragonfly_algorithm(tt.rosenbrock(shift, rotation), agents, lb, ub, it, param)[1]
        results[i, 3] = da.dragonfly_algorithm(tt.rastrigin(shift, rotation), agents, lb, ub, it, param)[1]

    mean = np.mean(results, 0)
    std = np.std(results, 0)
    median = np.median(results, 0)

    print '%1.1f & %1.1f' % (r[0], r[1]),
    for i in range(0, 4):
        print '& %.5f & %.5f & %.5f' % (mean[i], std[i], median[i]),
    print '\\\\'
