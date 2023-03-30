import multiprocessing
from multiprocessing import Process
import subprocess
import pyvirtualcam as pv
import os
import time

import config
from facetracker import FaceTracker
from checker import Checker


def Unity():
    subprocess.run(".\\unity\\live2d.exe")


def install_webcam():
    try:
        cam = pv.Camera(width=640, height=480, fps=30, device='VirtualCamera')
        cam.close()
    except RuntimeError:
        os.system('.\\vc\\Install.bat')
        failing_time = 0
        while True:
            try:
                cam = pv.Camera(width=640, height=480, fps=30, device='VirtualCamera')
                cam.close()
                break
            except RuntimeError:
                failing_time += 1
                if failing_time > 5:
                    raise RuntimeError('capture: fail to install webcam')
                time.sleep(0.5)


if __name__ == '__main__':
    os.chdir(config.root)
    multiprocessing.freeze_support()
    chk = Checker(config.addr, config.port)

    p1 = Process(target=Unity)
    p1.start()

    install_webcam()
    catcher = FaceTracker()
    catcher.run()

    p1.join()
