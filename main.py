import time
import subprocess
from gpiozero import Button

BTN_A_GPIO = 21
BTN_B_GPIO = 20


def show_result():
    pass


def dismiss():
    pass

btn_a = Button(BTN_A_GPIO)
btn_a.when_activated = show_result

btn_b = Button(BTN_B_GPIO)
btn_b.when_activated = dismiss