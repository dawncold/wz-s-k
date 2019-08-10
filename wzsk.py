#! coding: utf-8
from __future__ import unicode_literals, print_function, division
import serial

SERIAL_DEVICE = '/dev/ttyAMA0'
HEAD_FIRST = 0xff
BODY_LENGTH = 8


class WZSK:
    def __init__(self, serial_device=SERIAL_DEVICE):
        self.serial_device = serial_device
        self.serial = None
        self.setup_serial()

    def setup_serial(self):
        self.serial = serial.Serial(port=self.serial_device, baudrate=9600,
                                    bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE)

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
        without_checksum = frame[:-1]
        WZSK.print_frame(without_checksum)
        without_checksum_sum = sum(ord(b) for b in without_checksum)
        print('without checksum sum: {} (0x{:02x})'.format(without_checksum_sum, without_checksum_sum))
        expected_checksum = (~without_checksum_sum) + 1
        print('expected: 0x{:02x}'.format(expected_checksum))
        return checksum == expected_checksum

    @staticmethod
    def print_frame(frame):
        print(' '.join('0x{:02x}'.format(ord(b)) for b in frame))


if __name__ == '__main__':
    device = WZSK()
    frame = device.get_frame()
    WZSK.print_frame(frame)
    if WZSK.is_valid_frame(frame):
        print('Valid frame')
