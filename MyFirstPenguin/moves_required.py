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

    if diff_x != 0:
        diff_x_sign = diff_x/abs(diff_x)
    else:
        diff_x_sign = 0

    if diff_y != 0:
        diff_y_sign = diff_y/abs(diff_y)
    else:
        diff_y_sign = 0

    turn = (diff_y_sign != dir_y) + (diff_x_sign != diff_x_sign)

    return turn + abs(diff_x) + abs(diff_y)


    

