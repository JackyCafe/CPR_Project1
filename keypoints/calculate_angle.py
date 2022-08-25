import json
import os

import numpy as np
from pymongo import MongoClient

from BODY_25 import BODY_25
from keypoints.angle import HandAngle, Angle


def analysis_feature(features, write2Mongo = False):
    size: int = len(features)
    angles = []
    standard = 0
    total = 0
    non_stand_right = 0
    non_stand_left = 0
    standard_angle= 165
    for i in range(size):
        angle = {}
        RShoulder = features[i, BODY_25.RShoulder.value, :]
        RElbow = features[i, BODY_25.RElbow.value, :]
        RWrist = features[i, BODY_25.RWrist.value, :]
        right_hand = [RShoulder, RElbow, RWrist]
        right_angle = Angle(right_hand).angle_between_point()
        LShoulder = features[i, BODY_25.LShoulder.value, :]
        LElbow = features[i, BODY_25.LElbow.value, :]
        LWrist = features[i, BODY_25.LWrist.value, :]
        left_hand = [LShoulder, LElbow, LWrist]
        left_angle = Angle(left_hand).angle_between_point()
        if 0< right_angle< standard_angle :  non_stand_right +=1
        if 0< left_angle < standard_angle :  non_stand_left += 1

        if right_angle!=-1 or left_angle !=-1:
            angle["filename"] = file
            angle["right"]= right_angle
            angle["left"] = left_angle
            if write2Mongo == True:
                collection.insert_one(angle)
            total = total + 1
            if right_angle>= standard_angle and left_angle>=standard_angle:
                standard += 1

    if total != 0:
        rate = (standard/total)*100
        print("%d,%d,%d,%d,%.1f "%(non_stand_left, non_stand_right, standard, total, rate))
        # print("%s standard/total %d / %d = %.1f "%(file_path, standard, total, rate))
        # print(f" non standard right:{non_stand_right}, non standard left:{ non_stand_left} " )
    return angles


def read_npy(file):
    feartures = np.load(file)

    return feartures


if __name__ == '__main__':
    video_dir = './npy/'
    root, _, files = next(os.walk('./npy'))
    file_cnt = 0
    clients = MongoClient("mongodb://localhost:27017/")
    database = clients['cpr_db']
    collection = database['cpr_angle_data']
    print("standard keypoints:165 ")
    print("non_stand_left,non_stand_right,standard,total,rate")

    for file in files:
        file_path = os.path.join(root, file)
        features = read_npy(file_path)
        if features.nonzero():
            angle =  analysis_feature(features,True)
