import serial
import time
import random
import datetime
import glob, os
from PIL import Image
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
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

    # print screenshot and location
    if printing:
        cv.rectangle(haystack, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 0, 255), 2)
        cv.imshow('output', haystack)
        cv.waitKey(0)

    # Deletion of screenshot

    return [MPx, MPy]


def move_to(x_coord_target, y_coord_target, x_threshold=5, y_threshold=7):
    list1 = [x_coord_target, y_coord_target]
    list2 = get_coordinate(screenshot(), yellow_dot)
    difference = []
    for list1_i, list2_i in zip(list1, list2):
        difference.append(list1_i - list2_i)
    dx, dy = difference
    print('Coordinate difference', dx, dy) # measures from current -> target. + means has to move right (+ axis)

    while not (abs(dx) < x_threshold):
        print('dx dy is', dx, dy)
        if abs(dx) > 30:
            if dx < 0:
                for _ in range(int(round(abs(dx) / 35))):
                    print('going left')
                    doublejump_left()
                    rand_sleep(0.3)
            else:
                for _ in range(int(round(dx / 35))):
                    print('going right')
                    doublejump_right()
                    rand_sleep(0.3)

        else:
            if dx < 0:
                # walk_left()
                input('KDAL')
                time.sleep(abs(dx) / 10)  # 10 pixel per second walking speed
                input('KUAL')
            else:
                # walk_right()
                input('KDAR')
                time.sleep(dx / 10)  # 10 pixel per second walking speed
                input('KUAR')
        list1 = [x_coord_target, y_coord_target]
        list2 = get_coordinate(screenshot(), yellow_dot)
        difference = []
        for list1_i, list2_i in zip(list1, list2):
            difference.append(list1_i - list2_i)
        dx, dy = difference

    while not (abs(dy) < y_threshold):

        if abs(dy) > 10:
            if dy < 0:
                print('jump up')
                jump_up()
                rand_sleep(1)

            else:
                print('jump down')
                jump_down_maybeladder()
                rand_sleep(1)

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

    def jump_down():
        rand_sleep(0.03)
        input('KDAD')
        rand_sleep(0.03)
        presskey('LA')
        rand_sleep(0.03)
        input('KUAD')
        rand_sleep(0.03)


    def doublejump_left():
        rand_sleep(0.3)
        look_left()
        look_left()
        presskey('LA')
        rand_sleep(0.2)
        presskey('LA')
        rand_sleep(1)
        rand_sleep(0.03)



    def doublejump_right():
        rand_sleep(0.1)
        look_right()
        look_right()
        presskey('LA')
        rand_sleep(0.2)
        presskey('LA')
        rand_sleep(1)
        rand_sleep(0.03)

    def jump_down_maybeladder():
        rand_sleep(0.1)
        input('KDAD')
        rand_sleep(0.03)
        presskey('LA')
        rand_sleep(0.03)
        input('KUAD')
        rand_sleep(0.03)
        # input('KDAL')
        # rand_sleep(0.03)
        # presskey('LA')
        # input('KUAL')


    def jump_up():

        presskey('a')
        rand_sleep(0.5)

    def spider():
        rand_sleep(0.2)
        presskey('v')
        rand_sleep(0.3)

    def monkey_buisness():
        presskey('t')
        rand_sleep(0.9)

        presskey('LA')
        rand_sleep(0.2)
        presskey('LA')
        rand_sleep(1.5)
        presskey('a')
        rand_sleep(1.2)

        presskey('LA')
        rand_sleep(0.2)
        presskey('a')
        rand_sleep(1)

        look_right()
        look_right()

        presskey('LA')
        rand_sleep(0.2)
        presskey('LA')
        rand_sleep(1.1)
        presskey('LA')
        rand_sleep(0.2)
        presskey('LA')

        rand_sleep(1.3)
        presskey('LA')
        rand_sleep(0.2)
        presskey('LA')

        rand_sleep(1.5)

        presskey('d')
        rand_sleep(0.6)
        presskey('d')

        rand_sleep(0.5)

        presskey('a')
        rand_sleep(1.2)

        presskey('d')
        rand_sleep(0.6)
        presskey('d')

        input('KDAL')
        rand_sleep(1)
        input('KUAL')

        return time.time()


    def buff_up():
        print('buffing up')

        presskey("PD")
        rand_sleep(1.9)

        presskey('F2')
        rand_sleep(0.6)

        presskey("F4")
        rand_sleep(0.952)
        presskey("F2")
        rand_sleep(0.952)

        presskey("F3")
        rand_sleep(0.984)
        presskey("F5")
        rand_sleep(0.846)
        presskey("5")
        rand_sleep(0.846)

        return time.time()



    jobs = {

        "buff_up": {
            "func": buff_up,
            "cd": 163,
            "last": None,
            "args": None
        },

        "monkey_buisness": {
            "func": monkey_buisness,
            "cd": 110,
            "last": None,
            "args": None
        },

        "spider": {
            "func": spider,
            "cd": 240,
            "last": None,
            "args": None
        },


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

    main_loop_timer = time.time()
    coco_timer = 0
    rainbow_timer = 0
    poolmaker_timer = 0
    naut_timer = 0
    icbm_timer = 0
    def burn_cer_lib_4():
        global main_loop_timer, coco_timer, rainbow_timer, poolmaker_timer, naut_timer, icbm_timer

        move_to(117, 65)
        if time.time() - coco_timer > 25:
            presskey('LA')
            rand_sleep(0.4)
            presskey('ED')
            coco_timer = time.time()
            rand_sleep(0.7)

        if time.time() - icbm_timer > 35:
            input('KDr')
            rand_sleep(0.5)
            input('KDAU')
            rand_sleep(0.3)
            input('KUAU')
            rand_sleep(0.1)
            input('KUr')
            rand_sleep(0.7)

        if time.time() - poolmaker_timer > 59:
            presskey('g')
            rand_sleep(0.8)
            poolmaker_timer = time.time()



        look_right()
        look_right()

        if time.time() - rainbow_timer > 85:
            presskey('4')
            rand_sleep(0.8)
            rainbow_timer = time.time()

        rand_sleep(0.3)
        presskey('a')
        presskey('a')

        rand_sleep(0.38)
        input("KDLS")
        rand_sleep(1.1)
        input("KULS")

        rand_sleep(0.5)
        presskey('LA')
        rand_sleep(0.1)
        presskey('a')
        rand_sleep(0.5)
        presskey('a') # top platform

        rand_sleep(0.8)
        presskey('LS')

        rand_sleep(0.8)
        look_left()
        look_left()

        rand_sleep(0.1)

        jump_down()
        rand_sleep(0.12)
        presskey('LS')

        rand_sleep(0.75)
        jump_down()
        rand_sleep(0.15)
        presskey('LS')

        rand_sleep(0.75)
        presskey('LS')
        rand_sleep(0.7)




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
            burn_cer_lib_4()

            if job["last"] is None or time.time() - job["last"] >= job["cd"]:
                if job["args"] is not None:
                    done_at = job["func"](*(job["args"]))
                else:
                    done_at = job["func"]()
                    print('done at: ', done_at)
                job["last"] = done_at

    # move_to(117, 65)

    # print("current coordinate is ", get_coordinate(screenshot(), yellow_dot))

