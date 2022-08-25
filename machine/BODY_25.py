from enum import Enum

class BODY_25(Enum):
    Nose = 0
    Neck = 1
    RShoulder = 2
    RElbow = 3
    RWrist = 4
    LShoulder = 5
    LElbow = 6
    LWrist = 7
    MidHip = 8
    RHip = 9
    RKnee = 10
    RAnkle = 11
    LHip = 12
    LKnee = 13
    LAnkle = 14
    REye = 15
    LEye = 16
    REar = 17
    LEar = 18
    LBigToe = 19
    LSmallToe = 20
    LHeel = 21
    RBigToe = 22
    RSmallToe = 23
    RHeel = 24
    Background = 25

    @staticmethod
    def get_pairs():
        # pairs of connected body points
        point_pairs = [(0, 1), (2, 1), (2, 3), (3, 4), (5, 1), (5, 6), (6, 7), (8, 1), (8, 9), (9, 10), (10, 11),
                       (8, 12), (12, 13), (13, 14), (0, 15), (0, 16), (15, 17), (16, 18), (14, 19), (14, 21), (19, 20),
                       (11, 22), (23, 22), (11, 24)]
        return point_pairs
