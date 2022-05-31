import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.measure import find_contours
from skimage.io import imread, imsave
from skimage.color import rgb2gray
from skimage.transform import rotate


def rotate_img(path, angle, dest_path):
    orig_img = imread(path)
    rotated = rotate(orig_img, angle, resize=True) * 255
    imsave(dest_path, rotated)


# rotate_img('templates/test2.png', 20, 'templates/test10.png')
