import time
import os
import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt
import dlib
import face_alignment
from skimage import io
import plotly.express as px
import random

import numpy as np
import pandas as pd
from preprocess import img_to_feature_vec
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def add_to_dataset(src):
    time.sleep(random.randrange(2, 30) * 0.1)
    res = img_to_feature_vec(src[0], src[1])
    if res is not None:
        with open('./dataset.csv', 'a') as df:
            df.write(','.join([str(x) for x in res]) + '\n')


def main():
    srcs = []
    srcs += [(os.path.join('./dataset/hot', filename), 'hot')
             for filename in os.listdir('./dataset/hot')]
    srcs += [(os.path.join('./dataset/not', filename), 'not')
             for filename in os.listdir('./dataset/not')]
    random.shuffle(srcs)

    with open('dataset.csv', 'a') as df:
        df.write('age,gender,feat_1,feat_2,feat_3,feat_4,feat_5,label\n')

    # Use multiprocessing to compute list of feature vectors for each class
    with ThreadPoolExecutor(max_workers=24) as executor:
        for _ in tqdm(executor.map(add_to_dataset, srcs), total=len(srcs)):
            pass

    # If GPU is shit, non parallel version below
    # hot_vecs = []
    # not_vecs = []
    # for src in tqdm(srcs_hot):
    #     res = hot_vecs.append(img_to_feature_vec(src, 'hot'))
    #     if res is not None:
    #         hot_vecs.append(res)

    # for src in tqdm(srcs_not):
    #     res = not_vecs.append(img_to_feature_vec(src, 'not'))
    #     if res is not None:
    #         not_vecs.append(res)

    # data = hot_vecs + not_vecs
    # df = pd.DataFrame(data=data, columns='age gender 1 2 3 4 5 label'.split())
    # df.to_csv('dataset.csv', index=False)


if __name__ == '__main__':
    main()
