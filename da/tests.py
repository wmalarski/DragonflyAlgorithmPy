import numpy as np

_mr_bent_cigar = np.asmatrix(np.loadtxt("M_1_D10.txt"))
_os_bent_cigar = np.loadtxt("shift_data_1.txt")

_mr_zakharov = np.asmatrix(np.loadtxt("M_3_D10.txt"))
_os_zakharov = np.loadtxt("shift_data_3.txt")

_mr_rosenbrock = np.asmatrix(np.loadtxt("M_4_D10.txt"))
_os_rosenbrock = np.loadtxt("shift_data_4.txt")

_mr_rastrigin = np.asmatrix(np.loadtxt("M_5_D10.txt"))
_os_rastrigin = np.loadtxt("shift_data_5.txt")


def _sr_function(x, os, mr, sh_rate, s_flag, r_flag):
    y = (x - os if s_flag else x) * sh_rate
    return np.asarray(mr * y.T).T if r_flag else y


def bent_cigar(s_flag, r_flag):
    def func(x):
        x2 = _sr_function(x, _os_bent_cigar[:x.shape[1]], _mr_bent_cigar, 1.0, s_flag, r_flag)
        p1 = np.power(x2[:, 0], 2.0)
        p2 = 1e6 * np.sum(np.power(x2[:, 1:], 2), 1)
        return p1 + p2
    return func


def rosenbrock(s_flag, r_flag):
    def func(x):
        x2 = _sr_function(x, _os_rosenbrock[:x.shape[1]], _mr_rosenbrock, 2.048/100.0, s_flag, r_flag) + 1
        p1 = 100 * np.power(np.power(x2[:, :-1], 2.0) - x2[:, 1:], 2.0)
        p2 = np.power(x2[:, :-1] - 1, 2.0)
        return np.sum(p1 + p2, 1)
    return func


def rastrigin(s_flag, r_flag):
    def func(x):
        x2 = _sr_function(x, _os_rastrigin[:x.shape[1]], _mr_rastrigin, 5.12/100.0, s_flag, r_flag)
        inner = np.power(x2, 2.0) - 10 * np.cos(2.0 * np.pi * x2) + 10
        return np.sum(inner, 1)
    return func


def zakharov(s_flag, r_flag):
    def func(x):
        x2 = _sr_function(x, _os_zakharov[:x.shape[1]], _mr_zakharov, 1.0, s_flag, r_flag)
        sum1 = np.sum(np.power(x2, 2.0), 1)
        ir = np.arange(1.0, x.shape[1] + 1.0, 1.0)
        sum2 = np.sum(x2 * 0.5 * ir, 1)
        return sum1 + np.power(sum2, 2) + np.power(sum2, 4)
    return func
