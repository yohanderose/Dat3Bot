import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt
import dlib
import face_alignment
from skimage import io
import plotly.express as px

import numpy as np
import pandas as pd


def load_img(filename):
    capture = cv2.imread(filename)
    rows, cols, ch = capture.shape

    capture_grey = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
    face_detector = dlib.get_frontal_face_detector()
    landmark_predictor = dlib.shape_predictor("landmarks")

    fig, ax = plt.subplots(1, figsize=(16, 7))
    ax.imshow(capture[:, :, ::-1])
    plt.show()
