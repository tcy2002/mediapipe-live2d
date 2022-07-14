import socket
import pyvirtualcam as pv
import cv2
import numpy as np
import os
import sys
import time

import config


class VideoCapture:
    def __init__(self):
        self.initTcp()
        self.install_webcam()

    def __del__(self):
        self.server.close()
        self.webcam.close()
        print('capture: connection closed by unity')

    def initTcp(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.settimeout(20)
        failing_time = 0
        port = config.unityImagePort
        while True:
            try:
                self.server.bind((config.unityAddr, port))
                self.server.listen(1)
                print('capture is listening, port: %d' % port)
                break
            except socket.error as e:
                failing_time += 1
                port += 1
                if failing_time >= 3:
                    print('capture: ' + str(e))
                    sys.exit(0)

    def run(self):
        try:
            conn, addr = self.server.accept()
        except:
            print('capture: fail to connect to unity')
            sys.exit(1)
        print('capture: connected to unity')

        while True:
            data = conn.recv(16 * 1024)
            if not data or data == 'exit':
                break

            img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                try:
                    self.webcam.send(img)
                    self.webcam.sleep_until_next_frame()
                except Exception:
                    print('capture: fail to post image to virtual camera')
                    break

    def install_webcam(self):
        try:
            self.webcam = pv.Camera(width=config.img_width, height=config.img_height, fps=20, device='VirtualCamera')
        except RuntimeError:
            os.system('.\\vc\\Install.bat')
            error_n = 0
            while True:
                try:
                    self.webcam = pv.Camera(width=config.img_width, height=config.img_height, fps=20, device='VirtualCamera')
                    break
                except RuntimeError:
                    error_n += 1
                    if error_n > 5:
                        raise RuntimeError('capture: fail to install webcam')
                    time.sleep(1)
