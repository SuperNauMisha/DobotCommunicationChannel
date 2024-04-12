import time

import pydobot
from serial.tools import list_ports

# POSES = {'0': {'s': 'left', 'x': 0, 'y': -225.0, 'z': 55, 'r': -90},
#          '1': {'s': 'left', 'x': 0, 'y': -225.0, 'z': 145, 'r': -90},
#          '2': {'s': 'left', 'x': 0, 'y': -340, 'z': 40, 'r': -90},
#          '3': {'s': 'left', 'x': 0, 'y': -325.0, 'z': -60, 'r': -90},
#          '4': {'s': 'left', 'x': 0, 'y': -215.0, 'z': -60, 'r': -90},
#          '5': {'s': 'right', 'x': 0, 'y': 225.0, 'z': 55, 'r': 90},
#          '6': {'s': 'right', 'x': 0, 'y': 225.0, 'z': 145, 'r': 90},
#          '7': {'s': 'right', 'x': 0, 'y': 340.0, 'z': 40, 'r': 90},
#          '8': {'s': 'right', 'x': 0, 'y': 325.0, 'z': 127.0, 'r': 90},
#          '9': {'s': 'right', 'x': 0, 'y': 215.0, 'z': -60, 'r': 90}}

POSES = {'0': {'j1': -90.0, 'j2': 11.58477783203125, 'j3': 37.76371765136719},
         '1': {'j1': -90.0, 'j2': -0.304290771484375, 'j3': 1.2622052431106567},
         '2': {'j1': -90.0, 'j2': 54.439292907714844, 'j3': 18.293170928955078},
         '3': {'j1': -90.0, 'j2': 72.42658996582031, 'j3': 45.11402130126953},
         '4': {'j1': -90.0, 'j2': 54.04650115966797, 'j3': 83.9808349609375},
         '5': {'j1': 90.0, 'j2': 11.950546264648438, 'j3': 38.35327911376953},
         '6': {'j1': 90.0, 'j2': -0.2900543212890625, 'j3': 1.802386999130249},
         '7': {'j1': 90.0, 'j2': 54.85091781616211, 'j3': 19.04833984375},
         '8': {'j1': 90.0, 'j2': 41.898094177246094, 'j3': -5.440191745758057},
         '9': {'j1': 90.0, 'j2': 54.605735778808594, 'j3': 84.31359100341797}}

alphabet = {"a": "01",
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

# sides = {"right": {"x": 225.5, "y": 212, "z": 60},
#          "left": {"x": 225.5, "y": -200, "z": 60},
#          "mid": {"x": 225.5, "y": 0, "z": 60},
#          "end": {"x": 225.5, "y": 0, "z": -10}}

sides = {"right": {"j1": 43.2, "j2": 39.4, "j3": 24},
         "left": {"j1": -41.6, "j2": 36.2, "j3": 24},
         "mid": {"j1": 0, "j2": 10.5, "j3": 36},
         "end": {"j1": 0, "j2": 34, "j3": 64}}


# device.speed(1000, 1000)

# device.move_to(sides["right"]["x"], sides["right"]["y"],
#                sides["right"]["z"], sides["right"]["r"], wait=True)

# while True:
#     y = input("fdf: ")
#     device.move_to(POSES[y]["x"], POSES[y]["y"], POSES[y]["z"], POSES[y]["r"], wait=True)

def msg_out(word):
    available_ports = list_ports.comports()
    print(f'available ports: {[x.device for x in available_ports]}')
    port = available_ports[0].device

    device = pydobot.Dobot(port=port, verbose=False)

    word = word.lower()
    device.speed(1000, 1000)

    keys = []

    for i in word:
        keys.append(alphabet[i])

    for n, i in enumerate(keys):
        for j in i:
            device.angle(POSES[j]["j1"], POSES[j]["j2"], POSES[j]["j3"], wait=True)
            print(f"dobot came to position {j} in {i} for '{word[n]}' in {"".join(word)}")
            time.sleep(1.5)

    device.angle(sides["end"]["j1"], sides["end"]["j2"],
                 sides["end"]["j3"], wait=True)
    time.sleep(2.2)
    device.angle(sides["mid"]["j1"], sides["mid"]["j2"],
                 sides["mid"]["j3"], wait=False)
    print("dobot's message is over")
    print("".join(word))

    device.close()
