from run import *
from basic import *


def num_moves_to_target(body, target_x, target_y):
    """
    :param body: json body
    :param target: body['target']
    :return: int, num moves required to get to a certain target
    """

    my_x = body['you']['x']
    my_y = body['you']['y']
    direction = body['you']['direction']

    diff_x = target_x - my_x
    diff_y = target_y - my_y

    dir_x, dir_y = direction_to_coord_tuple(direction)

    turn = calc_turning_required(diff_x, diff_y, dir_x, dir_y)

    return abs(diff_x) + abs(diff_y)


def calc_turning_required(diff_x, diff_y, dir_x, dir_y):
    if diff_x != 0:
        diff_x = diff_x/abs(diff_x)
    if diff_y != 0:
        diff_y = diff_y/abs(diff_y)
    return int(diff_x != dir_x) + int(diff_y != dir_y)

