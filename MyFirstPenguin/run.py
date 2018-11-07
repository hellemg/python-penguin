import os
import json
import random
import math

from global_constants import *
from basic import *
from inFrontOfMe import *
from moves_required import *


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

    item_dir = coordinates_to_dir(body, pointX, pointY, penguinPositionX, penguinPositionY)

    # TODO: If penguin

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
    centerPointX = math.floor(body["mapWidth"] / 2)
    centerPointY = math.floor(body["mapHeight"] / 2)
    return moveTowardsPoint(body, centerPointX, centerPointY)


def coordinates_to_dir(body, item_x, item_y, penguinPositionX, penguinPositionY):
    centerPointX = math.floor(body["mapWidth"] / 2)
    centerPointY = math.floor(body["mapHeight"] / 2)
    # Defining offset to be positive for coords larger than centre
    # Larger x -> smaller right, Larger y -> smaller bottom
    offset_x = item_x - centerPointX
    offset_y = item_y - centerPointY
    max = centerPointY * 2 - offset_x - offset_y
    f1 = lambda y : y + offset_x - offset_y
    f2 = lambda y : max - offset_x - offset_y - y
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
            print(bonus_tiles)
            bonus_tile_ranges = [num_moves_to_target(body, t['x'], t['y']) for t in bonus_tiles]
            closest_bonus_tile_index = bonus_tile_ranges.index(min(bonus_tile_ranges))
            closest_bonus_tile = bonus_tiles[closest_bonus_tile_index]
            action = moveTowardsPoint(body, closest_bonus_tile['x'], closest_bonus_tile['y'])
        else:
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
