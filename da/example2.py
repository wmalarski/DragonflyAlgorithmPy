import da
import numpy as np
import matplotlib.pyplot as plt
import param as p
import tests as t

agents = 20
it = 500
tests = 100

# da.variable_plot(p.params1, it, tests)
lb = -100 * np.ones(10)
ub = 100 * np.ones(10)

s, r = True, True

# print da.dragonfly_algorithm(t.bent_cigar(s, r), agents, lb, ub, it, p.params1, True, 100.0)
# print da.dragonfly_algorithm(t.zakharov(s, r), agents, lb, ub, it, p.params1, True, 300.0)
# print da.dragonfly_algorithm(t.rosenbrock(s, r), agents, lb, ub, it, p.params1, True, 400.0)
# print da.dragonfly_algorithm(t.rastrigin(s, r), agents, lb, ub, it, p.params1, True, 500.0)


def kw(x):
    return np.sum(np.power(x + 5, 2.0), 1)

# pm = p.params3(0.1, 0.9, 0.5, 0.3, 0.9)
# pm = p.param_const(0.1, 0.1, 0.1, 2.2, 0.0, 0.5)
pm = p.params1

print da.dragonfly_algorithm(t.rastrigin(False, False), agents, lb, ub, it, pm, plot=True)

