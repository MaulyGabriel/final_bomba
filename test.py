from bsutils.board import BoardSerial
import logging
import yaml


class Test:

    def __init__(self):
        self.board = BoardSerial()

    def run(self):
        pass

    def setup_logger(cls):
        with open('app/logs/log_config.yaml') as f:
            config = yaml.safe_load(f.read())

        logging.config.dictConfig(config)


if __name__ == '__main__':
    t = Test()
    t.run()
