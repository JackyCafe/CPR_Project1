import math
import numpy as np


class Point:
    x: float
    y: float
    z: float

    def __init__(self, args):
        self.x = args[0]
        self.y = args[1]
        self.z = args[2]


class Angle:
    p0: Point
    p1: Point
    p2: Point

    def __init__(self, args):
        self.p0 = Point(args[0])
        self.p1 = Point(args[1])
        self.p2 = Point(args[2])

    def angle_between_point(self):
        return self.calculate_angle(self.p1, self.p0, self.p2)

    # def angle_between_point(self):
    #     return self.calculate_angle(self.p0, self.p1, self.p2) \
    #         , self.calculate_angle(self.p1, self.p0, self.p2), \
    #            self.calculate_angle(self.p2, self.p0, self.p1)


    def calculate_angle(self, p0: float, p1:float, p2:float)-> float:
            distant_a = (p0.x - p1.x) ** 2 + (p0.y - p1.y) ** 2
            distant_b = (p0.x - p2.x) ** 2 + (p0.y - p2.y) ** 2
            distant_c = (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2
            try:
                if distant_a * distant_b == 0:
                    return -1
                else:
                    angle = round(math.acos((distant_a + distant_b - distant_c) / math.sqrt(4 * distant_a * distant_b)) * 180 / math.pi,1)
            except:
                    angle = -1
            return angle


class HandAngle:
    r_shoulder: Point
    r_elbow: Point
    r_wrist: Point

    def __init__(self,key_points):
        self.r_shoulder = key_points[0]
        self.r_elbow = key_points[1]
        self.r_wrist = key_points[2]

    def __repr__(self):
        print(self.r_shoulder)
        print(self.r_elbow)
        print(self.r_wrist)

    def __str__(self):
       return f'r-hand {[self.r_shoulder, self.r_elbow,self.r_wrist ]}'