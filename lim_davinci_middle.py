import serial
import time
import random
import datetime

arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)


def input(x):
    arduino.write(bytes(x, 'utf-8'))
    return


def rand_sleep(x):
    time.sleep(x - (random.uniform(-1, 1) / 85))


def presskey(x):
    input("KD" + x)
    rand_sleep(0.08)
    input("KU" + x)

if __name__ == "__main__":


    def down_jump():

        input("KDAD")

        rand_sleep(0.1)

        input("KDc")

        rand_sleep(0.1)

        input("KUAD")

        rand_sleep(0.1)

        input("KUc")

        rand_sleep(0.1)



























    def look_right():
        input("KDAR")
        rand_sleep(0.025)
        input("KUAR")
        rand_sleep(0.03)


    def look_left():
        input("KDAL")
        rand_sleep(0.09)
        input("KUAL")
        rand_sleep(0.03)


    def bazooka():

        input("KDLS")  # attack
        rand_sleep(0.08)
        input("KULS")


    def jumpattack_1():
        input("KDLA")
        rand_sleep(0.06)
        input("KULA")
        rand_sleep(0.06)

        input("KDLA")
        rand_sleep(0.01)
        input("KDLS")
        rand_sleep(0.1)
        input("KULA")
        rand_sleep(0.3)
        input("KULS")
        rand_sleep(0.34)


    def jumpattack_2():
        input("KDLA")
        rand_sleep(0.12)
        input("KULA")
        rand_sleep(0.08)

        input("KDLA")
        rand_sleep(0.01)
        input("KDLS")
        rand_sleep(0.4)
        input("KULA")
        rand_sleep(0.2)
        input("KULS")
        rand_sleep(0.35)


    def jump_coco():

        input("KDLA")
        rand_sleep(0.08)
        input("KULA")
        rand_sleep(0.08)

        input("KDLA")
        rand_sleep(0.01)
        input("KDED")
        rand_sleep(0.39)
        input("KULA")
        rand_sleep(0.2)
        input("KUED")
        rand_sleep(0.48)


    def downjumpattack():
        input("KDAD")
        rand_sleep(0.1)
        input("KDLA")
        rand_sleep(0.01)
        input("KULA")
        rand_sleep(0.04)
        input("KUAD")

        rand_sleep(0.05)

        input("KDLS")  # attack
        rand_sleep(0.08)
        input("KULS")
        rand_sleep(0.1)


    def pool_maker():
        presskey("g")
        rand_sleep(0.43)
        return time.time()


    def monkey_buisness():
        print('monekey buisness')

        # totem?
        rand_sleep(0.12)
        presskey("9")
        rand_sleep(0.59)
        # ---

        presskey("t")
        rand_sleep(0.85)

        input("KDLA")  # double jump
        rand_sleep(0.08)
        input("KULA")
        rand_sleep(0.08)
        input("KDLA")
        rand_sleep(0.11)
        input("KULA")  # ---

        rand_sleep(0.8)

        input("KDLA")  # double jump
        rand_sleep(0.08)
        input("KULA")
        rand_sleep(0.08)
        input("KDLA")
        rand_sleep(0.11)
        input("KULA")  # --- at L1 corner
        rand_sleep(0.8)

        presskey('a')
        rand_sleep(0.977)

        input('KDAR')
        rand_sleep(0.5)

        presskey('f')
        rand_sleep(1.1)

        input("KDLA")  # double jump
        rand_sleep(0.07)
        input("KULA")
        rand_sleep(0.16)
        input("KDLA")
        rand_sleep(0.13)
        input("KULA")
        rand_sleep(1.8)

        input("KDLA")  # double jump
        rand_sleep(0.08)
        input("KULA")
        rand_sleep(0.08)
        input("KDLA")
        rand_sleep(0.11)
        input("KULA")
        rand_sleep(0.65)

        input("KDLA")  # double jump
        rand_sleep(0.08)
        input("KULA")
        rand_sleep(0.08)
        input("KDLA")
        rand_sleep(0.11)
        input("KULA")
        rand_sleep(0.68)  # at right corner R1

        presskey('a')
        rand_sleep(0.86)

        input('KUAR')
        rand_sleep(0.1)

        input('KDd')
        rand_sleep(0.768)
        input('KUd')
        time.sleep(random.randint(210, 250) / 100)

        presskey('a')
        time.sleep(random.randint(150, 220) / 100)

        presskey('a')
        time.sleep(random.randint(150, 220) / 100)

        presskey('DT')
        time.sleep(random.randint(80, 120) / 100)

        input('KDd')
        time.sleep(random.randint(65, 80) / 100)
        input('KUd')
        rand_sleep(1.5)

        return time.time()


    def militia():
        print('monekey militia')

        presskey("DT")
        rand_sleep(0.45)
        return time.time()


    def spider():
        print('spidering')

        presskey("v")
        rand_sleep(0.42)
        return time.time()


    def rainbow():
        print('rainbow')

        presskey("4")
        rand_sleep(0.368)
        return time.time()


    def buff_up():
        print('buffing up')

        presskey("PD")
        rand_sleep(1.9)

        presskey("F1")
        rand_sleep(0.952)

        presskey("F3")
        rand_sleep(0.984)
        presskey("F5")
        rand_sleep(0.846)

        return time.time()


    jobs = {

        "monkey_buisness": {
            "func": monkey_buisness,
            "cd": 95,
            "last": None,
            "args": None
        },

        "buff_up": {
            "func": buff_up,
            "cd": 175,
            "last": None,
            "args": None
        },

        "spider": {
            "func": spider,
            "cd": 245,
            "last": None,
            "args": None
        },

        "rainbow": {
            "func": rainbow,
            "cd": 87,
            "last": None,
            "args": None
        },

        "pool_maker": {
            "func": pool_maker,
            "cd": 58,
            "last": None,
            "args": None
        }
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


    def lim2_5():
        rand_sleep(0.4)
        input('KDa')
        rand_sleep(0.08)
        input('KUa')

        rand_sleep(0.15)
        look_right()
        look_right()
        time.sleep(0.15)
        look_right()

        input('KDa')
        rand_sleep(0.08)
        input('KUa')

        rand_sleep(0.430)

        look_right()

        input("KDLS")
        rand_sleep(2.023)
        input("KULS")  # back on floor

        rand_sleep(0.251)

        input('KDa')
        rand_sleep(0.09)
        input('KUa')

        time.sleep(0.415)
        look_left()

        input("KDLS")  # attack
        rand_sleep(1.125)
        input("KULS")
        rand_sleep(0.34)


    while True:

        print(datetime.datetime.now())

        count = count + 1
        print("Count number: ", count)

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
            lim2_5()

            if job["last"] is None or time.time() - job["last"] >= job["cd"]:
                if job["args"] is not None:
                    done_at = job["func"](*(job["args"]))
                else:
                    done_at = job["func"]()
                job["last"] = done_at
