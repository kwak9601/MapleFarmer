import serial
import time
import random
import datetime

arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)


def input(x):
    arduino.write(bytes(x, 'utf-8'))
    return


def rand_sleep(x):
    time.sleep(x - (random.uniform(-1, 1) / 500))


if __name__ == "__main__":
    def bazooka():

        input("KDLS")  # attack
        rand_sleep(0.08)
        input("KULS")


    def jumpattack_1():
        input("KDLA")
        rand_sleep(0.08)
        input("KULA")
        rand_sleep(0.15)

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
        rand_sleep(0.13)
        input("KULA")
        rand_sleep(0.07)

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


    def presskey(x):
        input("KD" + x)
        rand_sleep(0.05)
        input("KU" + x)


    def pool_maker():
        presskey("g")
        rand_sleep(0.43)
        return time.time()


    def monkey_buisness():
        print('monekey buisness')
        presskey("t")
        rand_sleep(0.55)

        presskey("a")
        rand_sleep(1)
        presskey('1')
        rand_sleep(0.34)
        presskey('f')
        rand_sleep(0.645)


        return time.time()


    def militia():
        print('monekey militia')

        presskey("DT")
        rand_sleep(0.45)
        return time.time()


    def whale():
        print('whale')

        presskey("q")
        rand_sleep(0.42)
        return time.time()


    def buff_up():
        print('buffing up')

        presskey("PD")
        rand_sleep(1.9)

        presskey("F1")
        rand_sleep(0.75)

        presskey("F3")
        rand_sleep(0.72)
        presskey("F5")
        rand_sleep(0.58)

        return time.time()


    jobs = {

        "monkey_buisness": {
            "func": monkey_buisness,
            "cd": 116,
            "last": None,
            "args": None
        },

        "buff_up": {
            "func": buff_up,
            "cd": 178,
            "last": None,
            "args": None
        },

        "militia": {
            "func": militia,
            "cd": 70,
            "last": None,
            "args": None
        },

        "whale": {
            "func": whale,
            "cd": 28,
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

    rand_sleep(2)

    count = 0

    while True:

        count = count + 1
        print("Count number: ", count)

        for job_name, job in jobs.items():

            if job["last"] is None or time.time() - job["last"] >= job["cd"]:
                if job["args"] is not None:
                    done_at = job["func"](*(job["args"]))
                else:
                    done_at = job["func"]()
                job["last"] = done_at

        input("KDAR")
        rand_sleep(0.1)

        if count % 2 == 0:
            jump_coco()

        else:
             jumpattack_1()

        jumpattack_2()
        jumpattack_1()
        input("KUAR")  # R1

        rand_sleep(0.3)
        input("KDa")
        rand_sleep(0.35)  # jumping to R2
        input("KUa")
        rand_sleep(0.1)
        input("KDAL")
        rand_sleep(0.03)
        input("KUAL")
        rand_sleep(0.03)
        input("KDLS")
        rand_sleep(0.01)
        input("KULS")  # R2

        rand_sleep(0.75)

        if count % 9 == 0:
            presskey("4")
            rand_sleep(0.67)

        if count % 11 == 0:
            input("KDAL")
            rand_sleep(1.123)
            input("KUAL")
            rand_sleep(0.245)

            input("KDa")
            rand_sleep(0.457)
            input("KUa")
            rand_sleep(1.32)

            input("KDLA")
            rand_sleep(0.08)
            input("KULA")
            rand_sleep(0.099)
            input("KDLA")
            rand_sleep((0.135))
            input("KULA")
            rand_sleep(1.5)





        input("KDa")
        rand_sleep(0.365)
        input("KUa")
        rand_sleep(0.1)

        input("KDAL")
        rand_sleep(0.03)
        input("KUAL")

        input("KDLS")
        rand_sleep(0.01)
        input("KULS")
        rand_sleep(0.8)  # R34

        # double jump start
        input("KDLA")
        time.sleep(0.08)
        input("KULA")
        time.sleep(0.08)

        input("KDLA")
        rand_sleep(0.12)
        input("KULA")
        rand_sleep(0.7)

        input("KDa")
        rand_sleep(0.41)
        input("KUa")
        rand_sleep(0.1)
        # Double jump end

        input("KDLS")
        rand_sleep(0.7)
        input("KULS")  # reset position
        rand_sleep(0.8)

        # print('end time: ', datetime.datetime.now())
