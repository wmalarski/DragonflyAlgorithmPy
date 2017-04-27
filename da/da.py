import numpy as np
import matplotlib.pyplot as plt

_gamma1d25 = 1.1330030963193471
_gamma2d5 = 3.323350970447843
_beta = 1.5
_l = (_gamma2d5 * np.sin(np.pi * _beta / 2.0))
_m = _gamma1d25 * _beta * pow(2.0, (_beta - 1.0) / 2.0)
_omega = np.power(_l / _m, 1 / _beta)


def _levy(dim, n):
    r1 = np.random.random((n, dim))
    r2 = np.random.random((n, dim))
    return 0.01 * ((r1 * _omega) / np.power(np.abs(r2), 1.0 / _beta))


def _variable_param(i, maxi):
    w = 0.9 - i * ((0.9 - 0.4) / maxi)
    my_c = 0.1 - i * ((0.1 - 0.0) / (maxi / 2.0))
    my_c = 0 if my_c < 0 else my_c
    s = 2 * np.random.sample() * my_c  # Seperation weight
    a = 2 * np.random.sample() * my_c  # Alignment weight
    c = 2 * np.random.sample() * my_c  # Cohesion weight
    f = 2 * np.random.sample()  # Food attraction weight
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


def _get_distance_matrix(pos):
    return np.sqrt(np.sum(np.power(pos - pos[:, np.newaxis], 2.0), 2))


def _divide(l, m):
    m2 = np.repeat(m, l.shape[1]).reshape(l.shape)
    ind_non0 = np.where(m2 > 0)
    l[ind_non0] /= m2[ind_non0]
    return l


def _border_reflection(pos, vel, lbd, ubd):
    diff = ubd - lbd
    f = np.floor(pos/diff + 0.5)
    pos = (pos - diff * f) * np.power(-1.0, f)
    yl = np.where(pos < lbd)
    yu = np.where(pos > ubd)
    vel[yl] *= -1
    vel[yu] *= -1
    return pos, vel


def dragonfly_algorithm(function, agents, lbd, ubd, iteration, param_fun=_variable_param, plot=False):
    dim = lbd.shape[0]
    x_shape = (agents, agents, dim)
    n_shape = (agents, agents, 1)

    pos = _random_population(lbd, ubd, agents)
    vel = np.random.random((agents, dim))
    values = function(pos)
    function_cnt = agents

    min_value_ind = np.argmin(values)
    min_pos = pos[min_value_ind, :]
    min_value = values[min_value_ind]

    iter_x = np.arange(iteration)
    results = np.zeros(iteration)
    mean = np.zeros(iteration)
    min_result = np.zeros(iteration)

    for i in range(iteration):
        # Update the food source and enemy
        food_ind = np.argmin(values)
        enemy_ind = np.argmax(values)
        food_pos = pos[food_ind, :]
        enemy_pos = pos[enemy_ind, :]

        # Update w, s, a, c, f, and e
        a, c, e, f, s, w = param_fun(i, iteration)

        # Update neighbouring radius
        radius = _get_radius(i, iteration, lbd, ubd)
        radius_norm = np.sqrt(np.sum(np.power(radius, 2)))

        # Calculate distance between agents
        distance_matrix = _get_distance_matrix(pos)

        # Find neighbours
        n_matrix = ((distance_matrix < radius_norm) - np.eye(agents, dtype=np.int8)).reshape(n_shape)

        # Position and Velocity matrix
        p_matrix = np.tile(pos, agents).reshape(x_shape)
        v_matrix = np.tile(vel, agents).reshape(x_shape)

        # Calculate number of neighbours
        neighbours_cnt = np.sum(n_matrix, axis=1)
        (neighbours_cnt_eq_0, _) = np.where(neighbours_cnt == 0)

        separation = np.sum((pos - p_matrix) * n_matrix, 0)                         # Eq. 3.1
        alignment = _divide(np.sum(v_matrix * n_matrix, 0), neighbours_cnt)         # Eq. 3.2
        cohesion = _divide(np.sum(p_matrix * n_matrix, 0), neighbours_cnt) - pos    # Eq. 3.3
        food = n_matrix[food_ind] * (food_pos - pos)                                # Eq. 3.4
        enemy = n_matrix[enemy_ind] * (enemy_pos + pos)                             # Eq. 3.5

        # Update velocity and position
        vel = vel * w + separation * s + alignment * a + cohesion * c + food * f + enemy * e  # Eq. 3.6
        vel[neighbours_cnt_eq_0] = np.zeros(dim)
        pos += vel  # Eq. 3.7
        pos[neighbours_cnt_eq_0] *= _levy(dim, neighbours_cnt_eq_0.size)  # Eq. 3.8

        # Check and correct the new positions based on the boundaries of variables
        pos, vel = _border_reflection(pos, vel, lbd, ubd)

        # Prepare to next iteration, save data
        values = function(pos)
        function_cnt += agents
        act_min_ind = np.argmin(values)
        act_min = values[act_min_ind]
        results[i] = act_min
        mean[i] = np.mean(values)
        if act_min < min_value:
            min_value, min_pos = act_min, pos[act_min_ind]
        min_result[i] = min_value

    if plot:
        plt.plot(iter_x, results, label="Iteration result")
        plt.plot(iter_x, min_result, label="Global result")
        plt.legend(fontsize='medium')
        plt.title("Dragonfly Algorithm Evolution")
        plt.xlabel("Iterations")
        plt.ylabel("Function value")
        plt.show()

    return min_pos, min_value, function_cnt
