# import the necessary packages
import numpy as np
import cv2




def blur_and_threshold(image, eps=1e-7):
    # apply a median blur to the image and then subtract the blurred
    # image from the original image to approximate the foreground
    blur = cv2.medianBlur(image, 27)
    foreground = image.astype("float") - blur

    # threshold the foreground image by setting any pixels with a
    # value greater than zero to zero
    foreground[foreground > 0] = 0

    # apply min/max scaling to bring the pixel intensities to the
    # range [0, 1]
    minVal = np.min(foreground)
    maxVal = np.max(foreground)
    foreground = (foreground - minVal) / (maxVal - minVal + eps)
    #output = rescale_intensity(foreground, in_range=(0, 255))  # Đưa giá trị về khoảng [0, 255]
    output = (foreground * 255).astype("uint8")  # Đưa picxel về lại dạng uint8




    # return the foreground-approximated image
    return output

