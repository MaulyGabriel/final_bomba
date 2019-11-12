import socket


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


if __name__ == '__main__':

    w = Wifi()
    con = w.open_connection(9090, '192.168.45.84')
    print(con)