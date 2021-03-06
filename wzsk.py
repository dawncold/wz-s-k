#! coding: utf-8
from __future__ import unicode_literals, print_function, division
import sys
import time

import serial
import serial.tools.list_ports

HEAD_FIRST = 0xff
COMMAND_PREFIX = 0x86
BODY_LENGTH = 8


class WZSK:
    def __init__(self, port='/dev/ttyAMA0'):
        self.port = port
        self.serial = None
        self.setup_serial()
        self.positive = True

    def setup_serial(self):
        self.serial = serial.Serial(port=self.port, timeout=0.5, write_timeout=0.5)

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
        print('getting frame...')
        if not self.positive:
            self.serial.write(b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79')
            time.sleep(.5)

        b = self.serial.read()
        if b is None or not b:
            if not self.positive:
                self.serial.reset_input_buffer()
            return None
        if b != chr(HEAD_FIRST):
            if not self.positive:
                self.serial.reset_input_buffer()
            return None
        body = self.serial.read(BODY_LENGTH)
        if len(body) != BODY_LENGTH:
            if not self.positive:
                self.serial.reset_input_buffer()
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
    device = WZSK(port='/dev/serial0')
    positive = len(sys.argv) < 2
    if positive:
        device.switch_to_positive_mode()
    else:
        device.switch_to_passive_mode()

    while True:
        frame = device.get_frame()
        if frame:
            WZSK.print_frame(frame)
            if WZSK.is_valid_frame(frame):
                if positive:
                    print('CH2O: {} ppb'.format(WZSK.calculate(*device.get_value_high_and_low(frame))))
                else:
                    print('Ch2O: {} µg/m³, {} ppb'.format(
                        WZSK.calculate(frame[1], frame[2]),
                        WZSK.calculate(*device.get_value_high_and_low(frame))))
        time.sleep(5)
