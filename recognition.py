import cv2
import math
import imutils

from pyzbar import pyzbar
from imutils.video import VideoStream
from time import sleep
from loguru import logger


class Recognition:

    def __init__(self, camera):
        self.lat_long = [0.0, 0.0, 0.0, 0.0]
        self.LIMIT = 6
        self.DISTANCE = 15
        self.SIZE = 480
        self.code = ''
        self.camera = camera

    def update_location(self, lat_long_actual):

        self.lat_long[0] = self.lat_long[2]
        self.lat_long[1] = self.lat_long[3]
        self.lat_long[2] = lat_long_actual[0]
        self.lat_long[3] = lat_long_actual[1]

    @staticmethod
    def run_distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 111111

    def start_camera(self):

        return VideoStream(src=self.camera).start()

    def read_qr(self, frame):

        image = pyzbar.decode(frame)

        for data in image:
            text = data.data.decode('utf-8')
            self.code = '{}'.format(text)

    def run(self, actions, battery, lat_long_actual):

        logger.info('Recognition start')

        camera = self.start_camera()

        sleep(0.9)

        while True:

            while actions[0]:

                try:

                    frame = camera.read()

                    if frame is None:
                        logger.debug('CAMERA INVALID')
                    else:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        frame = imutils.resize(frame, width=self.SIZE)

                        self.read_qr(frame=frame)

                        if len(self.code) > 0:

                            if self.code is None or self.code == '':
                                logger.info('QR CODE IS NONE')
                            else:

                                try:
                                    self.code = self.code.split('-')
                                    self.code = int(self.code[0] + self.code[1])

                                except ValueError:
                                    logger.error('QR CODE VALUE ERROR')
                                except IndexError:
                                    logger.error('QR CODE INDEX ERROR')

                                if self.code in battery[:]:

                                    if self.code == battery[-1]:
                                        self.lat_long[2] = lat_long_actual[0]
                                        self.lat_long[3] = lat_long_actual[1]
                                    else:
                                        temp_array = battery[:]
                                        temp_array.remove(self.code)
                                        temp_array.append(self.code)

                                        battery[:] = temp_array

                                        self.update_location(lat_long_actual=lat_long_actual)

                                else:
                                    battery[0:self.LIMIT - 1] = battery[1:self.LIMIT]
                                    try:
                                        battery[self.LIMIT - 1] = self.code
                                    except TypeError:
                                        logger.error('Error in Qr Code')

                                    self.update_location(lat_long_actual=lat_long_actual)

                                logger.debug(battery[:])

                                if self.lat_long[0:2] == [0.0, 0.0] or self.lat_long[2:-1] == [0.0, 0.0]:
                                    pass
                                else:
                                    d = self.run_distance(self.lat_long[0], self.lat_long[1], self.lat_long[2],
                                                          self.lat_long[3])

                                    if d > self.DISTANCE:
                                        d = 0.0
                                        battery[:-1] = [0, 0, 0, 0, 0]

                                        self.lat_long[0], self.lat_long[1] = 0.0, 0.0

                        self.code = ''

                except AttributeError:
                    logger.error('CAMERA RECONNECTED')
                    camera.stop()
                    sleep(1)
                    camera = self.start_camera()

                except KeyboardInterrupt:
                    camera.stop()
                    logger.info('END PROGRAM')
