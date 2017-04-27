import numpy as np
import da
import param as p


def fun(x):
    return np.sum(np.power(x, 2), 1) + 1

agents = 50
it = 1999

par = p.params2()

print da.dragonfly_algorithm(fun, agents, np.array([-100]), np.array([100]), it, par, True)
print da.dragonfly_algorithm(fun, agents, np.array([-100, -100]), np.array([100, 100]), it, par, True)
print da.dragonfly_algorithm(fun, agents, np.array([-100, -100, -100]), np.array([100, 100, 100]), it, par, True)
