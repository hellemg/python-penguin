from . import globals

def in_front_of_me(body):
    """
    :return:Returns everything in front of me, sorted by proximity
    """
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]
    bodyDirection = body["you"]["direction"]
    