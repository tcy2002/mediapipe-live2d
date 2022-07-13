import multiprocessing
from multiprocessing import Process
import subprocess

from videocapture import VideoCapture
from facetracker import FaceTracker


def Unity():
    subprocess.run(".\\unity\\live2d.exe")


def Mediapipe():
    catcher = FaceTracker()
    catcher.run()


if __name__ == '__main__':
    multiprocessing.freeze_support()

    p1 = Process(target=Unity)
    p1.start()

    p2 = Process(target=Mediapipe)
    p2.start()

    translator = VideoCapture()
    translator.run()

    p1.join()
    p2.join()
