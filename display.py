# -*- coding:utf-8 -*-

import time
from wzsk import WZSK


def main(epaper):
    device = WZSK(port='/dev/serial0')

    epaper.clear(epaper.WHITE)
    epaper.flush(epaper.PART)
    epaper.setTextCursor(0, 10)
    epaper.printStrLn('Warming up...')
    epaper.flush(epaper.PART)

    success_results = []
    while True:
        device.switch_to_positive_mode()
        try:
            frame = device.get_frame()
        except:
            success_results = []
        else:
            if frame and WZSK.is_valid_frame(frame):
                success_results.append(frame)
        if len(success_results) >= 5:
            break

    epaper.clear(epaper.WHITE)
    epaper.flush(epaper.PART)
    epaper.setTextCursor(0, 10)
    epaper.printStrLn('Reading...')
    epaper.flush(epaper.PART)

    device.switch_to_passive_mode()

    while True:
        try:
            frame = device.get_frame()
        except:
            epaper.clear(epaper.WHITE)
            epaper.flush(epaper.PART)
            epaper.setTextCursor(0, 10)
            epaper.printStrLn('Get frame error, retry...')
            epaper.flush(epaper.PART)
            continue

        if frame:
            if WZSK.is_valid_frame(frame):
                content1 = 'CH2O: {} µg/m³'.format(WZSK.calculate(frame[1], frame[2]))
                content2 = 'CH2O: {} ppb'.format(WZSK.calculate(*device.get_value_high_and_low(frame)))

                print(content1)
                print(content2)

                epaper.clear(epaper.WHITE)
                epaper.flush(epaper.PART)
                epaper.setTextCursor(0, 10)
                epaper.printStrLn(content1)
                epaper.printStrLn(content2)
                epaper.flush(epaper.PART)

        time.sleep(5)
