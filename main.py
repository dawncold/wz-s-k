import os
import time
from multiprocessing import Process
import daemon
from gpiozero import Button
from display import main as display_main
from epaper.dfrobot_epaper import DFRobot_Epaper_SPI
from epaper.display_extension.freetype_helper import Freetype_Helper

BTN_A_GPIO = 21
BTN_B_GPIO = 20

process = None


def show_result():
    global process
    if process is None:
        print('start process')
        process = Process(target=display_main, args=(epaper, ))
        process.start()


def dismiss():
    global process
    if process:
        print('terminate process')
        process.terminate()
        process.join()
        process = None

        welcome(epaper)


def welcome(epaper):
    epaper.setTextCursor(0, 10)
    epaper.printStrLn('Welcome')
    epaper.printStrLn('Press A to start')
    epaper.printStrLn('Press B to stop')
    epaper.flush(epaper.PART)


def initEpaper():
    fontFilePath = "{}/epaper/display_extension/wqydkzh.ttf".format(os.path.dirname(os.path.abspath(__file__)))

    # peripheral params
    RASPBERRY_SPI_BUS = 0
    RASPBERRY_SPI_DEV = 0
    RASPBERRY_PIN_CS = 27
    RASPBERRY_PIN_CD = 17
    RASPBERRY_PIN_BUSY = 4

    epaper = DFRobot_Epaper_SPI(RASPBERRY_SPI_BUS, RASPBERRY_SPI_DEV, RASPBERRY_PIN_CS,
                                RASPBERRY_PIN_CD, RASPBERRY_PIN_BUSY)  # create epaper object

    # clear screen
    epaper.begin()
    epaper.clear(epaper.WHITE)
    epaper.flush(epaper.FULL)
    time.sleep(1)

    # config extension fonts
    ft = Freetype_Helper(fontFilePath)
    ft.setDisLowerLimite(96)  # set display lower limite, adjust this to effect fonts color depth
    epaper.setExFonts(ft)  # init with fonts file
    epaper.setTextFormat(1, epaper.BLACK, epaper.WHITE, 2, 2)
    epaper.setExFontsFmt(24, 24)  # set extension fonts width and height

    return epaper


with daemon.DaemonContext():
    btn_a = Button(BTN_A_GPIO)
    btn_a.when_activated = show_result

    btn_b = Button(BTN_B_GPIO)
    btn_b.when_activated = dismiss

    epaper = initEpaper()

    welcome(epaper)


    while True:
        time.sleep(.1)
