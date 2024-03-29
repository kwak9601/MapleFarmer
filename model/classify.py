import argparse
import os
import re
import sys

sys.path.insert(0, os.path.abspath('.'))
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import colorful as cf
import cv2
import numpy as np
import pandas as pd
import tensorflow.keras

import common


def main(src_subdir, verbose, model_name):
    src_dir = os.path.join(common.DATA_DIR, src_subdir)
    
    model = tensorflow.keras.models.load_model(os.path.join(common.MODEL_DIR, model_name))

    # real (index) x predicted (column)
    confusion_matrix = pd.DataFrame(np.zeros((4, 4), dtype=np.int32),
                                    index=('down', 'left', 'right', 'up'),
                                    columns=('down', 'left', 'right', 'up'))

    classification_matrix = pd.DataFrame(np.zeros((4, 3)),
                                index=('down', 'left', 'right', 'up'),
                                columns=('precision', 'recall', 'f1'))

    type_matrix = pd.DataFrame(np.zeros((4, 2), dtype=np.int32), 
                                index=('round', 'wide', 'narrow', 'total'), 
                                columns=('correct', 'incorrect'))

    images = common.get_files(src_dir)

    print("Processing {} file(s) in {}/...\n".format(len(images), src_subdir))

    for path, filename in images:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        data = np.reshape(img, (1, ) + common.INPUT_SHAPE)
        prediction = model.predict(data)

        class_index = np.argmax(prediction)
        predicted_class = common.CLASSES[class_index]

        real_class, arrow_type = common.arrow_labels(filename)

        if verbose and real_class != predicted_class:
            print(path)
            print("Expected {} but got {}: {}\n".format(
                cf.lightGreen(real_class),
                cf.lightCoral(predicted_class),
                str(prediction[0])))

        confusion_matrix[predicted_class][real_class] += 1

        if real_class == predicted_class:
            type_matrix['correct'][arrow_type] += 1
            type_matrix['correct']['total'] += 1
        else:
            type_matrix['incorrect'][arrow_type] += 1
            type_matrix['incorrect']['total'] += 1

    print("\n" + cf.sandyBrown("Confusion matrix"))
    print(confusion_matrix)

    classification_matrix['precision'] = confusion_matrix.apply(precision)
    classification_matrix['recall'] = confusion_matrix.apply(recall, axis=1)

    classification_matrix['f1'] = classification_matrix.apply(f1, axis=1)

    print("\n" + cf.skyBlue("Classification summary"))
    print(classification_matrix)

    type_matrix['accuracy'] = type_matrix.apply(type_accuracy, axis=1)

    print("\n" + cf.plum("Accuracy by type"))
    print(type_matrix)

    print("\nFinished!")


def classify_image(path, model, mode='binarized'):
    from preprocessing.preprocess import SEARCH_REGION_WIDTH, SEARCH_REGION_HEIGHT, process_arrow, ARROW_BOX_DIST
    arrows = []

    if isinstance(path, str):
        display = cv2.imread(path)
    else:  # for opencv image
        display = path
    height, width, _ = display.shape

    # manually tuned values
    if width == 800:  # for 800 x 600
        search_x, search_y = width // 5 + 35, height // 4
        search_width, search_height = SEARCH_REGION_WIDTH, height // 2 - search_y
    else:  # for 1366 x 768
        search_x, search_y = width // 3 + 25, height // 5
        search_width, search_height = SEARCH_REGION_WIDTH + 30, max(SEARCH_REGION_HEIGHT, 300 - search_y)

    for _ in range(4):
        x0 = search_x
        x1 = x0 + search_width

        y0 = search_y
        y1 = y0 + search_height

        img = display[y0:y1, x0:x1]
        (cx, cy), arrow_box = process_arrow(img, mode)

        search_x += int(cx + ARROW_BOX_DIST - SEARCH_REGION_WIDTH / 2)
        search_y += int(cy - SEARCH_REGION_HEIGHT / 2)

        search_width = SEARCH_REGION_WIDTH
        search_height = SEARCH_REGION_HEIGHT

        arrows.append(arrow_box)

    predictions = []
    for arrow in arrows:
        data = np.reshape(arrow, (1, ) + common.INPUT_SHAPE)
        prediction = model.predict(data)
        class_index = np.argmax(prediction)
        classification = common.CLASSES[class_index]
        predictions.append(classification)

    return predictions


def precision(x):
    return round(x[x.name] / sum(x), 4)


def recall(x):
    return round(x[x.name] / sum(x), 4)


def f1(x):
    return round(2 * (x['precision'] * x['recall']) / (x['precision'] + x['recall']), 4)


def type_accuracy(x):
    return round(x['correct'] / (x['correct'] + x['incorrect']), 4)


if __name__ == "__main__":
    os.system('color')
    np.set_printoptions(suppress=True)

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--dir', type=str, default='testing',
                      help="Specifies the directory from which images will be classified")
    parser.add_argument('-v', '--verbose', action='store_true', 
                      help="Enables logging of misclassified examples")
    parser.add_argument('-m', '--model', type=str, default='arrow_model.h5', 
                      help="Specifies the model file name")

    args = parser.parse_args()

    main(args.dir, args.verbose, args.model)
