import serial
import time
import random
import datetime
import glob, os
from PIL import Image
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
yellow_dot = Image.open(os.getcwd() + "\\yellow_dot_4x4.png")
yellow_dot = cv.imread('yellow_dot_4x4.png')

rune_dot = os.getcwd() + "\\purple_dot.png"


def input(x):
    arduino.write(bytes(x, 'utf-8'))
    return


def rand_sleep(x):
    time.sleep(x - (random.uniform(-1, 1) / 85))


def presskey(x):
    input("KD" + x)
    rand_sleep(0.08)
    input("KU" + x)


def screenshot():

    rand_sleep(0.3)
    presskey('F10')
    rand_sleep(0.3)
    list_of_image = glob.glob("C:\\Nexon\\Library\\maplestory\\appdata\\*.jpg")
    print('list of image ', list_of_image)
    latest_image = cv.imread(max(list_of_image, key=os.path.getctime))
    cropped_image = latest_image[50:150, 10:300]  # sero, garo length
    # cv.imshow('image', cropped_image)
    cv.waitKey(0)
    os.remove(max(glob.glob("C:\\Nexon\\Library\\maplestory\\appdata\\*.jpg"), key=os.path.getctime))

    # cropped_image.show()
    return cropped_image


def get_coordinate(haystack, needle, printing=False):
    method = cv.TM_SQDIFF_NORMED
    result = cv.matchTemplate(needle, haystack, method)
    mn, _, mnLoc, _ = cv.minMaxLoc(result)
    MPx, MPy = mnLoc
    trows, tcols = needle.shape[:2]

    #print screenshot and location
    if printing:
        cv.rectangle(haystack, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 0, 255), 2)
        cv.imshow('output', haystack)
        cv.waitKey(0)

    # Deletion of screenshot

    return [MPx, MPy]



def move_to(x_coord_target, y_coord_target, x_threshold = 5, y_threshold = 7):

    list1 = [x_coord_target, y_coord_target]
    list2 = get_coordinate(screenshot(), yellow_dot)
    difference = []
    for list1_i, list2_i in zip(list1, list2):
        difference.append(list1_i - list2_i)
    dx, dy = difference
    print('Coordinate difference', dx, dy)

    while not(abs(dx) < x_threshold):
        print('dx dy is', dx, dy)
        if abs(dx) > 15:
            if dx < 0:
                for _ in range(int(round(abs(dx)/20))):
                    tp_left()
                    rand_sleep(0.3)
            else:
                for _ in range(int(round(dx/20))):
                    tp_right()
                    rand_sleep(0.3)

        else:
            if dx < 0:
                # walk_left()
                input('KDAL')
                time.sleep(abs(dx)/10) # 10 pixel per second walking speed
                input('KUAL')
            else:
                # walk_right()
                input('KDAR')
                time.sleep(dx/10) # 10 pixel per second walking speed
                input('KUAR')
        list1 = [x_coord_target, y_coord_target]
        list2 = get_coordinate(screenshot(), yellow_dot)
        difference = []
        for list1_i, list2_i in zip(list1, list2):
            difference.append(list1_i - list2_i)
        dx, dy = difference

    while not(abs(dy) < y_threshold):

        if abs(dy) > 10:
            if dy < 0:
                tp_up()
                rand_sleep(0.3)

            else:
                presskey('LA')
                tp_down()
                rand_sleep(0.3)

        list1 = [x_coord_target, y_coord_target]
        list2 = get_coordinate(screenshot(), yellow_dot)
        difference = []
        for list1_i, list2_i in zip(list1, list2):
            difference.append(list1_i - list2_i)
        dx, dy = difference

    return



