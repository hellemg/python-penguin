from global_constants import *


def in_front_of_me(body):
    """
    Returns everything in front of me, sorted by proximity
    :param body: dict
    :return: list of tuple, tuple cotains distance and item type
    """
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]
    bodyDirection = body["you"]["direction"]
    print("body_dir: ", bodyDirection)
    returnstuff = []
    enemies = body["enemies"]
    walls = body["walls"]
    bonusTiles = body["bonusTiles"]
    my_list = []
    if bodyDirection == "top":
        for item in enemies:
            if "x" in item.keys():
                if item['x'] == penguinPositionX:
                    item_y = item["y"]
                    if item_y < penguinPositionY:
                        my_list.append((abs(penguinPositionY - item_y), "enemies"))
        for item in walls:
            if item['x'] == penguinPositionX:
                item_y = item["y"]
                if item_y < penguinPositionY:
                    my_list.append((abs(penguinPositionY - item_y), "walls"))
        for item in bonusTiles:
            if item['x'] == penguinPositionX:
                item_y = item["y"]
                if item_y < penguinPositionY:
                    my_list.append((abs(penguinPositionY - item_y), "bonusTiles"))
    elif bodyDirection == "bottom":
        for item in enemies:
            if "x" in item.keys():
                if item['x'] == penguinPositionX:
                    item_y = item["y"]
                    if item_y > penguinPositionY:
                        my_list.append((abs(item_y - penguinPositionY), "enemies"))
        for item in walls:
            if item['x'] == penguinPositionX:
                item_y = item["y"]
                if item_y > penguinPositionY:
                    my_list.append((abs(item_y - penguinPositionY), "walls"))
        for item in bonusTiles:
            if item['x'] == penguinPositionX:
                item_y = item["y"]
                if item_y > penguinPositionY:
                    my_list.append((abs(item_y - penguinPositionY), "bonusTiles"))
    elif bodyDirection == "left":
        for item in enemies:
            if "x" in item.keys():
                if item['y'] == penguinPositionY:
                    item_x = item["x"]
                    if item_x < penguinPositionX:
                        my_list.append((abs(penguinPositionX - item_x), "enemies"))
        for item in walls:
            if item['y'] == penguinPositionY:
                item_x = item["x"]
                if item_x < penguinPositionX:
                    my_list.append((abs(penguinPositionX - item_x), "walls"))
        for item in bonusTiles:
            if item['y'] == penguinPositionX:
                item_x = item["x"]
                if item_x < penguinPositionX:
                    my_list.append((abs(penguinPositionX - item_x), "bonusTiles"))
    elif bodyDirection == "right":
        for item in enemies:
            if "x" in item.keys():
                if item['y'] == penguinPositionY:
                    item_x = item["x"]
                    if item_x > penguinPositionX:
                        my_list.append((abs(item_x - penguinPositionX), "enemies"))
        for item in walls:
            if item['y'] == penguinPositionY:
                item_x = item["x"]
                if item_x > penguinPositionX:
                    my_list.append((abs(item_x - penguinPositionX), "walls"))
        for item in bonusTiles:
            if item['y'] == penguinPositionX:
                item_x = item["x"]
                if item_x > penguinPositionX:
                    my_list.append((abs(item_x - penguinPositionX), "bonusTiles"))

    return sorted(my_list)
