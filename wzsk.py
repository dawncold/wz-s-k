#! coding: utf-8
from __future__ import unicode_literals, print_function, division

import time

import serial

SERIAL_DEVICE = '/dev/ttyAMA0'
HEAD_FIRST = 0xff
COMMAND_PREFIX = 0x86
BODY_LENGTH = 8


class WZSK:
    def __init__(self, serial_device=SERIAL_DEVICE):
        self.serial_device = serial_device
        self.serial = None
        self.setup_serial()
        self.positive = True

    def setup_serial(self):
        self.serial = serial.Serial(port=self.serial_device, baudrate=9600, timeout=0.5,
                                    write_timeout=0.5, xonxoff=False, rtscts=False, dsrdtr=False,
                                    inter_byte_timeout=None, exclusive=None)

    def switch_to_positive_mode(self):
        print('switch to positive mode')
        self.serial.write(b'\xFF\x01\x78\x40\x00\x00\x00\x00\x47')
        time.sleep(.5)
        self.positive = True

    def switch_to_passive_mode(self):
        print('switch to passive mode')
        self.serial.write(b'\xFF\x01\x78\x41\x00\x00\x00\x00\x46')
        time.sleep(.5)
        self.serial.reset_input_buffer()
        self.positive = False

    def get_frame(self):
        if not self.positive:
            self.serial.write(b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79')
            time.sleep(.5)

        b = self.serial.read()
        if b != chr(HEAD_FIRST):
            return None
        body = self.serial.read(BODY_LENGTH)
        if len(body) != BODY_LENGTH:
            return None
        return body

    def get_value_high_and_low(self, frame):
        if self.positive:
            return frame[3], frame[4]
        return frame[5], frame[6]

    @staticmethod
    def is_valid_frame(frame):
        checksum = ord(frame[-1])
        return checksum == (~sum(ord(b) for b in frame[:-1]) & 0xff) + 1

    @staticmethod
    def print_frame(frame):
        print(' '.join('0x{:02x}'.format(ord(b)) for b in frame))

    @staticmethod
    def calculate(high, low):
        return (ord(high) << 8) + ord(low)


if __name__ == '__main__':
    device = WZSK()
    device.switch_to_passive_mode()
    while True:
        frame = device.get_frame()
        if frame is None:
            print('no response')
            continue
        WZSK.print_frame(frame)
        print('CH2O: {}'.format(WZSK.calculate(*device.get_value_high_and_low(frame))))
        time.sleep(1)
