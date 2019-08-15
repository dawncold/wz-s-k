import time
from multiprocessing import Process
from gpiozero import Button
from display import main

BTN_A_GPIO = 21
BTN_B_GPIO = 20

process = None


def show_result():
    global process
    if process is None:
        print('start process')
        process = Process(target=main)
        process.start()


def dismiss():
    global process
    if process:
        print('terminate process')
        process.terminate()
        process.join()
        process = None


btn_a = Button(BTN_A_GPIO)
btn_a.when_activated = show_result

btn_b = Button(BTN_B_GPIO)
btn_b.when_activated = dismiss

while True:
    time.sleep(.1)
