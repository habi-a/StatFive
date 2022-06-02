#!/usr/bin/env python3

import cv2
import numpy as np

def count_nonblack_np(img):
    return img.any(axis=-1).sum()


def detect_color(image):
    # define the list of boundaries
    i = 0
    boundaries = [
        ([17, 15, 100], [50, 56, 200]), #red
        ([86, 31, 4], [220, 88, 50]) #blue
    ]

    for (lower, upper) in boundaries:
        ## create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        ## find the colors within the specified boundaries and apply the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask = mask)
        tot_pix = count_nonblack_np(image)
        color_pix = count_nonblack_np(output)

        ratio = color_pix/tot_pix
        if ratio > 0.01 and i == 0:
            return 'red'
        elif ratio > 0.01 and i == 1:
            return 'blue'
        i += 1

    return 'not_sure'