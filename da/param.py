import numpy as np


def params1(i, maxi):
    def rand():
        return np.random.sample()
    w1 = 0.9  # 0.9
    w2 = 0.2  # 0.4

    w3 = 0.15  # 0.1
    w4 = 0.0  # 0.0

    w5 = 1.5  # 2.0

    my_c = w3 - i * ((w3 - w4) / (maxi / w5))
    my_c = 0 if my_c < 0 else my_c

    s = 0.1 * my_c  # 2 * rand() * my_c
    a = 0.1 * my_c  # 2 * rand() * my_c
    c = 0.7 * my_c  # 2 * rand() * my_c

    f = 3.5 * np.random.sample()
    e = my_c

    w = w1 - i * ((w1 - w2) / maxi)

    return a, c, e, f, s, w


def params2(w1=0.9, w2=0.1, w3=0.1, w4=0.0, w5=2.0):
    def rand():
        return np.random.sample()

    def function(i, maxi):
        my_c = w3 - i * ((w3 - w4) / (maxi / w5))
        my_c = 0 if my_c < 0 else my_c
        s = 2 * rand() * my_c
        a = 2 * rand() * my_c
        c = 2 * rand() * my_c
        f = 2 * np.random.sample()
        e = my_c
        w = w1 - i * ((w1 - w2) / maxi)
        return a, c, e, f, s, w
    return function


def param_const(a, c, e, f, s, w):
    def function(i, maxi):
        return a, c, e, f, s, w
    return function
