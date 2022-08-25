import argparse
import os
import sys
from keypoints.BODY_25 import BODY_25
import cv2
import openpose.pyopenpose as op
import numpy as np


def command_parser():
    parser = argparse.ArgumentParser(description='program useage description')
    # parser.add_argument('--video_path', default='./videos/x_cpr20211028-154425.avi', help='Extract human body keypoints from videos in this directory.')
    parser.add_argument('--video_path', type=str, help='Extract human body keypoints from videos in this directory.')
    parser.add_argument('--truncate', type=float, default=0, help='Truncate last n seconds of video.')
    parser.add_argument('--video_dir', type=str, help='Extract human body keypoints from videos in this directory.')
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit()

    return parser.parse_args()


def is_video(filename):
    filename = filename.lower()
    videofile_extensions = ['.mp4', '.avi', '.mpeg', ]

    for extension in videofile_extensions:
        if filename.endswith(extension):
            return True
    return False


def analysis_feature(features) -> None:
    size: int = len(features)
    for i in range(size):
        RShoulder = features[i, BODY_25.RShoulder.value, :]
        RElbow = features[i, BODY_25.RElbow.value, :]
        RWrist = features[i, BODY_25.RWrist.value, :]
        p0 = [RShoulder, RElbow, RWrist]
        print(f'p0 {p0}')


def extract(video_path):
    cap = cv2.VideoCapture(video_path)
    video_info = {}
    FPS = cap.get(cv2.CAP_PROP_FPS)
    W = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    H = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    FRAME_CNT = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    video_info['FPS'] = FPS
    video_info['W'] = int(W)
    video_info['H'] = int(H)
    video_info['FRAME_CNT'] = int(FRAME_CNT)

    seq_length = int(FRAME_CNT - args.truncate * FPS)

    num_keypoint = 25
    feature_array = np.zeros([seq_length, num_keypoint, 3], np.float32)
    frame_cnt = 0
    try:
        while frame_cnt < seq_length:
            success, frame = cap.read()
            if not success:
                print('retrieve frame from', file_path, 'failed.', file=sys.stderr)
                sys.exit(-1)
            if frame_cnt % FPS == 1:
                datum.cvInputData = frame
                op_wrapper.emplaceAndPop(op.VectorDatum([datum]))
                if len(datum.poseKeypoints.shape) > 0:
                    keypoints = datum.poseKeypoints[0]
                    feature_array[frame_cnt, :, :] = keypoints
            frame_cnt += 1

    except:

        pass

    return video_info, feature_array


def normalization(features, shape):
    norm_features = np.array(features)
    norm_features[:, :, 0] = norm_features[:, :, 0] / shape[0]
    norm_features[:, :, 1] = norm_features[:, :, 1] / shape[1]

    return norm_features


if __name__ == '__main__':
    args = command_parser()
    poseModel = op.PoseModel.BODY_25

    params = dict()
    params["model_folder"] = "models/"
    params["net_resolution"] = "320x-1"
    params['number_people_max'] = 1
    op_wrapper = op.WrapperPython()
    op_wrapper.configure(params)
    op_wrapper.start()

    datum = op.Datum()
    selected_points = [BODY_25.Neck, BODY_25.RShoulder, BODY_25.RElbow, BODY_25.RWrist, BODY_25.LShoulder,
                       BODY_25.LElbow, BODY_25.LWrist]

    print(args)

    if args.video_path:
        if is_video(args.video_path):
            video_info, features = extract(args.video_path)
            save_path = os.path.join('111.npy')
            np.save(save_path, features)
            analysis_feature(features)

    elif args.video_dir:
        # root, _, files = next(os.walk(args.video_dir))
        try:
            root, _, files = next(os.walk('./modify'))
            file_cnt = 0
            for file in files:
                file_path = os.path.join(root, file)
                if is_video(os.path.join(file_path)):
                    video_info, features = extract(file_path)
                    filename = file[0:len(file) - 4]
                    print(f"get the features from file {filename}")
                    save_path = os.path.join('./npy', f'{filename}.npy')
                    norm_features = normalization(features, (video_info['W'], video_info['H']))
                    np.save(save_path, features)
                    print(filename)
        except StopIteration as e:
            print(e)
    #         #todo