if __name__ == "__main__":

    def look_right():
        input("KDAR")
        rand_sleep(0.025)
        input("KUAR")
        rand_sleep(0.03)


    def look_left():
        input("KDAL")
        rand_sleep(0.025)
        input("KUAL")
        rand_sleep(0.03)


    def tp_left():
        input("KDAL")

        rand_sleep(0.05)

        input("KDa")

        rand_sleep(0.08)
        presskey('LS')
        rand_sleep(0.07)

        input("KUAL")
        rand_sleep(0.1)
        input("KUa")
        rand_sleep(0.05)


    def tp_right():

        input("KDAR")

        rand_sleep(0.05)

        input("KDa")

        rand_sleep(0.08)
        presskey('LS')
        rand_sleep(0.07)

        input("KUAR")
        rand_sleep(0.1)
        input("KUa")
        rand_sleep(0.05)


    def tp_down():

        input("KDAD")

        rand_sleep(0.1)

        input("KDa")

        rand_sleep(0.08)
        presskey('LS')
        rand_sleep(0.07)

        input("KUAD")
        rand_sleep(0.1)
        input("KUa")
        rand_sleep(0.05)


    def tp_up():

        input("KDAU")

        rand_sleep(0.1)

        input("KDa")

        rand_sleep(0.08)
        presskey('LS')
        rand_sleep(0.07)

        input("KUAU")
        rand_sleep(0.1)
        input("KUa")
        rand_sleep(0.05)


    kishin_counter = 0
    kishin_time = 0


    def kishin():
        global kishin_counter
        global kishin_time

        print('kishin')

        presskey('IT')
        rand_sleep(0.1)

        if kishin_counter != 0:
            print('interval: ', (kishin_time - datetime.datetime.now()).total_seconds())
        kishin_time = datetime.datetime.now()

        kishin_counter += 1
        print('kishin counter = ', kishin_counter)

        presskey('LA')
        rand_sleep(0.15)
        tp_left()
        rand_sleep(0.3)
        presskey('LA')
        presskey('LA')
        rand_sleep(0.15)
        tp_left()
        rand_sleep(0.25)
        tp_left()
        rand_sleep(0.3)
        presskey("DT")
        kishin_time_return = time.time()
        rand_sleep(0.7)
        tp_right()
        rand_sleep(0.25)
        tp_down()
        rand_sleep(0.2)
        tp_right()
        rand_sleep(0.25)
        tp_right()
        rand_sleep(0.25)

        if kishin_counter % 5 == 0:
            presskey('v')
            rand_sleep(0.2)
            tp_right()
            rand_sleep(0.25)
            tp_right()
            rand_sleep(0.20)

            input('KDAR')
            rand_sleep(1.3)
            input('KUAR')
            rand_sleep(0.2)
            tp_left()
            rand_sleep(0.25)
            tp_left()
            rand_sleep(0.25)

        return kishin_time_return


    boss_count = 0


    def bossing():
        global boss_count
        # put eat meso every 3rd
        print('set boss ', 'boss count: ', boss_count % 3 + 1, '/3')
        presskey('IT')
        rand_sleep(0.1)
        boss_count += 1
        tp_down()
        rand_sleep(0.2)
        tp_left()
        rand_sleep(0.25)
        tp_left()
        rand_sleep(0.3)
        presskey('ED')
        presskey('ED')
        presskey('ED')

        bossing_time = time.time()
        rand_sleep(0.5)

        if boss_count % 3 == 0:
            presskey('5')
            rand_sleep(0.05)
            tp_left()
            rand_sleep(0.25)
            tp_left()
            rand_sleep(1)
            tp_right()
            rand_sleep(0.25)
            tp_right()
            rand_sleep(0.25)

        tp_right()
        rand_sleep(0.26)
        tp_right()
        rand_sleep(0.3)
        presskey('LA')
        rand_sleep(0.1)
        tp_up()
        rand_sleep(0.35)

        return bossing_time


    def yuki():
        rand_sleep(0.2)
        presskey('x')
        rand_sleep(0.6)
        return time.time()


    def domain():

        # TODO do position reset.

        print('domain')

        tp_down()
        rand_sleep(0.4)
        presskey('5')
        rand_sleep(0.4)
        presskey('IT')
        rand_sleep(0.3)
        input('KDg')
        rand_sleep(0.4)
        input('KDAR')
        rand_sleep(3.9)
        input('KUAR')
        rand_sleep(0.2)
        input('KUg')
        rand_sleep(0.3)
        tp_up()
        rand_sleep(0.2)
        tp_left()
        rand_sleep(0.2)
        tp_left()
        rand_sleep(0.3)

        return time.time()


    def balls():

        rand_sleep(0.2)
        presskey('x')
        rand_sleep(0.6)

        presskey('6')
        rand_sleep(1.28)
        presskey('7')
        rand_sleep(1.17)
        return time.time()


    def spider():
        print('spidering')

        presskey("v")
        rand_sleep(0.92)
        return time.time()


    def haku():
        print('summon haku')

        presskey("PU")
        rand_sleep(0.32)

        presskey('c')  # feed pet
        rand_sleep(0.2)

        return time.time()


    def yaksha():
        print('yaksha')

        rand_sleep(0.2)

        presskey('r')
        rand_sleep(1.3)

        return time.time()


    def buff_up():
        print('buffing up')
        presskey("v")
        rand_sleep(0.72)

        presskey('x')
        rand_sleep(0.65)

        presskey('7')
        rand_sleep(1.37)

        presskey("PD")
        rand_sleep(0.6)

        presskey("F1")
        rand_sleep(1.032)

        # presskey("F2")
        # rand_sleep(1.562)

        presskey("F3")
        presskey("F3")
        rand_sleep(1.384)

        presskey("F4")
        rand_sleep(1.554)

        presskey("F5")
        presskey("F5")
        presskey("F5")
        rand_sleep(1.346)

        presskey('HM')
        rand_sleep(0.65)

        presskey("PU")
        rand_sleep(0.32)

        presskey('c')  # feed pet
        rand_sleep(0.2)

        return time.time()


    jobs = {

        "buff_up": {
            "func": buff_up,
            "cd": 163,
            "last": None,
            "args": None
        },

        "bossing": {
            "func": bossing,
            "cd": 30,
            "last": None,
            "args": None
        },

        "kishin": {
            "func": kishin,
            "cd": 56,
            "last": None,
            "args": None
        },

        # "spider": {
        #     "func": spider,
        #     "cd": 245,
        #     "last": None,
        #     "args": None
        # },

        # "yuki": {
        #     "func": yuki,
        #     "cd": 81,
        #     "last": None,
        #     "args": None
        # },

        # "balls": {
        #     "func": balls,
        #     "cd": 100,
        #     "last": None,
        #     "args": None
        # },

        # "yaksha": {
        #     "func": yaksha,
        #     "cd": 250,
        #     "last": None,
        #     "args": None
        # },

        # "domain": {
        #     "func": domain,
        #     "cd": 220,
        #     "last": None,
        #     "args": None
        # },

        # "haku": {
        #     "func": haku,
        #     "cd": 480,
        #     "last": None,
        #     "args": None
        # },

    }

    from pynput import keyboard


    def on_press(key):
        global keyPressed
        try:
            k = key.char
        except:
            k = key.name

        if k in ["f11", "f12"]:
            keyPressed = k


    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    count = 0
    time.sleep(1)
    keyPressed = "f12"

    look_counter = 0


    def lab_SI1():
        global look_counter

        rand_sleep(0.2)
        presskey('2')
        rand_sleep(0.05)

        input("KDAD")
        rand_sleep(0.1)
        input("KDa")
        rand_sleep(0.1)
        input("KUAD")
        rand_sleep(0.1)
        input("KUa")

        rand_sleep(0.75)

        presskey('LS')
        presskey('LS')

        rand_sleep(0.55)

        if look_counter % 2 == 0:
            look_right()
        else:
            look_left()

        presskey('LS')
        presskey('LS')

        rand_sleep(0.35)

        input("KDAU")
        rand_sleep(0.1)
        input("KDa")
        rand_sleep(0.1)
        input("KUAU")
        rand_sleep(0.1)
        input("KUa")

        rand_sleep(0.25)

        presskey('LS')
        presskey('LS')

        move_to(138, 56)

        look_counter += 1


    while True:

        # print(datetime.datetime.now())

        if keyPressed == "f11":
            print("paused")
            while keyPressed != "f12":
                time.sleep(1)
            print("resuming")

        for job_name, job in jobs.items():

            if keyPressed != "f12":
                print("paused in skill")
                while keyPressed == "f11":
                    time.sleep(1)
                print("resuming")
            lab_SI1()

            if job["last"] is None or time.time() - job["last"] >= job["cd"]:
                if job["args"] is not None:
                    done_at = job["func"](*(job["args"]))
                else:
                    done_at = job["func"]()
                    print('done at: ', done_at)
                job["last"] = done_at

    # print("current coordinate is ", get_coordinate(screenshot(), yellow_dot))
