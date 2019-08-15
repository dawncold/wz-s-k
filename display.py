# -*- coding:utf-8 -*-

from epaper.dfrobot_epaper import DFRobot_Epaper_SPI
import time
from epaper.display_extension.freetype_helper import Freetype_Helper

fontFilePath = ".epaper/display_extension/wqydkzh.ttf" # fonts file

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

epaper.clear(epaper.WHITE)
epaper.flush(epaper.PART)
epaper.setTextCursor(0,10)
epaper.printStrLn("中国  北京")
epaper.printStrLn("USA   Washington")
epaper.printStrLn("日本  東京")
epaper.printStrLn("韩国  서울")
epaper.flush(epaper.PART)
time.sleep(1)
