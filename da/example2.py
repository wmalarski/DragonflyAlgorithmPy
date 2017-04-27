import da
import param as p
import numpy as np


def fun(x):
    return np.sum(np.power(x, 2), 1) + 1

agents = 50
it = 1999
n = 100

da.variable_plot(p.params1, it, n)
da.dragonfly_algorithm(fun, agents, np.array([-100, -100]), np.array([100, 100]), it, p.params1, True)
