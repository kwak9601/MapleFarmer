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
    rand_sleep(0.05)
    input("KU" + x)


def screenshot():
    rand_sleep(0.3)
    presskey('F10')
    rand_sleep(0.3)
    list_of_image = glob.glob("C:\\Nexon\\Library\\maplestory\\appdata\\*.jpg")
    # print('list of image ', list_of_image)
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
        rand_sleep(0.05)

        input("KDAR")
        time.sleep(0.09)
        input("KUAR")
        rand_sleep(0.025)


    def look_left():
        rand_sleep(0.05)
        input("KDAL")
        time.sleep(0.09)
        input("KUAL")
        rand_sleep(0.03)

    def jump_down():
        rand_sleep(0.03)
        input('KDAD')
        rand_sleep(0.08)
        presskey('LA')
        time.sleep(0.08)
        input('KUAD')
        rand_sleep(0.03)


    def doublejump_left():
        look_left()
        rand_sleep(0.1)
        presskey('LA')
        time.sleep(0.2)
        presskey('LA')
        rand_sleep(0.03)



    def doublejump_right(delayed_jump = 0):

        look_right()
        rand_sleep(0.1)
        presskey('LA')
        time.sleep(0.2)
        time.sleep(delayed_jump)
        presskey('LA')
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


    def place_installs():
        print('Placing summons')
        presskey('e')
        rand_sleep(0.95)
        global pos_disturbed
        pos_disturbed = True
        look_right()
        rand_sleep(0.1)
        presskey('a')
        doublejump_right()
        presskey('LS')

        rand_sleep(0.5)
        doublejump_right(delayed_jump=0.2)

        rand_sleep(0.7)
        look_left()
        look_left()
        rand_sleep(0.4)
        presskey('ED')

        rand_sleep(0.4)
        jump_down_maybeladder()
        rand_sleep(0.7)
        presskey('ED')
        rand_sleep(0.4)
        jump_down()
        input('KDAL')
        rand_sleep(0.2)
        presskey('LA')
        rand_sleep(0.05)
        presskey('LA')
        presskey('LA')
        rand_sleep(0.2)
        input('KUAL')
        rand_sleep(0.7)
        presskey('DT')
        rand_sleep(0.6)
        presskey('a')
        doublejump_left()
        rand_sleep(0.5)
        presskey('q')
        rand_sleep(0.6)

        return time.time()

    pos_disturbed = False
    r_counter = 0
    def burn_cer_ECRB2():
        global barage_counter, r_counter
        r_counter += 1
        if barage_counter % 3 == 1:
            presskey('v')
            rand_sleep(0.8)

        global pos_disturbed

        if pos_disturbed == True:
            move_to(102, 58)
            pos_disturbed = False
            rand_sleep(0.3)

        presskey('a')
        rand_sleep(0.2)
        look_left()
        look_left()

        rand_sleep(0.3)
        input('KDLS')
        rand_sleep(0.8)
        input('KULS')
        rand_sleep(0.48)
        jump_down()
        time.sleep(0.35)
        presskey('LS')
        rand_sleep(0.6)

        presskey('LA')
        look_right()
        rand_sleep(0.1)
        look_right()
        presskey('LS')
        rand_sleep(0.6)
        presskey('a')
        rand_sleep(0.5)
        presskey('LS')
        rand_sleep(0.7)

        if r_counter % 4 == 0:
            presskey('r')
            rand_sleep(0.8)

    def spider():
        print('v - spider')
        presskey('v')
        rand_sleep(0.8)
        return time.time()


    barage_counter = 0
    def w_bullet_barage():
        global barage_counter, r_counter
        barage_counter += 1
        r_counter += 1
        print('W - Bullet barage')
        global pos_disturbed
        presskey('w')
        rand_sleep(1)
        doublejump_left()

        rand_sleep(1.5)
        doublejump_right()
        rand_sleep(1.5)
        doublejump_right()
        rand_sleep(1.4)
        doublejump_left()
        rand_sleep(1.8)

        pos_disturbed = True

        return time.time()

    # def e_death_trigger():
    #
    #     return time.time()

    def r_target_lock():
        print('R, Q -  target lock + nautilus')
        presskey('r')
        rand_sleep(1.5)
        presskey('q')
        rand_sleep(0.95)
        return time.time()


    def buff_up():
        print('buffing up')
        presskey('6')
        rand_sleep(0.95)
        presskey('t')
        rand_sleep(0.85)
        presskey('4')
        rand_sleep(0.65)
        presskey('9')
        rand_sleep(0.2)
        return time.time()


    jobs = {

        "buff_up": {
            "func": buff_up,
            "cd": 150,
            "last": None,
            "args": None
        },


        "place_installs": {
            "func": place_installs,
            "cd": 45,
            "last": None,
            "args": None
        },

        # "r_target_lock": {
        #     "func": r_target_lock,
        #     "cd": 28,
        #     "last": None,
        #     "args": None
        # },

        "w_bullet_barrage": {
            "func": w_bullet_barage,
            "cd": 70,
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





    def lab_SI1():
        pass


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
            burn_cer_ECRB2()

            if job["last"] is None or time.time() - job["last"] >= job["cd"]:
                if job["args"] is not None:
                    done_at = job["func"](*(job["args"]))
                else:
                    done_at = job["func"]()
                    print('done at: ', done_at)
                job["last"] = done_at

    # move_to(101, 58)
    # time.sleep(1)
    # w_bullet_barage()

    print("current coordinate is ", get_coordinate(screenshot(), yellow_dot))
