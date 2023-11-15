import random

def gen_weight_rand(weight_arr):
    if not isinstance(weight_arr, list):
        return -1

    weight_sum = sum(weight_arr)
    result = weight_sum * random.random()

    _sum = 0
    for i, x in enumerate(weight_arr):
        _sum += x
        if _sum > result:
            return i

    return -1