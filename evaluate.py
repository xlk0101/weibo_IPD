import numpy as np


def calc_forward_dev(true_fcount, pre_fcount):
    return calc_dev(true_fcount, pre_fcount, 5)


def calc_comment_dev(true_ccount, pre_ccount):
    return calc_dev(true_ccount, pre_ccount, 3)


def calc_like_dev(true_lcount, pre_lcount):
    return calc_dev(true_lcount, pre_lcount, 3)


def calc_dev(true_num, pre_num, bias_num):
    return np.abs(pre_num - true_num) / (true_num + bias_num)


def single_precision(f_dev, c_dev, l_dev):
    return 1 - 0.5 * f_dev - 0.25 * c_dev - 0.25 * l_dev


def all_precision(all_counts, singal_precisions):
    assert len(all_counts) == len(singal_precisions)
    N = len(all_counts)
    p_d = 0.0
    p_m = 0.0
    for i in range(N):
        p_m += (all_counts[i] + 1)
        p_d += (all_counts[i] + 1) * sgn(singal_precisions[i] - 0.8)
    return p_d / p_m


def sgn(x):
    return 1 if x > 0 else 0


if __name__ == '__main__':
    print(all_precision([10, 20, 30], [0.9, 0.9, 0.5]))
