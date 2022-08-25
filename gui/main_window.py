import cv2
from PySide6.QtCore import Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from gui._gui import Ui_Form
from gui.image import Image
from machine.camera import Camera
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

from machine.mock import  MockCamera


class MainWindow(QMainWindow, Ui_Form):
    is_camera = True

    def __init__(self):
        super(MainWindow, self).__init__()  #
        self.setupUi(self)
        self.startVideo.clicked.connect(self.start_video)
        self.stopVideo.clicked.connect(self.stop_video)
        self.exit_btn.clicked.connect(self.exit)
        self.analysisBtn.clicked.connect(self.analysis)

        if self.is_camera:
            self.camera()
        else:
            self.mock_method()


    #ru8
    def mock_method(self):
        self.mock = MockCamera(0)
        self.mock.rawdata.update_image.connect(self.set_moke_image)
        self.mock.start()


    def camera(self):
        self.ProcessCam_X = Camera(0, 800, 600)  # 建立相機物件(x)
        self.ProcessCam_X.rawdata.update_image.connect(self.set_image_x)  # 槽功能：取得並顯示影像
        self.ProcessCam_X.right_hand.update_label.connect(self.set_right_hand_label)  # 右手角度
        self.ProcessCam_X.left_hand.update_label.connect(self.set_left_hand_label)  # 手角度
        # self.ProcessCam_X.time_label.update_label.connect(self.set_time_update)  # frequence
        self.ProcessCam_X.frequency_label.update_label.connect(self.set_frequency)
        self.ProcessCam_X.depth_estimate_label.update_label.connect(self.set_deepth)
        self.ProcessCam_X.preview()



    @Slot(str)
    def set_right_hand_label(self, message):
        self.right_hand.setText(message)

    @Slot(str)
    def set_left_hand_label(self, message):
        self.left_hand.setText(message)

    @Slot(str)
    def set_frequency(self, message):
        self.frequencyLabel.setText(message)

    @Slot(str)
    def set_deepth(self, message):
        self.depthLabel.setText(message)


    @Slot(Image)
    def set_moke_image(self,moke_image):
        image = QImage(moke_image, moke_image.shape[1], moke_image.shape[0], moke_image.strides[0],
                       QImage.Format_BGR888)
        pix = QPixmap.fromImage(image)
        self.img_label.setPixmap(pix)


    @Slot(Image)
    def set_image_x(self, camera_image):
        image = QImage(camera_image, camera_image.shape[1], camera_image.shape[0], camera_image.strides[0],
                       QImage.Format_BGR888)
        pix = QPixmap.fromImage(image)
        self.img_label.setPixmap(pix)

    def start_video(self):
        if self.ProcessCam_X.connect:  # and self.ProcessCam_Y.connect:
            self.ProcessCam_X.running = True
            self.ProcessCam_X.setId(self.Id.toPlainText())
            self.ProcessCam_X.open()
            self.ProcessCam_X.start()
            self.startVideo.setEnabled(False)
            self.stopVideo.setEnabled(True)

    def stop_video(self):
        if self.ProcessCam_X.connect:
            self.ProcessCam_X.stop()
            self.ProcessCam_X.preview()
            self.startVideo.setEnabled(True)
            self.stopVideo.setEnabled(False)

    def analysis(self):
        clients = MongoClient("mongodb://localhost:27017/")
        database = clients['cpr']
        collection = database['doctor_cpr_data']
        name_id = self.Id.toPlainText()
        print(name_id)
        cursors = collection.find({"Id": name_id, "depth":{'$gt':2},"depth":{'$lt':8},"Left_Angle": {'$gt': 150}, "Right_Angle": {'$gt': 150}})
        # cursors = collection.find({"Id": "9", "LWrist_y": {'$gt': 380}, "RWrist_y": {'$gt': 380}}).limit(150)
        df = pd.DataFrame(list(cursors))
        fig_depth, ax1 = plt.subplots(nrows=1, )
        fig_depth.autofmt_xdate(rotation=90)
        ax1.plot(df['datetime'], df['depth'])
        fig_depth.savefig('depth.jpg', dpi=75)
        depth_image = cv2.imread('depth.jpg')
        depth_image = QImage(depth_image, 480, 380, depth_image.strides[0],
                            QImage.Format_BGR888)
        depth = QPixmap.fromImage(depth_image)
        self.deepLabel.setPixmap(depth)


        fig_pose, ax1 = plt.subplots(nrows=1, )
        fig_pose.autofmt_xdate(rotation=90)
        ax1.plot(df['datetime'], df['Left_Angle'])
        ax1.plot(df['datetime'], df['Right_Angle'])
        fig_pose.savefig('pose.jpg', dpi=75)
        pose_image = cv2.imread('pose.jpg')
        pose_image = QImage(pose_image, 480, 380, pose_image.strides[0],
                            QImage.Format_BGR888)
        pose = QPixmap.fromImage(pose_image)
        self.poseLabel.setPixmap(pose)

        fig_freq, ax2 = plt.subplots(nrows=1, )
        fig_freq.autofmt_xdate(rotation=90)
        ax2.plot(df['datetime'], (480 - df['LWrist_y']))
        ax2.plot(df['datetime'], (480 - df['RWrist_y']))
        fig_freq.savefig('frequence.jpg', dpi=75)
        freq_image = cv2.imread('frequence.jpg')
        freq_image = QImage(freq_image, 480, 380, freq_image.strides[0],
                            QImage.Format_BGR888)
        freq = QPixmap.fromImage(freq_image)

        self.frequenceLabel.setPixmap(freq)

    def exit(self):
        self.ProcessCam_X.exit()
        self.close()
