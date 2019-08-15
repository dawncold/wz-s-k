# -*- coding:utf-8 -*-

import time
import os
from epaper.dfrobot_epaper import DFRobot_Epaper_SPI
from epaper.display_extension.freetype_helper import Freetype_Helper
from wzsk import WZSK

fontFilePath = "{}/epaper/display_extension/wqydkzh.ttf".format(os.path.dirname(os.path.abspath(__file__)))

# peripheral params
RASPBERRY_SPI_BUS = 0
RASPBERRY_SPI_DEV = 0
RASPBERRY_PIN_CS = 27
RASPBERRY_PIN_CD = 17
RASPBERRY_PIN_BUSY = 4

epaper = DFRobot_Epaper_SPI(RASPBERRY_SPI_BUS, RASPBERRY_SPI_DEV, RASPBERRY_PIN_CS, RASPBERRY_PIN_CD, RASPBERRY_PIN_BUSY) # create epaper object

# clear screen
epaper.begin()
epaper.clear(epaper.WHITE)
epaper.flush(epaper.FULL)
time.sleep(1)

# config extension fonts
ft = Freetype_Helper(fontFilePath)
ft.setDisLowerLimite(96) # set display lower limite, adjust this to effect fonts color depth
epaper.setExFonts(ft) # init with fonts file
epaper.setTextFormat(1, epaper.BLACK, epaper.WHITE, 2, 2)
epaper.setExFontsFmt(24, 24) # set extension fonts width and height

epaper.setTextCursor(0, 10)
epaper.printStrLn('Welcome')
epaper.printStrLn('Press A to start')
epaper.printStrLn('Press B to terminate')
epaper.flush(epaper.PART)


def main():
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
            if WZSK.is_valid_frame(frame):
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
                content1 = '{} µg/m³'.format(WZSK.calculate(frame[1], frame[2]))
                content2 = '{} ppb'.format(WZSK.calculate(*device.get_value_high_and_low(frame)))

                print(content1)
                print(content2)

                epaper.clear(epaper.WHITE)
                epaper.flush(epaper.PART)
                epaper.setTextCursor(0, 10)
                epaper.printStrLn('Ch2O:')
                epaper.printStrLn(content1)
                epaper.printStrLn(content2)
                epaper.flush(epaper.PART)

        time.sleep(5)
