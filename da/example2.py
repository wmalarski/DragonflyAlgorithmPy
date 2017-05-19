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
    ws=0.1, wa=0.1, wc=0.1,
    we=0.1, wf=2.0
)

print da.dragonfly_algorithm(
    function=t.rastrigin(False, False),
    agents=agents,
    lbd=lb,
    ubd=ub,
    iteration=it,
    param_fun=parameters,
    plot=True
)

