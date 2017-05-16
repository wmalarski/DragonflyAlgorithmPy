import numpy as np
import zmienne as ex


def params1(i, maxi, agents):
    def rand(): return np.random.sample((agents, 1))

    '''w = 0.9 - i * ((0.9 - 0.6) / maxi)
    m = 0.3 - i * ((0.3 - (-0.1)) / maxi)
    m = 0.0 if m < 0.0 else m

    s = 0.1 * m * rand()
    a = 0.1 * m * rand()
    c = 0.1 * m * rand()
    e = 0.01 * m
    f = 2.1 * rand()'''

    w = 0.9 - i * ((0.9 - 0.4) / maxi)
    m = 0.1 - i * ((0.15 - 0.0) / (maxi/2.0))
    m = 0.0 if m < 0.0 else m

    s = ex.ss * m * rand()
    a = ex.a * m * rand()
    c = ex.c * m * rand()
    e =  m
    f = 2 * rand()

    return a, c, e, f, s, w


def params2(w1=0.9, w2=0.1, w3=0.1, w4=0.0, w5=2.0):
    def rand():
        return np.random.sample()

    def function(i, maxi):
        my_c = 0.1 - i * ((0.1 - 0.0) / (maxi / 2.0))
        my_c = 0 if my_c < 0 else my_c
        s = 2 * rand() * my_c
        a = 2 * rand() * my_c
        c = 2 * rand() * my_c
        f = 2 * np.random.sample()
        e = my_c
        w = 0.9 - i * ((0.9 - 0.4) / maxi)
        return a, c, e, f, s, w
    return function


def params3(ws=0.5, wa=0.5, wc=0.5, we=0.5, wf=2.0):
    def rand(): return np.random.sample()

    def function(i, maxi):
        w = 0.9 - i * ((0.9 - 0.4) / maxi)
        m = 0.1 - i * ((0.1 - 0.0) / (maxi / 1.5))
        m = 0.0 if m < 0.0 else m
        s = ws * m * rand()
        a = wa * m * rand()
        c = wc * m * rand()
        e = we * m
        f = 4 * wf * rand()
        return a, c, e, f, s, w
    return function


def param_const(a, c, e, f, s, w):
    def function(i, maxi):
        return a, c, e, f, s, w
    return function
