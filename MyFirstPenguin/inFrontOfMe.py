from . import global_constants
import numpy as np

def in_front_of_me(body):
    """
    Returns everything in front of me, sorted by proximity
    :param body: dict
    :return: list of tuple, tuple cotains distance and item type
    """
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]
    bodyDirection = body["you"]["direction"]
    returnstuff = []
    enemies = body["enemies"]
    walls = body["walls"]
    bonusTiles = body["bonusTiles"]
    my_list = []
    if bodyDirection == "top":
        for item in enemies:
            if item['x'] == penguinPositionX:
                item_y = item["y"]
                if item_y > 0:
                    my_list.append((item_y-penguinPositionY, "enemies"))
        for item in walls:
            if item['x'] == penguinPositionX:
                item_y = item["y"]
                if item_y > 0:
                    my_list.append((item_y - penguinPositionY, "walls"))
        for item in bonusTiles:
            if item['x'] == penguinPositionX:
                item_y = item["y"]
                if item_y > 0:
                    my_list.append((item_y-penguinPositionY, "bonusTiles"))
    elif bodyDirection == "bottom":
        for item in enemies:
            if item['x'] == penguinPositionX:
                item_y = item["y"]
                if item_y < 0:
                    my_list.append((penguinPositionY-item_y, "enemies"))
        for item in walls:
            if item['x'] == penguinPositionX:
                item_y = item["y"]
                if item_y < 0:
                    my_list.append((penguinPositionY-item_y, "walls"))
        for item in bonusTiles:
            if item['x'] == penguinPositionX:
                item_y = item["y"]
                if item_y < 0:
                    my_list.append((penguinPositionY-item_y, "bonusTiles"))
    elif bodyDirection == "left":
        for item in enemies:
            if item['y'] == penguinPositionY:
                item_x = item["x"]
                if item_x < 0:
                    my_list.append((penguinPositionX-item_x, "enemies"))
        for item in walls:
            if item['y'] == penguinPositionY:
                item_x = item["x"]
                if item_x < 0:
                    my_list.append((penguinPositionX-item_x, "walls"))
        for item in bonusTiles:
            if item['y'] == penguinPositionX:
                item_x = item["x"]
                if item_x < 0:
                    my_list.append((penguinPositionX-item_x, "bonusTiles"))
    elif bodyDirection == "right":
        for item in enemies:
            if item['y'] == penguinPositionY:
                item_x = item["x"]
                if item_x > 0:
                    my_list.append((penguinPositionX - item_x, "enemies"))
        for item in walls:
            if item['y'] == penguinPositionY:
                item_x = item["x"]
                if item_x > 0:
                    my_list.append((penguinPositionX - item_x, "walls"))
        for item in bonusTiles:
            if item['y'] == penguinPositionX:
                item_x = item["x"]
                if item_x > 0:
                    my_list.append((penguinPositionX - item_x, "bonusTiles"))


    return sorted(my_list)