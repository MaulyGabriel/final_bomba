from bsutils.board import BoardSerial
from time import strftime, localtime, sleep
from loguru import logger
import os


class Communication:
    def __init__(self, port):
        self.board = BoardSerial()
        self.port = port
        self.connection = self.board.open_connection(port=self.port)
        self.reboot = 60
        self.PATTERN = '$PNEUL,G'
        self.NOT_FOUND = '$PNEUD,G,0,,'
        self.BOX_1 = '$PNEUL,G,1,1,*21\r\n'
        self.BOX_2 = '$PNEUL,G,1,2,*22\r\n'
        self.BOX_3 = '$PNEUL,G,1,3,*23\r\n'
        self.preview_state = 0

    def close_connection(self):
        self.connection = None

    def run(self, actions, battery, lat_long_actual, box):

        logger.info('start communication')

        init_hour = self.time_hour()
        init_minute = self.time_minute(init_hour)

        while True:

            if self.connection is None:
                self.connection = self.board.open_connection(port=self.port)
                sleep(0.9)

            try:

                message_board = self.connection.readline().decode('utf-8', 'replace')

                if str(message_board[:8]) == str(self.PATTERN):

                    if self.board.digit_verify(str(message_board)):

                        self.board.send_message(connection=self.connection, message=self.board.SEND_OK)

                        message_board = message_board.split(',')

                        # basculamento

                        if message_board[2] == '1':

                            box[0] = int(message_board[3])

                            code = self.code_cart(box=box[0], battery=battery[:])

                            if code is None:
                                self.board.send_message(connection=self.connection, message=self.NOT_FOUND)
                            else:
                                cart = '$PNEUD,G,1,{}'.format(code)
                                self.board.send_message(connection=self.connection, message=cart)

                        if message_board[2] == '2':

                            # camera off and analise reboot

                            if message_board[3] == '0':

                                if self.preview_state == 1:

                                    actions[0] = 0
                                    self.preview_state = int(message_board[3])

                                    actual_hour = self.time_hour()

                                    if actual_hour[0] < init_hour[0]:
                                        actual_hour[0] = int(actual_hour[0]) + 24

                                    actual_minute = self.time_minute(actual_hour)
                                    reboot = actual_minute - init_minute

                                    if reboot >= self.reboot:
                                        logger.info('REBOOT SYSTEM')
                                        sleep(0.8)
                                        os.system('sudo reboot')

                            # camera start

                            elif message_board[3] == '1':

                                if self.preview_state == 0:
                                    actions[0] = 1
                                    self.preview_state = int(message_board[3])

                                    try:
                                        lat_long_actual[0], lat_long_actual[1] = self.convert_coord(
                                            array=[float(message_board[4]), float(message_board[5])])

                                    except ValueError:
                                        logger.error('INVALID GPS')

            except UnicodeError:
                logger.error('UNICODE ERROR')

            except IOError:
                self.close_connection()
                logger.error('SERIAL ERROR')

            except AttributeError:
                self.close_connection()
                logger.error('INVALID ARGUMENT')

            except KeyboardInterrupt:
                logger.info('END PROGRAM')

    @staticmethod
    def code_cart(box, battery):

        code = str(battery[-1])
        if code != '0':
            seq = code[-1]

            if seq == '1' and box == '2':
                if battery[-2] != 0:
                    code = str(battery[-2])

            code = code[:-1]

            return code[:]
        else:
            return None

    @staticmethod
    def convert_coord(array):
        output = [0, 0]

        for idx, n in enumerate(array):
            temp = n * 0.01
            ent = int(temp)
            dec = (temp - ent) * 1.6667
            output[idx] = (ent + dec)

        return output[0], output[1]

    @staticmethod
    def time_hour():
        hour = strftime('%H,%M', localtime())
        hour = hour.split(',')

        return hour

    @staticmethod
    def time_minute(hour):
        minutes = (int(hour[0]) * 60) + int(hour[1])

        return minutes
