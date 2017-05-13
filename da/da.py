import numpy as np
import matplotlib.pyplot as plt

_gamma1d25 = 1.1330030963193471
_gamma2d5 = 3.323350970447843
_beta = 1.5
_l = (_gamma2d5 * np.sin(np.pi * _beta / 2.0))
_m = _gamma1d25 * _beta * pow(2.0, (_beta - 1.0) / 2.0)
_omega = np.power(_l / _m, 1 / _beta)
_eps = 1e-8


def _levy(dim, n):
    r1 = np.random.normal(size=(n, dim))
    r2 = np.random.normal(size=(n, dim))
    return 0.01 * ((r1 * _omega) / np.power(np.abs(r2), 1.0 / _beta))


def _variable_param(i, maxi, agents):
    w = 0.9 - i * ((0.9 - 0.4) / maxi)
    my_c = 0.1 - i * ((0.1 - (-0.1)) / maxi)
    my_c = 0 if my_c < 0 else my_c
    s = 2 * np.random.sample((agents, 1)) * my_c  # Seperation weight
    a = 2 * np.random.sample((agents, 1)) * my_c  # Alignment weight
    c = 2 * np.random.sample((agents, 1)) * my_c  # Cohesion weight
    f = 2 * np.random.sample((agents, 1))  # Food attraction weight
    e = my_c  # Enemy distraction weight
    return a, c, e, f, s, w


def variable_plot(param_fun, maxi, n):
    iter_x = np.arange(maxi)
    arr = np.zeros((maxi, 6))
    for i in range(maxi):
        res = np.zeros((n, 6))
        for j in range(n):
            res[j, :] = np.asarray(param_fun(i, maxi))
        arr[i, :] = np.mean(res, axis=0)
    plt.plot(iter_x, arr[:, 0], label="a")
    plt.plot(iter_x, arr[:, 1], label="c")
    plt.plot(iter_x, arr[:, 2], label="e")
    plt.plot(iter_x, arr[:, 3], label="f")
    plt.plot(iter_x, arr[:, 4], label="s")
    plt.plot(iter_x, arr[:, 5], label="w")
    plt.legend(fontsize='medium')
    plt.show()


def _get_radius(i, maxi, lbd, ubd):
    return (ubd - lbd) * (0.25 + ((2.0 * i)/maxi))


def _random_population(lbd, ubd, n):
    return np.random.random((n, lbd.size)) * (ubd - lbd) + lbd


def _get_neighbours_matrix(pos, radius, agents):
    t = np.abs(pos - pos[:, np.newaxis]) < radius
    return np.all(t, 2) - np.eye(agents, dtype=np.int8)


def _get_neighbours_vector(pos, radius, v):
    t = np.abs(pos - v) < radius
    return np.all(t, 1) + 0.0


def _divide(l, m, default):
    m2 = np.repeat(m, l.shape[1]).reshape(l.shape)
    ind_non0 = np.where(m2 > 0)
    ind_eq0 = np.where(m2 == 1)
    l[ind_non0] /= m2[ind_non0]
    l[ind_eq0] = default[ind_eq0]
    return l


def _border_reflection(pos, lbd, ubd):
    diff = ubd - lbd
    f = np.floor(pos/diff - lbd/diff)
    lm = (np.mod(f, 2.0) == 1.0).real * (ubd + lbd)
    pos = (pos - diff * f) * np.power(-1.0, f) + lm
    return pos


