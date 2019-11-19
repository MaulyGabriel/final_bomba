# Recognition

Classe Recognition, responsável por realizar a leitura do Qr Code.


``` python
from imutils.video import VideoStream
from loguru import logger
from pyzbar import pyzbar
from time import sleep
import imutils
import math
import cv2


class Recognition:

    def __init__(self, camera):
        '''
        Construtor da classe
        '''
        self.LAT_LONG = [0.0, 0.0, 0.0, 0.0]
        self.LIMIT = 6
        self.DISTANCE = 15
        self.SIZE = 480
        self.CODE, self.READ_CODE = '', ''
        self.CAMERA = camera

    def update_location(self, lat_long_actual):
        '''
        Responsável em atualizar as coordenadas do Qr Code identificado
        '''
        self.LAT_LONG[0] = self.LAT_LONG[2]
        self.LAT_LONG[1] = self.LAT_LONG[3]
        self.LAT_LONG[2] = lat_long_actual[0]
        self.LAT_LONG[3] = lat_long_actual[1]

    @staticmethod
    def run_distance(x1, y1, x2, y2):
        '''
        Responsável por calcular a distância que está sendo percorrida no momento do basculamento
        '''
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 111111

    def start_camera(self):
        '''
        Responsável em ativar a câmera
        '''
        return VideoStream(src=self.CAMERA).start()

    def read_qr(self, frame):
        '''
        Responsável em capturar o conteúdo do Qr Code
        '''
        image = pyzbar.decode(frame)

        for data in image:
            text = data.data.decode('utf-8')
            self.CODE = '{}'.format(text)

    def run(self, actions, battery, lat_long_actual):
        '''
        Responsável por ativar a câmera e sinalizar que o Qr Code está sendo identificado.
        '''
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

                        if len(self.CODE) > 0:

                            if self.CODE is None or self.CODE == '':
                                logger.info('Qr Code is none')
                            else:

                                logger.info(self.CODE)

                                try:
                                    self.CODE = self.CODE.split('-')
                                    self.READ_CODE = int(self.CODE[0] + self.CODE[1])

                                except ValueError:
                                    logger.error('Qr Code value error')
                                except IndexError:
                                    logger.error('Qr Code index error')

                                if self.READ_CODE in battery[:]:

                                    if self.READ_CODE == battery[-1]:
                                        self.LAT_LONG[2] = lat_long_actual[0]
                                        self.LAT_LONG[3] = lat_long_actual[1]
                                    else:
                                        temp_array = battery[:]
                                        temp_array.remove(self.READ_CODE)
                                        temp_array.append(self.READ_CODE)

                                        battery[:] = temp_array

                                        self.update_location(lat_long_actual=lat_long_actual)

                                else:
                                    battery[0:self.LIMIT - 1] = battery[1:self.LIMIT]
                                    try:
                                        battery[self.LIMIT - 1] = self.READ_CODE
                                    except TypeError:
                                        logger.error('Error in Qr Code')

                                    self.update_location(lat_long_actual=lat_long_actual)

                                logger.debug(battery[:])

                                if self.LAT_LONG[0:2] == [0.0, 0.0] or self.LAT_LONG[2:-1] == [0.0, 0.0]:
                                    pass
                                else:
                                    d = self.run_distance(self.LAT_LONG[0], self.LAT_LONG[1], self.LAT_LONG[2],
                                                          self.LAT_LONG[3])

                                    if d > self.DISTANCE:
                                        d = 0.0
                                        battery[:-1] = [0, 0, 0, 0, 0]

                                        self.LAT_LONG[0], self.LAT_LONG[1] = 0.0, 0.0

                        self.CODE = ''

                except AttributeError:
                    logger.error('Camera reconnected')
                    camera.stop()
                    sleep(1)
                    camera = self.start_camera()

``` 


