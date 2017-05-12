import da
import numpy as np
import matplotlib.pyplot as plt
import param as p
import tests as t

agents = 50
it = 1999
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
    return np.sum(np.power(x+5, 2.0), 1)

v = np.array([[[2.0] * 10], [[3.0] * 10]])
print da.dragonfly_algorithm(kw, agents, lb, ub, it, plot=True)