def dragonfly_algorithm(function, agents, lbd, ubd, iteration, param_fun=_variable_param, plot=False, goal=0.0):
    dim = lbd.shape[0]
    x_shape = (agents, agents, dim)
    n_shape = (agents, agents, 1)

    vel_max = (ubd - lbd)/10.0
    pos = _random_population(lbd, ubd, agents)
    vel = _random_population(lbd, ubd, agents)
    values = function(pos)
    function_cnt = agents

    min_value_ind = np.argmin(values)
    min_pos = pos[min_value_ind, :]
    min_value = values[min_value_ind]

    enemy_ind = np.argmax(values)
    enemy_pos = pos[enemy_ind, :]
    enemy_val = values[enemy_ind]

    iter_x = np.arange(iteration)
    results = np.zeros(iteration)
    mean = np.zeros(iteration)
    min_result = np.zeros(iteration)
    mean_vel = np.zeros(iteration)
    values_matrix = np.zeros((iteration, agents))

    for i in range(iteration):
        # Update the food source and enemy
        food_pos = min_pos[:]
        enemy_ind_act = np.argmax(values)
        enemy_pos_act = pos[enemy_ind_act, :]
        enemy_val_act = values[enemy_ind_act]
        if enemy_val_act > enemy_val:
            enemy_val, enemy_pos[:] = enemy_val_act, enemy_pos_act[:]

        # Update w, s, a, c, f, and e
        a, c, e, f, s, w = param_fun(i, iteration, agents)

        # Update neighbouring radius
        radius = _get_radius(i, iteration, lbd, ubd)

        # Find neighbours
        n_matrix = _get_neighbours_matrix(pos, radius, agents).reshape(n_shape)
        n_food = _get_neighbours_vector(pos, radius, food_pos).reshape((agents, 1))
        n_enemy = _get_neighbours_vector(pos, radius, enemy_pos).reshape((agents, 1))

        # Position and Velocity matrix
        p_matrix = np.tile(pos, agents).reshape(x_shape)
        v_matrix = np.tile(vel, agents).reshape(x_shape)

        # Calculate number of neighbours
        neighbours_cnt = np.sum(n_matrix, axis=1)
        neighbours_cnt_eq_0, _ = np.where(neighbours_cnt == 0)
        neighbours_cnt_gt_0, _ = np.where(neighbours_cnt > 0)

        separation = np.sum((pos - p_matrix) * n_matrix, 0)                         # Eq. 3.1
        alignment = _divide(np.sum(v_matrix * n_matrix, 0), neighbours_cnt, vel)         # Eq. 3.2
        cohesion = _divide(np.sum(p_matrix * n_matrix, 0), neighbours_cnt, pos) - pos    # Eq. 3.3
        food = n_food * (food_pos - pos)                                     # Eq. 3.4
        enemy = n_enemy * (enemy_pos + pos)                             # Eq. 3.5

        # Update velocity and position
        vel = vel * w + separation * s + alignment * a + cohesion * c + food * f + enemy * e  # Eq. 3.6

        vg_max_y, vg_max_x = np.where(vel > vel_max)
        vl_min_y, vl_min_x = np.where(vel < -vel_max)
        vel[vg_max_y, vg_max_x] = vel_max[vg_max_x]
        vel[vl_min_y, vl_min_x] = -vel_max[vl_min_x]

        pos[neighbours_cnt_gt_0] += vel[neighbours_cnt_gt_0]  # Eq. 3.7
        levy = _levy(dim, neighbours_cnt_eq_0.size)
        pos[neighbours_cnt_eq_0] += pos[neighbours_cnt_eq_0] * levy  # Eq. 3.8

        # Check and correct the new positions based on the boundaries of variables
        vel[np.where(pos < lbd)] *= -1
        vel[np.where(pos > ubd)] *= -1
        pos = _border_reflection(pos, lbd, ubd)

        # Prepare to next iteration, save data
        values = function(pos)
        function_cnt += agents

        # Iteration results
        act_min_ind = np.argmin(values)
        act_min = values[act_min_ind]
        results[i] = act_min
        mean[i] = np.mean(values)
        mean_vel[i] = np.mean(np.sqrt(np.sum(np.power(vel, 2), 1)))
        values_matrix[i, :] = values

        if act_min < min_value:
            min_value_ind, min_value, min_pos[:] = act_min_ind, act_min, pos[act_min_ind, :]
        min_result[i] = min_value

        if np.abs(min_value - goal) < _eps:
            break

    if plot:
        # plt.subplot(3, 1, 1)
        for i in range(values_matrix.shape[1]):
            plt.plot(iter_x, values_matrix[:, i], '-k', lw=0.25, ms=0.3)
        plt.plot(iter_x, results, label="Optimum w iteracji")
        plt.plot(iter_x, min_result, label="Optimum globalne")
        plt.legend(fontsize='medium')
        plt.title("Ewolucja roju czastek")
        plt.xlabel("Liczba iteracji")
        plt.ylabel("Wartosc funkcji")
        plt.savefig("evolution.png")

        # plt.subplot(3, 1, 2)
        # plt.plot(iter_x, mean_vel)
        # plt.title("Mean Velocity")
        #
        # plt.subplot(3, 1, 3)
        # plt.plot(iter_x, params[:, 0], label="a")
        # plt.plot(iter_x, params[:, 1], label="c")
        # plt.plot(iter_x, params[:, 2], label="e")
        # plt.plot(iter_x, params[:, 3], label="f")
        # plt.plot(iter_x, params[:, 4], label="s")
        # plt.plot(iter_x, params[:, 5], label="w")
        # plt.legend(fontsize='medium')
        plt.show()

    return min_pos, min_value, function_cnt
