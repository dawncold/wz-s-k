#! coding: utf-8
from __future__ import unicode_literals, print_function, division
import serial

SERIAL_DEVICE = '/dev/ttyAMA0'
HEAD_FIRST = 0xff
REMAINING_LENGTH = 8


class WZSK:
    def __init__(self, serial_device=SERIAL_DEVICE):
        self.serial_device = serial_device
        self.serial = None

    def setup_serial(self):
        self.serial = serial.Serial(port=self.serial_device, baudrate=9600,
                                    bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE)

    def get_frame(self):
        while True:
            b = self.serial.read()
            if b != chr(HEAD_FIRST):
                print('0x{:02x}'.format(b))
                continue
            body = self.serial.read(REMAINING_LENGTH)
            if len(body) != REMAINING_LENGTH:
                continue
            return body

    @staticmethod
    def print_frame(frame):
        print(' '.join('0x{:02x}'.format(b) for b in frame))


if __name__ == '__main__':
    device = WZSK()
    WZSK.print_frame(device.get_frame())
