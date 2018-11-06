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


