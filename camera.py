import cv2
import numpy as np
import time
cap = cv2.VideoCapture(0)


h_low = 0
h_high = 17
s_low = 187
s_high = 255
v_low = 104
v_high = 255
r_click_counter = 0
base = [640 // 2 - 20, 480 // 2 - 20, 640 // 2 + 20, 480 // 2 + 20]
kx = 2.1
ky = 3.1
kzon1x = 1.0
kzon2x = 1.1
kzon1y = 1.5
kzon2y = 1.5

ABC = {'01': 'a',
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


def current_time():
    return round(time.time() * 1000)
def changeHLow(value):
    global h_low
    h_low = value

def changeHHigh(value):
    global h_high
    h_high = value

def changeSLow(value):
    global s_low
    s_low = value

def changeSHigh(value):
    global s_high
    s_high = value

def changeVLow(value):
    global v_low
    v_low = value

def changeVHigh(value):
    global v_high
    v_high = value


def click(event, x, y, flags, param):
    global r_click_counter, rect, base
    if event == cv2.EVENT_RBUTTONDOWN:
        r_click_counter += 1
        if r_click_counter % 2 == 1:
            base[0], base[1] = x, y
        if r_click_counter % 2 == 0:
            base[2], base[3] = x, y
    if event == cv2.EVENT_LBUTTONUP:
        print(x, y)


def getCurrentZone(x, y):
    x0 = int(base[0] - abs(base[2] - base[0]) * kx)
    x1 = int(base[2] + abs(base[2] - base[0]) * kx)
    y0 = int(base[1] - abs(base[3] - base[1]) * ky)
    xzone1 = int(x0 + abs(base[2] - base[0]) * kzon1x)
    xzone2 = int(xzone1 + abs(base[2] - base[0]) * kzon2x)
    xzone4 = int(x1 - abs(base[2] - base[0]) * kzon1x)
    xzone3 = int(xzone4 - abs(base[2] - base[0]) * kzon2x)
    yzone1 = int(y0 + abs(base[3] - base[1]) * kzon1y)
    yzone2 = int(yzone1 + abs(base[3] - base[1]) * kzon2y)
    ans = -1
    # if y < y0 or y > base[3] or x < x0 or x > x1:
    #     ans = -1
    if y < yzone1:
        if x < xzone1:
            pass
        elif x < xzone2:
            ans = 1
        elif x < xzone3:
            pass
        elif x < xzone4:
            ans = 6
        elif x < x1:
            ans = 8
    elif y < yzone2:
        if x < xzone1:
            ans = 2
        elif x < xzone2:
            ans = 0
        elif x < xzone3:
            pass
        elif x < xzone4:
            ans = 5
        elif x < x1:
            ans = 7
    elif y <= base[3]:
        if x < xzone1:
            ans = 3
        elif x < xzone2:
            ans = 4
        elif x < xzone3:
            pass
        elif x < xzone4:
            ans = 9
        elif x < x1:
            pass
    return ans


cv2.namedWindow("trackbars")
cv2.namedWindow("frame")
cv2.createTrackbar("h low", "trackbars", h_low, 180, changeHLow)
cv2.createTrackbar("h high", "trackbars", h_high, 180, changeHHigh)
cv2.createTrackbar("s low", "trackbars", s_low, 255, changeSLow)
cv2.createTrackbar("s high", "trackbars", s_high, 255, changeSHigh)
cv2.createTrackbar("v low", "trackbars", v_low, 255, changeVLow)
cv2.createTrackbar("v high", "trackbars", v_high, 255, changeVHigh)

cv2.setMouseCallback("frame", click)
timer = current_time()
porog_time = 3000
old_zone = -1
letters = ""
start = False
while True:

    x0 = int(base[0] - abs(base[2] - base[0]) * kx)
    x1 = int(base[2] + abs(base[2] - base[0]) * kx)
    y0 = int(base[1] - abs(base[3] - base[1]) * ky)

    ret, frame = cap.read()
    try:
        cropframe = frame[y0:base[3], x0:x1]
        hsv_frame = cv2.cvtColor(cropframe, cv2.COLOR_BGR2HSV)
    except Exception:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_low = np.array([h_low, s_low, v_low])
    hsv_high = np.array([h_high, s_high, v_high])
    mask = cv2.inRange(hsv_frame, hsv_low, hsv_high)
    obj = cv2.moments(mask)

    cv2.rectangle(frame, (base[0], base[1]), (base[2], base[3]), (0, 255, 0), 3)
    cv2.rectangle(frame, (x0, y0), (x1, base[3]), (0, 255, 0), 3)
    xzone1 = int(x0 + abs(base[2] - base[0]) * kzon1x)
    cv2.line(frame, (xzone1,  y0), (xzone1, base[3]), (0, 255, 0), 3)
    xzone2 = int(xzone1 + abs(base[2] - base[0]) * kzon2x)
    cv2.line(frame, (xzone2, y0), (xzone2, base[3]), (0, 255, 0), 3)
    xzone4 = int(x1 - abs(base[2] - base[0]) * kzon1x)
    cv2.line(frame, (xzone4, y0), (xzone4, base[3]), (0, 255, 0), 3)
    xzone3 = int(xzone4 - abs(base[2] - base[0]) * kzon2x)
    cv2.line(frame, (xzone3, y0), (xzone3, base[3]), (0, 255, 0), 3)
    yzone1 = int(y0 + abs(base[3] - base[1]) * kzon1y)
    cv2.line(frame, (x0, yzone1), (x1, yzone1), (0, 255, 0), 3)
    yzone2 = int(yzone1 + abs(base[3] - base[1]) * kzon2y)
    cv2.line(frame, (x0, yzone2), (x1, yzone2), (0, 255, 0), 3)

    if obj["m00"]:
        cx = int(obj["m10"] / obj["m00"]) + x0
        cy = int(obj["m01"] / obj["m00"]) + y0
        cv2.circle(frame, (cx, cy), 20, (255, 0, 0), 3)
        if getCurrentZone(cx, cy) == old_zone and current_time() - timer > porog_time and getCurrentZone(cx, cy) != -1:
            letters += str(getCurrentZone(cx, cy))
            print(letters)
            if len(letters) == 2:
                print(ABC[letters])
                letters = ""
            timer = current_time()


        elif getCurrentZone(cx, cy) != old_zone:
            timer = current_time()
        # print(getCurrentZone(cx, cy), current_time())
        old_zone = getCurrentZone(cx, cy)
    cv2.imshow("frame", frame)
    cv2.imshow("hsv Frame", hsv_frame)
    cv2.imshow("mask", mask)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
