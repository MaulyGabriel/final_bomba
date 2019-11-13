import os
import sys
import socket
import serial
from loguru import logger


class BoardSerial:

    def __init__(self):

        self.rate = 9600
        self.time = 1
        self.OK = '$POK'
        self.SEND_OK = '$PNEUDOK'

    def open_connection(self, port):

        try:

            if sys.platform == 'linux':
                pass
                # os.system('sudo chmod -R 777 ' + port)

            board = serial.Serial(port, baudrate=self.rate, timeout=self.time)

            return board

        except serial.SerialException:
            logger.error('Invalid argument')
            return None

    def send_message(self, connection, message):

        if connection is None:
            logger.error('Error in connection')
            return False
        else:
            message = str(message)

            message = self.digit_create(message.upper())

            # logger.debug(message)

            connection.write(message.upper().encode())

            return True

    @staticmethod
    def digit_create(information):

        information = information.upper()

        information += ','

        verify_digit = 0

        for digit in str(information):
            verify_digit ^= ord(digit)

        validated_information = ''
        hexadecimal = hex(verify_digit)
        len_hexadecimal = len(hexadecimal)

        if len_hexadecimal == 3:
            validated_information = '0' + hexadecimal[2]
        elif len_hexadecimal == 4:
            validated_information = hexadecimal[2:4]
        else:
            logger.info('Unable to generate checksum')

        validated_information = information + '*' + validated_information.upper() + '\r\n'

        return validated_information.upper()

    def digit_verify(self, information):

        position = information.find('*')

        result = self.digit_create(information[:position - 1])

        if information[position + 1:] == result[position + 1:]:
            return True
        else:
            return False


class Wifi(object):

    def __init__(self):
        pass

    @staticmethod
    def open_connection(port, host):
        board = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        board.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server = (host, port)
        board.bind(server)
        board.listen(1)

        return board.accept()






