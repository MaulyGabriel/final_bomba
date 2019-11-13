from loguru import logger


class Test(object):

    def __init__(self):
        self.battery = [0, 0, 20511, 20512, 20511, 20522]
        self.box = 2

    def code_cart(self):

        code = str(self.battery[-1])
        if code != '0':
            seq = code[-1]

            if seq == '1' and self.box == 2:
                if self.battery[-2] != 0:
                    code = str(self.battery[-2])

            code = code[:-1]
            logger.success('Caixote {} foi basculado na carreta {}'.format(self.box, code))
            return code[:]
        else:
            return None


if __name__ == '__main__':
    t = Test()
    t.code_cart()
