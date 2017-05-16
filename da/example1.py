import numpy as np
import da
import param as p
import tests as t
import zmienne as ex

dim = 10
agents = 50
it = 2000
lb = -100 * np.ones(dim)
ub = 100 * np.ones(dim)
s, r = True, True

n = 30
results = np.zeros((n, 5))


def kw(x):
    return np.sum(np.power(x + 25, 2.0), 1)
ex.ss = 0.1
ex.a = 0.1
ex.c = 0.1
for j in range(1,28):
    for i in range(n):

        cnt = np.zeros(5)
        #x, results[i, 0], cnt[0] = da.dragonfly_algorithm(kw, agents, lb, ub, it, p.params1)  # , 100)
        x, results[i, 1], cnt[1] = da.dragonfly_algorithm(t.bent_cigar(s, r), agents, lb, ub, it, p.params1)  # , 100)
        x, results[i, 2], cnt[2] = da.dragonfly_algorithm(t.zakharov(s, r), agents, lb, ub, it, p.params1)  # , 300)
        x, results[i, 3], cnt[3] = da.dragonfly_algorithm(t.rosenbrock(s, r), agents, lb, ub, it, p.params1)  # , 400)
        x, results[i, 4], cnt[4] = da.dragonfly_algorithm(t.rastrigin(s, r), agents, lb, ub, it, p.params1)  # , 500)
        print i, results[i, :], cnt
    mean =  np.mean(results, 0)
    std =  np.std(results, 0)
    median =  np.median(results, 0)
    print "\n\n"
    print j
    print "DLA C="
    print ex.c
    print "; A="
    print ex.a
    print "S="
    print ex.ss
    print "Bent cigar: \n srednia = "
    print mean[1]
    print "odchylenie = "
    print std[1]
    print "mediana = "
    print median [1]
    print "Zakharov: \n srednia = "
    print mean[2]
    print "odchylenie = "
    print std[2]
    print "mediana = "
    print median [2]
    print "Rosenbrock: \n srednia = "
    print mean[3]
    print "odchylenie = "
    print std[3]
    print "mediana = "
    print median [3]
    print "Rastrigin: \n srednia = "
    print mean[4]
    print "odchylenie = "
    print std[4]
    print "mediana = "
    print median [4]

    if(j%9==0):
        ex.c+=0.6
        ex.a=0.1
        ex.ss=0.1
    elif (j%3==0):
        ex.a+=0.6
        ex.ss=0.1
    else:
        ex.ss+=0.6

# 0.00151779