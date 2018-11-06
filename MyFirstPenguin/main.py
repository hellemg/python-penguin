if __name__ == '__main__':
    # Endrer MasterFlag for å få kjørt ønsket kode
    MasterFlag = {
        -1: 'Testspace'
    }[-1]
    if MasterFlag == 'Testspace':
        print('Welcome to testspace')
        my_x = 15
        my_y = 0
        dict = {"bonusTiles": [{
      "x": 12,
      "y": 5,
      "type": "weapon-range",
      "value": 1
  },
  {
      "x": 15,
      "y": 11,
      "type": "strength",
      "value": 3
  },
  {
      "x": 15,
      "y": -5,
      "type": "weapon-damage",
      "value": 4
  }]}
        enemies = dict["bonusTiles"]
        my_list = []
        for item in enemies:
            if item['x'] == my_x:
                item_y = item["y"]
                if item_y > 0:
                    my_list.append((item_y-my_y, "enemies"))


        print("my_list: ", my_list)