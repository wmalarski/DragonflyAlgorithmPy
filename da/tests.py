import numpy as np
import matplotlib.pyplot as plt

_mr_bent_cigar = np.loadtxt("M_1_D10.txt")
_os_bent_cigar = np.loadtxt("shift_data_1.txt")

_mr_rosenbrock = np.loadtxt("M_3_D10.txt")
_os_rosenbrock = np.loadtxt("shift_data_3.txt")

_mr_rastrigin = np.loadtxt("M_4_D10.txt")
_os_rastrigin = np.loadtxt("shift_data_4.txt")

_mr_zakharov = np.loadtxt("M_5_D10.txt")
_os_zakharov = np.loadtxt("shift_data_5.txt")


def _sr_function(x, os, mr, sh_rate, s_flag, r_flag):
    dim = x.shape[1]
    if s_flag:
        sr_x = (x - os[:dim]) * sh_rate
    else:
        sr_x = x * sh_rate
    if r_flag:
        sr_x = np.asarray(x * np.asmatrix(mr)[:dim, :dim])
    return sr_x


def bent_cigar(s_flag, r_flag):
    def func(x):
        x = _sr_function(x, _os_bent_cigar, _mr_bent_cigar, 1.0, s_flag, r_flag)
        p1 = np.power(x[:, 0], 2.0)
        p2 = 1e6 * np.sum(np.power(x[:, 1:], 2), 1)
        return p1 + p2
    return func


def rosenbrock(s_flag, r_flag):
    def func(x):
        x = _sr_function(x, _os_rosenbrock, _mr_rosenbrock, 2048.0 / 100.0, s_flag, r_flag)
        p1 = np.power(x[:, 1:] - np.power(x[:, :-1], 2.0), 2.0)
        p2 = (1 - x[:, 0:-1])
        return np.sum(p1 + p2, 1)
    return func


def rastrigin(s_flag, r_flag):
    def func(x):
        x = _sr_function(x, _os_rastrigin, _mr_rastrigin, 5.12/100.0, s_flag, r_flag)
        n = x.shape[1]
        a = 10
        inner = np.power(x, 2.0) - a * np.cos(2.0 * np.pi * x)
        return a * n + np.sum(inner, 1)
    return func


def zakharov(s_flag, r_flag):
    def func(x):
        x = _sr_function(x, _os_zakharov, _mr_zakharov, 1.0, s_flag, r_flag)
        sum1 = np.sum(np.power(x, 2.0), 1)
        itr = np.arange(1, x.shape[1] + 1)
        sum2 = np.sum(x * itr * 0.5, 1)
        return sum1 + np.power(sum2, 2) + np.power(sum2, 4)
    return func


def plot_contour(func):
    X, Y = np.mgrid[-100:100:0.5, -100:100:0.5]
    positions = np.vstack([X.ravel(), Y.ravel()]).T
    Z = func(positions).reshape(X.shape)
    CS = plt.contour(X, Y, Z)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.show()

