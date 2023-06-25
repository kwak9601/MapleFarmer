import argparse
import os
import re
import uuid
import sys

# sys.setrecursionlimit(4000)

sys.path.insert(0, os.path.abspath('.'))

import colorful as cf
import cv2
import numpy as np
import pandas as pd
from skimage import morphology

import common

OUTPUT_WIDTH = common.INPUT_SHAPE[0]

ARROW_BOX_DIST = 100
SEARCH_REGION_WIDTH = 120
SEARCH_REGION_HEIGHT = 100

EXIT_KEY = 113 # q
APPROVE_KEY = 32 # space
ANOMALY_KEY = 120 # x



def main(inspection, mode, automatic):
    print("     SPACE = approve")
    print("OTHER KEYS = skip")
    print("         X = anomaly")
    print("         Q = quit\n")

    labeled_imgs = common.get_files(common.LABELED_DIR)

    approved = 0
    anomaly = 0
    for path, filename in labeled_imgs:
        print("\nProcessing " + cf.skyBlue(path), end=": ")

        arrows = []

        display = cv2.imread(path)

        height, width, _ = display.shape

        # manually tuned values
        if width == 800:  # for 800 x 600
            search_x, search_y = width // 5 + 35, height // 4
            search_width, search_height = SEARCH_REGION_WIDTH, height // 2 - search_y
        else:  # for 1366 x 768
            search_x, search_y = width // 3 + 25, height // 5
            search_width, search_height = SEARCH_REGION_WIDTH + 30, max(SEARCH_REGION_HEIGHT, 300 - search_y)    # init search_width + 30

        for _ in range(4):
            print(f"{_} ", end="")
            x0 = search_x
            x1 = x0 + search_width

            y0 = search_y
            y1 = y0 + search_height

            img = display[y0:y1, x0:x1]
            cv2.imshow(f"prev_{_}", img)
            cv2.moveWindow(f"prev_{_}", 40 + (_*SEARCH_REGION_WIDTH), 40)
            (cx, cy), arrow_box = process_arrow(img, mode)

            # search_x += int(cx + ARROW_BOX_DIST - SEARCH_REGION_WIDTH / 2)
            search_x += int(cx + (OUTPUT_WIDTH // 2) + 5)
            search_y += int(cy - SEARCH_REGION_HEIGHT / 2)
            # cv2.imshow(f"after_{_}", display[search_x:search_x+100, search_y:search_y+100])

            search_width = SEARCH_REGION_WIDTH
            search_height = SEARCH_REGION_HEIGHT

            arrows.append(arrow_box)

        if not automatic:
            arrow_type, directions, _ = re.split('_', filename)
            reference = get_reference_arrows(directions, arrows[0].shape)

            cv2.imshow(arrow_type, np.vstack([np.hstack(arrows), reference]))

            key = cv2.waitKey()
            cv2.destroyAllWindows()
        else:
            key = APPROVE_KEY

        if key == APPROVE_KEY:
            if not inspection:
                save_arrow_imgs(arrows, filename)
            approved += 1
        elif key == ANOMALY_KEY:
            if not inspection:
                os.rename(os.path.join(common.LABELED_DIR, filename),
                          os.path.join(common.PREPROCESSED_DIR, filename))
            anomaly += 1
        elif key == EXIT_KEY:
            break
        else:
            print("Skipped!")

    if len(labeled_imgs) > 0:
        print("\nSkipped {} out of {} images ({}%).".format(
            len(labeled_imgs) - approved - anomaly, len(labeled_imgs),
            100 * len(labeled_imgs) - approved - anomaly, len(labeled_imgs) // len(labeled_imgs)))
        print("Put as anomaly {} out of {} images ({}%).".format(
            anomaly, len(labeled_imgs), 100 * anomaly // len(labeled_imgs)))
        print("Approved {} out of {} images ({}%).\n".format(
            approved, len(labeled_imgs), 100 * approved // len(labeled_imgs)))
    else:
        print("There are no images to preprocess.\n")

    show_summary()

    print("Finished!")


def isSafe(M, row, col, visited):
    # row number is in range, column number is in
    # range and value is 1 and not yet visited
    return ((row >= 0) and (row < len(M[0])) and
            (col >= 0) and (col < len(M)) and
            (M[col][row] > 0 and not visited[col][row]))


# A utility function to do DFS for a 2D
# boolean matrix. It only considers
# the 8 neighbours as adjacent vertices
def DFS(M, row, col, visited, coords):
    # These arrays are used to get row and column
    # numbers of 8 neighbours of a given cell
    rowNbr = [-1, -1, -1, 0, 0, 1, 1, 1]
    colNbr = [-1, 0, 1, -1, 1, -1, 0, 1]

    # Mark this cell as visited
    visited[col][row] = True

    # Recur for all connected neighbours
    for k in range(8):
        new_row = row + rowNbr[k]
        new_col = col + colNbr[k]
        if isSafe(M, new_row, new_col, visited):
            # increment region length by one
            coords.append((new_row, new_col))
            DFS(M, new_row, new_col, visited, coords)

        # The main function that returns largest


# length region of a given boolean 2D matrix
def largestRegion(M, threshold=100):
    # Make a bool array to mark visited cells.
    # Initially all cells are unvisited
    visited = [[False for _ in __] for __ in M]

    # Initialize result as 0 and travesle
    # through the all cells of given matrix
    result = []
    above_thresholds = []
    for row in range(len(M[0])):
        for col in range(len(M)):

            # If a cell with value 1 is not
            if (M[col][row] and not visited[col][row]):
                # visited yet, then new region found
                coords = []
                DFS(M, row, col, visited, coords)
                if len(coords) >= threshold:
                    above_thresholds.append(coords)
                # maximum region
                if len(coords) > len(result):
                    result = coords
    return result, above_thresholds


# Driver Code


def process_arrow(img, mode):
    cx, cy = None, None
    image = img.copy()
    result = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([155, 25, 0])
    upper = np.array([179, 255, 255])
    y_lower = np.array([22, 93, 0])
    y_upper = np.array([45, 255, 255])
    mask = cv2.inRange(image, lower, upper)
    mask = cv2.inRange(image, (36, 25, 25), (86, 255, 255))
    mask = cv2.inRange(image, y_lower, y_upper)
    mask = cv2.inRange(image, (25, 200, 50), (35, 255, 255))
    mask = cv2.inRange(image, (0, 200, 50), (75, 255, 255))
    result = cv2.bitwise_and(result, result, mask=mask)

    # cv2.imshow('mask', mask)
    # cv2.imshow('result', result)
    cv2.waitKey()
    try:
        largest_region, potential_regions = largestRegion(mask)
    except RecursionError as err:
        print("\n\nRecursion Error...")
        potential_regions = []
        largest_region = []

    if len(potential_regions) > 1:
        largest_region = potential_regions[0]

    # print("\nlargest", len(largest_region))

    xs = set()
    ys = set()


    # gaussian blur
    img = cv2.GaussianBlur(img, (3, 3), 0)
    # img = cv2.GaussianBlur(result, (3, 3), 0)
    # color transform
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    coefficients = (0.0445, 0.6568, 0.2987) # (h, s, v)
    img = cv2.transform(img, np.array(coefficients).reshape((1, 3)))

    if mode == 'gray':
        output = img.copy()

    # binarization
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, -1)

    # noise removal
    denoise(img, threshold=8, conn=2)

    if mode == 'binarized':
        output = img.copy()

    if len(largest_region) == 0:
        cx, cy = compute_arrow_centroid(img)
    else:
        for x, y in largest_region:
            xs.add(x)
            ys.add(y)
        cx, cy = (min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2
    # processing
    #

    # result cropping
    max_height, max_width = img.shape

    x0 = max(int(cx - OUTPUT_WIDTH / 2), 0)
    y0 = max(int(cy - OUTPUT_WIDTH / 2), 0)

    x1 = int(x0 + OUTPUT_WIDTH)
    if x1 >= max_width:
        x0 -= x1 - max_width
        x1 = max_width

    y1 = int(y0 + OUTPUT_WIDTH)
    if y1 >= max_height:
        y0 -= y1 - max_height
        y1 = max_height

    box = output[y0:y1, x0:x1]

    return (cx, cy), box


def denoise(img, threshold=64, conn=2):
    processed = img > 0

    processed = morphology.remove_small_objects(
        processed, min_size=threshold, connectivity=conn)

    processed = morphology.remove_small_holes(
        processed, area_threshold=threshold, connectivity=conn)

    mask_x, mask_y = np.where(processed == True)
    img[mask_x, mask_y] = 255

    mask_x, mask_y = np.where(processed == False)
    img[mask_x, mask_y] = 0


def compute_arrow_centroid(img):
    # cv2.imshow("test", img)

    contours, _ = cv2.findContours(
        img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # filter contours by area
    candidates = []

    for contour in contours:
        score, (cx, cy), area = circle_features(contour)

        if area > 784 and area < 3600:
            candidates.append(((cx, cy), score))

    if candidates:
        match = max(candidates, key=lambda x: x[1])
        (cx, cy), score = match

        if score > 0.8:
            return (int(cx), int(cy))

    print("\nCentroid not found! Returning the center point...")
    
    height, width = img.shape
    return (width // 2, height // 2)


def circle_features(contour):
    hull = cv2.convexHull(contour)

    if len(hull) < 5:
        return 0, (-1, -1), -1

    hull_area = cv2.contourArea(hull)

    (ex, ey), (d1, d2), angle = cv2.fitEllipse(hull)
    ellipse_area = np.pi * (d1 / 2) * (d2 / 2)

    (cx, cy), r = cv2.minEnclosingCircle(hull)
    circle_area = np.pi * r ** 2

    s1 = abs(ellipse_area - hull_area) / max(ellipse_area, hull_area)
    s2 = abs(ellipse_area - circle_area) / max(ellipse_area, circle_area)

    score = 1 - np.mean([s1, s2])

    return score, (ex, ey), ellipse_area


def get_reference_arrows(directions, shape):
    reference = []

    for d in directions:
        arrow = np.zeros(shape, dtype=np.uint8)

        w, h = shape[1], shape[0]
        cx, cy = w // 2, h // 3

        # upward arrow
        points = np.array([(cx - w // 5, cy + h // 8),
                           (cx + w // 5, cy + h // 8),
                           (cx, cy - h // 8)])

        cv2.fillConvexPoly(arrow, points, (255, 255, 255))
        cv2.line(arrow, (cx, cy), (cx, 3 * h // 5), (255, 255, 255), 10)

        rotations = 0

        if d == 'r':
            rotations = 1
        elif d == 'd':
            rotations = 2
        elif d == 'l':
            rotations = 3

        for _ in range(rotations):
            arrow = cv2.rotate(arrow, cv2.ROTATE_90_CLOCKWISE)

        reference.append(arrow)

    return np.hstack(reference)


def save_arrow_imgs(arrows, labeled_filename):
    words = re.split('_', labeled_filename)
    arrow_type = words[0]
    directions = words[1]

    # save individual arrows + their rotated and flipped versions
    for x, arrow_img in enumerate(arrows):
        for rotation in range(4):
            if rotation > 0:
                arrow_img = cv2.rotate(arrow_img, cv2.ROTATE_90_CLOCKWISE)

            direction = get_direction(directions[x], rotation)
            arrow_path = "{}{}_{}_{}.png".format(common.SAMPLES_DIR, arrow_type, direction, uuid.uuid4())

            cv2.imwrite(arrow_path + ".png", arrow_img)

            if direction in ['down', 'up']:
                flipped_img = cv2.flip(arrow_img, 1)
            else:
                flipped_img = cv2.flip(arrow_img, 0)
            
            cv2.imwrite(arrow_path + "F.png", flipped_img)

    os.rename(os.path.join(common.LABELED_DIR, labeled_filename),
              os.path.join(common.PREPROCESSED_DIR, labeled_filename))


def get_direction(direction, rotation):
    direction_dict = {
        'l': 'left',
        'u': 'up',
        'r': 'right',
        'd': 'down'
    }
    rotation_list = ['l', 'u', 'r', 'd']

    new_index = (rotation_list.index(direction) +
                 rotation) % len(rotation_list)
    new_direction = rotation_list[new_index]

    return direction_dict[new_direction]


def show_summary():
    matrix = pd.DataFrame(np.zeros((4, 5), dtype=np.int32), index=(
        'round', 'wide', 'narrow', 'total'), columns=('down', 'left', 'right', 'up', 'total'))

    images = common.get_files(common.SAMPLES_DIR)

    for _, filename in images:
        arrow_direction, arrow_type = common.arrow_labels(filename)

        matrix[arrow_direction][arrow_type] += 1

        matrix['total'][arrow_type] += 1
        matrix[arrow_direction]['total'] += 1
        matrix['total']['total'] += 1

    print(cf.salmon("Samples summary"))
    print(matrix, "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--inspection', action='store_true',
                        help="Toggles the inspection mode, which disables the output")
    parser.add_argument('-m', '--mode', default='binarized', type=str,
                        choices=['binarized', 'gray'],
                        help="Sets the output mode to binarized or grayscale")
    parser.add_argument('-a', '--automatic', action='store_true',
                        help="Toggles the automatic mode, which approves all screenshots")

    args = parser.parse_args()

    main(args.inspection, args.mode, args.automatic)
