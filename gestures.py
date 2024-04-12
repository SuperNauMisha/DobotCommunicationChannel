import time

import pydobot
from serial.tools import list_ports

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device

device = pydobot.Dobot(port=port, verbose=False)

POSES = {'0': {'s': 'left', 'x': 0, 'y': -225.0, 'z': 55, 'r': -90},
         '1': {'s': 'left', 'x': 0, 'y': -225.0, 'z': 145, 'r': -90},
         '2': {'s': 'left', 'x': 0, 'y': -340, 'z': 40, 'r': -90},
         '3': {'s': 'left', 'x': 0, 'y': -325.0, 'z': -60, 'r': -90},
         '4': {'s': 'left', 'x': 0, 'y': -215.0, 'z': -60, 'r': -90},
         '5': {'s': 'right', 'x': 0, 'y': 225.0, 'z': 55, 'r': 90},
         '6': {'s': 'right', 'x': 0, 'y': 225.0, 'z': 145, 'r': 90},
         '7': {'s': 'right', 'x': 0, 'y': 340.0, 'z': 40, 'r': 90},
         '8': {'s': 'right', 'x': 0, 'y': 325.0, 'z': 127.0, 'r': 90},
         '9': {'s': 'right', 'x': 0, 'y': 215.0, 'z': -60, 'r': 90}}

CBA = {'01': 'a',
       '02': 'b',
       '03': 'c',
       '04': 'd',
       '10': 'e',
       '12': 'f',
       '13': 'g',
       '14': 'h',
       '20': 'i',
       '21': 'j',
       '23': 'k',
       '24': 'l',
       '30': 'm',
       '31': 'n',
       '32': 'o',
       '34': 'p',
       '40': 'q',
       '41': 'r',
       '42': 's',
       '43': 't',
       '56': 'u',
       '57': 'v',
       '58': 'w',
       '59': 'x',
       '65': 'y',
       '67': 'z',
       '68': ' ',
       '69': '.',
       '75': ',',
       '76': '!',
       '78': '?'}

ABC = {"a": "01",
       "b": "02",
       "c": "03",
       "d": "04",
       "e": "10",
       "f": "12",
       "g": "13",
       "h": "14",
       "i": "20",
       "j": "21",
       "k": "23",
       "l": "24",
       "m": "30",
       "n": "31",
       "o": "32",
       "p": "34",
       "q": "40",
       "r": "41",
       "s": "42",
       "t": "43",
       "u": "56",
       "v": "57",
       "w": "58",
       "x": "59",
       "y": "65",
       "z": "67",
       " ": "68",
       ".": "69",
       ",": "75",
       "!": "76",
       "?": "78"}

sides = {"right": {"x": 225.5, "y": 212, "z": 60, "r": 45},
         "left": {"x": 225.5, "y": -200, "z": 60, "r": -45},
         "mid": {"x": 225.5, "y": 0, "z": 60, "r": 0},
         "end": {"x": 225.5, "y": 0, "z": -40, "r": 0}}

device.speed(1000, 1000)

# device.move_to(sides["right"]["x"], sides["right"]["y"],
#                sides["right"]["z"], sides["right"]["r"], wait=True)
# while True:
#     y = input("fdf: ")
#     device.move_to(POSES[y]["x"], POSES[y]["y"], POSES[y]["z"], POSES[y]["r"], wait=True)

"""
Начало движения
"""
device.move_to(sides["mid"]["x"], sides["mid"]["y"],
               sides["mid"]["z"], sides["mid"]["r"], wait=True)
word = list(input("Enter the text: ").lower())
keys = []

for i in word:
    keys.append(ABC[i])

stor = POSES[keys[0][0]]["s"]

device.move_to(sides["mid"]["x"], sides["mid"]["y"],
               sides["mid"]["z"], sides["mid"]["r"], wait=False)
device.move_to(sides[stor]["x"], sides[stor]["y"],
               sides[stor]["z"], sides[stor]["r"], wait=False)

for i in keys:
    for j in i:
        if stor != POSES[j]["s"]:
            device.move_to(sides[stor]["x"], sides[stor]["y"],
                           sides[stor]["z"], sides[stor]["r"], wait=False)
            device.move_to(sides["mid"]["x"], sides["mid"]["y"],
                           sides["mid"]["z"], sides["mid"]["r"], wait=False)
            device.move_to(sides[POSES[j]["s"]]["x"], sides[POSES[j]["s"]]["y"],
                           sides[POSES[j]["s"]]["z"], sides[POSES[j]["s"]]["r"], wait=False)
            stor = POSES[j]["s"]
        device.move_to(POSES[j]["x"], POSES[j]["y"], POSES[j]["z"], POSES[j]["r"], wait=True)
        print(f"dobot came to position {j} in {i} for {CBA[i]} ({"".join(word)})")
        time.sleep(2.5)

device.move_to(sides[stor]["x"], sides[stor]["y"],
               sides[stor]["z"], sides[stor]["r"], wait=False)
device.move_to(sides["end"]["x"], sides["end"]["y"],
               sides["end"]["z"], sides["end"]["r"], wait=True)
time.sleep(2.5)
device.move_to(sides["mid"]["x"], sides["mid"]["y"],
               sides["mid"]["z"], sides["mid"]["r"], wait=False)
print("dobot's message is over")
print("".join(word))

device.close()
