import socket
import sys

from mediapipe.python.solutions import face_mesh
import cv2
import numpy as np
from numpy import degrees, clip

import calc
import config
from stabilizer import Stabilizer


class FaceTracker:
    def __init__(self):
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
        self.pose_estimator = calc.PoseEstimator()
        self.params = 0.0, 0.0, 0.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0

        self.openCamera()
        self.initTcp()

    def __del__(self):
        self.server.close()
        self.cam.release()
        print('tracker: tracking terminated')

    def initTcp(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        failing_time = 0
        port = config.unityPort
        while True:
            try:
                self.server.connect((config.unityAddr, port))
                print('tracker: connected to unity, port: %d' % port)
                break
            except OSError:
                failing_time += 1
                if failing_time >= 5:
                    print('tracker: fail to connect to unity')
                    sys.exit(0)

    def openCamera(self):
        try:
            self.cam = cv2.VideoCapture(0)
            print('tracker: camera is open')
        except Exception:
            print('tracker: fail to open camera')

    # 启动本机摄像头，读取图像
    def run(self):
        while self.cam.isOpened():
            msg = '%.4f ' * config.num_params % self.params
            try:
                self.server.send(bytes(msg, "utf-8"))
            except socket.error:
                print('tracker: connection is closed by unity')
                sys.exit(0)

            success, img = self.cam.read()
            if not success:
                self.openCamera()
                print('tracker: try to reopen camera')
                continue

            landmarks = self.process_img(img)
            if len(landmarks) != 0:
                if not calc.head_valid(landmarks):
                    continue
                self.params = self.translate_to_live2d(landmarks)

    # 翻译数据
    def translate_to_live2d(self, landmarks):
        image_points = np.array(landmarks[:config.num_landmarks])
        pose = self.pose_estimator.xyz_pose(image_points)
        pose_np = np.array(pose).flatten()

        steady_pose = []
        for value, ps_stb in zip(pose_np, self.pose_stabilizers):
            ps_stb.update([value])
            steady_pose.append(ps_stb.state[0])
        steady_pose = np.reshape(steady_pose, (-1, 3))

        roll = clip(degrees(steady_pose[0][1]), -90, 90)
        pitch = clip(-(180 + degrees(steady_pose[0][0])), -90, 90)
        yaw = clip(degrees(steady_pose[0][2]), -90, 90)

        left = calc.eye_open(landmarks, True, pitch, yaw)
        right = calc.eye_open(landmarks, False, pitch, yaw)
        mouth = calc.mouth_open(landmarks, yaw)

        return roll, pitch, yaw, left, right, 0.5, 0.5, 0.5, 0.5, mouth, 0.0

    # 解析面部数据点
    def process_img(self, img):
        landmarks = []
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        img.flags.writeable = False
        h, w, _ = img.shape
        results = self.face_mesh.process(img)

        if results.multi_face_landmarks:
            total_landmarks = results.multi_face_landmarks[0]
            for idx, landmark in enumerate(total_landmarks.landmark):
                x, y = landmark.x * w, landmark.y * h
                landmarks.append([x, y])

        return landmarks
