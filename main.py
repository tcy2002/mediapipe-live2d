import os
import multiprocessing
from multiprocessing import Process
import subprocess

from translator import Translator
from facecatcher import FaceCatcher


def Unity():
    subprocess.run(".\\unity\\live2d.exe")


def Mediapipe():
    catcher = FaceCatcher()
    catcher.run()


if __name__ == '__main__':
    multiprocessing.freeze_support()

    p1 = Process(target=Unity)
    p1.start()

    p2 = Process(target=Mediapipe)
    p2.start()

    translator = Translator()
    translator.run()

    p1.join()
    p2.join()
