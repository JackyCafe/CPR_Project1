# Camera
import argparse
import datetime
import json
import time
from pathlib import Path
from queue import Queue
from threading import Thread

import numpy as np
from PySide6.QtCore import QThread
import cv2
from pymongo import MongoClient
import openpose.pyopenpose as op
from gui.signal_container import SignalContainer, LabelContainer, FrequenceContainer, LabelDeepContainer, \
    FrequencyLabelContainer
from keypoints.angle import Angle
from machine.BODY_25 import BODY_25
from machine.position_config import PositionConfig
from fancy import config as cfg
import playsound


class Camera(QThread):
    y1: float
    y2: float
    y3: float
    depth: float
    play_sound: int
    is_test: bool
    is_pose_abnormal: bool  #
    is_deep_abnormal: bool
    is_freq_abnormal: bool

    def __init__(self, num_camera, width=800, height=600):
        super(Camera, self).__init__()
        self.num_camera = num_camera
        self.cap = cv2.VideoCapture(num_camera)

        self.width = width
        self.height = height
        # todo y1,y2,de
        args = self.get_arg_parser().parse_args()
        position_config = PositionConfig(cfg.YamlConfigLoader(args.position))
        # self.y1 = 381
        # self.y2 = 391
        # self.depth = 53
        self.y1 = position_config.y1
        self.y2 = position_config.y2
        self.depth = position_config.depth
        self.ratio = self.depth / (self.y2 - self.y1)
        self.is_play_sound = position_config.is_play_sound
        self.is_test = position_config.is_test

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.rawdata = SignalContainer()  # original image
        self.right_hand = LabelContainer()  # angle of pose
        self.left_hand = LabelContainer()
        self.frequency_label = FrequencyLabelContainer()
        self.depth_estimate_label = LabelDeepContainer()
        # self.time_label = TimeLabelContainer()
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        # pose

        # mongodb setup
        self.clients = MongoClient("mongodb://localhost:27017/")
        self.database = self.clients['cpr']
        self.collection = self.database['doctor_cpr_data']

        if self.is_play_sound:
            self.is_deep_abnormal = True
            self.is_pose_abnormal = True
            self.is_freq_abnormal = True

        self.sound_queue = Queue()
        self.sound_thread = Thread(target=handle_playsound, args=(self.sound_queue, ), daemon=True)
        self.sound_thread.start()

        if self.cap is None or not self.cap.isOpened():
            self.running = False
            self.connect = False
            self.is_preview = False
        else:
            self.connect = True
            self.running = False
            self.is_preview = True

    def setId(self, Id=9527):
        self.id = Id

    def run(self) -> None:
        frame_cnt = 0
        # todo
        # openpose using model
        num_keypoint = 25
        FRAME_CNT = 50000
        #
        seq_length = int(FRAME_CNT)
        feature_array = np.zeros([seq_length, num_keypoint, 3], np.float32)
        is_play_sound = False
        poseModel = op.PoseModel.BODY_25

        params = dict()
        params["model_folder"] = "../models/"
        params["net_resolution"] = "320x-1"
        params['number_people_max'] = 1
        op_wrapper = op.WrapperPython()
        op_wrapper.configure(params)
        op_wrapper.start()
        datum = op.Datum()

        i = 0
        j = 0
        is_trace_down = True
        while self.running and self.connect:
            ret, frame = self.cap.read()
            if ret and self.is_preview:
                self.rawdata.update_image.emit(frame)  # 發
            if ret and not self.is_preview:
                try:
                    last_time = datetime.datetime.now()
                    datum.cvInputData = frame
                    op_wrapper.emplaceAndPop(op.VectorDatum([datum]))
                    # get the 25 key points
                    keypoints = datum.poseKeypoints[0]
                    feature_array[frame_cnt, :, :] = keypoints
                    # Right hand position [wrist, shouder ,elbow]
                    RWrist = feature_array[frame_cnt, BODY_25.RWrist.value, :]
                    RShoulder = feature_array[frame_cnt, BODY_25.RShoulder.value, :]
                    RElbow = feature_array[frame_cnt, BODY_25.RElbow.value, :]
                    right_hand = [RShoulder, RElbow, RWrist]
                    right_angle = Angle(right_hand).angle_between_point()

                    # Left hand position  [wrist, shouder ,elbow]
                    LWrist = feature_array[frame_cnt, BODY_25.LWrist.value, :]
                    LShoulder = feature_array[frame_cnt, BODY_25.LShoulder.value, :]
                    LElbow = feature_array[frame_cnt, BODY_25.LElbow.value, :]
                    left_hand = [LShoulder, LElbow, LWrist]
                    left_angle = Angle(left_hand).angle_between_point()

                    #  write data into mongodb
                    cpr_info = {}
                    cpr_info['Id'] = self.id
                    cpr_info['items'] = i
                    cpr_info['datetime'] = datetime.datetime.now()
                    cpr_info['RShoulder_x'] = float(RShoulder[0])
                    cpr_info['RShoulder_y'] = float(RShoulder[1])
                    cpr_info['RElbow_x'] = float(RElbow[0])
                    cpr_info['RElbow_y'] = float(RElbow[1])
                    cpr_info['RWrist_x'] = float(RWrist[0])
                    cpr_info['RWrist_y'] = float(RWrist[1])
                    cpr_info['LShoulder_x'] = float(LShoulder[0])
                    cpr_info['LShoulder_y'] = float(LShoulder[1])
                    cpr_info['LElbow_x'] = float(LElbow[0])
                    cpr_info['LElbow_y'] = float(LElbow[1])
                    cpr_info['LWrist_x'] = float(LWrist[0])
                    cpr_info['LWrist_y'] = float(LWrist[1])
                    cpr_info['Left_Angle'] = left_angle
                    cpr_info['Right_Angle'] = right_angle
                    deepth = self.ratio * (float(RWrist[1]) - self.y1)
                    cpr_info['depth'] = deepth
                    # dt = datetime.datetime.now()
                    # self.frequency_label.update_label.emit(str(dt))

                    if left_angle != -1 and right_angle != -1:
                        self.collection.insert_one(cpr_info)
                    if i % 10 == 0:
                        hands = self.collection.find({"Id": self.id, "items": i}).next()
                        if self.is_test:
                            self.left_hand.update_label.emit(str(LWrist[1]))
                            self.right_hand.update_label.emit(str(RWrist[1]))
                        else:
                            self.left_hand.update_label.emit(str(hands['Left_Angle']))
                            self.right_hand.update_label.emit(str(hands['Right_Angle']))

                        current_time = datetime.datetime.now()
                        self.frequency_label.update_label.emit(str(current_time))
                        last_time = current_time

                        # print(self.ratio)
                        # 2020.08.17
                        depth = round(self.ratio * (float(RWrist[1]) - self.y1), 2)
                        # self.depth_estimate_label.update_label.emit(str(depth))
                        if depth <= 0 :
                           self.depth_estimate_label.update_label.emit('手掌離開')
                        elif depth > 2 and depth < 8:
                           self.depth_estimate_label.update_label.emit(str(depth))
                        j = j + 1

                        # 2022.08.22
                        if self.is_play_sound and j >= 10:
                            if self.is_deep_abnormal and (depth > 7 or depth < 5):
                                self.sound_queue.put('../sound/deep_abnormal.mp3')
                                self.is_deep_abnormal = False

                            if self.is_pose_abnormal and (right_angle <= 165 or left_angle <= 165):
                                self.sound_queue.put('../sound/post_abnormal.mp3')
                                self.is_pose_abnormal = False


                except Exception as e:
                    print(e.__str__())
                    pass
                    # raise
                i = i + 1
                ''' '''
                self.rawdata.update_image.emit(datum.cvOutputData)  # 發
                if not self.is_preview and self.out:
                    self.out.write(frame)

    # preview the video
    def preview(self):
        if self.connect:
            self.running = True  # 啟動讀取狀態
            self.start()

    def open(self):
        if self.connect:
            self.running = True  # 啟動讀取狀態
            self.is_preview = False
            time_str = time.strftime("%Y%m%d-%H%M%S")
            if self.num_camera == 0:
                self.filename = '../medias/x_cpr' + time_str + '.avi'
                self.out = cv2.VideoWriter(self.filename, self.fourcc, 30.0, (self.width, self.height))

    def stop(self):
        if self.connect:
            self.running = False  # 關閉讀取狀態
            # self.cap.release()
            self.out.release()

    def exit(self, retcode=0):
        if self.connect:
            self.running = False  # 關閉讀取狀態
            # self.is_preview = False
        super().exit(retcode)

    def get_arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--position", type=Path, default=Path("../configs/config.yaml"))

        return parser


def handle_playsound(queue: Queue):
    while True:
        sound_path = queue.get()
        playsound.playsound(sound_path)
