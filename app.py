import multiprocessing as mp
from communication import Communication
from recognition import Recognition
from loguru import logger


class App:

    def __init__(self):
        self.actions = mp.Array('i', [1])
        self.box = mp.Array('i', [0])
        self.battery = mp.Array('i', [0, 0, 0, 0, 0, 0, ])
        self.lat_long_actual = mp.Array('d', [0.0, 0.0])
        self.c = Communication(port='/dev/SERIAL_PORT')
        self.r = Recognition(camera='rtsp://192.168.1.11:554/live/0/MAIN')

    def run(self):
        c_service = mp.Process(target=self.c.run, args=(self.actions, self.battery, self.lat_long_actual, self.box))
        r_service = mp.Process(target=self.r.run, args=(self.actions, self.battery, self.lat_long_actual))

        c_service.start()
        r_service.start()

        c_service.join()
        r_service.join()


if __name__ == '__main__':
    logger.info('Start services ...')
    app = App()
    app.run()
