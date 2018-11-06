def coordinates_to_direction(my_x, my_y, target_x, target_y):
    """
    :param MUST BE IN A STRAIGHT LINE
    :param body:
    :param x:
    :param y:
    :return: direction: top, bottom, right, left
    """
    if target_y - my_y != 0 and target_x - my_x != 0:
        return False

    if target_x > my_x:
        return 'right'
    if target_y > my_y:
        return 'top'
    if target_x < my_x:
        return 'left'
    if target_y < my_y:
        return 'bottom'


def can_shoot_enemy(body, infront_list):
    """
    :param body:
    :param infront_list: list from inFrontOfMe.py
    :return: True if can shoot enemy, False if not
    """
    i = 0
    while infront_list[i][0] <= body['you']['weaponRange']:
        if infront_list[i][1] == 'wall':
            break
        elif infront_list[i][1] == 'enemy':
            return True
        i += 1
    return False

