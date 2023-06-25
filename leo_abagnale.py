from ahk import AHK  ############################

from enum import Enum
from position import Position
from model.classify import classify_image

import time, os
import random
import pyautogui
import numpy
import cv2
import tensorflow

import threading

from datetime import datetime
import sys  ### changed added

import serial

arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    # time.sleep(0.05)
    # data = arduino.readline()
    return



sys.setrecursionlimit(3000)  ### changed added

_print = print


def print(*args, **kwargs):
    _print(datetime.now(), end="\t")
    _print(*args, **kwargs)


RESOLUTION = (1366, 768)

TELEPORT_THRESHOLD = 17
JUMP_THRESHOLD_Y = 20
X_THRESHOLD = 3
Y_THRESHOLD = 2

MOVE_MODE = "X_FIRST"
# MOVE_MODE = "Y_FIRST"

MODEL_PATH = os.path.join(
    os.getcwd(),
    "model",
    "latest_model.h5")

MODEL = tensorflow.keras.models.load_model(MODEL_PATH)

ahk = AHK()


class Status(Enum):
    MOVING = "MOVING"
    IDLE = "IDLE"


class Direction(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    DOWN = "Down"
    UP = "Up"
    NONE = "NONE"

    def __str__(self):
        return self.value


class Rune:
    _image_location = os.getcwd() + "\\purple_dot_smaller.png"
    COUNT = 0


class Character:
    MY_POSITION = Position()
    MAPLE_WINDOW = None

    _instance = None
    _image_location = os.getcwd() + "\\yellow_dot_smaller.png"
    LOCK = threading.Lock()

    def __init__(self):
        if Character._instance is not None:
            self = Character._instance
            return
        self._status = Status.IDLE
        self._direction = Direction.NONE
        self.position = Position()
        self.last_position = None
        self.esc_tried = False

        Character._instance = self

    def get_maple_window(self):
        if Character.MAPLE_WINDOW is None:
            windows = list(filter(lambda window: window.title == b'MapleStory', ahk.windows()))
            Character.MAPLE_WINDOW = sorted(windows, key=lambda x: x.width)[-1]
        return Character.MAPLE_WINDOW

    def get_image_position(self, image, relative=True, can_fail=True):
        window = self.get_maple_window()
        window.activate()
        lower_bound = window.position[0] + 200, window.position[1] + 200
        result = ahk.image_search(image, window.position, lower_bound)
        if result is None:
            # Retry
            time.sleep(1)
            result = ahk.image_search(image, window.position, lower_bound)
            if result is None and not can_fail:
                raise Exception(f"Could not find image: {image} on screen")
            else:
                return None
        if relative:
            result = result[0] - window.position[0], result[1] - window.position[1]
        self.position.set(result)
        # print(f"Image @ {self.position}")
        return self.position

    def get_character_position(self, relative=True):
        pos = self.get_image_position(Character._image_location, relative)
        return pos

    def get_rune_position(self, relative=True):
        return self.get_image_position(Rune._image_location, relative, can_fail=True)

    def stop(self):
        if self._status == Status.IDLE:
            return
        self.get_maple_window().activate()
        ahk.key_up(self._direction.value)
        self._status = Status.IDLE

    def teleport(self, direction=None, key="j"):
        if direction is not None:
            self.move(direction)
        # ahk.key_down(key)
        # time.sleep(0.2)
        # ahk.key_up(key)
        ahk.key_press(key)

        if direction is not None:
            time.sleep(random.randint(50, 120) / 100)
            ahk.key_up(direction.value)

    def jump(self, direction=Direction.NONE):
        if direction is not None and direction != Direction.NONE:
            self.move(direction)
            time.sleep(random.randint(50, 70) / 1000)

        ahk.key_press("j")
        if direction is not None and direction != Direction.NONE:
            time.sleep(random.randint(80, 100) / 1000)
            self.stop()

    def jump_teleport(self, direction=None):
        # direction = Direction.DOWN
        if direction != Direction.UP:
            if direction is not None and direction != Direction.NONE:
                ahk.key_down(direction.value)
                time.sleep(random.randint(50, 70) / 1000)
        ahk.key_down("j")
        if direction == Direction.UP:
            time.sleep(0.1)
            ahk.key_down(direction.value)
            ############ ahk.key_down("w")
            time.sleep(random.randint(70, 100) / 1000)
            ########### ahk.key_up("w")
        ahk.key_up("j", blocking=False)
        time.sleep(0.06)
        self.teleport()
        if direction is not None:
            time.sleep(random.randint(50, 80) / 100)
            ahk.key_up(direction.value)

    def move(self, direction, teleport=False, jump=False):
        self.get_maple_window().activate()
        if self._direction != direction:
            self.stop()

        if direction in [Direction.LEFT, Direction.RIGHT]:
            self.get_maple_window().activate()
            ahk.key_down(direction.value)
            self._direction = direction
            self._status = Status.MOVING
            if teleport:
                # self.jump_teleport()
                self.teleport()

        else:
            if direction == Direction.UP:

                ahk.key_press('j') #jump to reach up there
                time.sleep(0.2)
                ahk.key_press("5")
                time.sleep(1.5)
                return




            if random.randint(0, 8) == -1:
                self.jump(direction)
            else:
                self.jump_teleport(direction)
                # self.teleport(direction)

    def unblock(self):
        window = self.get_maple_window()
        region = (window.position[0] + window.width - RESOLUTION[0],
                  window.position[1] + window.height - RESOLUTION[1]) + RESOLUTION
        filename = f"MapleStory-Blocked-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jpg"
        image = pyautogui.screenshot(region=region).convert(mode="RGB")
        # image.save(os.path.join(
        #     ".",
        #     "screenshots",
        #     "blocked",
        #     filename))
        pos = self.get_character_position()
        # if pos is not None:
        x, y = pos

        # if y not in Target.BASES:
        print("jumping")
        self.stop()
        self.jump(Direction.RIGHT)
        # time.sleep(random.randint(60, 100) / 100)
        new_pos = self.get_character_position()
        if new_pos is not None:
            new_x, new_y = new_pos
            if new_x != x or new_y != y:
                return
        print("unblocking")

        ####### ahk.key_press("Esc")
        # print("esc")
        # time.sleep(random.randint(10, 20)/100)

        for _ in range(0, 51):
            print(f"{_}: moving l rs")
            directions = [Direction.RIGHT, Direction.LEFT]
            # random.shuffle(directions)
            for d in directions:
                ahk.key_down(d.value)
                time.sleep(random.randint(20, 30) / 1000)
                ahk.key_up(d.value)
                time.sleep(random.randint(20, 30) / 1000)
            if _ % 10 == 0:
                new_pos = self.get_character_position()
                if new_pos is not None:
                    new_x, new_y = new_pos
                    if new_x != x or new_y != y:
                        return
        self.stop()
        ahk.key_press("Esc")
        print("esc")
        time.sleep(random.randint(30, 40) / 1000)

    def move_to(self, x, y=None, relative=True, x_threshold=X_THRESHOLD, y_threshold=Y_THRESHOLD):
        # self.key_reset()
        if y is None:
            y = x[1]
            x = x[0]
        not_move_count = 0
        direction, teleport, jump, (last_x, last_y) = self.get_target_direction(x, y, relative, x_threshold,
                                                                                y_threshold)
        while direction != Direction.NONE:
            global keyPressed
            if keyPressed == "f11":
                print("paused in move_to")
                while keyPressed == "f11":  #### changed
                    time.sleep(1)
                print("resuming")
            self.move(direction, teleport=teleport, jump=jump)
            direction, teleport, jump, (now_x, now_y) = self.get_target_direction(x, y, relative, x_threshold,
                                                                                  y_threshold)
            if direction != Direction.NONE and (last_x, last_y) == (now_x, now_y):
                not_move_count += 1
                if not_move_count >= 3:
                    self.unblock()
                    not_move_count = 0
                print(f"not moving count: {not_move_count}")
            else:
                self.esc_tried = False
                not_move_count = 0
            last_x, last_y = now_x, now_y

        char.stop()

    def key_reset(self):
        window = self.get_maple_window()
        window.activate()
        window.wait_active()
        for k in ["l", "j", "F1", "F2", "r", "a", "s", "e", "1", "2", "3", "4", "9", "F7", "F8", "F3", "F4", "d",
                  "PgDn", "LShift"]:
            ahk.key_up(k, blocking=False)
        ahk.key_up(Direction.RIGHT.value)
        ahk.key_up(Direction.LEFT.value)
        ahk.key_up(Direction.DOWN.value)
        ahk.key_up(Direction.UP.value)
        time.sleep(0.05)

    def get_dx_dy(self, x, y, relative=True):
        pos = self.get_character_position(relative)
        while pos is None:
            time.sleep(2)
            pos = self.get_character_position(relative)
        char_x, char_y = pos
        dx = char_x - x
        dy = char_y - y
        return dx, dy, pos

    def get_target_direction(self, x, y, relative=True, x_threshold=X_THRESHOLD, y_threshold=Y_THRESHOLD):
        dx, dy, pos = self.get_dx_dy(x, y, relative)

        if MOVE_MODE == "X_FIRST":
            if abs(dx) > x_threshold:
                return (
                    Direction.LEFT if dx > 0 else Direction.RIGHT,
                    abs(dx) > TELEPORT_THRESHOLD,
                    False,
                    pos)
            if abs(dy) > y_threshold:
                return (
                    Direction.UP if dy > 0 else Direction.DOWN,
                    False,
                    dy > JUMP_THRESHOLD_Y,
                    pos)
        else:
            if abs(dy) > y_threshold:
                return (
                    Direction.UP if dy > 0 else Direction.DOWN,
                    False,
                    False,
                    pos)
            if abs(dx) > x_threshold:
                return (
                    Direction.LEFT if dx > 0 else Direction.RIGHT,
                    abs(dx) > TELEPORT_THRESHOLD,
                    dy > JUMP_THRESHOLD_Y,
                    pos)

        return Direction.NONE, None, False, pos

    def break_rune(self, relative=True):
        rune_pos = self.get_rune_position(relative)
        if rune_pos is None:
            print("No rune found")
            return True
        print(f"rune @ {rune_pos}")
        self.move_to(rune_pos.x, rune_pos.y, relative, x_threshold=3)
        self.stop()
        time.sleep(random.randint(30, 50) / 1000)
        ahk.key_press("space", blocking=True)
        time.sleep(random.randint(90, 120) / 100)
        window = self.get_maple_window()

        region = (window.position[0] + window.width - RESOLUTION[0],
                  window.position[1] + window.height - RESOLUTION[1]) + RESOLUTION
        image = pyautogui.screenshot(region=region).convert(mode="RGB")
        # image.save(os.path.join(
        #     ".",
        #     "screenshots",
        #     "runes",
        #     f"MapleStory-Rune-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jpg"))
        open_cv_image = numpy.array(image)[:, :, ::-1].copy()
        result = classify_image(open_cv_image, MODEL)

        print(f"Prediction: {result}")
        for key_name in result:
            ahk.key_press(key_name.capitalize())
            time.sleep(random.randint(30, 50) / 100)

        return self.get_rune_position(relative) is None

    def use_skill(self, key, sleep=True):
        for _ in range(random.randint(3, 6)):
            ahk.key_press(key)
            if sleep:
                time.sleep(random.randint(40, 50) / 1000)

    def use_shiki(self, direction=Direction.LEFT, count=7):
        ahk.key_down(direction.value)
        time.sleep(random.randint(80, 100) / 1000)
        ahk.key_down('LShift')
        count = random.randint(count, count + 3)
        for _ in range(count):
            time.sleep(random.randint(30, 50) / 1000)
            ahk.key_up('LShift')
            time.sleep(random.randint(40, 70) / 1000)
            ahk.key_down('LShift')
            if _ == count // 2:
                ahk.key_up(direction.value)
                time.sleep(0.1)
                direction = Direction.LEFT if direction == Direction.RIGHT else Direction.RIGHT
                ahk.key_down(direction.value)
                time.sleep(0.1)

        time.sleep(random.randint(30, 50) / 1000)
        ahk.key_up('LShift')
        time.sleep(random.randint(30, 50) / 1000)
        ahk.key_up(direction.value)

    def use_exo(self):
        self.use_skill("2")

    def set_kishin(self):
        self.use_skill("Del")

    def set_boss(self, direction):
        self.move(direction)
        time.sleep(random.randint(30, 80) / 1000)
        self.stop()
        self.use_skill("End")
        time.sleep(0.2)

    def set_pink_ball(self):
        self.use_skill("F7")

    def set_blue_ball(self):
        self.use_skill("F8")

    def buff_up(self):
        time.sleep(random.randint(80, 100) / 100)
        self.use_skill("F1")
        time.sleep(random.randint(75, 85) / 100)
        self.use_skill("F2")
        time.sleep(random.randint(77, 85) / 100)
        self.use_skill("F3")
        time.sleep(random.randint(50, 80) / 100)
        self.use_skill("F4")
        time.sleep(random.randint(75, 85) / 100)
        self.use_skill("PgDn")
        time.sleep(random.randint(130, 140) / 100)
        self.use_skill("F5")
        time.sleep(random.randint(100, 105) / 100)

    def feed_pet(self):
        for _ in range(6):
            self.use_skill("c")
            time.sleep(random.randint(50, 70) / 100)

    def battle_stat(self):
        window = self.get_maple_window()
        region = (window.position[0] + window.width - RESOLUTION[0],
                  window.position[1] + window.height - RESOLUTION[1]) + RESOLUTION
        filename = f"MapleStory-BattleStat-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jpg"
        image = pyautogui.screenshot(region=region).convert(mode="RGB")
        image.save(os.path.join(
            ".",
            "screenshots",
            "battlestats",
            filename))
        ahk.key_press(",")
        time.sleep(random.randint(100, 200) / 1000)
        ahk.key_press("Enter")
        return filename


def timeit(f):
    import time
    start_time = time.time()
    f()
    return time.time() - start_time


class Outlaw:
    EXO_POSITION = (152, 107)
    BOSS_POSITION = (110, 109)  # TO LEFT
    KISHIN_POSITION = (90, 122)

    MESO_ROUTE = [(140, 94), (150, 94), (160, 122), (42, 122),
                  (49, 104), (44, 88), (59, 88), (63, 104), (79, 104), (110, 96)]


class CFE:
    EXO_POSITION = (63, 107)
    BOSS_POSITION = (95, 122)  # TO RIGHT
    BOSS_DIRECCTION = Direction.RIGHT
    KISHIN_POSITION = (65, 88)
    DOMAIN_POSITION = (65, 122)
    DOMAIN_DIRECTION = Direction.RIGHT
    SHIKI_DIRECTION = Direction.RIGHT

    MESO_ROUTE = [
        # (72, 88),  # Left Top
        # (87, 87),  # Middle Top
        (112, 102),  # middle middle
        (145, 122),  # Right Bottom
        (57, 122),  # Left Bottom
    ]


class OUTLAW3:
    EXO_POSITION = (140, 117)  # TO RIGHT
    SHIKI_DIRECTION = Direction.RIGHT
    BOSS_POSITION = (112, 117)  # TO RIGHT
    BOSS_DIRECCTION = Direction.LEFT
    KISHIN_POSITION = (109, 130)
    DOMAIN_POSITION = (127, 130)

    MESO_ROUTE = [
        (163, 116),  # Right Middle
        (160, 102),  # Right Top
        (54, 99),  # Left Top
        (72, 113),  # Middle Left
        (112, 101),  # middle middle
        (55, 130),  # Left Bottom
    ]


class SIDEPATH:
    EXO_POSITION = (161, 106)
    BOSS_POSITION = (119, 138)
    BOSS_DIRECCTION = Direction.LEFT
    KISHIN_POSITION = (79, 106)
    DOMAIN_POSITION = (79, 132)
    DOMAIN_DIRECTION = Direction.RIGHT
    SHIKI_DIRECTION = Direction.LEFT

    MESO_ROUTE = [
        (55, 106),  # Left Top
        (185, 106),  # Right Top
        (185, 132),  # Right Bot
        (55, 132),  # Left BOT
    ]

    BASES = [110, 132, 138, 106]


class LCUP:  #################################################
    EXO_POSITION = (156, 109)
    BOSS_POSITION = (120, 137)
    BOSS_DIRECCTION = Direction.LEFT
    KISHIN_POSITION = (90, 109)
    DOMAIN_POSITION = (161, 137)
    DOMAIN_DIRECTION = Direction.LEFT
    SHIKI_DIRECTION = Direction.LEFT
    SHIKI_POSITION = (156, 137)

    MESO_ROUTE = [
        # (182, 109),  # Right Top
        (72, 109),  # Left Top
        (72, 137),  # Left Bot
        # (182, 137),  # Right BOT
    ]

    BASES = [109, 137]


##########################################################

class LCUP_DESKTOP:
    EXO_POSITION = (156, 102)
    BOSS_POSITION = (120, 131)
    BOSS_DIRECCTION = Direction.LEFT
    KISHIN_POSITION = (90, 102)
    DOMAIN_POSITION = (161, 131)
    DOMAIN_DIRECTION = Direction.LEFT
    SHIKI_DIRECTION = Direction.LEFT
    SHIKI_POSITION = (156, 131)

    MESO_ROUTE = [
        # (182, 102),  # Right Top
        (72, 102),  # Left Top
        (72, 131),  # Left Bot
        # (190, 131),  # Right BOT
    ]

    BASES = [102, 131]


class CLP:
    EXO_POSITION = (61, 123)
    BOSS_POSITION = (59, 138)
    BOSS_DIRECCTION = Direction.RIGHT
    KISHIN_POSITION = (91, 108)
    DOMAIN_POSITION = (83, 138)
    DOMAIN_DIRECTION = Direction.LEFT
    SHIKI_DIRECTION = Direction.LEFT

    MESO_ROUTE = [
        (35, 123),  # Left Mid
        (117, 138),  # Right Bot
        # (177, 102),  # Right Bot
    ]

    BASES = [123, 138, 108]


char = Character()
lock = threading.Lock()


def place_boss(direction):
    lock.acquire()
    print("placing boss")
    char.move_to(Target.BOSS_POSITION)
    char.set_boss(direction)
    time.sleep(random.randint(20, 25) / 100)
    done_at = time.time()
    lock.release()
    return done_at
    # threading.Timer(29, place_boss, args=[direction]).start()


def place_kishin():
    lock.acquire()
    print("placing kishin")
    char.move_to(Target.KISHIN_POSITION)
    time.sleep(random.randint(70, 120) / 100)
    char.set_kishin()
    time.sleep(random.randint(70, 140) / 100)
    done_at = time.time()
    lock.release()
    return done_at
    # threading.Timer(57, place_kishin).start()


def use_spider():
    lock.acquire()
    print("using spider")
    char.move_to(Target.DOMAIN_POSITION)
    time.sleep(random.randint(80, 100) / 1000)
    char.use_skill("0")
    time.sleep(random.randint(70, 100) / 1000)
    done_at = time.time()
    lock.release()
    return done_at


meso_count = 0


def get_mesos():
    # lock.acquire()
    # char.move_to(Target.EXO_POSITION)  # move from top
    char.move_to(190, 131)  # LCUP specific
    # lock.release()
    global meso_count
    meso_count += 1
    if meso_count % 2 == 0:
        use_domain(Target.DOMAIN_DIRECTION)
    else:
        use_spider()
        char.use_skill("Insert")

    done_at = time.time()
    meso_locations = Target.MESO_ROUTE

    def sort_func(xy):
        x, y = xy
        if y == cy:
            return abs(cx - x)
        return abs(cx - x) + 200

    lock.acquire()
    routes = meso_locations[:]
    cx, cy = char.get_character_position()
    routes.sort(key=sort_func)
    print(f"char @ {cx, cy}")
    # for x,y in routes:
    char.use_skill("1", sleep=False)
    while len(routes) >= 1:
        x, y = routes.pop(0)
        cx, cy = x, y
        routes.sort(key=sort_func)
        print(f"getting meso @ {(x, y)}")
        # threading.Thread(target=char.use_skill, args=("d",), kwargs = {"sleep":False}).run()
        time.sleep(random.randint(150, 200) / 1000)
        # time.sleep(random.randint(70, 120) / 100)
        char.move_to(x, y, x_threshold=3)
    char.use_skill("Insert")
    char.use_skill("7")
    lock.release()
    # threading.Timer(85, get_mesos).start()
    return done_at


def buff():
    lock.acquire()
    print("buffing")
    done_at = time.time()
    char.buff_up()
    lock.release()
    return done_at
    # threading.Timer(177, buff).start()


exo_count = 0


def use_exo(direction=Direction.LEFT, jump=True):
    lock.acquire()
    global exo_count

    print(f"exoing {exo_count}")
    target_direction, _, _, _ = char.get_target_direction(*Target.EXO_POSITION, x_threshold=8)
    if target_direction != Direction.NONE:
        char.teleport()
        char.move_to(Target.EXO_POSITION)
    exo_count += 1
    if exo_count % 5 == 0:
        if exo_count % 10 == 0:
            char.set_pink_ball()
            char.set_blue_ball()
    if jump:
        char.jump()
        time.sleep(0.19)
    char.use_exo()
    time.sleep(random.randint(40, 45) / 100)
    char.use_shiki(direction=direction)
    # char.move_to(Target.SHIKI_POSITION)
    # char.use_shiki(direction=direction)
    lock.release()
    # threading.Timer(0.5, use_exo, args=[direction]).start()


def use_domain(direction=Direction.RIGHT):
    lock.acquire()
    print("using domain")
    char.move_to(Target.DOMAIN_POSITION)
    time.sleep(random.randint(80, 100) / 1000)
    char.use_skill("5")
    time.sleep(random.randint(30, 80) / 100)
    char.use_skill("r")  # ghost
    time.sleep(random.randint(30, 80) / 100)
    done_at = time.time()
    char.use_skill("Insert")
    time.sleep(0.4)
    ahk.key_down("l")  # v charm
    time.sleep(random.randint(70, 100) / 1000)
    char.move(direction)
    ahk.key_down(direction.value)
    time.sleep(random.randint(500, 555) / 100)
    # char.stop()
    # char.move(Direction.RIGHT if direction == Direction.LEFT else direction.LEFT)
    time.sleep(random.randint(200, 255) / 100)
    # time.sleep(random.randint(500, 555) / 100)
    ahk.key_up("l")  # v charm
    time.sleep(random.randint(30, 50) / 1000)
    char.stop()
    # ahk.key_down(direction.value)
    lock.release()
    return done_at

    # threading.Timer(210, use_domain, kwargs={"direction": direction}).start()


def fill_mana():
    lock.acquire()
    print("filling mana")
    char.use_skill("9")
    # char.use_skill("End")  # HP Pot
    lock.release()
    # threading.Timer(random.randint(30, 60), fill_mana).start()


def use_blue_ball():
    lock.acquire()
    print("blue balling")
    char.move_to(Target.EXO_POSITION)
    char.set_blue_ball()
    lock.release()
    # threading.Timer(random.randint(90, 100), use_blue_ball).start()


def use_pink_ball():
    lock.acquire()
    print("pink balling")
    # char.move_to(Target.EXO_POSITION)
    char.set_pink_ball()
    lock.release()
    # threading.Timer(random.randint(80, 95), use_pink_ball).start()


def release_rune():
    lock.acquire()
    print("checking rune")
    if char.get_rune_position() is not None:
        print("breaking rune")
        success = char.break_rune()
        while not success:
            print("trying to break rune again")
            time.sleep(random.randint(30, 50) / 10)
            success = char.break_rune()
    lock.release()
    return time.time()
    # threading.Timer(random.randint(30, 35), release_rune).start()


def feed_pets():
    lock.acquire()
    print("feeding pet")
    char.feed_pet()
    lock.release()
    # threading.Timer(random.randint(600, 900), feed_pets).start()


def battle_stat():
    lock.acquire()
    print("battle stat")
    name = char.battle_stat()
    print(f"{name} is saved")
    lock.release()
    # threading.Timer(random.randint(3600, 3605), battle_stat).start()


def use_legion():
    print("usemonkey")
    ahk.key_press("t")
    return time.time()


def mp_potion():
    ahk.key_press("9")
    time.sleep(0.3)
    return time.time()

def spidering():
    time.sleep(0.3)
    ahk.key_press("v")
    time.sleep(0.3)
    return time.time()

def monkey_buisness():
    print('monkey buisness + meso')

    time.sleep(1.0)
    ahk.key_press("t")
    time.sleep(0.5)

    char.move_to(82, 159)

    time.sleep(0.3)
    ahk.key_press('a')
    ahk.key_press('a')
    ahk.key_press('a')

    time.sleep(1.1)
    ahk.key_down('right')
    time.sleep(0.87)
    ahk.key_up('right')
    time.sleep(0.2)
    ahk.key_press('5')
    ahk.key_press('5')

    time.sleep(2.2)
    #on top left platform
    lookright()
    ahk.key_press('j')
    time.sleep(0.06)
    ahk.key_press('j')
    ahk.key_press('j')
    ahk.key_press('j')
    time.sleep(0.05)
    ahk.key_press('a')
    time.sleep(0.7)
    ahk.key_press('a')
    time.sleep(0.8)
    ahk.key_press('d')
    time.sleep(0.7)
    ahk.key_press('d')
    time.sleep(0.5)

    #monkey install
    ahk.key_press('delete')
    time.sleep(0.28)


    downjump()
    time.sleep(0.9)

    downjump()
    time.sleep(0.9)


    downjump()
    time.sleep(0.7)

    char.break_rune()



    return time.time()




if __name__ == "__main__":
    Target = LCUP_DESKTOP
    print(char.get_character_position())
    char.key_reset()
    # char.unblock()
    # exit(0)
    # # # #

    #
    # char.jump_teleport(Direction.DOWN)

    jobs = {

        "buff": {
            "func": buff,
            "cd": 178,
            "last": None,
            "args": None
        },

        "mp_potion": {
            "func": mp_potion,
            "cd": 1800,
            "last": None,
            "args": None
        },

        "monkey_buisness": {
            "func": monkey_buisness,
            "cd": 104,
            "last": None,
            "args": None
        },

        "spidering": {
            "func": spidering,
            "cd": 240,
            "last": None,
            "args": None
        }


    }

    from pynput import keyboard

    keyPressed = "f12"


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


    def lookleft():
        time.sleep(0.08)
        ahk.key_press("Left")
        time.sleep(0.08)


    def lookright():
        time.sleep(0.08)
        ahk.key_press("Right")
        time.sleep(0.08)


    def downjump():
        ahk.key_down("Down")
        time.sleep(0.1)
        ahk.key_press("j")
        time.sleep(0.02)
        ahk.key_up("Down")
        time.sleep(0.02)


    def cycle1():
        time.sleep(0.01)
        ahk.key_press("LShift")
        time.sleep(0.68)
        ahk.key_press("a")
        ahk.key_press("a")
        ahk.key_press("a")

        time.sleep(0.7)

        ahk.key_press("LShift")
        time.sleep(0.69)
        ahk.key_press("a")
        time.sleep(0.8)

        ahk.key_press("j")
        time.sleep(0.2)
        ahk.key_press("LShift")
        time.sleep(0.65)
        lookright()


    def cycle2():
        downjump()
        ahk.key_press("LShift")
        time.sleep(0.7)

        downjump()
        ahk.key_press("LShift")
        time.sleep(0.7)

        ahk.key_press("LShift")
        time.sleep(0.35)


    count = 0


    def core6():
        global count

        char.move_to(129, 159)
        lookleft()

        print('count = ', count)



        if count % 6 == 0:
            time.sleep(0.1)
            ahk.key_press("g")
            time.sleep(0.5)

        if count % 3 == 0:
            time.sleep(0.1)
            print("bombing")
            ahk.key_down('r')
            time.sleep(0.6)
            ahk.key_down('Up')
            time.sleep(0.03)
            ahk.key_up('Up')
            ahk.key_up('r')

        if (count + 1) % 2 == 0:
            time.sleep(0.3)
            print("Cocoball")
            ahk.key_press("End")
            time.sleep(0.5)

        cycle1()

        time.sleep(0.1)

        if count % 3 == 0:
            time.sleep(0.1)
            ahk.key_press("q")
            time.sleep(0.2)
            char.break_rune()

        cycle2()

        if count % 3 == 0:
            char.break_rune()

        count = count + 1

        # if count % 10 == 0:
        #     time.sleep(1.5)
        #     ahk.key_press("t")
        #     time.sleep(0.5)
        #
        #     mesograbbing()


    # def mesograbbing():
    #     char.move_to(94, 159)
    #     time.sleep(0.7)
    #     ahk.key_press('a')
    #     time.sleep(1.5)
    #     ahk.key_press('a')
    #     time.sleep(0.3)
    #     ahk.key_press('a')
    #     time.sleep(1.2)
    #     #on top left platform
    #     lookright()
    #     ahk.key_press('j')
    #     time.sleep(0.06)
    #     ahk.key_press('j')
    #     time.sleep(0.06)
    #     ahk.key_press('a')
    #     time.sleep(0.8)
    #     ahk.key_press('a')
    #     time.sleep(0.5)
    #     ahk.key_press('d')
    #     time.sleep(1.5)
    #
    #     #monkey install
    #     ahk.key_press('delete')
    #     time.sleep(0.4)
    #
    #
    #     downjump()
    #     time.sleep(0.9)
    #
    #     downjump()
    #     time.sleep(1)
    #
    #     downjump()
    #     time.sleep(0.9)












    while True:  ##3

        if keyPressed == "f11":
            print("paused")
            while keyPressed != "f12":
                time.sleep(1)
            print("resuming")
        core6()

        for job_name, job in jobs.items():
            if keyPressed != "f12":
                print("paused in skill")
                while keyPressed == "f11":
                    time.sleep(1)
                print("resuming")
            if job["last"] is None or time.time() - job["last"] >= job["cd"]:
                if job["args"] is not None:
                    done_at = job["func"](*(job["args"]))
                else:
                    done_at = job["func"]()
                job["last"] = done_at

    #
