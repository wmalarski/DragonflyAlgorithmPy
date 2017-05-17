import numpy as np


def params(ws, wa, wc, we, wf):
    """
    Funkcja zwraca funkcje ktora zwraca zbior parametrow dla zadanego numeru iteracji.
    Parametry obliczane sa na podstawie wag zadanych w wywolaniu funkcji.
    """
    def rand(): return np.random.sample()

    def function(i, maxi, agents=1):
        w = 0.9 - i * ((0.9 - 0.4) / maxi)
        m = 0.1 - i * ((0.10 - (-0.5)) / (maxi / 2.0))
        m = 0.0 if m < 0.0 else m

        s = ws * m * rand()
        a = wa * m * rand()
        c = wc * m * rand()

        e = we * m
        f = wf * rand()

        return a, c, e, f, s, w
    return function
