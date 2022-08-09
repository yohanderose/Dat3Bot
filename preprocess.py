import cv2
import sys
from deepface import DeepFace
import matplotlib.pyplot as plt
import dlib
import face_alignment
from skimage import io
import plotly.express as px

import numpy as np
import pandas as pd


def img_to_feature_vec(img_path, label):
    try:
        meta_obj = extract_img_metadata(img_path)
    except Exception as e:
        print(e)
        return None
    try:
        landmark_df = extract_facial_landmarks(img_path)
    except Exception as e:
        print(e)
        return None
    return build_feature_vector(meta_obj, landmark_df, label)


def extract_img_metadata(img_path) -> dict:
    return DeepFace.analyze(img_path=img_path, actions=['age', 'gender', 'race', 'emotion'])


def extract_facial_landmarks(img_path) -> pd.DataFrame:
    fa = face_alignment.FaceAlignment(
        face_alignment.LandmarksType._3D, flip_input=False)

    img = io.imread(img_path)
    preds = np.array(fa.get_landmarks(img)[0])
    df = pd.DataFrame({'x': preds[::, 0], 'y': preds[::, 1], 'z': preds[::, 2], 'id': range(
        len(preds)), 'colour': [1] * len(preds)})
    # Append other key points to dataframe that need to be calculated
    data = []
    pupil_x = (abs((df[df['id'] == 39]['x'].values) - (df[df['id'] == 36]
               ['x'].values))[0] / 2) + (df[df['id'] == 36]['x'].values)[0]
    pupil_y = (abs((df[df['id'] == 41]['y'].values) - (df[df['id'] == 37]
               ['y'].values))[0] / 2) + (df[df['id'] == 37]['y'].values)[0]
    pupil_z = df[df['id'] == 41]['z'].values[0]
    pupil = [pupil_x, pupil_y, pupil_z, len(df) + 1, 2]
    data.append(pupil)
    return df.append(pd.DataFrame(data=data, columns='x y z id colour'.split()))


def build_feature_vector(obj, df, label) -> list:
    # Extract key distances
    nose_chin = abs((df[df['id'] == 33]['y'].values) -
                    (df[df['id'] == 8]['y'].values))[0]
    nose_lips = abs((df[df['id'] == 33]['y'].values) -
                    (df[df['id'] == 66]['y'].values))[0]
    pupil_nose = abs((df[df['id'] == 69]['y'].values) -
                     (df[df['id'] == 33]['y'].values))[0]
    nose_width = abs((df[df['id'] == 31]['x'].values) -
                     (df[df['id'] == 35]['x'].values))[0]
    eye_span_outside = abs(
        (df[df['id'] == 36]['x'].values) - (df[df['id'] == 45]['x'].values))[0]
    lip_height = abs((df[df['id'] == 57]['y'].values) -
                     (df[df['id'] == 51]['y'].values))[0]
    face_width = abs((df[df['id'] == 0]['x'].values) -
                     (df[df['id'] == 16]['x'].values))[0]
    middle_third = abs((df[df['id'] == 50]['y'].values) -
                       (df[df['id'] == 37]['y'].values))[0]

    return [
        obj["age"],
        1 if obj["gender"] == "Woman" else 0,
        face_width / middle_third,
        nose_chin / nose_lips,
        nose_chin / pupil_nose,
        nose_width / nose_lips,
        lip_height / nose_width,
        1 if (label == 'hot' and obj["gender"] == "Woman") else 0
    ]


def dirty_unit_test():
    img_path = './some_asian_baddie.jpg'

    print('Extracting feature vector for test image...', end='')
    print('OK') if (img_to_feature_vec(img_path, 'hot') == [
        27, 1, 2.269662921348315, 2.2857142857142856, 1.5609756097560976, 0.7142857142857143, 1.2333333333333334, 1]) else sys.exit('ERROR')
