from loguru import logger


def code_cart(box, battery):
    code = str(battery[-1])
    if code != '0':
        seq = code[-1]

        if seq == '1' and box == 2:
            if battery[-2] != 0:
                code = str(battery[-2])

        code = code[:-1]

        return code[:]
    else:
        return None


if __name__ == '__main__':
    logger.info('Basculado na carreta: {}'.format(code_cart(2, [20101, 20102, 20201])))
