from . import globals


def target_in_straight_line(my_x, my_y, target_x, target_y):
    """
    :param my_x:
    :param my_y:
    :param target_x:
    :param target_y:
    :return: tuple (x,y), diff*1 if in a positive direction, diff*-1 if negative. (0,0) if target not in straight line
    """
    diff = (target_x - my_x, target_y - my_y)

    if diff[0] != 0 and diff[1] != 0:
        return tuple((0, 0))
    return diff



