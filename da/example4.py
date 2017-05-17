import da
import numpy as np
import param as p
import tests as t

# Skrypt generuje ewolucje roju czastek

agents = 50
it = 2000
tests = 100

lb = -100 * np.ones(10)
ub = 100 * np.ones(10)

shift, rotation = True, True

parameters = p.params(
    ws=1.3, wa=1.3, wc=1.3,
    we=1.0, wf=2.0
)

da.variable_plot(parameters, it, tests)

