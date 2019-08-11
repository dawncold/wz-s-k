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

    def switch_to_passive_mode(self):
        data = bytearray()
        data.append(0xff)
        data.append(0x01)
        data.append(0x78)
        data.append(0x41)
        data.append(0x00)
        data.append(0x00)
        data.append(0x00)
        data.append(0x00)
        data.append(0x46)
        self.serial.write(bytes(data))

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

        b = self.serial.read()
        if b != chr(HEAD_FIRST):
            return
        frame = self.serial.read(BODY_LENGTH)
        if len(frame) != BODY_LENGTH:
            return
        return frame

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
    frame = device.get_frame()
    WZSK.print_frame(frame)
    if WZSK.is_valid_frame(frame):
        print('CH2O: {}'.format(WZSK.calculate(frame[3], frame[4])))

    print('switch to passive mode')
    device.switch_to_passive_mode()
    response = device.request()
    if response:
        WZSK.print_frame(response)
        if WZSK.is_valid_frame(response):
            print('CH2O: {}'.format(WZSK.calculate(response[5], response[6])))
        else:
            print('invalid response')
    else:
        print('no response')
