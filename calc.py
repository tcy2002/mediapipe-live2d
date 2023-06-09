import numpy as np
import cv2
from math import cos, radians

import config
from utils import avg_p, dist_p


class PoseEstimator:
    def __init__(self):
        self.size = (config.cam_width, config.cam_height)

        self.model_points_full = self.get_full_model_points()

        # Camera internals
        self.focal_length = self.size[1]
        self.camera_center = (self.size[1] / 2, self.size[0] / 2)
        self.camera_matrix = np.array(
            [[self.focal_length, 0, self.camera_center[0]],
             [0, self.focal_length, self.camera_center[1]],
             [0, 0, 1]], dtype="double")

        # Assuming no lens distortion
        self.dist_coeefs = np.zeros((4, 1))

        # Rotation vector and translation vector
        self.r_vec = None
        self.t_vec = None

    def get_full_model_points(self, filename='model.dat'):
        """Get all 468 3D model points from file"""
        raw_value = []

        with open(filename) as file:
            for line in file:
                raw_value.append(line)

        model_points = np.array(raw_value, dtype=np.float32)
        model_points = np.reshape(model_points, (-1, 3))

        return model_points

    def xyz_pose(self, image_points):
        """
        Solve pose from all the 468 image points
        Return (rotation_vector, translation_vector) as pose.
        """

        if self.r_vec is None:
            (_, rotation_vector, translation_vector) = cv2.solvePnP(
                self.model_points_full, image_points, self.camera_matrix, self.dist_coeefs)
            self.r_vec = rotation_vector
            self.t_vec = translation_vector

        (_, rotation_vector, translation_vector) = cv2.solvePnP(
            self.model_points_full,
            image_points,
            self.camera_matrix,
            self.dist_coeefs,
            rvec=self.r_vec,
            tvec=self.t_vec,
            useExtrinsicGuess=True)

        return rotation_vector, translation_vector


# 计算嘴部开合状态
def mouth_open(landmarks, yaw):
    h_left = dist_p(landmarks[38], landmarks[86])
    h_right = dist_p(landmarks[268], landmarks[316])
    h_avg = (h_right + h_left) / 2

    w_above = dist_p(landmarks[183], landmarks[407])
    w_below = dist_p(landmarks[96], landmarks[325])
    w_avg = (w_below + w_above) / 2

    normalized = h_avg / w_avg / cos(radians(yaw))
    return linear_scale(normalized,
                        config.mouthClosedThreshold,
                        config.mouthOpenThreshold,
                        True, False)


# 计算眼睛的开闭状态
def eye_open(landmarks, left_right, pitch, yaw):
    ratio = eye_ratio([landmarks[33], landmarks[160], landmarks[158],
                       landmarks[133], landmarks[153], landmarks[144]]
                      if left_right else
                      [landmarks[362], landmarks[385], landmarks[387],
                       landmarks[263], landmarks[373], landmarks[380]])

    corr_ratio = ratio / cos(radians(yaw)) * cos(radians(pitch))

    return linear_scale(corr_ratio,
                        config.eyeClosedThreshold,
                        config.eyeOpenThreshold)


# 计算眼睛位置
def eye(landmarks):
    eye1 = avg_p([landmarks[33], landmarks[160], landmarks[158],
                  landmarks[133], landmarks[153], landmarks[144]])
    eye2 = avg_p([landmarks[362], landmarks[385], landmarks[387],
                  landmarks[263], landmarks[373], landmarks[380]])
    return eye1, eye2


# 计算眼睛的长宽比例
def eye_ratio(points):
    width = dist_p(points[0], points[3])
    h1 = dist_p(points[1], points[5])
    h2 = dist_p(points[2], points[4])
    return (h1 + h2) / (2 * width)


# 计算整体位置
def head_valid(landmarks):
    centre = avg_p([landmarks[10], landmarks[4], landmarks[152],
                    landmarks[227], landmarks[323]])
    w_ratio = centre[0] / config.cam_width
    h_ratio = centre[1] / config.cam_height
    return (config.w_ratio_min <= w_ratio <= config.w_ratio_max) and \
           (config.h_ratio_min <= h_ratio <= config.h_ratio_max)


# 线性比例
def linear_scale(num, mi, ma, clip_mi=True, clip_ma=True):
    if num < mi and clip_mi:
        return 0.0
    if num > ma and clip_ma:
        return 1.0
    return (num - mi) / (ma - mi)
