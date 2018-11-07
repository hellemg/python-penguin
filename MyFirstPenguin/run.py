import os
import json
import random
import math

from global_constants import *
from basic import *
from inFrontOfMe import *


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
        diff_x_sign = diff_x / abs(diff_x)
    else:
        diff_x_sign = 0

    if diff_y != 0:
        diff_y_sign = diff_y / abs(diff_y)
    else:
        diff_y_sign = 0

    turn = diff_y_sign != dir_y + diff_x_sign != diff_x_sign

    return turn + abs(diff_x) + abs(diff_y)


def doesCellContainWall(walls, x, y):
    for wall in walls:
        if wall["x"] == x and wall["y"] == y:
            return True
    return False


def wallInFrontOfPenguin(body):
    xValueToCheckForWall = body["you"]["x"]
    yValueToCheckForWall = body["you"]["y"]
    bodyDirection = body["you"]["direction"]

    if bodyDirection == "top":
        yValueToCheckForWall -= 1
    elif bodyDirection == "bottom":
        yValueToCheckForWall += 1
    elif bodyDirection == "left":
        xValueToCheckForWall -= 1
    elif bodyDirection == "right":
        xValueToCheckForWall += 1
    return doesCellContainWall(body["walls"], xValueToCheckForWall, yValueToCheckForWall)


def moveTowardsPoint(body, pointX, pointY):
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]
    plannedAction = PASS
    bodyDirection = body["you"]["direction"]
"""
    item_dir = coordinates_to_dir(body, pointX, pointY, penguinPositionX, penguinPositionY)
    print("Item dir:", item_dir)
    print("Item coord:", pointX ,",", pointY)
    print("body dir:", bodyDirection)
    print("body coord:", penguinPositionX, ",", penguinPositionY)
    if item_dir == bodyDirection:
        if bodyDirection == "top":
            plannedAction = MOVE_UP[bodyDirection]
        elif bodyDirection == "bottom":
            plannedAction = MOVE_DOWN[bodyDirection]
        elif bodyDirection == "left":
            plannedAction = MOVE_LEFT[bodyDirection]
        elif bodyDirection == "right":
            plannedAction = MOVE_RIGHT[bodyDirection]
    else:
"""
    if penguinPositionX < pointX:
        plannedAction = MOVE_RIGHT[bodyDirection]
    elif penguinPositionX > pointX:
        plannedAction = MOVE_LEFT[bodyDirection]
    elif penguinPositionY < pointY:
        plannedAction = MOVE_DOWN[bodyDirection]
    elif penguinPositionY > pointY:
        plannedAction = MOVE_UP[bodyDirection]

    if plannedAction == ADVANCE and wallInFrontOfPenguin(body):
        plannedAction = SHOOT
    return plannedAction


def moveTowardsCenterOfMap(body):
    centerPointX = math.ceil(body["mapWidth"] / 2)
    centerPointY = math.ceil(body["mapHeight"] / 2)
    return moveTowardsPoint(body, centerPointX, centerPointY)


def coordinates_to_dir(body, item_x, item_y, penguinPositionX, penguinPositionY):
    centerPointX = math.ceil(body["mapWidth"] / 2)
    centerPointY = math.ceil(body["mapHeight"] / 2)
    # Defining offset to be positive for coords larger than centre
    # Larger x -> smaller right, Larger y -> smaller bottom
    offset_x = item_x - centerPointX
    offset_y = item_y - centerPointY
    max = centerPointY * 2 - offset_x - offset_y
    f1 = lambda y: offset_y - offset_x + y
    f2 = lambda y: max - offset_x - offset_y - y
    if item_y >= penguinPositionY:
        if item_x > f1(item_y):
            return 'right'
        elif item_x < f2(item_y):
            return 'left'
        return 'bottom'
    else:
        if item_x > f2(item_y):
            return 'right'
        elif item_x < f1(item_y):
            return 'left'
        return 'top'


def chooseAction(body):
    action = PASS
    if can_shoot_enemy(body, in_front_of_me(body)):
        action = SHOOT
    else:
        if 'x' in body["enemies"][0].keys():
            action = moveTowardsPoint(body, body['enemies'][0]['x'], body['enemies'][0]['y'])
        elif body.get("bonusTiles", None):
            bonus_tiles = body['bonusTiles']
            bonus_tile_ranges = [num_moves_to_target(body, t['x'], t['y']) for t in bonus_tiles]
            print("bonues tile ranges", bonus_tile_ranges)
            closest_bonus_tile_index = bonus_tile_ranges.index(min(bonus_tile_ranges))
            closest_bonus_tile = bonus_tiles[closest_bonus_tile_index]
            print("closest tile", "x:", closest_bonus_tile['x'], "y:", closest_bonus_tile['y'])
            action = moveTowardsPoint(body, closest_bonus_tile['x'], closest_bonus_tile['y'])
        else:
            print("move to center of map")
            action = moveTowardsCenterOfMap(body)
    return action


env = os.environ
req_params_query = env['REQ_PARAMS_QUERY']
responseBody = open(env['res'], 'w')

response = {}
returnObject = {}
if req_params_query == "info":
    returnObject["name"] = "Pingu"
    returnObject["team"] = "Team Python"
elif req_params_query == "command":
    body = json.loads(open(env["req"], "r").read())
    returnObject["command"] = chooseAction(body)

response["body"] = returnObject
responseBody.write(json.dumps(response))
responseBody.close()
