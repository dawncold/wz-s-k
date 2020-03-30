# -*- coding:utf-8 -*-

import time
from wzsk import WZSK
from ams import read as ams_read


def main(epaper):
    device = WZSK(port='/dev/serial0')

    epaper.clear(epaper.WHITE)
    epaper.flush(epaper.PART)
    epaper.setTextCursor(0, 10)
    epaper.printStrLn('Warming up...')
    epaper.flush(epaper.PART)

    success_results = []
    while True:
        device.switch_to_positive_mode()
        try:
            frame = device.get_frame()
        except:
            success_results = []
        else:
            if frame and WZSK.is_valid_frame(frame):
                success_results.append(frame)
        if len(success_results) >= 5:
            break

    epaper.clear(epaper.WHITE)
    epaper.flush(epaper.PART)
    epaper.setTextCursor(0, 10)
    epaper.printStrLn('Reading...')
    epaper.flush(epaper.PART)

    device.switch_to_passive_mode()

    while True:
        try:
            frame = device.get_frame()
        except:
            content1 = 'CH2O: -- µg/m³'
            content2 = 'CH2O: -- ppb'
        else:
            if frame and WZSK.is_valid_frame(frame):
                content1 = 'CH2O: {} µg/m³'.format(WZSK.calculate(frame[1], frame[2]))
                content2 = 'CH2O: {} ppb'.format(WZSK.calculate(*device.get_value_high_and_low(frame)))
            else:
                content1 = 'CH2O: -- µg/m³'
                content2 = 'CH2O: -- ppb'
        
        try:
            ams_result = ams_read()
        except:
            content3 = 'eCO2: -- ppm'
            content4 = 'eTVOC: -- ppb'
        else:
            if ams_result['status'] == 'OK':
                name2value = {e['name']: e for e in ams_result['values']}
                eco2_result = name2value.get('eCO2')
                content3 = 'eCO2: {} ppm'.format(eco2_result['value'] if eco2_result else '--')
                etvoc_result = name2value.get('eTVOC')
                content3 = 'eTVOC: {} ppb'.format(etvoc_result['value'] if etvoc_result else '--')
            else:
                content3 = 'eCO2: -- ppm'
                content4 = 'eTVOC: -- ppb'
                
        epaper.clear(epaper.WHITE)
        epaper.flush(epaper.PART)
        epaper.setTextCursor(0, 10)
        epaper.printStrLn(content1)
        epaper.printStrLn(content2)
        epaper.printStrLn(content3)
        epaper.printStrLn(content4)
        epaper.flush(epaper.PART)
        time.sleep(5)
