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


def wallInBehindPenguin(body):
    xValueToCheckForWall = body["you"]["x"]
    yValueToCheckForWall = body["you"]["y"]
    bodyDirection = body["you"]["direction"]

    if bodyDirection == "top":
        yValueToCheckForWall += 1
    elif bodyDirection == "bottom":
        yValueToCheckForWall -= 1
    elif bodyDirection == "left":
        xValueToCheckForWall += 1
    elif bodyDirection == "right":
        xValueToCheckForWall -= 1
    return doesCellContainWall(body["walls"], xValueToCheckForWall, yValueToCheckForWall)


def moveTowardsPoint(body, pointX, pointY):
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]
    plannedAction = PASS
    bodyDirection = body["you"]["direction"]

    item_dir = coordinates_to_dir(body, pointX, pointY, penguinPositionX, penguinPositionY)

    dir_diff_x = direction_to_coord_tuple(item_dir)[0] + direction_to_coord_tuple(bodyDirection)[0]
    dir_diff_y = direction_to_coord_tuple(item_dir)[1] + direction_to_coord_tuple(bodyDirection)[1]

    print("Item dir:", item_dir)
    print("Item coord:", pointX, ",", pointY)
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


    elif (dir_diff_x == 0 and dir_diff_y == 0) and not wallInBehindPenguin(body):
        plannedAction = RETREAT

    else:
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
    dist_x = abs(penguinPositionX - item_x)
    dist_y = abs(penguinPositionY - item_y)
    if item_y >= penguinPositionY:
        print("Bottom half")
        if item_x < penguinPositionX:
            print("Left quarter")
            if dist_x > dist_y:
                return "left"
            else:
                return "bottom"
        else:
            print("Right quarter")
            if dist_x > dist_y:
                return "right"
            else:
                return "bottom"
    else:
        print("top half")
        if item_x < penguinPositionX:
            print("Left quarter")
            if dist_x > dist_y:
                return "left"
            else:
                return "top"
        else:
            print("Right quarter")
            if dist_x > dist_y:
                return "right"
            else:
                return "top"


def enemy_far(penguinPositionX, penguinPositionY, enemy_x, enemy_y, dist_tres = 6, diff_tres = 2):
    dist_x = abs(penguinPositionX - enemy_x)
    dist_y = abs(penguinPositionY - enemy_y)
    distance = dist_x + dist_y
    difference = abs(dist_x - dist_y)
    return distance > dist_tres and difference <= diff_tres


def chooseAction(body):
    action = PASS
    if can_shoot_enemy(body, in_front_of_me(body)):
        action = SHOOT
    else:
        if 'x' in body["enemies"][0].keys() and not enemy_far(body["you"]["x"], body["you"]["y"], body['enemies'][0]['x'], body['enemies'][0]['y']):
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
    returnObject["name"] = "Noot-noot"
    returnObject["team"] = "Tenkepause"
elif req_params_query == "command":
    body = json.loads(open(env["req"], "r").read())
    returnObject["command"] = chooseAction(body)

response["body"] = returnObject
responseBody.write(json.dumps(response))
responseBody.close()
