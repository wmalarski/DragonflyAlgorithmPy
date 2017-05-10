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

s, r = True, False

print da.dragonfly_algorithm(t.bent_cigar(s, r), agents, lb, ub, it, p.params1, True)
print da.dragonfly_algorithm(t.rosenbrock(s, r), agents, lb, ub, it, p.params1, True)
print da.dragonfly_algorithm(t.rastrigin(s, r), agents, lb, ub, it, p.params1, True)
print da.dragonfly_algorithm(t.zakharov(s, r), agents, lb, ub, it, p.params1, True)

