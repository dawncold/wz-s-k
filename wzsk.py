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

    def setup_serial(self):
        self.serial = serial.Serial(port=self.serial_device, baudrate=9600, write_timeout=0.5)

    def switch_to_passive_mode(self):
        print('switch to passive mode')
        self.serial.write(b'\xFF\x01\x78\x41\x00\x00\x00\x00\x46')
        time.sleep(1)
        self.serial.reset_input_buffer()

    def request(self):
        data = bytearray()
        data.append(0xff)
        data.append(0x01)
        data.append(0x86)
        data.append(0x00)
        data.append(0x00)
        data.append(0x00)
        data.append(0x00)
        data.append(0x00)
        data.append(0x79)
        self.serial.write(bytes(data))

        if self.serial.in_waiting == 9:
            b = self.serial.read()
            if b != chr(HEAD_FIRST):
                return None
            frame = self.serial.read(BODY_LENGTH)
            return frame
        self.serial.reset_input_buffer()
        return None

    def get_frame(self):
        while True:
            b = self.serial.read()
            if b != chr(HEAD_FIRST):
                continue
            body = self.serial.read(BODY_LENGTH)
            if len(body) != BODY_LENGTH:
                continue
            return body

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
        WZSK.print_frame(frame)
        time.sleep(1)
