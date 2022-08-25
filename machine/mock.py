import argparse
import time
from pathlib import Path

import cv2
from PySide6.QtCore import QThread
import openpose.pyopenpose as op
from gui.signal_container import SignalContainer
from machine.position_config import PositionConfig
from fancy import config as cfg


class MockCamera(QThread):
    y1: float
    y2: float
    y3: float
    depth: float
    w: int
    h: int
    fps: float
    params = {}
    params["model_folder"] = "../models/"
    params["net_resolution"] = "320x-1"
    params['number_people_max'] = 1
    op_wrapper = op.WrapperPython()
    op_wrapper.configure(params)
    op_wrapper.start()
    datum = op.Datum()

    def __init__(self, num_camera, width=800, height=600):
        super(MockCamera, self).__init__()
        video_path = '../medias/x_cpr20220605-115841.avi'
        self.cap = cv2.VideoCapture(video_path)
        video_info = {}
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        FRAME_CNT = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.length = FRAME_CNT
        args = self.get_arg_parser().parse_args()
        position_config = PositionConfig(cfg.YamlConfigLoader(args.position))
        # self.y1 = 381
        # self.y2 = 391
        # self.depth = 53
        self.y1 = position_config.y1
        self.y2 = position_config.y2
        self.depth = position_config.depth
        self.ratio = self.depth / (self.y2 - self.y1)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.h)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.rawdata = SignalContainer()  # original image

    def run(self) -> None:
        frame_cnt = 0
        while frame_cnt < self.length:
            ret, frame = self.cap.read()
            if ret:
                # if frame_cnt % self.fps == 1:
                self.datum.cvInputData = frame
                self.op_wrapper.emplaceAndPop(op.VectorDatum([self.datum]))
                self.rawdata.update_image.emit(frame)
                # self.rawdata.update_image.emit(self.datum.cvOutputData)
            frame_cnt += 1

    def get_arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--position", type=Path, default=Path("../configs/config.yaml"))

        return parser
