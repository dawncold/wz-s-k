# -*- coding:utf-8 -*-

import time

"""
return None

return {
    status: "OK",
    values: [
        {
            name: "eco2",
            unit: "ppm",
            value: ...
        },
        {
            name: "resistance",
            unit: "ohm",
            value: ...
        },
        {
            name: "etvoc",
            unit: "ppb",
            value: ...
        }
    ]
}
"""

def read(gpio, i2c_handle):
    c, d = gpio.i2c_read_device(i2c_handle, 9)
    length=len(d)
    if length != 9:
        return None
    status = read_status(d[2])
    ret_obj = dict(status=status, values=[])
    prediction = d[0] * pow(2, 8) + d[1]
    if d[2] == 0x01:
        prediction=d[0]*pow(2,8)+d[1]
    ret_obj['values'].append(dict(name='eCO2', unit='ppm', value=prediction))
    if status == 'OK':
        resistance = d[4]*pow(2,16)+d[5]*pow(2,8)+d[6]
        ret_obj['values'].append(dict(name='resistance', unit='Ohm', value=resistance))
        eTVOC= d[7]*pow(2,8)+d[8]
        ret_obj['values'].append(dict(name='eTVOC', unit='ppb', value=eTVOC))
    
    return ret_obj

def read_status(val):
    if val == 0:
        return 'OK'
    if val == 0x01:
        return 'BUSY'
    if val == 0x10:
        return 'RUNIN'
    if val == 0x80:
        return 'BUSY'

if __name__ == '__main__':
    import pigpio
    
    pi = pigpio.pi()
    h = pi.i2c_open(1, 0x5a)
    print(read(pi, h))
    pi.i2c_close(h)
    pi.stop()