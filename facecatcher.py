import socket
import sys
import time

from mediapipe.python.solutions import face_mesh
import cv2
import numpy as np
from numpy import degrees

import calc
import config
from utils import Point
from stabilizer import Stabilizer


class FaceCatcher:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.face_mesh = face_mesh.FaceMesh(
            False, 1, True,
            config.min_detection_confidence,
            config.min_tracking_confidence
        )
        self.pose_stabilizers = [Stabilizer(
            state_num=2,
            measure_num=1,
            cov_process=0.1,
            cov_measure=0.1) for _ in range(6)]
        self.pose_estimator = calc.PoseEstimator((config.img_width, config.img_height))

        failing_time = 0
        while True:
            try:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.connect((config.unityAddr, config.unityParamPort))
                print('catcher: connected to unity')
                break
            except OSError as e:
                failing_time += 1
                time.sleep(0.2)
                if failing_time > 5:
                    print('catcher: ' + str(e))
                    sys.exit(1)

    def __del__(self):
        self.cam.release()
        print('catcher: tracking terminated')

    # 启动本机摄像头，读取图像
    def run(self):
        while self.cam.isOpened():
            success, img = self.cam.read()
            if not success:
                print('catcher: Ignoring empty frame')
                continue

            landmarks = self.process_img(img)
            if len(landmarks) != 0:
                params = self.translate_to_live2d(landmarks)
                msg = '%.4f ' * config.num_params % params
                try:
                    self.server.send(bytes(msg, "utf-8"))
                except socket.error as e:
                    print(str(e))
                    sys.exit(1)

    # 翻译数据
    def translate_to_live2d(self, landmarks):
        image_points = np.zeros((config.num_landmarks, 2))
        for i in range(config.num_landmarks):
            image_points[i, :] = [landmarks[i].x, landmarks[i].y]
        pose = self.pose_estimator.xyz_pose(image_points)
        pose_np = np.array(pose).flatten()

        steady_pose = []
        for value, ps_stb in zip(pose_np, self.pose_stabilizers):
            ps_stb.update([value])
            steady_pose.append(ps_stb.state[0])
        steady_pose = np.reshape(steady_pose, (-1, 3))

        x = np.clip(degrees(steady_pose[0][1]), -90, 90)
        y = np.clip(-(180 + degrees(steady_pose[0][0])), -90, 90)
        z = np.clip(degrees(steady_pose[0][2]), -90, 90)
        left = calc.eye_open(landmarks, True, z)
        right = calc.eye_open(landmarks, False, z)
        mouth = calc.mouth_open(landmarks)
        return x, y, z, left, right, 0.0, 0.0, 0.0, 0.0, mouth, 0.0

    # 解析面部数据点
    def process_img(self, img):
        landmarks = []
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        img.flags.writeable = False
        h, w, c = img.shape
        results = self.face_mesh.process(img)

        if results.multi_face_landmarks:
            total_landmarks = results.multi_face_landmarks[0]
            for idx, landmark in enumerate(total_landmarks.landmark):
                x, y = landmark.x * w, landmark.y * h
                landmarks.append(Point(x, y))

        return landmarks


