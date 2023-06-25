import cv2
import numpy as np
import common
from PIL import Image

image = cv2.imread('15.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

if __name__ == "__main__":
    result = image.copy()

    lower = np.array([155, 25, 0])
    upper = np.array([179, 255, 255])
    y_lower = np.array([22, 93, 0])
    y_upper = np.array([45, 255, 255])
    mask = cv2.inRange(image, lower, upper)
    mask = cv2.inRange(image, (36, 25, 25), (86, 255, 255))
    mask = cv2.inRange(image, y_lower, y_upper)
    mask = cv2.inRange(image, (25, 200, 50), (35, 255, 255))
    mask = cv2.inRange(image, (0, 200, 50), (75, 255, 255))
    mask = cv2.inRange(image, (20,164,245),(23, 167, 255))
    result = cv2.bitwise_and(result, result, mask=mask)

    cv2.imshow('mask', mask)
    cv2.imshow('result', result)


    # blurr image first ---
    #                 blur = cv2.bilateralFilter(image, 9, 150, 1000)
    #                 cv2.imshow('blur', blur)
    #---

    # filter = np.array([[3, -2, -3], [-4, 8, -6], [5, -1, -0]])
    # sharpen = cv2.filter2D(blur, -1, filter)
    # cv2.imshow('sharpen', sharpen)

    # rune color spectrum for mask
    #                 lower_red = np.array([0, 140, 180])  # BGR
    #                 upper_red = np.array([70, 255, 254])
    #
    #                 mask = cv2.inRange(blur, lower_red, upper_red)
    # cv2.imshow('mask', mask)

    #--- Remove noise + chunk out
                    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                    # finalimage = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    # coins_contours, _ = cv2.findContours(finalimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # coins_and_contours = np.copy(finalimage)
    #
    # min_coin_area = 10
    # large_contours = [cnt for cnt in coins_contours if cv2.contourArea(cnt) > min_coin_area]
    # cv2.drawContours(coins_and_contours, large_contours, -1, (255, 0, 0))
    #
    # bounding_img = np.copy(finalimage)
    #
    # for contour in large_contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(bounding_img, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # cv2.imshow('finalimage', finalimage)

    cv2.waitKey()
